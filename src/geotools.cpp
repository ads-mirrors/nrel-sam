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

#include <clocale>
#include <wx/wx.h>
#include<wx/tokenzr.h>

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

bool GeoTools::coordinates_to_lat_lon(wxString& coord, wxString& lat, wxString& lon) {

    wxString str = coord.Lower();
    str.Replace("north", "n");
    str.Replace("south", "s");
    str.Replace("east", "e");
    str.Replace("west", "w");

    wxString err = "";

    int x = -1;
    int n = 0;
    bool is_numeric = true;

    std::locale loc{ "" };
    wchar_t decimal_symbol = std::use_facet< std::numpunct<wchar_t> >(loc).decimal_point();

    /*
    for (int i = 0; i < str.Length(); i++) {
		if (str[i] == 'n' || str[i] == 's' ) {
            x=size_t(i);
            n++;
		}
	}*/
    int i = 0;
    for (wxString::const_iterator it = str.begin(); it != str.end(); ++it) {
        wxUniChar c = *it;
        if (wxIsalpha(c) && c!=decimal_symbol) {
            is_numeric = false;
        }
        if (c == 'n' || c == 's') {
            x = i;
            n++;
        }
        i++;
    }

	if (x == -1) {
        if (is_numeric) {
            wxStringTokenizer tk(str, ',');
            //wxArrayString arr = wxSplit(str, ',');
            if (tk.CountTokens() == 2) {
                lat = tk.GetNextToken();
                lon = tk.GetNextToken();
            }
            else
                err = "No n/s/e/w indicator or comma decimal degree separator";
        }
        else 
		    err = "No n/s/e/w indicator";
	}
	else if (n > 1) {
		err = "More than one latitude / longitude found";
	}
	else if (n == 0) {
		err = "No latitude / longitude found";
	}
	else {
        lat = str.Left(x + 1);
        lon = str.Right(str.Length() - x - 1);
	}

	if (err == "")
		return true;
    else {
        wxMessageBox(wxString::Format("GeoTools error.\nCould not convert coordinates (%s) to a latitude / longitude pair: %s", coord, err));
        return false;
    }
}

bool GeoTools::dms_to_dd(double& d, double& m, double& s, double* dd) {
    
    int sign = 1;

    wxString err = "";

	if (m < 0 || s < 0) {
		err = "Negative minutes or seconds not allowed";
	}
	else if (m > 60.0 || s > 60.0) {
		err = "Minutes and seconds must be less than 60";
	}
	else if(std::abs(d) > 180) {
		err = "Degrees must be between -180 and 180";
	}
	else if ((d != int(d)) && (m != 0 || s != 0)) {
		err = "Degrees must be an integer if minutes and seconds are not zero";
	}
	else if (m != int(m) && s != 0) {
		err = "Minutes must be an integer if seconds are not zero";
	}
    else {
        if (d < 0) {
            sign = -1;
        }
		*dd = sign * (std::abs(d) + m / 60.0 + s / 3600.0);
    }
    
	if (err == "") {
        return true;
	}
	else {
        wxMessageBox(wxString::Format("GeoTools error.\nCould not convert DMS (%g, %g, %g) to DD: %s", d, m, s, err));
        return false;
    }
}

bool GeoTools::coordinate_to_dms(wxString& coord, double* d, double* m, double* s)
{

    std::locale loc{ "" };
    wchar_t decimal_symbol = std::use_facet< std::numpunct<wchar_t> >(loc).decimal_point();

    wxString str = coord.Lower();
    str.Replace("north", "n");
    str.Replace("south", "s");
    str.Replace("east", "e");
    str.Replace("west", "w");

    wchar_t c_prev = ' ';
    int n = 0;
    std::string num = "";
    int sign = 1;
	wxString err = ""; // implement error check later?
	double dms[3] = { 0.0, 0.0, 0.0 };

    for (int i = 0; i < str.Length(); i++) {
        char c = str[i];
        if (std::isdigit(c) || c == decimal_symbol) {
            num = num + c;
        }
        else if (c == 's' || c == 'w' || c == '-') {
            sign = -1;
        }
        else if (std::isdigit(c_prev) && n<3) {
			dms[n] = std::stod(num);
            num = "";
            n++;
        }
        c_prev = c;
    }

	if (err == "") {
        if (n == 0) 
            dms[0] = std::stod(num);
        *d = dms[0] * sign;
		*m = dms[1];
		*s = dms[2];
        return true;
	}
    else {
		wxMessageBox(wxString::Format("GeoTools error.\nCould not convert coordinates (%s) to DMS: %s", coord, err));
		return false;
	}

}

// Geocode using Google API for non-NREL builds of SAM
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

bool GeoTools::TimeZoneBing(const double* lat, const double* lon, double* tz, bool showprogress) {

    wxEasyCurl curl;
    curl = wxEasyCurl();

    rapidjson::GenericDocument < rapidjson::UTF16<> > reader;

	bool success = false;

    wxString url = SamApp::WebApi("bing_maps_timezone_api");
    url.Replace("<POINT>", wxString::Format("%.14lf,%.14lf", *lat, *lon));
    url.Replace("<BINGAPIKEY>", wxString(bing_api_key));

    curl.AddHttpHeader("Content-Type: application/json");
    curl.AddHttpHeader("Accept: application/json");

    if (showprogress)
    {
        if (!curl.Get(url, wxString::Format("Getting time zone for Lat = %g Lon = %g...", *lat, *lon)))
            return false;
    }
    else {
        if (!curl.Get(url))
            return false;
    }

    wxString str = curl.GetDataAsString();

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

    return success;

}

// Geocode using NREL Developer API (MapQuest) for NREL builds of SAM
bool GeoTools::GeocodeDeveloper(const wxString& address, double* lat, double* lon, double* tz, bool showprogress) {
    wxBusyCursor _curs;

    bool success = false;

    wxString plusaddr = address;
    plusaddr.Replace(", ", "+");
    plusaddr.Replace(",", "+");
    plusaddr.Replace("   ", " ");
    plusaddr.Replace("  ", " ");
    plusaddr.Replace(" ", "+");

	wxString url = ""; 
	wxString webapi_string = SamApp::WebApi("nrel_geocode_api");

    if (webapi_string == "debug-mock-api")
        url = address;
    else {
        url = SamApp::WebApi("nrel_geocode_api") + "&location=" + plusaddr;
        url.Replace("<GEOCODEAPIKEY>", wxString(geocode_api_key));
    }

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
        if (reader.HasMember(L"results")) {
            if (!reader[L"results"].Empty()) {
                if (reader[L"results"].IsArray()) {
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
                                        success &= true;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // check status code
        success = false;//overrides success of retrieving data

        if (reader.HasMember(L"info")) {
            if (reader[L"info"].HasMember(L"statuscode")) {
                if (reader[L"info"][L"statuscode"].IsInt()) {
                    success = reader[L"info"][L"statuscode"].GetInt() == 0;
                }
            }
        }
    }
    else {
        wxMessageBox(rapidjson::GetParseError_En(ok.Code()), "geocode developer parse error ");
    }

	// if geocode was successful and tz , get timezone
    if (success && tz!=0) {
        success = GeoTools::TimeZoneBing(lat, lon, tz, showprogress);
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
