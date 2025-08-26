import os
import sys
import json

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
G3P3_post_processDir = os.path.join(parentDir, "G3P3_post_process")
sys.path.append(G3P3_post_processDir)
G3P3_analysis_plottingDir = os.path.join(parentDir, "G3P3_analysis_plotting")
sys.path.append(G3P3_analysis_plottingDir)

import cost_post_process
import sco2_filenames
import phx_costs

def get_g3p3_dict():
    g3p3_json_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\raw data\sam_gen3_particle_for_tmb.json"
    with open(g3p3_json_filename, 'r') as json_file:
        local_g3p3_json = json.load(json_file)

    return local_g3p3_json

def run_post_process():

    # Get filenames
    base_folder = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post"
    TIT625_filenames = sco2_filenames.get_all_files_from_folder(base_folder)

    # Get g3p3 dictionary
    g3p3_json_dict = get_g3p3_dict()

    # TES
    if True:
        tes_vars = ["csp.pt.cost.storage"]
        cost_post_process.modify_baseline(tes_vars, 0.5, "tes50", "tes", 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)
        cost_post_process.modify_baseline(tes_vars, 1.5, "tes150", "tes",
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)
        cost_post_process.modify_baseline(tes_vars, 10, "tes1000", "tes",
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)

    # Recup
    if True:
        recup_vars = ["LTR_cost_equipment", "LTR_cost_bare_erected",
                    "HTR_cost_equipment", "HTR_cost_bare_erected"]
        
        cost_post_process.modify_baseline(recup_vars, 0.5, "recup50", "recup", 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)
        cost_post_process.modify_baseline(recup_vars, 1.5, "recup150", "recup", 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)
        cost_post_process.modify_baseline(recup_vars, 10, "recup1000", "recup", 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)
    
    # PHX
    if True:
        cost_post_process.modify_baseline([], None, "phxblo", "phxbl0", phx_costs.buck_low_2021, 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)
        cost_post_process.modify_baseline([], None, "phxbhi", "phxbhi", phx_costs.buck_high_2021, 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)

    # Heliostat cost
    if True:
        # Instead of changing $/m2 from 75 to 127, use factor to change total heliostat cost (127/75 = 1.693333333)
        helio_vars = ["csp.pt.cost.heliostats"]
        cost_post_process.modify_baseline(helio_vars, 127.0/75.0, "helio127", "helio", 
                                        g3p3_json_dict_arg = g3p3_json_dict, filenames=TIT625_filenames)

    pass


if __name__ == "__main__":
    run_post_process()
    pass