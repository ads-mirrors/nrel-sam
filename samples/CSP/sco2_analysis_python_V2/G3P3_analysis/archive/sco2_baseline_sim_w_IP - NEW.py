# -*- coding: utf-8 -*-

import numpy as np
import sys
import os
import shutil

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

import design_point_examples as design_pt

# Global variables

folder_location = "C:\\Users\\tbrown2\\OneDrive - NREL\\sCO2-CSP 10302.41.01.40\\Notes\\G3P3\\runs\\baseline_w_IP\\"
Nproc = 20
eta_cutoff = 0.2
N_per_batch = 100000

# Default Case Parameters

def get_sco2_G3P3():

    des_par = {}

    # G3P3 Parameters

    # Power
    W_thermo_net = 10.0     # [MWt] Gross thermo output
    W_air_cooler = 0.1      # [MWe] Air Cooler Parasitic
    W_thermo_gross = W_thermo_net + W_air_cooler    #[MWe]
    des_par["W_dot_net_des"] = W_thermo_gross       #[MWe]
    des_par["fan_power_frac"] = W_air_cooler/W_thermo_net  # [-] Fraction of net cycle power consumed by air cooler fan

    # HTF
    T_HTF_in = 775                          # [C]
    T_turbine_in = 720                      # [C] sco2 turbine inlet temp    
    des_par["T_htf_hot_des"] = T_HTF_in     # [C] HTF design hot temperature (PHX inlet)
    des_par["dT_PHX_hot_approach"] = T_HTF_in - T_turbine_in     # [C/K] Temperature difference between hot HTF and turbine inlet
    des_par["dT_PHX_cold_approach"] = 20     # [C/K] Temperature difference between cold HTF and hot sco2

    des_par["set_HTF_mdot"] = 0

    # Efficiency (ASSUMPTION)
    des_par["eta_isen_t"] = 0.85   # [-] Turbine isentropic efficiency
    des_par["eta_isen_t2"] = 0.85  # [-] Secondary turbine isentropic efficiency
    des_par["eta_isen_mc"] = 0.85  # [-] Main compressor isentropic efficiency
    des_par["eta_isen_pc"] = 0.85  # [-] Precompressor isentropic efficiency
    des_par["eta_isen_rc"] = 0.85  # [-] Recompressor Polytropic efficiency

    # Design Variables
    des_par["is_PR_fixed"] = -7.918     # 0 = No, >0 = fixed pressure ratio at input <0 = fixed LP at abs(input)
    des_par["is_turbine_split_ok"] = -0.431364843
    des_par["is_IP_fixed"] = 0      # partial cooling config: 0 = No, >0 = fixed HP-IP pressure ratio at input, <0 = fixed IP at abs(input)
    des_par["is_bypass_ok"] = -0.114
    des_par["is_recomp_ok"] = -0.35 	# 1 = Yes, 0 = simple cycle only, < 0 = fix f_recomp to abs(input)
    des_par["design_method"] = 2  # [-] 1 = specify efficiency, 2 = specify total recup UA, 3 = Specify each recup design (see inputs below)
    des_par["UA_recup_tot_des"] = 36851.92  # [kW/K] (used when design_method == 2)
    des_par["HTR_UA_des_in"] = 0.77925 * 959.37     # [kW/K] (required if LTR_design_code == 1)
    des_par["LTR_UA_des_in"] = 1.61506 * 112.18     # [kW/K] (required if LTR_design_code == 1)

    des_par["N_nodes_air_cooler_pass"] = 100

    # from Alfani 2021

    # Configuration
    des_par["cycle_config"] = 4  # [1] = RC, [2] = PC, [3] = HTRBP, [4] = TSF

    # Ambient
    des_par["T_amb_des"] = 25.0  # [C] Ambient temperature at design
    des_par["dT_mc_approach"] = 8.0  # [C] Use 6 here per Neises & Turchi 19. Temperature difference between main compressor CO2 inlet and ambient air

    # Pressure
    des_par["PHX_co2_deltaP_des_in"] = -200  # [kPa] Absolute pressure loss
    des_par["deltaP_cooler_frac"] = 0.005  # [-] Fraction of CO2 inlet pressure that is design point cooler CO2 pressure drop
    des_par["LTR_LP_deltaP_des_in"] = 0.01  # [-]
    des_par["HTR_LP_deltaP_des_in"] = 0.01  # [-]
    des_par["is_P_high_fixed"] = 1  # 0 = No, optimize. 1 = Yes (=P_high_limit)
    des_par["P_high_limit"] = 25  # [MPa] Cycle high pressure limit
    

    # Recuperators
    
        # LTR
    des_par["LTR_design_code"] = 2        # 1 = UA, 2 = min dT, 3 = effectiveness
    des_par["LTR_min_dT_des_in"] = 10.0   # [C] (required if LTR_design_code == 2)
    

        # HTR
    des_par["HTR_design_code"] = 2        # 1 = UA, 2 = min dT, 3 = effectiveness
    des_par["HTR_min_dT_des_in"] = 10.0   # [C] (required if LTR_design_code == 2)

    # DEFAULTS

    # ADDED to converge LTR and HTR 
    des_par["HTR_n_sub_hx"] = 10
    des_par["LTR_n_sub_hx"] = 10

        # Pressure
    des_par["LTR_HP_deltaP_des_in"] = 0.01  # [-]
    des_par["HTR_HP_deltaP_des_in"] = 0.01  # [-]
 
        # System design parameters
    des_par["htf"] = 17  # [-] Solar salt
    des_par["site_elevation"] = 588  # [m] Elevation of Daggett, CA. Used to size air cooler...

    # Convergence and optimization criteria
    des_par["rel_tol"] = 6  # [-] Baseline solver and optimization relative tolerance exponent (10^-rel_tol)

    # Default
    des_par["deltaP_counterHX_frac"] = 0.0054321  # [-] Fraction of CO2 inlet pressure that is design point counterflow HX (recups & PHX) pressure drop



    # NOT USED

    # LTR
    eff_max = 1
    
    des_par["LTR_eff_des_in"] = 0.895     # [-] (required if LTR_design_code == 3)
    des_par["LT_recup_eff_max"] = eff_max    # [-] Maximum effectiveness low temperature recuperator
    
    # HTR
    des_par["HTR_eff_des_in"] = 0.945      # [-] (required if LTR_design_code == 3)
    des_par["HT_recup_eff_max"] = eff_max  # [-] Maximum effectiveness high temperature recuperator

    des_par["eta_thermal_des"] = 0.44  # [-] Target power cycle thermal efficiency (used when design_method == 1)
    

    
    return des_par

# Methods for each config type

def run_G3P3_tsf_sweep(n_par, run_folder = ''):

    # Define constant parameters
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 4
    default_par["eta_thermal_cutoff"] = eta_cutoff

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(0,1.0,Npts, True)
    min_pressure = 5
    max_pressure = 13
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(100, 5000, Npts, True)
    split_frac_list = np.linspace(0, 0.7, Npts, True)

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   split_frac_list=split_frac_list,
                                   pres_ratio_list=pressure_list)

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
    for i in range(N_batches):
        run_index_current = i * N_per_batch
        solve_collection = design_pt.run_opt_parallel_solve_dict(dict_list_batches[i], default_par, Nproc, N_run_total=N_cases, N_run_curr=run_index_current)

        file_name = "TSF_G3P3_collection"
        combined_name = folder_location + run_folder + file_name + '_' + str(n_par) + '_' + time_string + '_' + str(i).zfill(3) + ".csv"
        solve_collection.write_to_csv(combined_name)

    finished = ""

def run_G3P3_recomp_sweep(n_par, run_folder = ''):

    # Define constant parameters
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 1
    default_par["eta_thermal_cutoff"] = eta_cutoff

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(0,1.0,Npts, True)
    min_pressure = 5
    max_pressure = 13
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(100, 5000, Npts, True)
    recomp_frac_list = np.linspace(0, 0.7, Npts, True)
    eta_compressor_list = np.linspace(0.7, 0.9, 5, True)
    approach_list = np.linspace(10, 70, 7, True)

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   recomp_list=recomp_frac_list,
                                   pres_ratio_list=pressure_list)

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
    for i in range(N_batches):
        run_index_current = i * N_per_batch
        solve_collection = design_pt.run_opt_parallel_solve_dict(dict_list_batches[i], default_par, Nproc, N_run_total=N_cases, N_run_curr=run_index_current)

        file_name = "recomp_G3P3_collection"
        combined_name = folder_location + run_folder + file_name + '_' + str(n_par) + '_' + time_string + '_' + str(i).zfill(3) + ".csv"
        solve_collection.write_to_csv(combined_name)

    finished = ""

def run_G3P3_htrbp_sweep(n_par, run_folder = ''):

    # Define constant parameters
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 3
    default_par["T_bypass_target"] = 0 # (not used)
    default_par["deltaT_bypass"] = 0
    default_par["eta_thermal_cutoff"] = eta_cutoff

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(0,1.0,Npts, True)
    min_pressure = 5
    max_pressure = 13
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(100, 5000, Npts, True)
    recomp_frac_list = np.linspace(0, 0.7, Npts, True)
    bp_frac_list = np.linspace(0, 0.99, Npts, True)

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   recomp_list=recomp_frac_list,
                                   pres_ratio_list=pressure_list,
                                   bp_list=bp_frac_list)

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
    for i in range(N_batches):
        run_index_current = i * N_per_batch
        solve_collection = design_pt.run_opt_parallel_solve_dict(dict_list_batches[i], default_par, Nproc, N_run_total=N_cases, N_run_curr=run_index_current)

        file_name = "htrbp_G3P3_collection"
        combined_name = folder_location + run_folder + file_name + '_' + str(n_par) + '_' + time_string + '_' + str(i).zfill(3) + ".csv"
        solve_collection.write_to_csv(combined_name)

    finished = ""

def run_G3P3_partial_sweep(n_par, run_folder = ''):

    # Define constant parameters
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 2
    default_par["eta_thermal_cutoff"] = eta_cutoff

    # Organize Variable Combinations
    Npts = n_par
    ltr_ua_frac_list = np.linspace(0,1.0,Npts, True)
    min_pressure = 1
    max_pressure = 13
    pressure_list = np.linspace(min_pressure, max_pressure, Npts, True)
    UA_total_list = np.linspace(100, 5000, Npts, True)
    recomp_frac_list = np.linspace(0, 0.7, Npts, True)
    partial_IP_frac_list = np.linspace(0.0, 0.54, Npts, True)
    max_pressure_list = [default_par["P_high_limit"]]

    dict_list = design_pt.make_dict_par_list(ltr_ua_frac_list=ltr_ua_frac_list, 
                                   UA_total_list=UA_total_list, 
                                   recomp_list=recomp_frac_list,
                                   pres_ratio_list=pressure_list,
                                   max_pressure_list=max_pressure_list,
                                   partial_IP_frac_list=partial_IP_frac_list)

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
    for i in range(N_batches):
        run_index_current = i * N_per_batch
        solve_collection = design_pt.run_opt_parallel_solve_dict(dict_list_batches[i], default_par, Nproc, N_run_total=N_cases, N_run_curr=run_index_current)

        file_name = "partial_G3P3_collection"
        combined_name = folder_location + run_folder + file_name + '_' + str(n_par) + '_' + time_string + '_' + str(i).zfill(3) + ".csv"
        solve_collection.write_to_csv(combined_name)

    finished = ""


# Methods to run all sweeps

def run_G3P3_sweeps(n_par):
    
    # Get Run Meta Data
    time = design_pt.get_time_string()
    py_basename = os.path.basename(__file__)
    py_basename_no_ext, py_ext = os.path.splitext(py_basename)
    run_folder_name = 'run_' + str(n_par) + '_' + time + '\\'

    # Run Sweeps
    run_G3P3_partial_sweep(n_par, run_folder_name)
    run_G3P3_recomp_sweep(n_par, run_folder_name)
    run_G3P3_tsf_sweep(n_par, run_folder_name)
    run_G3P3_htrbp_sweep(n_par, run_folder_name)

    # Copy this py script to save folder
    shutil.copy(__file__, folder_location + run_folder_name) 
    py_copy_name = folder_location + run_folder_name + py_basename
    py_copy_newname = folder_location + run_folder_name + py_basename_no_ext + time + py_ext
    os.rename(py_copy_name, py_copy_newname)
    


# Main function

if __name__ == "__main__":
    run_G3P3_sweeps(2)