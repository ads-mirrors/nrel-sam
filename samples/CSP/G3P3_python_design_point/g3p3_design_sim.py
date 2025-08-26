import numpy as np

import matplotlib.lines as mlines
import multiprocessing
from functools import partial
import time
import datetime
import sys
import os
from tkinter.filedialog import askopenfilenames
import tkinter as tk
import pandas as pd
import shutil
import json




fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
parentDir2 = os.path.dirname(parentDir)
sco2Dir = os.path.join(fileDir, "sco2-python")
sys.path.append(sco2Dir)
#newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')

def initialize_global_var():
    local_var_dict = {}

    json_file_path = os.path.join(fileDir, 'local_var.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            local_var_dict = json.load(json_file)

    #corePath = os.path.join(parentDir2, local_var_dict['py_core_folder'])
    sys.path.append(local_var_dict['py_core_folder'])
    return local_var_dict

#Nproc = 14
global_var_dict = initialize_global_var()

import sco2_sim_result_collection as sco2_result_collection
import g3p3_annual_sim_refactored as g3p3_case
import ssc_inout_v2 as ssc_sim


# Archive Functions

def orig_func():
    recomp_filename = r"..\g3p3_design_sweep1\recomp_G3P3_collection_10_20240426_223109.csv"
    tsf_filename = r"..\g3p3_design_sweep1\TSF_G3P3_collection_10_20240426_224925.csv"
    partial_filename = r"..\g3p3_design_sweep1\partial_G3P3_collection_10_20240426_204607.csv"
    htrbp_filename = r"..\g3p3_design_sweep1\htrbp_G3P3_collection_10_20240427_205838.csv"
    filenames = [recomp_filename, tsf_filename, partial_filename, htrbp_filename]

    result_collection = sco2_result_collection.C_sco2_sim_result_collection()

    

    # Loop through each sco2 config
    for filename in filenames:
        filename_stripped = os.path.basename(filename)
        print("Opening " + filename_stripped + "...")
        sco2_collection = sco2_result_collection.C_sco2_sim_result_collection()
        sco2_collection.open_csv(filename)
        print("sco2 file open")

        # Loop through each case
        num_cases = sco2_collection.num_cases
        for id in range(num_cases):

            if((id%100)==0):
                print((id/num_cases))

            # Prep Inputs (and validate)
            if(sco2_collection.old_result_dict['cmod_success'] == False):
                continue

            W_dot_net_des = sco2_collection.old_result_dict['W_dot_net_des'][id]                      # MWe
            eta_thermal_calc = sco2_collection.old_result_dict['eta_thermal_calc'][id]                # 
            cycle_cost = sco2_collection.old_result_dict['cycle_cost'][id]                            # M$
            cycle_spec_cost = sco2_collection.old_result_dict['cycle_spec_cost'][id]                  # $/kWe
            W_dot_net_less_cooling = sco2_collection.old_result_dict['W_dot_net_less_cooling'][id]    # MWe
            fan_power_frac = sco2_collection.old_result_dict['fan_power_frac'][id]                    #
            q_dot_in_total = sco2_collection.old_result_dict['q_dot_in_total'][id]                    # MWt
            T_htf_hot_des = sco2_collection.old_result_dict['T_htf_hot_des'][id]                      # C
            T_htf_cold_des = sco2_collection.old_result_dict['T_htf_cold_des'][id]                    # C
            W_dot_cycle_parasitic_input = W_dot_net_des * fan_power_frac                              # MWe

            # test some things
            cycle_spec_cost_calc = (cycle_cost * 1e6) / (W_dot_net_des * 1e3)   # $/kWe
            if(cycle_spec_cost_calc != cycle_spec_cost):
                print("cycle cost issue")

            W_dot_net_less_cooling_calc = W_dot_net_des * (1.0 - fan_power_frac)
            if(abs((W_dot_net_less_cooling_calc/W_dot_net_less_cooling) - 1) > 0.001):
                print("cooling issue")
            
            eta_recalc = W_dot_net_des / q_dot_in_total
            if(abs((eta_recalc/eta_thermal_calc) - 1) > 0.001):
                print("eta issue")

            result_dict = g3p3_case.run_g3p3_case(W_dot_net_des, eta_thermal_calc, T_htf_cold_des, T_htf_hot_des,
                                                cycle_spec_cost, W_dot_cycle_parasitic_input, suppress_print=True)

            # Add a few sco2 parameters
            result_dict["id"] = id
            result_dict["sco2_filename"] = filename_stripped

            sco2_labels = ['cycle_config', 'config_name']
            for label in sco2_labels:
                result_dict[label] = sco2_collection.old_result_dict[label][id]
            

            result_collection.add(result_dict, is_sco2=False)

        sco2_collection.write_to_csv("test.csv")

        exit()
    


    print("this is a test")

def multi_thread_run():
    recomp_filename = r"..\g3p3_design_sweep1\recomp_G3P3_collection_10_20240426_223109.csv"
    tsf_filename = r"..\g3p3_design_sweep1\TSF_G3P3_collection_10_20240426_224925.csv"
    partial_filename = r"..\g3p3_design_sweep1\partial_G3P3_collection_10_20240426_204607.csv"
    htrbp_filename = r"..\g3p3_design_sweep1\htrbp_G3P3_collection_10_20240427_205838.csv"
    
    #recomp_filename = r"..\g3p3_design_reduced_test\recomp_G3P3_collection_5_20240426_163437.csv"
    #tsf_filename = r"..\g3p3_design_reduced_test\TSF_G3P3_collection_5_20240426_163601.csv"
    #partial_filename = r"..\g3p3_design_reduced_test\partial_G3P3_collection_5_20240426_162235.csv"
    #htrbp_filename = r"..\g3p3_design_reduced_test\htrbp_G3P3_collection_5_20240426_174143.csv"

    #filenames = [recomp_filename, tsf_filename, partial_filename, htrbp_filename]
    filenames = [htrbp_filename]

    result_collection = sco2_result_collection.C_sco2_sim_result_collection()

    # Loop through each sco2 config
    for filename in filenames:
        filename_stripped = os.path.basename(filename)
        print("Opening " + filename_stripped + "...")
        sco2_collection = sco2_result_collection.C_sco2_sim_result_collection()
        sco2_collection.open_csv(filename)
        print("sco2 file open")

        list_of_dicts = sco2_collection.get_list_of_dicts()

        # Add some meta parameters
        for i in range(len(list_of_dicts)):
            list_of_dicts[i]['id'] = i
            list_of_dicts[i]['filename'] = filename_stripped

        local_result_collection = run_parallel_solve_dict(list_of_dicts, global_var_dict['Nproc'])

        local_result_collection.write_to_csv(filename + get_time_string())
        print("saved " + filename + "testsavedata")

# Utility Functions

def get_time_string():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")

def convert_result_dict_to_list(result_dict):
    df = pd.DataFrame(result_dict)
    return df.to_dict('records')

def compare_vals(val1, val2, tol):
    if abs(val1 - val2) < tol:
        return True
    else:
        return False

# Simulation Functions

def run_once_solve_dict(sco2_dict, solve_dict_queue = None, N_run_total = 0):

    # Prep Inputs (and validate)
    if(sco2_dict['cmod_success'] == False or sco2_dict['cycle_success'] == 0):
        return

    #if(compare_vals(sco2_dict['eta_thermal_calc'], 0.2892, 0.001)):
    #    y = 0

    W_dot_net_des = sco2_dict['W_dot_net_des']                          # MWe
    eta_thermal_calc = sco2_dict['eta_thermal_calc']                    # 
    cycle_cost = sco2_dict['cycle_cost']                                # M$
    cycle_spec_cost = sco2_dict['cycle_spec_cost']                      # $/kWe
    W_dot_net_less_cooling = sco2_dict['W_dot_net_less_cooling']        # MWe
    fan_power_frac = sco2_dict['fan_power_frac']                        #
    q_dot_in_total = sco2_dict['q_dot_in_total']                        # MWt
    T_htf_hot_des = sco2_dict['T_htf_hot_des']                          # C
    T_htf_cold_des = sco2_dict['T_htf_cold_des']                        # C
    W_dot_cycle_parasitic_input = W_dot_net_des * fan_power_frac        # MWe

    cycle_spec_cost_calc = (cycle_cost * 1e6) / (W_dot_net_des * 1e3)   # $/kWe
    if(cycle_spec_cost_calc != cycle_spec_cost):
        print("cycle cost issue")

    W_dot_net_less_cooling_calc = W_dot_net_des * (1.0 - fan_power_frac)
    if(abs((W_dot_net_less_cooling_calc/W_dot_net_less_cooling) - 1) > 0.001):
        print("cooling issue")
    
    eta_recalc = W_dot_net_des / q_dot_in_total
    if(abs((eta_recalc/eta_thermal_calc) - 1) > 0.001):
        print("eta issue")

    # SENSITIVITY FOR HELIOSTAT COST
    #overwrite_dict = {"heliostat_spec_cost":127}

    result_dict = g3p3_case.run_g3p3_case(W_dot_net_des, eta_thermal_calc, T_htf_cold_des, T_htf_hot_des,
                                          cycle_spec_cost, W_dot_cycle_parasitic_input, 
                                          ssc_sim,
                                          suppress_print=True)

    # Combine input and output dict
    #for input_key in g3p3_input_dict:
    #    if (input_key in result_dict) == False:
    #        result_dict[input_key] = g3p3_input_dict[input_key]

    # Add a few sco2 parameters
    result_dict["id"] = sco2_dict['id']
    result_dict["sco2_filename"] = sco2_dict['filename']

    sco2_labels = ['cycle_config', 'config_name', 
                   'T_htf_hot_des', 'T_htf_cold_des',
                   'eta_thermal_calc', 'W_dot_net_des',
                   'q_dot_in_total','cycle_cost',
                   "is_recomp_ok", "is_bypass_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                   "P_high_limit", "is_PR_fixed", "is_IP_fixed", "is_turbine_split_ok",
                   "eta_isen_mc", "dT_PHX_cold_approach",
                   "recomp_frac", "bypass_frac", "recup_total_UA_calculated",
                   "P_comp_in", "pc_P_in_des", "is_turbine_split_ok",
                   "LTR_UA_calculated", "HTR_UA_calculated"]
    sco2_single_labels = ["cost", "state_points"]

    for label in sco2_labels:
        if label in sco2_dict:
            result_dict[label] = sco2_dict[label]
    for key in sco2_dict:
        for single_label in sco2_single_labels:
            if single_label in key:
                result_dict[key] = sco2_dict[key]
                break

    if(result_dict['cmod_success'] == 0):
        x = 0

    # Add result to queue (if necessary)
    if(solve_dict_queue != None):
        solve_dict_queue.put(result_dict)

    # Report Progress (if necessary)
    if(N_run_total > 0):
        completed = solve_dict_queue.qsize()
        percent = (completed / N_run_total) * 100
        print(str(round(percent, 2)) + "% complete")

    return

def run_parallel_solve_dict(dict_list_total, nproc):
    # Initialize
    N_run = len(dict_list_total)

    # Make Cycle Collection Class
    result_collection = sco2_result_collection.C_sco2_sim_result_collection()

    start = time.time()

    manager = multiprocessing.Manager()
    solve_dict_queue = manager.Queue()

    with multiprocessing.Pool(nproc, maxtasksperchild=20) as p:
        p.imap_unordered(partial(run_once_solve_dict, solve_dict_queue=solve_dict_queue, N_run_total = N_run), dict_list_total)
        p.close()
        p.join()

    # Collect results from queue
    q_size = solve_dict_queue.qsize()
    count = 0

    print("Runs complete. Collecting results")

    while not solve_dict_queue.empty():
        solve_dict = solve_dict_queue.get()
        if(solve_dict['cmod_success'] == 0):
            x = 0
        result_collection.add(solve_dict, key_ref='cycle_config')
        count = count + 1

        if(count % 100 == 0):
            print("Collecting " + str(round((count / q_size) * 100.0, 2)) + "%")

    print("Collecting complete.")
    end = time.time()

    return result_collection 

def multi_thread_run_filenames(filenames):
    #result_collection = sco2_result_collection.C_sco2_sim_result_collection()

    # Loop through each sco2 config
    for filename in filenames:
        filename_stripped = os.path.basename(filename)
        print("Opening " + filename_stripped + "...")
        sco2_collection = sco2_result_collection.C_sco2_sim_result_collection()
        sco2_collection.open_csv(filename)
        print("sco2 file open")

        file_basename = os.path.basename(filename)
        file_basename_no_ext, py_ext = os.path.splitext(file_basename)
        folder_name = os.path.dirname(filename)

        list_of_dicts = convert_result_dict_to_list(sco2_collection.old_result_dict)

        #list_of_dicts = sco2_collection.get_list_of_dicts()

        # Add some meta parameters
        for i in range(len(list_of_dicts)):
            list_of_dicts[i]['id'] = i
            list_of_dicts[i]['filename'] = filename_stripped

        local_result_collection = run_parallel_solve_dict(list_of_dicts, global_var_dict['Nproc'])

        result_filename = folder_name + "//zG3P3_results_" + get_time_string() + "__" + file_basename

        local_result_collection.write_to_csv(result_filename)
        print("saved " + filename)

# Public Functions

def multi_thread_fileopendlg(filenames = []):
    # Select sco2 files to run
    #window = tk.Tk()

    #window.mainloop()
    
    if filenames == []:
        filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Open sco2 results csv")
        for filename in filename_tuple:
            filenames.append(filename)

    if(len(filenames) > 0):
        # Save Folder
        dir_path = os.path.dirname(filenames[0])

        # Copy py scripts to save folder
        shutil.copy(__file__, dir_path) # This py file

        refactored_filename = "g3p3_annual_sim_refactored.py" # refactored file
        this_dir = os.path.dirname(__file__)
        refactored_path = os.path.join(this_dir, refactored_filename)
        shutil.copy(refactored_path, dir_path)

        json_filename = "sam_gen3_particle_for_tmb.json" # json
        json_path = os.path.join(this_dir, json_filename)
        shutil.copy(json_path, dir_path)

        # Simulate
        multi_thread_run_filenames(filenames)

if __name__ == "__main__":
    
    #global_var_dict = initialize_global_var()
    multi_thread_fileopendlg()


