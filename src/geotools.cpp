/*
BSD 3-Clause License

Copyright (c) Alliance for Sustainable Energy, LLC. See also https://github.com/NREL/SAM/blob/develop/LICENSE
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <wx/wx.h>

#include <wex/easycurl.h>

#include <rapidjson/reader.h>
#include <rapidjson/error/en.h> // parser errors returned as char strings

#include "main.h"
#include "geotools.h"

/*
static wxString MyGet(const wxString& url)
{
    wxEasyCurl curl;
    curl.AddHttpHeader("Content-type: text/plain");
    curl.AddHttpHeader("Cache-Control: no-cache");
    curl.Get(url);
    return curl.GetDataAsString();
}
*/
// Geocode using Google API for non-NREL builds of SAM
// Set key in private.h: Google API key
bool GeoTools::GeocodeGoogle(const wxString& address, double* lat, double* lon, double* tz, bool showprogress) {
    wxBusyCursor _curs;

    bool success = false;

    wxString plusaddr = address;
    plusaddr.Replace(", ", "+");
    plusaddr.Replace(",", "+");
    plusaddr.Replace("   ", " ");
    plusaddr.Replace("  ", " ");
    plusaddr.Replace(" ", "+");
   
    // Get lat/lon from Google geocoding API
    wxString url = SamApp::WebApi("google_geocode_api");
    url = url + "&address=";
    url = url + plusaddr;
    url.Replace("<GOOGLEAPIKEY>", wxString(google_api_key));

    wxEasyCurl curl;
    wxBusyCursor curs;
    if (showprogress) {
        if (!curl.Get(url, "Geocoding address '" + address + "'..."))
            return false;
    }
    else {
        if (!curl.Get(url))
            return false;
    }

    // change from UTF8 to UTF16 encoding to address unicode characters per SAM GitHub issue 1848
    rapidjson::GenericDocument < rapidjson::UTF16<> > reader;
    wxString str = curl.GetDataAsString();
    reader.Parse(str.c_str());

    if (!reader.HasParseError()) {
        if (reader.HasMember(L"results")) {
            if (reader[L"results"].IsArray()) {
                if (reader[L"results"][0].HasMember(L"geometry")) {
                    if (reader[L"results"][0][L"geometry"].IsArray()) {
                        if (reader[L"results"][0][L"geometry"][0].HasMember(L"location")) {
                            if (reader[L"results"][0][L"geometry"][0][L"location"].HasMember(L"lat")) {
                                if (reader[L"results"][0][L"geometry"][0][L"location"][L"lat"].IsNumber()) {
                                    *lat = reader[L"results"][0][L"geometry"][0][L"location"][L"lat"].GetDouble();
                                    success = true;
                                }
                            }
                            if (reader[L"results"][0][L"geometry"][0][L"location"].HasMember(L"lng")) {
                                if (reader[L"results"][0][L"geometry"][0][L"location"][L"lng"].IsNumber()) {
                                    *lon = reader[L"results"][0][L"geometry"][0][L"location"][L"lng"].GetDouble();
                                    success &= true;
                                }
                            }
                        }
                    }
                }
            }
        }
        // check status code
        success = false;//overrides success of retrieving data

        success = false;//overrides success of retrieving data

        if (reader.HasMember(L"status")) {
            if (reader[L"status"].IsString()) {
                str = reader[L"status"].GetString();
                success = str.Lower() == "ok";
            }
        }
    }

    if (!success)
        return false;


    if (tz != 0) {
        success = false;

        // get timezone from Google timezone API
        url = SamApp::WebApi("google_timezone_api") + wxString::Format("&location=%.14lf,%.14lf", *lat, *lon);
        url.Replace("<GOOGLEAPIKEY>", wxString(google_api_key));

        bool ok;
        if (showprogress)
            ok = curl.Get(url, "Geocoding address...");
        else
            ok = curl.Get(url);


        str = curl.GetDataAsString();
        reader.Parse(str.c_str());

        if (!reader.HasParseError()) {
            if (reader.HasMember(L"rawOffset")) {
                if (reader[L"rawOffset"].IsNumber()) {
                    *tz = reader[L"rawOffset"].GetDouble() / 3600.0;
                    success = true;
                }
                else if (reader[L"rawOffset"].IsInt()) {
                    *tz = reader[L"rawOffset"].GetInt() / 3600.0;
                    success = true;
                }
            }
        }
    
        // check status code
        success = false;//overrides success of retrieving data

        if (reader.HasMember(L"status")) {
            if (reader[L"status"].IsString()) {
                str = reader[L"status"].GetString();
                success = str.Lower() == "ok";
            }
        }
    }
    
    return success;

}

// Geocode using NREL Developer API (MapQuest) for NREL builds of SAM
// Set keys in private.h: NREL Developer API key for geocode, and Bing API key for time zone
// Set variables in webapis.conf to URLs: bing_maps_timezone_api, nrel_geocode_api
bool GeoTools::GeocodeDeveloper(const wxString& address, double* lat, double* lon, double* tz, bool showprogress) {
    wxBusyCursor _curs;

    bool success = false;

    wxString plusaddr = address;
    plusaddr.Replace(", ", "+");
    plusaddr.Replace(",", "+");
    plusaddr.Replace("   ", " ");
    plusaddr.Replace("  ", " ");
    plusaddr.Replace(" ", "+");

    wxString url = SamApp::WebApi("nrel_geocode_api") + "&location=" + plusaddr;
    url.Replace("<GEOCODEAPIKEY>", wxString(geocode_api_key));

    wxEasyCurl curl;
    wxBusyCursor curs;
    
    // SAM issue 1968 
    curl.AddHttpHeader("Content-Type: application/json");
    curl.AddHttpHeader("Accept: application/json");


    if (showprogress) {
        if (!curl.Get(url, "Geocoding address '" + address + "'..."))
            return false;
    }
    else {
        if (!curl.Get(url))
            return false;
    }
 
    // change from UTF8 to UTF16 encoding to address unicode characters per SAM GitHub issue 1848
    rapidjson::GenericDocument < rapidjson::UTF16<> > reader;
    wxString str = curl.GetDataAsString();

    rapidjson::ParseResult ok = reader.Parse(str.c_str());

    if (!reader.HasParseError()) {
        success = false;
        if (reader.HasMember(L"results") ) {
            if (reader[L"results"].IsArray() && reader[L"results"].Size() > 0) {
                if (reader[L"results"][0].HasMember(L"locations")) {
                    if (reader[L"results"][0][L"locations"].IsArray()) {
                        if (reader[L"results"][0][L"locations"][0].HasMember(L"latLng")) {
                            if (reader[L"results"][0][L"locations"][0][L"latLng"].HasMember(L"lat")) {
                                if (reader[L"results"][0][L"locations"][0][L"latLng"][L"lat"].IsNumber()) {
                                    *lat = reader[L"results"][0][L"locations"][0][L"latLng"][L"lat"].GetDouble();
                                    success = true;
                                }
                            }
                            if (reader[L"results"][0][L"locations"][0][L"latLng"].HasMember(L"lng")) {
                                if (reader[L"results"][0][L"locations"][0][L"latLng"][L"lng"].IsNumber()) {
                                    *lon = reader[L"results"][0][L"locations"][0][L"latLng"][L"lng"].GetDouble();
                                    success = true;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    else {
        wxMessageBox(rapidjson::GetParseError_En(ok.Code()), "geocode developer parse error for requested location: " + address);
    }

    if (!success) {
        wxMessageBox("geocode developer returned no results for requested location: " + address);
        return false;
    }


    if (tz != 0) 
    {
        success = false;

        curl = wxEasyCurl();

        url = SamApp::WebApi("bing_maps_timezone_api");
        url.Replace("<POINT>", wxString::Format("%.14lf,%.14lf", *lat, *lon));
        url.Replace("<BINGAPIKEY>", wxString(bing_api_key));

        curl.AddHttpHeader("Content-Type: application/json");
        curl.AddHttpHeader("Accept: application/json");

        if (showprogress) 
        {
            if (!curl.Get(url, "Geocoding address '" + address + "'..."))
                return false;
        }
        else {
            if (!curl.Get(url))
                return false;
        }

        str = curl.GetDataAsString();

        reader.Parse(str.c_str());

        if (!reader.HasParseError()) {
            if (reader.HasMember(L"resourceSets")) {
                if (reader[L"resourceSets"].IsArray()) {
                    if (reader[L"resourceSets"][0].HasMember(L"resources")) {
                        if (reader[L"resourceSets"][0][L"resources"].IsArray()) {
                            if (reader[L"resourceSets"][0][L"resources"][0].HasMember(L"timeZone")) {
                                if (reader[L"resourceSets"][0][L"resources"][0][L"timeZone"].HasMember(L"utcOffset")) {
                                    if (reader[L"resourceSets"][0][L"resources"][0][L"timeZone"][L"utcOffset"].IsString()) {
                                        wxString stz = reader[L"resourceSets"][0][L"resources"][0][L"timeZone"][L"utcOffset"].GetString();
                                        wxArrayString as = wxSplit(stz, ':');
                                        if (as.Count() != 2) return false;
                                        if (!as[0].ToDouble(tz)) return false;
                                        double offset = 0;
                                        if (as[1] == "30") offset = 0.5;
                                        if (*tz < 0)
                                            *tz = *tz - offset;
                                        else
                                            *tz = *tz + offset;
                                        success = true;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            // check status code
            success = false;//overrides success of retrieving data

            if (reader.HasMember(L"statusDescription")) {
                if (reader[L"statusDescription"].IsString()) {
                    wxString str = reader[L"statusDescription"].GetString();
                    success = str.Lower() == "ok";
                }
            }
        }

    }
    return success;
}


wxBitmap GeoTools::StaticMap(double lat, double lon, int zoom, MapProvider service) {
    if (zoom > 21) zoom = 21;
    if (zoom < 1) zoom = 1;
    wxString zoomStr = wxString::Format("%d", zoom);

    wxString url;
    if (service == GOOGLE_MAPS) {
        url = SamApp::WebApi("google_static_map_api");
        url.Replace("<POINT>", wxString::Format("%.14lf,%.14lf", lat, lon));
        url.Replace("<ZOOM>", zoomStr);
        url.Replace("<GOOGLEAPIKEY>", wxString(google_api_key));

    }
    else {
        url = SamApp::WebApi("bing_maps_imagery_api");
        url.Replace("<POINT>", wxString::Format("%.14lf,%.14lf", lat, lon));
        url.Replace("<ZOOMLEVEL>", zoomStr);
        url.Replace("<BINGAPIKEY>", wxString(bing_api_key));
    }

    wxEasyCurl curl;
    bool ok = curl.Get(url, "Obtaining aerial imagery...");
    return ok ? wxBitmap(curl.GetDataAsImage(wxBITMAP_TYPE_JPEG)) : wxNullBitmap;
}
