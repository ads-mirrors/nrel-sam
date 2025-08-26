import numpy as np

import matplotlib.lines as mlines
import multiprocessing
from functools import partial
import time
import datetime
import sys
import os
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
import tkinter as tk
import pandas as pd
import json

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
global_var_dict = {}

def initialize_global_var():
    local_var_dict = {}

    json_file_path = os.path.join(parentDir, 'local_var.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            local_var_dict = json.load(json_file)

    #corePath = os.path.join(parentDir2, local_var_dict['py_core_folder'])
    sys.path.append(local_var_dict['py_core_folder'])

    global global_var_dict

    global_var_dict = local_var_dict

initialize_global_var()

core_sco2 = global_var_dict['py_core_folder']
dir_sco2 = os.path.dirname(core_sco2)
example_sco2 = os.path.join(dir_sco2, "example")
g3p3_plotting_sco2 = os.path.join(dir_sco2, "G3P3_analysis_plotting")

sys.path.append(core_sco2)
sys.path.append(example_sco2)
sys.path.append(g3p3_plotting_sco2)

from sco2_plot_g3p3_baseline_FINAL import open_pickle
import sco2_cycle_ssc as sco2_solve
import design_point_tools as design_tools

# Functions file names

def get_baseline_filenames():
    filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
    filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
    filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
    filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"
    return [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

def get_helio_filenames():
    filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250215_171644__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
    filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_163031__recomp_G3P3_collection_10_20250210_180210_000.pkl"
    filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_175940__TSF_G3P3_collection_10_20250210_180908_000.pkl"
    filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_053648__partial_G3P3_collection_10_20250210_142613_000.pkl"
    return [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

# Helper functions

def compare_vals(val1, val2, tol):
    diff = abs(1 - (val1 / val2))
    if(diff <= tol):
        return True
    else:
        return False

def get_split_dicts(filenames):

    input_dict_list = []
    for filename in filenames:
        input_dict_list.append(open_pickle(filename))

    # Reclassify config name
    print('Naming cycles...')
    for result_dict in input_dict_list:
        NVal = len(result_dict[list(result_dict.keys())[0]])
        if('config_name' in result_dict == False):
            result_dict['config_name'] = []
            for i in range(NVal):
                result_dict['config_name'].append('')
        
        for i in range(NVal):
            cycle_config = result_dict['cycle_config'][i]
            recomp_frac = result_dict['recomp_frac'][i]
            bypass_frac = 0 if (('bypass_frac' in result_dict) == False) else result_dict['bypass_frac'][i]
            LTR_UA = result_dict['LTR_UA_calculated'][i]
            HTR_UA = result_dict['HTR_UA_calculated'][i]
            is_LTR = LTR_UA > 0
            is_HTR = HTR_UA > 0
            if(is_LTR == False) and (is_HTR == False):
                x = 0

            result_dict['config_name'][i] = sco2_solve.get_config_name(cycle_config, recomp_frac, bypass_frac, is_LTR, is_HTR)
            #result_dict['config_name'][i] = sco2_solve.get_config_name(cycle_config, recomp_frac, bypass_frac, True, True)

    print('Splitting dictionaries by config_name...')
    result_dict_list = design_tools.split_by_config_name(input_dict_list)

    return result_dict_list

def dict_list_to_dict(dict_list):
    config_name_key = 'config_name'
    config_dict = {}

    for diction in dict_list:
        config_name = diction[config_name_key][0]
        config_dict[config_name] = diction

    return config_dict

def save_dict_duo(dict1, i, dict2, j):
    save_dict = {}

    for key in dict1:
        save_dict[key] = [dict1[key][i]]

    dict2_keys = list(dict2.keys())

    for key2 in dict2_keys:
        if key2 in save_dict:
            save_dict[key2].append(dict2[key2][j])
        else:
            save_dict[key2] = ['', dict2[key2][j]]

    save_filename = asksaveasfilename(filetypes =[('TXT Files', '*.txt')], title="Select save sco2 txt")
    design_tools.write_dict(save_filename, save_dict, '\t')

def compare_dicts(dict1, dict2, input_vars, output_vars):
    NVar_1 = len(dict1[list(dict1.keys())[0]])
    NVar_2 = len(dict2[list(dict2.keys())[0]])

    if(NVar_1 != NVar_2):
        print("variables do not match")
        return

    no_match_vec = []
    output_mismatch_vec = []

    for i in range(NVar_1):
        
        j_match = -1
        for j in range(NVar_2):

            is_match = True

            # Check inputs are the same
            for input_var in input_vars:
                val1 = dict1[input_var][i]
                val2 = dict2[input_var][j]

                flag = compare_vals(val1, val2, 0.000001)
            
                if flag == False:
                    is_match = False
                    break

            if is_match == True:
                j_match = j
                break
            
        if j_match >= 0:
            # Check outputs
            output_match = True
            for output_var in output_vars:
                val1 = dict1[output_var][i]
                val2 = dict2[output_var][j_match]
                flag = compare_vals(val1, val2, 0.0000001)
                if flag == False:
                    print("Output values do not match: " + str(i))
                    output_match = False
                    break
            if output_match == True:
                pass
                #print("A perfect match")
            else:
                print("A mismatch")
                output_mismatch_vec.append(i)
                save_dict_duo(dict1, i, dict2, j_match)
                

        else:
            print("No match: " + i)
            no_match_vec.append(i)

        if (i % 100) == 0:
            percent = (i / NVar_1) * 100
            print("Completed " + str(round(percent, 2)))

    x = 0

    return no_match_vec, output_mismatch_vec

# Main function

def validate_solarpilot_helio_cost():
    
    # Get filenames
    filenames_baseline = get_baseline_filenames()
    filenames_helio = get_helio_filenames()

    # Open files and split by type
    baseline_dict_list = get_split_dicts(filenames_baseline)
    helio_dict_list = get_split_dicts(filenames_helio)

    # Make dict with keys of each type
    baseline_config_dict = dict_list_to_dict(baseline_dict_list)
    helio_config_dict = dict_list_to_dict(helio_dict_list)

    # Loop through each config type
    for config_key in baseline_config_dict:

        # Skip known passed cases
        good_configs = ["Simple", "Simple Double Recup", "Recompression w/o LTR", "Recompression", "Recompression w/o HTR",
                        "Simple Split Flow Bypass w/o LTR", "HTR BP w/o LTR"]
        
        if config_key in good_configs:
            continue

        baseline_result_dict = baseline_config_dict[config_key]
        helio_result_dict = helio_config_dict[config_key]

        input_vars = ["T_htf_hot_des", "T_htf_cold_des", "design_eff", "plant_spec_cost"]
        output_vars = ["csp.pt.cost.tower", "csp.pt.cost.receiver", "csp.pt.cost.power_block",
                       "m_dot_htf_rec_des", "P_tower_lift_des", "rec_width_calc"]

        no_match_vec, output_mismatch_vec = compare_dicts(baseline_result_dict, helio_result_dict, input_vars, output_vars)

        if (len(no_match_vec) == 0) and len(output_mismatch_vec) == 0:
            print(config_key + " passed")


    x = 0



if __name__ == "__main__":
    validate_solarpilot_helio_cost()