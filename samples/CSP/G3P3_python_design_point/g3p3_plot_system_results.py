import numpy as np

import matplotlib.lines as mlines
import multiprocessing
from functools import partial
import time
import datetime
import sys
import os
import matplotlib.pyplot as plt
from tkinter.filedialog import asksaveasfilename

sys.path.append("sco2-python")

newPath = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')

import sco2_sim_result_collection as sco2_result_collection
import g3p3_annual_sim_refactored as g3p3_case
import design_point_tools as design_tools

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
        if(val <= val_min):
            remove_id_list.append(id)
        id += 1

    for remove_counter in range(len(remove_id_list)):
        id_remove = remove_id_list[len(remove_id_list) - remove_counter - 1]
        for key in result_dict:
            del result_dict[key][id_remove]

    return result_dict

def plot_contours(dict_list_with_kwarg, X_info, Y_info, Z_info, title="", figure_size=[], ax=0, show_legend=True, legend_loc="", show_Z_legend=True):

    #marker_list = get_marker_list()

    # Process Labels
    X_label = ""
    Y_label = ""
    Z_label = ""

    X_unit = ""
    Y_unit = ""
    Z_unit = ""

    if(isinstance(X_info, list)):
        X_label = X_info[0]
        if len(X_info) > 0:
            X_unit = X_info[1]
    else:
        X_label = X_info

    if(isinstance(Y_info, list)):
        Y_label = Y_info[0]
        if len(Y_info) > 0:
            Y_unit = Y_info[1]
    else:
        Y_label = Y_info

    if(isinstance(Z_info, list)):
        Z_label = Z_info[0]
        if len(Z_info) > 0:
            Z_unit = Z_info[1]
    else:
        Z_label = Z_info

    # Make figure and axis if it doesn't exist already
    if(ax == 0):
        if(len(figure_size) == 2):
            fig = plt.figure(figsize=(figure_size[0],figure_size[1]))
        else:
            fig = plt.figure()
        
        if(ax == 0):
            ax = fig.add_subplot()        
    else:
        fig = ax.get_figure()
    i = 0
    dict_list = []
    for data in dict_list_with_kwarg:
        diction = data[0]

        kwarg_dict = {}
        if(len(data) > 1):
            kwarg_dict = data[1]
        #if ('marker' in kwarg_dict) == False:
        #    kwarg_dict['marker'] = marker_list[i+1]
        if (('c' in kwarg_dict) == False) and (Z_label != ""):
            kwarg_dict['c'] = diction[Z_label]

        #sca = ax.scatter(diction[X_label], diction[Y_label], c=diction[Z_label], label=label, marker=marker_list[i+1])

        #if(len(kwarg_dict.keys() == 0)):
        #    sca.set_marker

        sca = ax.tricontourf(diction[X_label], diction[Y_label], diction[Z_label], **kwarg_dict)
        #cmap='coolwarm', 
        dict_list.append(diction)

        i += 1

    cp3 = ax.collections[0]

    if isinstance(X_info, list) and len(X_info) > 2:
        X_plot_label = X_info[2]
    else:
        X_plot_label = X_label

    if isinstance(Y_info, list) and len(Y_info) > 2:
        Y_plot_label = Y_info[2]
    else:
        Y_plot_label = Y_label

    if(X_unit != ""):
        X_plot_label += " (" + X_unit + ")"

    if(Y_unit != ""):
        Y_plot_label += " (" + Y_unit + ")"

    ax.set_xlabel(X_plot_label)
    ax.set_ylabel(Y_plot_label)

    if isinstance(Z_info, list) and len(Z_info) > 2:
        Z_plot_label = Z_info[2]
    else:
        Z_plot_label = Z_label

    if(Z_unit != ""):
        Z_plot_label += " (" + Z_unit + ")"

    if(show_Z_legend == True):
        cb3 = fig.colorbar(ax.collections[0])
        cb3.set_label(Z_plot_label)

    if(title != ""):
        ax.set_title(title)

    # Handle Legend business
    if(show_legend):
        if(legend_loc == ""):
            legend_loc = "upper left"
        legend = ax.legend(loc=legend_loc)

    # Handle Click Business
    annot = ax.annotate("",xy=(0,0), xytext=(-100,20), textcoords="offset points",
                             bbox=dict(boxstyle="round", fc="w"),
                             arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    
    label_list = ["cycle_config", "config_name", "T_htf_cold_des", "eta_thermal_calc", "recup_total_UA_calculated", "LTR_UA_calculated", 
                  "HTR_UA_calculated", "UA_BPX", "UA_PHX",
                  "cycle_cost", "mc_cost_bare_erected", "rc_cost_bare_erected", "pc_cost_bare_erected", "t_cost_bare_erected", "t2_cost_bare_erected", "LTR_cost_bare_erected", "HTR_cost_bare_erected",
                  "PHX_cost_bare_erected", "BPX_cost_bare_erected", "mc_cooler_cost_bare_erected", "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost"]
    #fig.canvas.mpl_connect("button_press_event", lambda event: hover_multiple_pts(event, dict_list, label_list, fig, annot, ax, ax.collections))
   
    return ax


def plot_system_results(reduced=False):
    
    if reduced == True:
        recomp_csp_filename = r"..\g3p3_design_reduced\recomp_G3P3_system_cost.csv"
        tsf_csp_filename = r"..\g3p3_design_reduced\TSF_G3P3_system_cost.csv"
        partial_csp_filename = r"..\g3p3_design_reduced\partial_G3P3_system_cost.csv"
        htrbp_csp_filename = r"..\g3p3_design_reduced\htrbp_G3P3_system_cost.csv"
    else:
        recomp_csp_filename = r"..\g3p3_design_sweep1\recomp_G3P3_system_cost.csv"
        tsf_csp_filename = r"..\g3p3_design_sweep1\TSF_G3P3_system_cost.csv"
        partial_csp_filename = r"..\g3p3_design_sweep1\partial_G3P3_system_cost.csv"
        htrbp_csp_filename = r"..\g3p3_design_sweep1\htrbp_G3P3_system_cost.csv"

    print("Opening htrbp...")
    htrbp_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv(htrbp_csp_filename)
    print("HTR BP opened")

    print("Opening recomp...")
    recomp_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_csp_filename)
    print("Recomp open")

    print("Opening tsf...")
    tsf_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    tsf_sim_collection.open_csv(tsf_csp_filename)
    print("TSF opened")

    print("Opening partial...")
    partial_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    partial_sim_collection.open_csv(partial_csp_filename)
    print("Partial opened")

    print("")

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
    tsf_sim_collection.old_result_dict = remove_cases(tsf_sim_collection.old_result_dict, COST_PER_kW_NET_label[0], 0)

    # Get Minimum Net Cost
    min_net_cost, min_diction = get_min([htrbp_compiled_dict, recomp_compiled_dict, simple_compiled_dict,
                            simple_htrbp_compiled_dict, partial_compiled_dict, partial_ic_compiled_dict,
                            tsf_sim_collection.old_result_dict], COST_PER_kW_NET_label[0])

    save_min_file = True
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
    tsf_net_norm_list = get_norm_list(tsf_sim_collection.old_result_dict[COST_PER_kW_NET_label[0]], min_net_cost)

    htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = htrbp_net_norm_list
    recomp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = recomp_net_norm_list
    simple_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_net_norm_list
    simple_htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_htrbp_net_norm_list
    partial_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_net_norm_list
    partial_ic_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_ic_net_norm_list
    tsf_sim_collection.old_result_dict[COST_PER_kW_NET_NORM_label[0]] = tsf_net_norm_list

    # Create Net Cost vs Efficiency Pareto Front
    print("Forming eff pareto fronts...")
    htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    recomp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_ic_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    tsf_eff_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)

    # Create Net Cost vs T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)

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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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


    plt.show(block = True)

def plot_system_contours(reduced=False):
    if reduced == True:
        recomp_csp_filename = r"..\g3p3_design_reduced\recomp_G3P3_system_cost.csv"
        tsf_csp_filename = r"..\g3p3_design_reduced\TSF_G3P3_system_cost.csv"
        partial_csp_filename = r"..\g3p3_design_reduced\partial_G3P3_system_cost.csv"
        htrbp_csp_filename = r"..\g3p3_design_reduced\htrbp_G3P3_system_cost.csv"
    else:
        recomp_csp_filename = r"..\g3p3_design_sweep1\recomp_G3P3_system_cost.csv"
        tsf_csp_filename = r"..\g3p3_design_sweep1\TSF_G3P3_system_cost.csv"
        partial_csp_filename = r"..\g3p3_design_sweep1\partial_G3P3_system_cost.csv"
        htrbp_csp_filename = r"..\g3p3_design_sweep1\htrbp_G3P3_system_cost.csv"

    print("Opening htrbp...")
    htrbp_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv(htrbp_csp_filename)
    print("HTR BP opened")

    print("Opening recomp...")
    recomp_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_csp_filename)
    print("Recomp open")

    print("Opening tsf...")
    tsf_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    tsf_sim_collection.open_csv(tsf_csp_filename)
    print("TSF opened")

    print("Opening partial...")
    partial_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    partial_sim_collection.open_csv(partial_csp_filename)
    print("Partial opened")

    print("")

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
    ETA_label = ["design_eff", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    COST_PER_kW_GROSS_label = ["cost_per_kWe_gross", "$/kWe", "Cost per kWe Gross"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    W_DOT_NET_label = ["W_dot_net_ish", "MWe", "Net Power Output"]
    COST_PER_kW_GROSS_NORM_label = ["cost_per_kWe_gross_norm", "", "Cost per kWe Gross Normalized"]
    COST_PER_kW_NET_NORM_label = ["cost_per_kWe_net_ish_norm", "", "Cost per kWe Net Normalized"]
    
    REC_ETA_label = ["eta_rec_thermal_des", "", "Receiver Thermal Efficiency"]
    A_SF_label = ["A_sf", "m3", "Solar Field Area"]
    W_LIFT_label = ["W_dot_cycle_lift_des", "MWe", "Lift Power"]

    # Remove negative power output cases
    htrbp_compiled_dict = remove_cases(htrbp_compiled_dict, COST_PER_kW_NET_label[0], 0)
    recomp_compiled_dict = remove_cases(recomp_compiled_dict, COST_PER_kW_NET_label[0], 0)
    simple_compiled_dict = remove_cases(simple_compiled_dict, COST_PER_kW_NET_label[0], 0)
    simple_htrbp_compiled_dict = remove_cases(simple_htrbp_compiled_dict, COST_PER_kW_NET_label[0], 0)
    partial_compiled_dict = remove_cases(partial_compiled_dict, COST_PER_kW_NET_label[0], 0)
    partial_ic_compiled_dict = remove_cases(partial_ic_compiled_dict, COST_PER_kW_NET_label[0], 0)
    tsf_sim_collection.old_result_dict = remove_cases(tsf_sim_collection.old_result_dict, COST_PER_kW_NET_label[0], 0)

    # Get Minimum Net Cost
    min_net_cost, empty = get_min([htrbp_compiled_dict, recomp_compiled_dict, simple_compiled_dict,
                            simple_htrbp_compiled_dict, partial_compiled_dict, partial_ic_compiled_dict,
                            tsf_sim_collection.old_result_dict], COST_PER_kW_NET_label[0])

    # Add normalized COST
    htrbp_net_norm_list = get_norm_list(htrbp_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    recomp_net_norm_list = get_norm_list(recomp_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    simple_net_norm_list = get_norm_list(simple_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    simple_htrbp_net_norm_list = get_norm_list(simple_htrbp_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    partial_net_norm_list = get_norm_list(partial_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    partial_ic_net_norm_list = get_norm_list(partial_ic_compiled_dict[COST_PER_kW_NET_label[0]], min_net_cost)
    tsf_net_norm_list = get_norm_list(tsf_sim_collection.old_result_dict[COST_PER_kW_NET_label[0]], min_net_cost)

    htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = htrbp_net_norm_list
    recomp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = recomp_net_norm_list
    simple_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_net_norm_list
    simple_htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_htrbp_net_norm_list
    partial_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_net_norm_list
    partial_ic_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_ic_net_norm_list
    tsf_sim_collection.old_result_dict[COST_PER_kW_NET_NORM_label[0]] = tsf_net_norm_list

    # Create Net Cost vs Efficiency Pareto Front
    print("Forming eff pareto fronts...")
    htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    recomp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_ic_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    tsf_eff_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)

    # Create Net Cost vs T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)

    # Plot
    print("Plotting...")
    htrbp_legend_label = "recompression \nw/ htr bypass"
    recomp_legend_label = "recompression"
    simple_legend_label = "simple"
    simple_bp_legend_label = "simple w/ bypass"
    partial_legend_label = "partial cooling"
    partial_ic_legend_label = "simple intercooling"
    tsf_legend_label = "turbine split flow"

    # Receiver Efficiency
    plot_contours([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, ETA_label, REC_ETA_label, show_legend=False, legend_loc='upper left')

    # Solar Field Area
    plot_contours([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, ETA_label, A_SF_label, show_legend=False, legend_loc='upper left')
    
    # Lift Parasitics
    plot_contours([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, ETA_label, W_LIFT_label, show_legend=False, legend_loc='upper left')

    plt.tight_layout()
    plt.rc('font', size=11) 


    plt.show(block = True)

def save_min_configs(reduced=False):
    if reduced == True:
        recomp_csp_filename = r"..\g3p3_design_reduced\recomp_G3P3_system_cost.csv"
        tsf_csp_filename = r"..\g3p3_design_reduced\TSF_G3P3_system_cost.csv"
        partial_csp_filename = r"..\g3p3_design_reduced\partial_G3P3_system_cost.csv"
        htrbp_csp_filename = r"..\g3p3_design_reduced\htrbp_G3P3_system_cost.csv"
    else:
        recomp_csp_filename = r"..\g3p3_design_sweep1\recomp_G3P3_system_cost.csv"
        tsf_csp_filename = r"..\g3p3_design_sweep1\TSF_G3P3_system_cost.csv"
        partial_csp_filename = r"..\g3p3_design_sweep1\partial_G3P3_system_cost.csv"
        htrbp_csp_filename = r"..\g3p3_design_sweep1\htrbp_G3P3_system_cost.csv"

    print("Opening htrbp...")
    htrbp_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv(htrbp_csp_filename)
    print("HTR BP opened")

    print("Opening recomp...")
    recomp_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_csp_filename)
    print("Recomp open")

    print("Opening tsf...")
    tsf_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    tsf_sim_collection.open_csv(tsf_csp_filename)
    print("TSF opened")

    print("Opening partial...")
    partial_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    partial_sim_collection.open_csv(partial_csp_filename)
    print("Partial opened")

    print("")

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
    tsf_sim_collection.old_result_dict = remove_cases(tsf_sim_collection.old_result_dict, COST_PER_kW_NET_label[0], 0)

    # Get Minimum Net Cost
    min_htrbp_cost, min_htrbp_diction = get_min([htrbp_compiled_dict,], COST_PER_kW_NET_label[0])

    min_recomp_cost, min_recomp_diction = get_min([recomp_compiled_dict,], COST_PER_kW_NET_label[0])
    
    min_simple_cost, min_simple_diction = get_min([simple_compiled_dict,], COST_PER_kW_NET_label[0])
    
    min_simple_htrbp_cost, min_simple_htrbp_diction = get_min([simple_htrbp_compiled_dict,], COST_PER_kW_NET_label[0])
    
    min_partial_cost, min_partial_diction = get_min([partial_compiled_dict, ], COST_PER_kW_NET_label[0])
    
    min_partial_ic_cost, min_partial_ic_diction = get_min([partial_ic_compiled_dict,], COST_PER_kW_NET_label[0])
    
    min_tsf_cost, min_tsf_diction = get_min([tsf_sim_collection.old_result_dict,], COST_PER_kW_NET_label[0])

    min_dict_list = [["htrbp", min_htrbp_diction],["recomp", min_recomp_diction], ["simple", min_simple_diction],
                     ["simple_htrbp", min_simple_htrbp_diction], ["partial", min_partial_diction], ["partial_ic", min_partial_ic_diction],
                     ["tsf", min_tsf_diction]]
    
    for min_dic_vec in min_dict_list:
        save_file = asksaveasfilename(confirmoverwrite=True, filetypes =[('CSV Files', '*.csv')], title="Save " + min_dic_vec[0])
        if(save_file != ''):
            design_tools.write_dict(save_file, min_dic_vec[1], ',')



if __name__ == "__main__":
    #plot_system_results(False)
    save_min_configs()
    #plot_system_contours()