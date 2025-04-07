import sys
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import pickle
import numpy as np
import copy
import math

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

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
        if(key in diction) == False:
            continue

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
    if (key in result_dict) == False:
        return {}

    for val in result_dict[key]:
        if((val == '') or val <= val_min):
            remove_id_list.append(id)
        id += 1

    #fun_list = [0,1,2,3,4,5,6,7,8,9,10]
    #remove_list = [5,8,9]
    #fun_list = [i for j, i in enumerate(fun_list) if j not in remove_list]

    for key in result_dict:
        result_dict[key] = [i for j, i in enumerate(result_dict[key]) if j not in remove_id_list]
        

    #for remove_counter in range(len(remove_id_list)):
    #    id_remove = remove_id_list[len(remove_id_list) - remove_counter - 1]
    #    for key in result_dict:
    #        del result_dict[key][id_remove]

    return result_dict

def open_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def sum_var(result_dict, var_list, new_var_name):
    result_dict[new_var_name] = []

    for i in range(len(result_dict[var_list[0]])):
        sum = 0
        for var in var_list:
            sum += result_dict[var][i]
        result_dict[new_var_name].append(sum)

    return result_dict

def get_best_dict(result_dict, best_key, is_max=True):
    best_index = -1
    best_val = float('-inf')
    if is_max == False:
        best_val = float('inf')

    for i in range(len(result_dict[best_key])):
        val = result_dict[best_key][i]
        if(is_max):
            if val > best_val:
                best_val = val
                best_index = i
        else:
            if val < best_val:
                best_val = val
                best_index = i
    
    return_dict = {}
    for key in result_dict:
        if len(result_dict[key]) > 0:
            return_dict[key] = [result_dict[key][best_index]]

    return return_dict

def get_best_dict_optimized(result_dict, best_key, is_max=True):
    # Determine the comparison function based on is_max
    compare = max if is_max else min

    # Find the best index based on the comparison function
    best_index = compare(range(len(result_dict[best_key])), key=lambda i: result_dict[best_key][i])

    # Create a dictionary with the best values
    return {key: [values[best_index]] for key, values in result_dict.items() if values}

def sum_w_nan(iterable):
    sum_total = 0
    for val in iterable:
        if(math.isnan(val) == False):
            sum_total += val
    return sum_total

def validate_sco2_cost(result_dict, index):
    
    # Get calculated cost from cmod
    cycle_cost = result_dict['cycle_cost'][index]

    # Get individual costs
    mc_cost_bare_erected = result_dict['mc_cost_bare_erected'][index]
    rc_cost_bare_erected = result_dict['rc_cost_bare_erected'][index]
    pc_cost_bare_erected = result_dict['pc_cost_bare_erected'][index]
    LTR_cost_bare_erected = result_dict['LTR_cost_bare_erected'][index]
    HTR_cost_bare_erected = result_dict['HTR_cost_bare_erected'][index]
    PHX_cost_bare_erected = result_dict['PHX_cost_bare_erected'][index]
    BPX_cost_bare_erected = 0
    if 'BPX_cost_bare_erected' in result_dict: 
        BPX_cost_bare_erected = result_dict['BPX_cost_bare_erected'][index] 
    t_cost_bare_erected = result_dict['t_cost_bare_erected'][index]
    t2_cost_bare_erected = 0
    if 't2_cost_bare_erected' in result_dict:
        t2_cost_bare_erected = result_dict['t2_cost_bare_erected'][index]
    mc_cooler_cost_bare_erected = result_dict['mc_cooler_cost_bare_erected'][index]
    pc_cooler_cost_bare_erected = result_dict['pc_cooler_cost_bare_erected'][index]
    piping_inventory_etc_cost = result_dict['piping_inventory_etc_cost'][index]

    # Calculate Cycle cost
    cycle_cost_calc = sum_w_nan([mc_cost_bare_erected, rc_cost_bare_erected, pc_cost_bare_erected, 
                                 LTR_cost_bare_erected, HTR_cost_bare_erected, 
                                 PHX_cost_bare_erected, BPX_cost_bare_erected, 
                                 t_cost_bare_erected, t2_cost_bare_erected,
                                 mc_cooler_cost_bare_erected, 
                                 pc_cooler_cost_bare_erected, piping_inventory_etc_cost])
    
    diff = abs(cycle_cost - cycle_cost_calc)

    if(diff > 0.00001):
        print('cycle cost error')
        return False

    return True

def validate_sco2_LTR_HTR(result_dict, index):
    cycle_config = result_dict['cycle_config'][index]
    config_name = result_dict['config_name'][index]

    # Check UA

# Plot Utility

def plot_g3p3_kwargs(dict_list_with_kwarg):

    # Labels
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "PC HTF Outlet Temperature"]
    REC_ETA_label = ["eta_rec_thermal_des", "", "Receiver Efficiency"]
    V_TES_label = ["V_tes_htf_total_des", f"m\u00B3", "TES Volume"]
    A_SF_label = ["A_sf", f"m\u00B2", "Solar Field Area"]
    H_TOWER_label = ["h_tower_calc", "m", "Tower Height"]
    TOTAL_INSTALLED_COST_label = ["total_installed_cost", "$", "Total Installed Cost"]
    W_DOT_NET_label = ["W_dot_net_ish", "MWe", "Net Power Output"]
    W_DOT_GROSS_label = ["W_dot_net_des", "MWe", "Gross Power Output"]

    COST_PER_kW_GROSS_label = ["cost_per_kWe_gross", "$/kWe", "Cost per kWe Gross"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    
    COST_PER_kW_GROSS_NORM_label = ["cost_per_kWe_gross_norm", "", "Cost per kWe Gross Normalized"]
    COST_PER_kW_NET_NORM_label = ["cost_per_kWe_net_ish_norm", "", "Cost per kWe Net Normalized"]

    CYCLE_cost_label = ["cycle_cost", "M$", "Cycle Cost"]

     # Pop up variables to show
    label_list = ["config_name", "cycle_config", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total",
                  "eta_rec_thermal_des", "V_tes_htf_total_des",
                  "HTR_UA_des_in", "LTR_UA_des_in", 
                  "HTR_UA_calculated", "LTR_UA_calculated", 
                  "recomp_frac", "bypass_frac",
                  "recup_total_UA_calculated"]
    
    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "mc_cost_bare_erected", "rc_cost_bare_erected",
    #              "pc_cost_bare_erected", "LTR_cost_bare_erected",
    #              "HTR_cost_bare_erected", "PHX_cost_bare_erected",
    #              "t_cost_bare_erected", "mc_cooler_cost_bare_erected",
    #              "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost",
    #              "cycle_cost"
    #              ]

    print('Plotting...')

    # Receiver Efficiency
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=REC_ETA_label, 
                                  show_legend=False, title='Receiver Efficiency',
                                  label_list=label_list,
                                  vrange=[0.8,0.9])

    # TES Volume
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=V_TES_label, 
                                  show_legend=False, title='TES Volume',
                                  label_list=label_list)
    
    # Lift Cost
    for i in range(len(dict_list_with_kwarg)):
        dict_list_with_kwarg[i][0] = sum_var(dict_list_with_kwarg[i][0], ['receiver_lift_cost', 'tes_lift_cost', 'phx_lift_cost'], 'total_lift_cost')
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=['total_lift_cost', '$', 'Total Lift Cost'], 
                                  show_legend=False, title='Lift Cost',
                                  label_list=label_list)
    
    # Lift Power
    for i in range(len(dict_list_with_kwarg)):
        dict_list_with_kwarg[i][0] = sum_var(dict_list_with_kwarg[i][0], ['P_tower_lift_des', 'W_dot_cycle_lift_des'], 'W_lift_total')
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=['W_lift_total', 'MWe', 'Total Lift Power'], 
                                  show_legend=False, title='Lift Power',
                                  label_list=label_list)
    
    # Solar Field Area
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=A_SF_label, 
                                  show_legend=False, title='Solar Field Area',
                                  label_list=label_list)
    
    # Tower Height
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=H_TOWER_label, 
                                  show_legend=False, title='Tower Height',
                                  label_list=label_list)

    # Total Installed Cost
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=TOTAL_INSTALLED_COST_label, 
                                  show_legend=False, title='Total Installed Cost',
                                  label_list=label_list)
    
    # Net Power (ish)
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=W_DOT_NET_label, 
                                  show_legend=False, title='Net Power (ish)',
                                  label_list=label_list)
    
    # Gross Power (ish)
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=W_DOT_GROSS_label, 
                                  show_legend=False, title='Gross Power',
                                  label_list=label_list,
                                  vrange=[5,20])
    
    # $/kWe Net
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=COST_PER_kW_NET_label, 
                                  show_legend=False, title='$/kWe Net',
                                  label_list=label_list)
    
    # $/kWe Net (highlight bottom 10%)
    vmin = float('inf')
    vmax = float('-inf')
    for dict_kwarg in dict_list_with_kwarg:
        diction = dict_kwarg[0]
        val_min = min(diction[COST_PER_kW_NET_label[0]])
        val_max = max(diction[COST_PER_kW_NET_label[0]])
        if val_min < vmin : vmin = val_min
        if val_max > vmax : vmax = val_max
    vmax = 0.1 * (vmax - vmin) + vmin
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label, Z_info=COST_PER_kW_NET_label, 
                                  show_legend=False, title='$/kWe Net (focused)',
                                  label_list=label_list,
                                  vrange=[vmin, vmax])
    
    # No Z Axis
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    # Get Best Values
    best_dict_list_with_kwarg = []
    for dict_kwarg in dict_list_with_kwarg:
        diction = dict_kwarg[0]
        kwarg = copy.deepcopy(dict_kwarg[1])
        if('marker' in kwarg) == False:
            kwarg['marker'] = 'X'
        kwarg['label'] = 'best ' + kwarg['label']
        kwarg['c'] = 'black'
        best_dict = get_best_dict(diction, COST_PER_kW_NET_label[0], False)
        best_dict_list_with_kwarg.append([best_dict, kwarg])
    design_tools.plot_scatter_pts(best_dict_list_with_kwarg, 
                                  PC_ETA_label, T_HTF_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    # Plot cost breakdown
    dict_index_duo_list = []
    for best_dict_kwarg in best_dict_list_with_kwarg:
        best_dict = best_dict_kwarg[0]
        dict_index_duo_list.append([best_dict, 0])
    design_tools.plot_costs_barchart(dict_index_duo_list, type='sco2')
    design_tools.plot_costs_barchart(dict_index_duo_list, type='system')


    design_tools.plot_scatter_pts(best_dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    design_tools.plot_scatter_pts(best_dict_list_with_kwarg, 
                                  T_HTF_label, COST_PER_kW_NET_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    # No Z Axis
    design_tools.plot_scatter_pts([*dict_list_with_kwarg, *best_dict_list_with_kwarg],
                                  PC_ETA_label, T_HTF_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
     # No Z Axis
    design_tools.plot_scatter_pts([*dict_list_with_kwarg, *best_dict_list_with_kwarg],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    

    design_tools.plot_scatter_pts([*dict_list_with_kwarg, *best_dict_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    # No Z Axis
    design_tools.plot_scatter_pts([*dict_list_with_kwarg, *best_dict_list_with_kwarg],
                                  PC_ETA_label, CYCLE_cost_label,
                                  show_legend=True, title='Cycle Cost', legend_loc='upper right',
                                  label_list=label_list)
    
    # No Z Axis    
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    plt.tight_layout()
    return
    # Only Simple Cycle
    design_tools.plot_scatter_pts([dict_list_with_kwarg[2], dict_list_with_kwarg[3]],
                                  PC_ETA_label, CYCLE_cost_label, ['LTR_UA_des_in', 'kW/K', "LTR UA IN"],
                                  show_legend=True, title='Simple from recomp and htr bp', legend_loc='upper right',
                                  label_list=label_list)
    
    design_tools.plot_scatter_pts([dict_list_with_kwarg[2]],
                                  PC_ETA_label, CYCLE_cost_label,
                                  show_legend=True, title='Simple from recomp', legend_loc='upper right',
                                  label_list=label_list)
    
def plot_sco2_kwargs(dict_list_with_kwarg):
    # Labels
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "PC HTF Outlet Temperature"]
    RECOMP_label = ["is_recomp_ok", "", "Recompression Fraction"]
    BYPASS_label = ["is_bypass_ok", "", "Bypass Fraction"]
    HTR_label = ["HTR_UA_des_in", "", "HTR UA"]
    LTR_label = ["LTR_UA_des_in", "", "LTR UA"]
    P_MC_label = ["is_PR_fixed", "", "Pressure Ratio"]
    P_IP_label = ["is_IP_fixed", "", "Intermediate Pressure Ratio"]

    COST_PER_kW_GROSS_label = ["cost_per_kWe_gross", "$/kWe", "Cost per kWe Gross"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    

     # Pop up variables to show
    label_list = ["config_name", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total",
                  "eta_rec_thermal_des", "V_tes_htf_total_des"]
    
    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "mc_cost_bare_erected", "rc_cost_bare_erected",
    #              "pc_cost_bare_erected", "LTR_cost_bare_erected",
    #              "HTR_cost_bare_erected", "PHX_cost_bare_erected",
    #              "t_cost_bare_erected", "mc_cooler_cost_bare_erected",
    #              "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost",
    #              "cycle_cost"
    #              ]

    # Recompression Fraction
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label, Z_info=RECOMP_label, 
                                  show_legend=False, title='Recompression Fraction',
                                  label_list=label_list)
    
    # Bypass Fraction
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label, Z_info=BYPASS_label, 
                                  show_legend=False, title='Bypass Fraction',
                                  label_list=label_list)
    
    # HTR_label
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label, Z_info=HTR_label, 
                                  show_legend=False, title='HTR UA',
                                  label_list=label_list)
    
    # LTR
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label, Z_info=LTR_label, 
                                  show_legend=False, title='LTR UA',
                                  label_list=label_list)
    
    # MC Pressure 
    design_tools.plot_scatter_pts(dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label, Z_info=P_MC_label, 
                                  show_legend=False, title='MC Pressure',
                                  label_list=label_list)
    




# Plot methods

def plot_g3p3(htrbp_result_dict, recomp_result_dict,
               partial_result_dict):
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
    #tsf_result_dict = remove_cases(tsf_result_dict, COST_PER_kW_NET_label[0], 0)

    # Get Minimum Net Cost
    min_net_cost, min_diction = get_min([htrbp_compiled_dict, recomp_compiled_dict, simple_compiled_dict,
                            simple_htrbp_compiled_dict, partial_compiled_dict, partial_ic_compiled_dict], 
                            COST_PER_kW_NET_label[0])

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
    #tsf_net_norm_list = get_norm_list(tsf_result_dict[COST_PER_kW_NET_label[0]], min_net_cost)

    htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = htrbp_net_norm_list
    recomp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = recomp_net_norm_list
    simple_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_net_norm_list
    simple_htrbp_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = simple_htrbp_net_norm_list
    partial_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_net_norm_list
    partial_ic_compiled_dict[COST_PER_kW_NET_NORM_label[0]] = partial_ic_net_norm_list
    #tsf_result_dict[COST_PER_kW_NET_NORM_label[0]] = tsf_net_norm_list

    # Create Net Cost vs Efficiency Pareto Front
    print("Forming eff pareto fronts...")
    htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    recomp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    simple_htrbp_compiled_eff_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    partial_ic_compiled_eff_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)
    #tsf_eff_pareto_dict = design_tools.get_pareto_dict(tsf_result_dict, ETA_label[0], COST_PER_kW_NET_label[0], True, False)

    # Create Net Cost vs T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)
    #tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_result_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], False, False)

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
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_GROSS_label, show_legend=True, legend_loc='upper right')
    
    # Cost Gross vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]        
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_GROSS_label, show_legend=True, legend_loc='upper right')
    
    # Cost Net vs ETA
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_label, show_legend=True, legend_loc='upper right')
    
    # Cost Net vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_label, show_legend=True, legend_loc='upper right')

    # Cost Gross vs W_dot_net
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_label, ax=ax1_poster_net_cost, show_legend=False, legend_loc='upper right')

    # Cost Net vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_label, ax=ax2_poster_net_cost, show_legend=True, legend_loc='center left')

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
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_NORM_label, ax=ax1_poster_net_cost_norm, show_legend=False, legend_loc='upper right')
    

    # Cost Net vs min Temp
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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
                    [partial_compiled_eff_pareto_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_eff_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, COST_PER_kW_NET_label, ax=ax1_pareto_eff, show_legend=False, legend_loc='upper right')
    

    # Cost Net vs min Temp Pareto
    design_tools.plot_scatter_pts([
                    [simple_compiled_T_HTF_pareto_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_T_HTF_pareto_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_T_HTF_pareto_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_T_HTF_pareto_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_T_HTF_pareto_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_T_HTF_pareto_dict, {'label':partial_legend_label, 'marker':'.'}]          
                    #,[tsf_T_HTF_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    T_HTF_label, COST_PER_kW_NET_label, ax=ax2_pareto_T_HTF, show_legend=True, legend_loc='center left')

    plt.tight_layout()
    plt.rc('font', size=11) 

def plot_pkl_g3p3_via_filedlg():
    
    window = tk.Tk()
    htrbp_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 htrbp pkl file")
    recomp_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 recomp pkl file")
    #tsf_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 tsf pkl file")
    partial_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 partial pkl file")

    filename_list = [htrbp_filename, recomp_filename,
                     partial_filename]
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

    # Pop up variables to show
    label_list = ["config_name", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total"]

    # Plot all results, Z axis cmod_success
    ax_result = design_tools.plot_scatter_pts([
                    [result_dict, {'label':label, 'marker':'.'}]
                    ], 
                    ETA_label, T_HTF_label, success_label, show_legend=True, legend_loc='upper right', title=label + ' complete',
                    label_list=label_list)
    
    # Get X and Y axis
    xlim = ax_result.get_xlim()
    ylim = ax_result.get_ylim()
    fig_failed, (ax1_pass, ax2_fail) = plt.subplots(1,2)
    ax1_pass.set_xlim(xlim)
    ax1_pass.set_ylim(ylim)
    ax2_fail.set_xlim(xlim)
    ax2_fail.set_ylim(ylim)

    # Separate Pass and Fail result dict
    result_dict_pass = design_tools.combine_dict_by_key([result_dict], 
                                                        "cmod_success", 1)
    
    result_dict_fail = design_tools.combine_dict_by_key([result_dict], 
                                                        "cmod_success", 0)
    
    # Plot Success Vals
    if(len(result_dict_pass) > 0):
        design_tools.plot_scatter_pts([
            [result_dict_pass, {'label':'pass', 'marker':'.', 'c':'red'}]
            ], 
            ETA_label, T_HTF_label, ax=ax1_pass, show_legend=True, legend_loc='upper right', title=label + ' pass',
            label_list=label_list)
    
    # Plot Fail Vals
    if(len(result_dict_fail) > 0):
        design_tools.plot_scatter_pts([
            [result_dict_fail, {'label':'fail', 'marker':'.', 'c':'blue'}]
            ], 
            ETA_label, T_HTF_label, ax=ax2_fail, show_legend=True, legend_loc='upper right', title=label + ' fail',
            label_list=label_list)

def prep_g3p3_plot():
    
    # Get Filenames
    hardcode = True
    filename_htrbp = ''
    filename_recomp = ''
    filename_partial = ''
    if hardcode:
        #filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\slim_pickled_merged\zG3P3_results_20250104_071844__htrbp_G3P3_collection_10_20250103_192511_000.pkl"
        #filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\slim_pickled_merged\zG3P3_results_20250105_132500__recomp_G3P3_collection_10_20250103_190235_000.pkl"
        #filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\slim_pickled_merged\zG3P3_results_20250104_235339__partial_G3P3_collection_10_20250103_132840_000.pkl"

        #filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839\pickled_merged\zG3P3_results_20250110_121241__htrbp_G3P3_collection_10_20250103_192511_000.pkl"
        #filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839\pickled_merged\zG3P3_results_20250110_163436__recomp_G3P3_collection_10_20250103_190235_000.pkl"
        #filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839\pickled_merged\zG3P3_results_20250110_091255__partial_G3P3_collection_10_20250103_132840_000.pkl"
        #filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839\pickled_merged\zG3P3_results_20250110_210037__TSF_G3P3_collection_10_20250103_191443_000.pkl"

        #filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\slim_pickle_merged\zG3P3_results_20250114_005959__htrbp_G3P3_collection_10_20250103_192511_000.pkl"
        #filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\slim_pickle_merged\zG3P3_results_20250114_000750__recomp_G3P3_collection_10_20250103_190235_000.pkl"
        #filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\slim_pickle_merged\zG3P3_results_20250114_015025__TSF_G3P3_collection_10_20250103_191443_000.pkl"
        #filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\slim_pickle_merged\zG3P3_results_20250114_192827__partial_G3P3_collection_10_20250113_144036_000.pkl"

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\mega\slim_pickled_merged\combined_zG3P3_results_20250114_005959__htrbp_G3P3_collection_10_20250103_192511_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\mega\slim_pickled_merged\combined_zG3P3_results_20250114_000750__recomp_G3P3_collection_10_20250103_190235_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\mega\slim_pickled_merged\combined_zG3P3_results_20250114_015025__TSF_G3P3_collection_10_20250103_191443_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\Fixed Receiver ETA\run_10_20250103_132839 - v2\mega\slim_pickled_merged\combined_zG3P3_results_20250114_192827__partial_G3P3_collection_10_20250113_144036_000.pkl"

    else:
        filename_htrbp = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 htrbp pkl file")
        filename_recomp = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 recomp pkl file")
        filename_partial = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 partial pkl file")
    
    # Load result dicts
    print('Opening pickles...')
    result_dict_htrbp = open_pickle(filename_htrbp)
    result_dict_recomp = open_pickle(filename_recomp)
    result_dict_partial = open_pickle(filename_partial)
    result_dict_tsf = open_pickle(filename_tsf)


    # Reclassify config name
    print('Naming cycles...')
    for result_dict in [result_dict_htrbp, result_dict_recomp, result_dict_partial, result_dict_tsf]:
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
            result_dict['config_name'][i] = sco2_solve.get_config_name(cycle_config, recomp_frac, bypass_frac, is_LTR, is_HTR)
            o = 0

    print('Splitting dictionaries by config_name...')
    result_dict_list = design_tools.split_by_config_name([result_dict_htrbp, result_dict_recomp, result_dict_partial, result_dict_tsf])

    # Validate split
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        for config_val in result_dict['config_name']:
            if(config_val != config_name):
                print('split fail')
                return

    # make dict_list_with_kwarg
    dict_list_with_kwargs = []
    marker_list = design_tools.get_marker_list()
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        dict_w_kwarg = [result_dict, {'label':config_name, 'marker':marker_list[i]}]
        dict_list_with_kwargs.append(dict_w_kwarg)
        i += 1

    
    # Validate costs
    print('Validating cost models...')
    dict_list = [result_dict_htrbp, result_dict_recomp, result_dict_partial, result_dict_tsf]
    for diction in dict_list:
        NVal = len(diction["eta_thermal_calc"])
        for i in range(NVal):

            # make sure recomp input equals output
            recomp_input = -1.0 * diction["is_recomp_ok"][i]
            recomp_frac = diction["recomp_frac"][i]
            diff = abs(recomp_input - recomp_frac)

            if(diff > 0.0001):
                y = 0
                print('Recomp frac input does not equal output')
                return

            # Validate cost calcs
            cost_validated = validate_sco2_cost(diction, i)
            if(cost_validated == False):
                print('sco2 cycle costs do not sum to reported cost')
                return


    
    if False:
        # HTR BP (only comes from htr bp file)
        htrbp_compiled_dict = design_tools.combine_dict_by_key([result_dict_htrbp],
                                                                "config_name", "htr bp")

        # Recompression (comes from recomp and htr bp)
        recomp_compiled_dict = design_tools.combine_dict_by_key([result_dict_htrbp, 
                                                                result_dict_recomp],  
                                                                "config_name", "recompression")

        ## Simple (from recomp and htr bp)
        #simple_compiled_dict = design_tools.combine_dict_by_key([result_dict_htrbp, 
        #                                                        result_dict_recomp],  
        #                                                        "config_name", "simple")

        # Simple (from recomp only)
        simple_compiled_dict = design_tools.combine_dict_by_key([#result_dict_htrbp, 
                                                                result_dict_recomp],  
                                                                "config_name", "simple")

        # Simple (from htr bp)
        #simple_double_compiled_dict = design_tools.combine_dict_by_key([result_dict_htrbp],  
        #                                                        "config_name", "simple")

        # Simple w/ htr bypass (from htr bp only)
        simple_htrbp_compiled_dict = design_tools.combine_dict_by_key([result_dict_htrbp],
                                                                "config_name", "simple split flow bypass")
        
        # Partial (only comes from partial file)
        partial_compiled_dict = design_tools.combine_dict_by_key([result_dict_partial],
                                                                "config_name", "partial")

        # Partial Intercooling (only comes from partial file)
        partial_ic_compiled_dict = design_tools.combine_dict_by_key([result_dict_partial],
                                                                "config_name", "partial intercooling")

        # Make dict list with kwargs
        dict_list_with_kwargs = [[htrbp_compiled_dict, {'label':'htrbp', 'marker':'.'}],
                                [recomp_compiled_dict, {'label':'recomp', 'marker':'.'}],             
                                [simple_compiled_dict, {'label':'simple', 'marker':'.'}],
                                [simple_htrbp_compiled_dict, {'label':'simple bp', 'marker':'.'}],
                                [partial_compiled_dict, {'label':'partial', 'marker':'.'}],
                                [partial_ic_compiled_dict, {'label':'partial ic', 'marker':'.'}],
                                [result_dict_tsf, {'label':'tsf', 'marker':'.'}]]
    
    # Validate number of cases
    print('Validating number of cases...')
    for dict_w_kwarg in dict_list_with_kwargs:
        diction = dict_w_kwarg[0]
        Nval = len(diction[list(diction.keys())[0]])

        for key in diction:
            N_val_key = len(diction[key])
            if(N_val_key != Nval):
                print('mismatch number of cases')
                return

    #dict_list_with_kwargs = [[recomp_compiled_dict, {'label':'recomp', 'marker':'.'}],             
    #                         [simple_compiled_dict, {'label':'simple', 'marker':'.'}],
    #                         [partial_compiled_dict, {'label':'partial', 'marker':'.'}]]
    
    # Plot
    plot_g3p3_kwargs(dict_list_with_kwargs)
    #plot_sco2_kwargs(dict_list_with_kwargs)



def plot_failed_test():
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
    #plot_pkl_g3p3_via_filedlg()
    prep_g3p3_plot()
    plt.show(block = True)