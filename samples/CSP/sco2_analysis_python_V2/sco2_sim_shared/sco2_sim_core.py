# -*- coding: utf-8 -*-

import numpy as np
import sys
import os
import shutil
import csv

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
TIT550Folder = os.path.join(parentDir, 'sco2_sim_shared')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)
sys.path.append(TIT550Folder)

import design_point_examples as design_pt
import sco2_baseline_parameters
import json
import sco2_baseline_parameters as sco2_pars

# Global variables

#folder_location = "C:\\Users\\tbrown2\\OneDrive - NREL\\sCO2-CSP 10302.41.01.40\\Notes\\G3P3\\runs\\baseline_FINAL\\"
#Nproc = 16
#run_name = "baseline_OPT"

global_var_dict = {}

eta_cutoff = 0.2
N_per_batch = 50000

def _save_dict_to_csv(data_dict, folder_path, filename_prefix):
    """
    Save a dictionary as a CSV file where the first column contains key names
    and subsequent columns contain the values from the vectors.
    
    Args:
        data_dict (dict): Dictionary with keys as row names and lists/arrays/single values as values
        folder_path (str): Path to the folder where CSV should be saved
        filename_prefix (str): Prefix for the CSV filename (timestamp will be added)
    """
    if not data_dict:
        return
    
    # Create filename with timestamp
    time_string = design_pt.get_time_string()
    csv_filename = os.path.join(folder_path, f"{filename_prefix}_{time_string}.csv")
    
    # Get all keys and find the maximum length of vectors
    keys = list(data_dict.keys())
    max_length = max(len(data_dict[key]) if hasattr(data_dict[key], '__len__') and not isinstance(data_dict[key], str) else 1 
                     for key in keys)
    
    # Write CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write data rows - one row per key (no header row)
        for key in keys:
            row = [key]  # Start with the key name
            value = data_dict[key]
            
            if hasattr(value, '__len__') and not isinstance(value, str):
                # It's a list/array - add all values
                row.extend(value)
            else:
                # It's a single value
                row.append(value)
            
            writer.writerow(row)
    
    print(f"Dictionary saved to: {csv_filename}")

# Methods for each config type

def _run_dict_list(n_par, default_par, dict_list, config_file_name,
               run_folder = ''):
    
    # Separate Dict List into batches
    N_cases = len(dict_list)
    N_batches = int(np.ceil(N_cases / N_per_batch))
    dict_list_batches = []
    for i in range(N_batches):
        index_low = i * N_per_batch
        index_high = (i + 1) * N_per_batch - 1
        if(index_high >= N_cases):
            index_high = N_cases - 1

        dict_list_batches.append(dict_list[index_low:index_high])

    # Batch run cases
    time_string = design_pt.get_time_string()
    save_file_names = []
    for i in range(N_batches):
        run_index_current = i * N_per_batch
        solve_collection = design_pt.run_opt_parallel_solve_dict(dict_list_batches[i], default_par, global_var_dict["Nproc"], N_run_total=N_cases, N_run_curr=run_index_current)

        combined_name = global_var_dict['folder_location'] + run_folder + config_file_name + '_' + str(n_par) + '_' + time_string + '_' + str(i).zfill(3) + ".csv"
        solve_collection.write_to_csv(combined_name)
        save_file_names.append(combined_name)

    return save_file_names

def _run_G3P3_tsf_sweep(n_par, default_par, design_var_dict, 
                       run_folder = ''):
    
    # Define constant parameters
    default_par["cycle_config"] = 4

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(design_var_dict['LTR_UA_split'][0],design_var_dict['LTR_UA_split'][1],Npts, True)
    min_pressure = design_var_dict['is_PR_fixed'][0]
    max_pressure = design_var_dict['is_PR_fixed'][1]
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(design_var_dict['UA_recup_tot_des'][0],design_var_dict['UA_recup_tot_des'][1], Npts, True)
    split_frac_list = np.linspace(design_var_dict['tsf_split_frac'][0],design_var_dict['tsf_split_frac'][1], Npts, True)

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   split_frac_list=split_frac_list,
                                   pres_ratio_list=pressure_list)

    file_name = "TSF_G3P3_collection"

    save_file_names = _run_dict_list(n_par, default_par, dict_list, file_name, run_folder)
    return save_file_names

def _run_G3P3_recomp_sweep(n_par, default_par, design_var_dict, 
                          run_folder = ''):

    # Define constant parameters
    default_par["cycle_config"] = 1

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(design_var_dict['LTR_UA_split'][0],design_var_dict['LTR_UA_split'][1],Npts, True)
    min_pressure = design_var_dict['is_PR_fixed'][0]
    max_pressure = design_var_dict['is_PR_fixed'][1]
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(design_var_dict['UA_recup_tot_des'][0],design_var_dict['UA_recup_tot_des'][1], Npts, True)
    recomp_frac_list = np.linspace(design_var_dict['is_recomp_ok'][0],design_var_dict['is_recomp_ok'][1], Npts, True)

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   recomp_list=recomp_frac_list,
                                   pres_ratio_list=pressure_list)

    file_name = "recomp_G3P3_collection"
    
    save_file_names = _run_dict_list(n_par, default_par, dict_list, file_name, run_folder)
    return save_file_names

def _run_G3P3_htrbp_sweep(n_par, default_par, design_var_dict, 
                         run_folder = ''):

    # Define constant parameters
    default_par["cycle_config"] = 3
    default_par["T_bypass_target"] = 0 # (not used)

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(design_var_dict['LTR_UA_split'][0],design_var_dict['LTR_UA_split'][1],Npts, True)
    min_pressure = design_var_dict['is_PR_fixed'][0]
    max_pressure = design_var_dict['is_PR_fixed'][1]
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(design_var_dict['UA_recup_tot_des'][0],design_var_dict['UA_recup_tot_des'][1], Npts, True)
    recomp_frac_list = np.linspace(design_var_dict['is_recomp_ok'][0],design_var_dict['is_recomp_ok'][1], Npts, True)
    bp_frac_list = np.linspace(design_var_dict['is_bypass_ok'][0],design_var_dict['is_bypass_ok'][1],  Npts, True)

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   recomp_list=recomp_frac_list,
                                   pres_ratio_list=pressure_list,
                                   bp_list=bp_frac_list)

    file_name = "htrbp_G3P3_collection"
    
    save_file_names = _run_dict_list(n_par, default_par, dict_list, file_name, run_folder)
    return save_file_names

def _run_G3P3_partial_sweep(n_par, default_par, design_var_dict, 
                           run_folder = ''):

    # Define constant parameters
    default_par["cycle_config"] = 2

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(design_var_dict['LTR_UA_split'][0],design_var_dict['LTR_UA_split'][1],Npts, True)
    min_pressure = design_var_dict['is_PR_fixed'][0]
    max_pressure = design_var_dict['is_PR_fixed'][1]
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(design_var_dict['UA_recup_tot_des'][0],design_var_dict['UA_recup_tot_des'][1], Npts, True)
    recomp_frac_list = np.linspace(design_var_dict['is_recomp_ok'][0],design_var_dict['is_recomp_ok'][1], Npts, True)
    partial_IP_frac_list = np.linspace(design_var_dict['partial_IP'][0],design_var_dict['partial_IP'][1], Npts, True)
    max_pressure_list = [default_par["P_high_limit"]]

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   recomp_list=recomp_frac_list,
                                   pres_ratio_list=pressure_list,
                                   max_pressure_list=max_pressure_list,
                                   partial_IP_frac_list=partial_IP_frac_list)

    file_name = "partial_G3P3_collection"
    
    save_file_names = _run_dict_list(n_par, default_par, dict_list, file_name, run_folder)
    return save_file_names

# PUBLIC
    
def run_all_sweeps(n_par, run_name, default_par, design_var_dict,
                   global_var_dict_arg, run_g3p3=False):
    global global_var_dict
    global_var_dict = global_var_dict_arg

    # Get Run Meta Data
    time = design_pt.get_time_string()
    py_basename = os.path.basename(__file__)
    py_basename_no_ext, py_ext = os.path.splitext(py_basename)
    run_folder_name = run_name + '\\run_' + str(n_par) + '_' + time + '\\'

    # Run Sweeps
    save_file_names = []
    save_file_names.extend(_run_G3P3_partial_sweep(n_par, default_par, design_var_dict, run_folder_name))
    save_file_names.extend(_run_G3P3_recomp_sweep(n_par, default_par, design_var_dict, run_folder_name))
    save_file_names.extend(_run_G3P3_tsf_sweep(n_par, default_par, design_var_dict, run_folder_name))
    save_file_names.extend(_run_G3P3_htrbp_sweep(n_par, default_par, design_var_dict, run_folder_name))

    # Copy this py script to save folder
    shutil.copy(__file__, global_var_dict['folder_location'] + run_folder_name) 
    py_copy_name = global_var_dict['folder_location'] + run_folder_name + py_basename
    py_copy_newname = global_var_dict['folder_location'] + run_folder_name + py_basename_no_ext + time + py_ext
    os.rename(py_copy_name, py_copy_newname)
    
    # Save both dictionaries as CSV to the same folder
    save_folder = global_var_dict['folder_location'] + run_folder_name
    _save_dict_to_csv(design_var_dict, save_folder, f"{run_name}_design_vars")
    _save_dict_to_csv(default_par, save_folder, f"{run_name}_default_par")

    print("Finished running sco2.")

    # Run G3P3 Sims for all files
    if run_g3p3:

        print("Running g3p3...")

        # Add g3p3 folder to path
        sys.path.append(global_var_dict['g3p3_design_sim'])
        import g3p3_design_sim
        g3p3_design_sim.multi_thread_fileopendlg(save_file_names)

    return save_file_names


# Main function

if __name__ == "__main__":
    pass