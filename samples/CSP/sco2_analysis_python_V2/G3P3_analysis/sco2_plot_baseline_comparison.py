import sys
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backend_bases import MouseButton

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

import sco2_cycle_ssc as sco2_solve
import design_point_tools as design_tools
import math

def plot_sweep(tsf_filename, recomp_filename, partial_filename, htrbp_filename):
    print("Opening htrbp...")
    htrbp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv(htrbp_filename)
    print("HTR BP opened")

    print("Opening recomp...")
    recomp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_filename)
    print("Recomp open")

    print("Opening tsf...")
    tsf_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    tsf_sim_collection.open_csv(tsf_filename)
    print("TSF opened")

    print("Opening partial...")
    partial_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    partial_sim_collection.open_csv(partial_filename)
    print("Partial opened")

    # Split Dicts by 'Actual' config name

    print("Splitting by config type...")

    # HTR BP (only comes from htr bp file)
    htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict],
                                                            "config_name", "htr bp")

    # Recompression (comes from recomp and htr bp)
    recomp_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict, 
                                                            recomp_sim_collection.old_result_dict],  
                                                            "config_name", "recompression")

    # Simple (from recomp and htr bp)
    simple_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict, 
                                                            recomp_sim_collection.old_result_dict],  
                                                            "config_name", "simple")

    # Simple w/ htr bypass (from htr bp only)
    simple_htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict],
                                                            "config_name", "simple split flow bypass")
    
    # Partial (only comes from partial file)
    partial_compiled_dict = design_tools.combine_dict_by_key([partial_sim_collection.old_result_dict],
                                                            "config_name", "partial")

    # Partial Intercooling (only comes from partial file)
    partial_ic_compiled_dict = design_tools.combine_dict_by_key([partial_sim_collection.old_result_dict],
                                                            "config_name", "partial intercooling")

    # Variables to Display
    ETA_label = ["eta_thermal_calc", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    # Create Cycle Split T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, ETA_label[0], T_HTF_label[0], True, False)

    # Create Cycle Split Cost Pareto
    print("Forming split cycle cost pareto fronts...")
    htrbp_compiled_cost_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], COST_label[0], True, False)
    recomp_compiled_cost_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], COST_label[0], True, False)
    simple_compiled_cost_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], COST_label[0], True, False)
    simple_htrbp_compiled_cost_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], COST_label[0], True, False)
    partial_compiled_cost_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], COST_label[0], True, False)
    partial_ic_compiled_cost_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], COST_label[0], True, False)
    tsf_cost_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, ETA_label[0], COST_label[0], True, False)

    # Plot
    print("Plotting...")
    htrbp_legend_label = "recompression \nw/ htr bypass"
    recomp_legend_label = "recompression"
    simple_legend_label = "simple"
    simple_bp_legend_label = "simple w/ bypass"
    partial_legend_label = "partial cooling"
    partial_ic_legend_label = "simple intercooling"
    tsf_legend_label = "turbine split flow"

    fig_width = 6 * 1.6
    fig_height = 2.2 * 1.6

    # Combine All 4 Plots
    fig_abstract_all, ((ax1_abstract_allsweep, ax2_abstract_allsweep), (ax1_abstract_allpareto, ax2_abstract_allpareto)) = plt.subplots(2,2)
    fig_abstract_all.set_size_inches(fig_width, fig_height * 2)

    ax1_abstract_allsweep.set_xlim(0.2,0.6)
    ax2_abstract_allsweep.set_xlim(0.2,0.6)
    ax1_abstract_allpareto.set_xlim(0.2,0.6)
    ax2_abstract_allpareto.set_xlim(0.2,0.6)

    ax1_abstract_allsweep.set_ylim(0,700)
    ax2_abstract_allsweep.set_ylim(0,60)
    ax1_abstract_allpareto.set_ylim(0,700)
    ax2_abstract_allpareto.set_ylim(0,20)

    # Sweep (Temp vs ETA)
    design_tools.plot_scatter_pts([
                [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                ], 
                ETA_label, T_HTF_label, ax=ax1_abstract_allsweep, show_legend=False)
    
    # Sweep (Cost vs ETA)
    design_tools.plot_scatter_pts([
                [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],
                [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],
                [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                ], 
                ETA_label, COST_label, ax=ax2_abstract_allsweep, show_legend=True, legend_loc='upper right')
    
    # Pareto (Temp vs ETA)
    design_tools.plot_scatter_pts([
                [simple_compiled_T_HTF_pareto_dict, {'label':simple_legend_label, 'marker':'.'}],
                [simple_htrbp_compiled_T_HTF_pareto_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                [recomp_compiled_T_HTF_pareto_dict, {'label':recomp_legend_label, 'marker':'.'}],
                [htrbp_compiled_T_HTF_pareto_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                [partial_ic_compiled_T_HTF_pareto_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                [partial_compiled_T_HTF_pareto_dict, {'label':partial_legend_label, 'marker':'.'}],          
                [tsf_T_HTF_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                ], 
                ETA_label, T_HTF_label, ax=ax1_abstract_allpareto, show_legend=False)

    # Pareto (Cost vs ETA)
    design_tools.plot_scatter_pts([
                [simple_compiled_cost_pareto_dict, {'label':simple_legend_label, 'marker':'.'}],
                [simple_htrbp_compiled_cost_pareto_dict, {'label':simple_bp_legend_label, 'marker':'.'}],
                [recomp_compiled_cost_pareto_dict, {'label':recomp_legend_label, 'marker':'.'}],
                [htrbp_compiled_cost_pareto_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                [partial_ic_compiled_cost_pareto_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                [partial_compiled_cost_pareto_dict, {'label':partial_legend_label, 'marker':'.'}],
                [tsf_cost_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                ], 
                ETA_label, COST_label, ax=ax2_abstract_allpareto, show_legend=False, legend_loc='upper left')

    plt.tight_layout()
    plt.rc('font', size=11) 

def plot_compare_sweeps(filename1, filename2, X_label, Y_label, title='',
                        label1='1', label2='2'):
    
    print("Opening " + label1 + '...')
    sim_collection1 = sco2_solve.C_sco2_sim_result_collection()
    sim_collection1.open_csv(filename1)
    print("Opened " + label1)

    print("Opening " + label2 + '...')
    sim_collection2 = sco2_solve.C_sco2_sim_result_collection()
    sim_collection2.open_csv(filename2)
    print("Opened " + label2)
    
    # Create Cycle Split T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    pareto_dict1 = design_tools.get_pareto_dict(sim_collection1.old_result_dict, X_label[0], Y_label[0], True, False)
    pareto_dict2 = design_tools.get_pareto_dict(sim_collection2.old_result_dict, X_label[0], Y_label[0], True, False)

    # Pareto (Temp vs ETA)
    design_tools.plot_scatter_pts([
                [pareto_dict1, {'marker':'.', 'label':label1}],
                [pareto_dict2, {'marker':'.', 'label':label2}],
                ], 
                X_label, Y_label, title=(title + ' pareto'))
    
    # Sweep (Temp vs ETA)
    design_tools.plot_scatter_pts([
                [sim_collection1.old_result_dict, {'marker':'.', 'label':label1}],
                [sim_collection2.old_result_dict, {'marker':'.', 'label':label2}],
                ], 
                X_label, Y_label, title=(title + ' sweep'))

def get_bounds_filename(design_var_arr, result_filename):
    print("Opening " + result_filename)
    sim_collection = sco2_solve.C_sco2_sim_result_collection()
    sim_collection.open_csv(result_filename)
    print(result_filename + " opened")

    return get_bounds(design_var_arr, sim_collection.old_result_dict)

def get_bounds(design_var_arr, result_dict):
    design_var_dict = {}
    for key in design_var_arr:
        if(key in result_dict):
            min_val = min(result_dict[key])
            max_val = max(result_dict[key])
            design_var_dict[key] = [min_val, max_val]

    return design_var_dict



def compare_new_vs_old_plots():

    # Plot original data
    tsf_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\TSF_G3P3_collection_10_20240426_224925.csv"
    recomp_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\recomp_G3P3_collection_10_20240426_223109.csv"
    partial_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\partial_G3P3_collection_10_20240426_204607.csv"
    htrbp_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\htrbp_G3P3_collection_10_20240427_205838.csv"

    #plot_sweep(tsf_filename_old, recomp_filename_old, partial_filename_old, htrbp_filename_old)

    # Plot new data
    tsf_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\TSF_G3P3_collection_10_20241209_171618.csv"
    recomp_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\recomp_G3P3_collection_10_20241209_171025.csv"
    partial_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\partial_G3P3_collection_10_20241209_170434.csv"
    htrbp_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\htrbp_G3P3_collection_10_20241209_182054.csv"

    #plot_sweep(tsf_filename_new, recomp_filename_new, partial_filename_new, htrbp_filename_new)

    plot_compare_sweeps(recomp_filename_old, recomp_filename_new, 
                        ["eta_thermal_calc", "", "Cycle Thermal Efficiency"],
                        ["T_htf_cold_des", "C", "HTF Outlet Temperature"])

def compare_bounds():
    # Original data
    tsf_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\TSF_G3P3_collection_10_20240426_224925.csv"
    recomp_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\recomp_G3P3_collection_10_20240426_223109.csv"
    partial_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\partial_G3P3_collection_10_20240426_204607.csv"
    htrbp_filename_old = r"C:\Users\tbrown2\Desktop\sco2_python\G3P3\htrbp_G3P3_collection_10_20240427_205838.csv"

    # New data
    tsf_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\TSF_G3P3_collection_10_20241209_171618.csv"
    recomp_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\recomp_G3P3_collection_10_20241209_171025.csv"
    partial_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\partial_G3P3_collection_10_20241209_170434.csv"
    htrbp_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\htrbp_G3P3_collection_10_20241209_182054.csv"

    # Define design variables
    design_var_arr = ["UA_recup_tot_des", "is_bypass_ok", "is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed", "T_bypass_target", "min_phx_deltaT", "is_turbine_split_ok",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    recomp_bounds_old = get_bounds_filename(design_var_arr, recomp_filename_old)
    recomp_bounds_new = get_bounds_filename(design_var_arr, recomp_filename_new)

    tsf_bounds_old = get_bounds_filename(design_var_arr, tsf_filename_old)
    tsf_bounds_new = get_bounds_filename(design_var_arr, tsf_filename_new)

    

    partial_bounds_old = get_bounds_filename(design_var_arr, partial_filename_old)
    partial_bounds_new = get_bounds_filename(design_var_arr, partial_filename_new)

    htrbp_bounds_old = get_bounds_filename(design_var_arr, htrbp_filename_old)
    htrbp_bounds_new = get_bounds_filename(design_var_arr, htrbp_filename_new)


    x = 0


def compare_sweeps_recomp():
    recomp_filename_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\reduced\recomp_G3P3_collection_5_20240426_163437.csv"
    recomp_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_orig\run_5_20241212_090715\recomp_G3P3_collection_5_20241212_090958.csv"

    plot_compare_sweeps(recomp_filename_old, recomp_filename_new, 
                        ["eta_thermal_calc", "", "Cycle Thermal Efficiency"],
                        ["T_htf_cold_des", "C", "HTF Outlet Temperature"], 'recomp')
    
    # Define design variables
    design_var_arr = ["UA_recup_tot_des", "is_bypass_ok", "is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed", "T_bypass_target", "min_phx_deltaT", "is_turbine_split_ok",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    recomp_bounds_old = get_bounds_filename(design_var_arr, recomp_filename_old)
    recomp_bounds_new = get_bounds_filename(design_var_arr, recomp_filename_new)

    input_var_vec = ["is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    output_var_vec = ["eta_thermal_calc"]

    no_input_match_vec, outputs_match_vec, outputs_no_match_vec = compare_sweeps_complete(recomp_filename_old, recomp_filename_new, input_var_vec, output_var_vec)
    
    total_cases = len(no_input_match_vec) + len(outputs_match_vec) + len(outputs_no_match_vec)
    total_input_match = total_cases - len(no_input_match_vec)
    missing_percent = (len(no_input_match_vec) / total_cases) * 100
    match_percent = (len(outputs_match_vec) / total_input_match) * 100
    no_match_percent = (len(outputs_no_match_vec) / total_input_match) * 100


    x = 0

def compare_sweeps_partial():
    filename_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\reduced\partial_G3P3_collection_5_20240426_162235.csv"
    filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_orig\run_5_20241212_090715\partial_G3P3_collection_5_20241212_090911.csv"

    plot_compare_sweeps(filename_old, filename_new, 
                        ["eta_thermal_calc", "", "Cycle Thermal Efficiency"],
                        ["T_htf_cold_des", "C", "HTF Outlet Temperature"], 'partial')
    
    # Define design variables
    design_var_arr = ["UA_recup_tot_des", "is_bypass_ok", "is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed", "T_bypass_target", "min_phx_deltaT", "is_turbine_split_ok",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    bounds_old = get_bounds_filename(design_var_arr, filename_old)
    bounds_new = get_bounds_filename(design_var_arr, filename_new)

    x = 0

    input_var_vec = ["is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed",
                      "eta_isen_mc", "dT_PHX_cold_approach"]

    output_var_vec = ["eta_thermal_calc"]

    no_input_match_vec, outputs_match_vec, outputs_no_match_vec = compare_sweeps_complete(filename_old, filename_new, input_var_vec, output_var_vec)
    
    total_cases = len(no_input_match_vec) + len(outputs_match_vec) + len(outputs_no_match_vec)
    total_input_match = total_cases - len(no_input_match_vec)
    missing_percent = (len(no_input_match_vec) / total_cases) * 100
    match_percent = (len(outputs_match_vec) / total_input_match) * 100
    no_match_percent = (len(outputs_no_match_vec) / total_input_match) * 100
    
    x = 0

def compare_sweeps_partial_IP():
    filename_orig = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\partial_G3P3_collection_10_20240426_204607.csv"
    filename_w_IP = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_w_IP\run_10_20241218_121515\partial_G3P3_collection_10_20241218_172723.csv"
    
    plot_compare_sweeps(filename_w_IP, filename_orig,
                        ["eta_thermal_calc", "", "Cycle Thermal Efficiency"],
                        ["T_htf_cold_des", "C", "HTF Outlet Temperature"], 'partial',
                        label1='IP Manual', label2='IP Auto')
    return
    # Define design variables
    design_var_arr = ["UA_recup_tot_des", "is_bypass_ok", "is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed", "T_bypass_target", "min_phx_deltaT", "is_turbine_split_ok",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    bounds_old = get_bounds_filename(design_var_arr, filename_orig)
    bounds_new = get_bounds_filename(design_var_arr, filename_w_IP)

    x = 0

    input_var_vec = ["is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed",
                      "eta_isen_mc", "dT_PHX_cold_approach"]

    output_var_vec = ["eta_thermal_calc"]

    no_input_match_vec, outputs_match_vec, outputs_no_match_vec = compare_sweeps_complete(filename_orig, filename_w_IP, input_var_vec, output_var_vec)
    
    total_cases = len(no_input_match_vec) + len(outputs_match_vec) + len(outputs_no_match_vec)
    total_input_match = total_cases - len(no_input_match_vec)
    missing_percent = (len(no_input_match_vec) / total_cases) * 100
    match_percent = (len(outputs_match_vec) / total_input_match) * 100
    no_match_percent = (len(outputs_no_match_vec) / total_input_match) * 100
    
    x = 0

def compare_sweeps_tsf():
    filename_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\reduced\TSF_G3P3_collection_5_20240426_163601.csv"
    filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_orig\run_5_20241212_090715\TSF_G3P3_collection_5_20241212_091054.csv"

    plot_compare_sweeps(filename_old, filename_new, 
                        ["eta_thermal_calc", "", "Cycle Thermal Efficiency"],
                        ["T_htf_cold_des", "C", "HTF Outlet Temperature"], 'tsf')
    
    # Define design variables
    design_var_arr = ["UA_recup_tot_des", "is_bypass_ok", "is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed", "T_bypass_target", "min_phx_deltaT", "is_turbine_split_ok",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    bounds_old = get_bounds_filename(design_var_arr, filename_old)
    bounds_new = get_bounds_filename(design_var_arr, filename_new)

    x = 0

    input_var_vec = ["is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in", "is_turbine_split_ok",
                      "P_high_limit", "is_PR_fixed",
                      "eta_isen_mc", "dT_PHX_cold_approach"]

    output_var_vec = ["eta_thermal_calc"]

    no_input_match_vec, outputs_match_vec, outputs_no_match_vec = compare_sweeps_complete(filename_old, filename_new, input_var_vec, output_var_vec)
    
    total_cases = len(no_input_match_vec) + len(outputs_match_vec) + len(outputs_no_match_vec)
    total_input_match = total_cases - len(no_input_match_vec)
    missing_percent = (len(no_input_match_vec) / total_cases) * 100
    match_percent = (len(outputs_match_vec) / total_input_match) * 100
    no_match_percent = (len(outputs_no_match_vec) / total_input_match) * 100
    
    x = 0

def compare_sweeps_htrbp():
    filename_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\reduced\htrbp_G3P3_collection_5_20240426_174143.csv"
    filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_orig\run_5_20241212_090715\htrbp_G3P3_collection_5_20241212_091408.csv"

    plot_compare_sweeps(filename_old, filename_new, 
                        ["eta_thermal_calc", "", "Cycle Thermal Efficiency"],
                        ["T_htf_cold_des", "C", "HTF Outlet Temperature"], 'htrbp')
    
    # Define design variables
    design_var_arr = ["UA_recup_tot_des", "is_bypass_ok", "is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed", "T_bypass_target", "min_phx_deltaT", "is_turbine_split_ok",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    bounds_old = get_bounds_filename(design_var_arr, filename_old)
    bounds_new = get_bounds_filename(design_var_arr, filename_new)

    x = 0

    input_var_vec = ["is_recomp_ok", "is_bypass_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed",
                      "eta_isen_mc", "dT_PHX_cold_approach"]

    output_var_vec = ["eta_thermal_calc"]

    no_input_match_vec, outputs_match_vec, outputs_no_match_vec = compare_sweeps_complete(filename_old, filename_new, input_var_vec, output_var_vec)
    
    total_cases = len(no_input_match_vec) + len(outputs_match_vec) + len(outputs_no_match_vec)
    total_input_match = total_cases - len(no_input_match_vec)
    missing_percent = (len(no_input_match_vec) / total_cases) * 100
    match_percent = (len(outputs_match_vec) / total_input_match) * 100
    no_match_percent = (len(outputs_no_match_vec) / total_input_match) * 100
    
    x = 0

def compare_sweeps_complete(sweep1_filename, sweep2_filename,
                            input_var_vec, output_var_vec,
                            eta_cutoff=-1       
                            ):
    print("Opening " + sweep1_filename)
    sim_collection1 = sco2_solve.C_sco2_sim_result_collection()
    sim_collection1.open_csv(sweep1_filename)
    print(sweep1_filename + " opened")

    print("Opening " + sweep2_filename)
    sim_collection2 = sco2_solve.C_sco2_sim_result_collection()
    sim_collection2.open_csv(sweep2_filename)
    print(sweep2_filename + " opened")

    sim_result_dict1 = sim_collection1.old_result_dict
    sim_result_dict2 = sim_collection2.old_result_dict

    # Sort by first input key
    sim_result_dict1 = design_tools.sort_by_key(sim_result_dict1, input_var_vec[0], reverse=False)
    sim_result_dict2 = design_tools.sort_by_key(sim_result_dict2, input_var_vec[0], reverse=False)

    # Allocate Results
    no_input_match_vec = []
    outputs_match_vec = []
    outputs_no_match_vec = []

    # Loop through every result in sweep1
    diff_dict_vec = []
    NVals = len(sim_result_dict1[input_var_vec[0]])
    for i in range(NVals):
        input_dict = {}
        # Loop through design inputs
        for input_key in input_var_vec:
            input_dict[input_key] = sim_result_dict1[input_key][i]

        # Find case with same parameters
        NVals2 = len(sim_result_dict2[input_var_vec[0]])
        match_id = -1
        for i2 in range(NVals2):
            equal_inputs = True
            for key1 in input_dict:
                if(input_dict[key1] != sim_result_dict2[key1][i2]):
                    equal_inputs = False
                    continue
            if equal_inputs == True:
                match_id = i2
                break
        
        # Compare results
        cases_match = True
        if(equal_inputs == True):
            # Collect Results
            for output_key in output_var_vec:
                if(sim_result_dict1[output_key][i] != sim_result_dict2[output_key][match_id]):
                    # Case Results do not match
                    cases_match = False
            if(cases_match == True):
                outputs_match_vec.append(i)
            else:
                outputs_no_match_vec.append(i)
        else:
            cases_match = False
            no_input_match_vec.append(i)


    return no_input_match_vec, outputs_match_vec, outputs_no_match_vec        

def test_compare_sweeps():
    recomp_filename_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\reduced\recomp_G3P3_collection_5_20240426_163437.csv"
    recomp_filename_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_orig\run_5_20241211_153631\recomp_G3P3_collection_5_20241211_153704.csv"

    input_var_vec = ["is_recomp_ok", "HTR_UA_des_in", "LTR_UA_des_in",
                      "P_high_limit", "is_PR_fixed",
                      "eta_isen_mc", "dT_PHX_cold_approach"]
    
    output_var_vec = ["eta_thermal_calc"]

    no_input_match_vec, outputs_match_vec, outputs_no_match_vec = compare_sweeps_complete(recomp_filename_old, recomp_filename_new, input_var_vec, output_var_vec)
    
    total_cases = len(no_input_match_vec) + len(outputs_match_vec) + len(outputs_no_match_vec)
    total_input_match = total_cases - len(no_input_match_vec)
    missing_percent = (len(no_input_match_vec) / total_cases) * 100
    match_percent = (len(outputs_match_vec) / total_input_match) * 100
    no_match_percent = (len(outputs_no_match_vec) / total_input_match) * 100

    x = 0

# Main Script

if __name__ == "__main__":
    #test_compare_sweeps()
    #compare_sweeps_recomp()
    #compare_sweeps_partial()
    #compare_sweeps_tsf()
    #compare_sweeps_htrbp()
    #compare_new_vs_old_plots()
    compare_sweeps_partial_IP()
    plt.show(block = True)