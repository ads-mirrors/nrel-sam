import numpy as np

import matplotlib.lines as mlines
import multiprocessing


import sys
import os

sys.path.append("sco2-python")

newPath = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')

import sco2_sim_result_collection as test_collection
import g3p3_annual_sim_refactored as g3p3_case


if __name__ == "__main__":
    tsf_filename = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\TSF_G3P3_collection_10_20240426_224925.csv"
    recomp_filename = r"..\g3p3_design_sweep1\recomp_G3P3_collection_10_20240426_223109.csv"
    partial_filename = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\partial_G3P3_collection_10_20240426_204607.csv"
    htrbp_filename = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\htrbp_G3P3_collection_10_20240427_205838.csv"

    print("Opening recomp...")
    recomp_sim_collection = test_collection.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_filename)
    print("Recomp open")


    # Prep Inputs (and validate)
    id = 1
    cmod_success = "cmod_success"
    W_dot_net_des = recomp_sim_collection.old_result_dict['W_dot_net_des'][id]                      # MWe
    eta_thermal_calc = recomp_sim_collection.old_result_dict['eta_thermal_calc'][id]                # 
    cycle_cost = recomp_sim_collection.old_result_dict['cycle_cost'][id]                            # M$
    cycle_spec_cost = recomp_sim_collection.old_result_dict['cycle_spec_cost'][id]                  # $/kWe
    W_dot_net_less_cooling = recomp_sim_collection.old_result_dict['W_dot_net_less_cooling'][id]    # MWe
    fan_power_frac = recomp_sim_collection.old_result_dict['fan_power_frac'][id]                    #
    q_dot_in_total = recomp_sim_collection.old_result_dict['q_dot_in_total'][id]                    # MWt
    T_htf_hot_des = recomp_sim_collection.old_result_dict['T_htf_hot_des'][id]                      # C
    T_htf_cold_des = recomp_sim_collection.old_result_dict['T_htf_cold_des'][id]                    # C

    W_dot_cycle_parasitic_input = W_dot_net_des * fan_power_frac                                    # MWe


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

    result_collection = test_collection.C_sco2_sim_result_collection()

    result_dict = g3p3_case.run_g3p3_case(W_dot_net_des, eta_thermal_calc, T_htf_cold_des, T_htf_hot_des,
                                        cycle_spec_cost, W_dot_cycle_parasitic_input, suppress_print=True)

    

    # Add a few sco2 parameters
    result_dict["id"] = id
    result_dict["sco2_filename"] = recomp_filename

    sco2_labels = ['cycle_config', 'config_name']
    for label in sco2_labels:
        result_dict[label] = recomp_sim_collection.old_result_dict[label][id]
    

    result_collection.add(result_dict, is_sco2=False)

    


    print("this is a test")


