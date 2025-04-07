import sys
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import pickle

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

from G3P3_analysis.sco2_baseline_sim_w_IP import get_sco2_G3P3
import sco2_cycle_ssc as sco2_solve
import design_point_examples as design_pt
import design_point_tools as design_tools
import sco2_plot_sandbox as plot_sandbox

# Utility

def get_min(dict_list, key):
    min_val = min(dict_list[0][key])
    min_dict_index = 0
    min_col_index = dict_list[0][key].index(min_val)

    for dict_id in range(len(dict_list)):
        diction = dict_list[dict_id]
        min_local = min(diction[key])
        if(min_local < min_val):
            min_val = min_local
            min_dict_index = dict_id
            min_col_index = diction[key].index(min_val)

    min_diction = {}
    for key in dict_list[min_dict_index]:
        min_diction[key] = dict_list[min_dict_index][key][min_col_index]

    return min_val, min_diction

def get_norm_list(val_list, val_min=0):
    if val_min == 0:
        val_min = min(val_list)
    norm_list = []
    for val in val_list:
        norm_list.append(val / val_min)
    return norm_list

def remove_cases(result_dict, key, val_min):
    # remove all cases with key value below val
    remove_id_list = []
    id = 0
    for val in result_dict[key]:
        if((val == '') or val <= val_min):
            remove_id_list.append(id)
        id += 1

    for remove_counter in range(len(remove_id_list)):
        id_remove = remove_id_list[len(remove_id_list) - remove_counter - 1]
        for key in result_dict:
            del result_dict[key][id_remove]

    return result_dict

# Plot methods

def plot_g3p3(htrbp_result_dict, recomp_result_dict,
               tsf_result_dict, partial_result_dict):
    # HTR BP (only comes from htr bp file)
    htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict],
                                                            "config_name", "htr bp")

    # Recompression (comes from recomp and htr bp)
    recomp_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict, 
                                                            recomp_result_dict],  
                                                            "config_name", "recompression")

    # Simple (from recomp and htr bp)
    simple_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict, 
                                                            recomp_result_dict],  
                                                            "config_name", "simple")

    # Simple w/ htr bypass (from htr bp only)
    simple_htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict],
                                                            "config_name", "simple split flow bypass")
    
    # Partial (only comes from partial file)
    partial_compiled_dict = design_tools.combine_dict_by_key([partial_result_dict],
                                                            "config_name", "partial")

    # Partial Intercooling (only comes from partial file)
    partial_ic_compiled_dict = design_tools.combine_dict_by_key([partial_result_dict],
                                                            "config_name", "partial intercooling")

    # Variables to Display
    ETA_label = ["design_eff", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    COST_PER_kW_GROSS_label = ["cost_per_kWe_gross", "$/kWe", "Cost per kWe Gross"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    W_DOT_NET_label = ["W_dot_net_ish", "MWe", "Net Power Output"]
    COST_PER_kW_GROSS_NORM_label = ["cost_per_kWe_gross_norm", "", "Cost per kWe Gross Normalized"]
    COST_PER_kW_NET_NORM_label = ["cost_per_kWe_net_ish_norm", "", "Cost per kWe Net Normalized"]

    # Remove negative power output cases
    htrbp_compiled_dict = remove_cases(htrbp_compiled_dict, COST_PER_kW_NET_label[0], 0)
    recomp_compiled_dict = remove_cases(recomp_compiled_dict, COST_PER_kW_NET_label[0], 0)
    simple_compiled_dict = remove_cases(simple_compiled_dict, COST_PER_kW_NET_label[0], 0)
    simple_htrbp_compiled_dict = remove_cases(simple_htrbp_compiled_dict, COST_PER_kW_NET_label[0], 0)
    partial_compiled_dict = remove_cases(partial_compiled_dict, COST_PER_kW_NET_label[0], 0)
    partial_ic_compiled_dict = remove_cases(partial_ic_compiled_dict, COST_PER_kW_NET_label[0], 0)
    tsf_result_dict = remove_cases(tsf_result_dict, COST_PER_kW_NET_label[0], 0)

    # Get Minimum Net Cost
    min_net_cost, min_diction = get_min([htrbp_compiled_dict, recomp_compiled_dict, simple_compiled_dict,
                            simple_htrbp_compiled_dict, partial_compiled_dict, partial_ic_compiled_dict,
                            tsf_result_dict], COST_PER_kW_NET_label[0])

    save_min_file = False
    if save_min_file:
        save_file = asksaveasfilename(confirmoverwrite=True, filetypes =[('CSV Files', '*.gif')], title="Save min case?")
        if(save_file != ''):
            design_tools.write_dict(save_file, min_diction, ',')

    # Add normalized COST
    htrbp_net_norm_list = get_norm_list(htrbp_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    recomp_net_norm_list = get_norm_list(recomp_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    simple_net_norm_list = get_norm_list(simple_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    simple_htrbp_net_norm_list = get_norm_list(simple_htrbp_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    partial_net_norm_list = get_norm_list(partial_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    partial_ic_net_norm_list = get_norm_list(partial_ic_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    tsf_net_norm_list = get_norm_list(tsf_result_dict[COST_PER_kW_NET_label[0]], min_net_cost)

    htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = htrbp_net_norm_list
    recomp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = recomp_net_norm_list
    simple_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_net_norm_list
    simple_htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_htrbp_net_norm_list
    partial_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_net_norm_list
    partial_ic_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_ic_net_norm_list
    tsf_result_dict[COST_PER_kW_NET_NORM_label[0]] = tsf_net_norm_list

    # Create Net Cost vs Efficiency Pareto Front
    print("Forming eff pareto fronts...")
    htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    recomp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_ic_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    tsf_eff_pareto_dict = design_tools.get_pareto_dict(tsf_result_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)

    # Create Net Cost vs T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_result_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)

    # Plot
    print("Plotting...")
    htrbp_legend_label = "recompression \nw/ htr bypass"
    recomp_legend_label = "recompression"
    simple_legend_label = "simple"
    simple_bp_legend_label = "simple w/ bypass"
    partial_legend_label = "partial cooling"
    partial_ic_legend_label = "simple intercooling"
    tsf_legend_label = "turbine split flow"

    # Cost Gross vs ETA
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_GROSS_label, show_legend=True, legend_loc='upper right')
    
    # Cost Gross vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_GROSS_label, show_legend=True, legend_loc='upper right')
    
    # Cost Net vs ETA
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_label, show_legend=True, legend_loc='upper right')
    
    # Cost Net vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_label, show_legend=True, legend_loc='upper right')

    # Cost Gross vs W_dot_net
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    W_DOT_NET_label, COST_PER_kW_GROSS_label, show_legend=True, legend_loc='upper right')

    # Poster specific plots
    size_factor = 1.6
    fig_width = 6 * size_factor
    fig_height = 2.2 * size_factor
    fig_poster_net_cost, (ax1_poster_net_cost, ax2_poster_net_cost) = plt.subplots(1,2)
    fig_poster_net_cost.set_size_inches(fig_width, fig_height)
    ax1_poster_net_cost.set_xlim(0.2, 0.6)
    ax1_poster_net_cost.set_ylim(5000, 10000)
    ax2_poster_net_cost.set_xlim(400, 700)
    ax2_poster_net_cost.set_ylim(5000, 10000)
    ax1_poster_net_cost.xaxis.grid(True)
    ax1_poster_net_cost.yaxis.grid(True)
    ax2_poster_net_cost.xaxis.grid(True)
    ax2_poster_net_cost.yaxis.grid(True)
    ax1_poster_net_cost.set_axisbelow(True)
    ax2_poster_net_cost.set_axisbelow(True)

    # Cost Net vs ETA
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_label, ax=ax1_poster_net_cost, show_legend=False, legend_loc='upper right')

    # Cost Net vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_label, ax=ax2_poster_net_cost, show_legend=True, legend_loc='center left', legend_outside=(1,0.5))

    plt.tight_layout()
    plt.rc('font', size=11) 

    # Poster Normalized
    fig_poster_net_cost_norm, (ax1_poster_net_cost_norm, ax2_poster_net_cost_norm) = plt.subplots(1,2)
    fig_poster_net_cost_norm.set_size_inches(fig_width, fig_height)
    ax1_poster_net_cost_norm.set_xlim(0.2, 0.6)
    ax1_poster_net_cost_norm.set_ylim(0.9, 1.8)
    ax2_poster_net_cost_norm.set_xlim(400, 700)
    ax2_poster_net_cost_norm.set_ylim(0.9, 1.8)
    ax1_poster_net_cost_norm.xaxis.grid(True)
    ax1_poster_net_cost_norm.yaxis.grid(True)
    ax2_poster_net_cost_norm.xaxis.grid(True)
    ax2_poster_net_cost_norm.yaxis.grid(True)
    ax1_poster_net_cost_norm.set_axisbelow(True)
    ax2_poster_net_cost_norm.set_axisbelow(True)
    
    # Cost Net vs ETA
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_NORM_label, ax=ax1_poster_net_cost_norm, show_legend=False, legend_loc='upper right')
    

    # Cost Net vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_NORM_label, ax=ax2_poster_net_cost_norm, show_legend=False, legend_loc='upper left')

    # Pareto Fronts
    fig_pareto, (ax1_pareto_eff, ax2_pareto_T_HTF) = plt.subplots(1,2)
    fig_pareto.set_size_inches(fig_width, fig_height)
    pareto_y_limit = [5400, 6400]
    #ax1_pareto_eff.set_xlim(0.2, 0.6)
    ax1_pareto_eff.set_ylim(pareto_y_limit[0], pareto_y_limit[1])
    ax2_pareto_T_HTF.set_xlim(450, 600)
    ax2_pareto_T_HTF.set_ylim(pareto_y_limit[0], pareto_y_limit[1])
    ax1_pareto_eff.xaxis.grid(True)
    ax1_pareto_eff.yaxis.grid(True)
    ax2_pareto_T_HTF.xaxis.grid(True)
    ax2_pareto_T_HTF.yaxis.grid(True)
    ax1_pareto_eff.set_axisbelow(True)
    ax2_pareto_T_HTF.set_axisbelow(True)
    
    # Cost Net vs ETA Pareto
    design_tools.plot_scatter_pts([
                    [simple_compiled_eff_pareto_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_eff_pareto_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_eff_pareto_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_eff_pareto_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_eff_pareto_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_eff_pareto_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_eff_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_label, ax=ax1_pareto_eff, show_legend=False, legend_loc='upper right')
    

    # Cost Net vs min Temp Pareto
    design_tools.plot_scatter_pts([
                    [simple_compiled_T_HTF_pareto_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_T_HTF_pareto_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_T_HTF_pareto_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_T_HTF_pareto_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_T_HTF_pareto_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_T_HTF_pareto_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_T_HTF_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_label, ax=ax2_pareto_T_HTF, show_legend=True, legend_loc='center left', legend_outside=(1,0.5))

    plt.tight_layout()
    plt.rc('font', size=11) 

def plot_pkl_g3p3_via_filedlg():
    
    window = tk.Tk()
    htrbp_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 htrbp pkl file")
    recomp_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 recomp pkl file")
    tsf_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 tsf pkl file")
    partial_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 partial pkl file")

    filename_list = [htrbp_filename, recomp_filename,
                     tsf_filename, partial_filename]
    result_dict_list = []

    for filename in filename_list:
        with open(filename, 'rb') as f:
            result_dict = pickle.load(f)
        result_dict_list.append(result_dict)
    
    plot_g3p3(*result_dict_list)

def plot_g3p3_failed(result_dict, label=''):
    # Variables to Display
    ETA_label = ["eta_thermal_calc", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]
    success_label = ["cmod_success", "", "cmod_success"]

    COST_PER_kW_GROSS_label = ["cost_per_kWe_gross", "$/kWe", "Cost per kWe Gross"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    W_DOT_NET_label = ["W_dot_net_ish", "MWe", "Net Power Output"]
    COST_PER_kW_GROSS_NORM_label = ["cost_per_kWe_gross_norm", "", "Cost per kWe Gross Normalized"]
    COST_PER_kW_NET_NORM_label = ["cost_per_kWe_net_ish_norm", "", "Cost per kWe Net Normalized"]

    design_tools.plot_scatter_pts([
                    [result_dict, {'label':label, 'marker':'.'}]
                    ], 
                    ETA_label, T_HTF_label, success_label, show_legend=True, legend_loc='upper right')

def plot_test():
    filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\zG3P3_results_20250104_071844__htrbp_G3P3_collection_10_20250103_192511_000.pkl"
    filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\zG3P3_results_20250105_132500__recomp_G3P3_collection_10_20250103_190235_000.pkl"
    filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\zG3P3_results_20250105_152227__TSF_G3P3_collection_10_20250103_191443_000.pkl"
    filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\zG3P3_results_20250104_235339__partial_G3P3_collection_10_20250103_132840_000.pkl"

    filename_tuple_list = [[filename_htrbp, "htrbp"],
                           [filename_recomp, "recomp"],
                           [filename_tsf, "tsf"],
                           [filename_partial, "partial"]]

    for filename_tuple in filename_tuple_list:
        filename = filename_tuple[0]
        filename_title = filename_tuple[1]
        result_dict = {}
        with open(filename, 'rb') as f:
                result_dict = pickle.load(f)

        plot_g3p3_failed(result_dict, filename_title)

    




if __name__ == "__main__":
    #display_eff()
    #plot_sweep()
    #plot_via_filedlg()
    plot_test()
    #plot_pkl_via_filedlg()
    #plot_pkl_g3p3_via_filedlg()
    plt.show(block = True)