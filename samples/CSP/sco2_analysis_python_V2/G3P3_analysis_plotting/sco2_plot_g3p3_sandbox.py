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
from sco2_plot_g3p3_baseline_FINAL import open_pickle
import sco2_plot_g3p3_baseline_FINAL
import sco2_filenames
import sco2_plot_compare_all

# G3P3 Utility

def add_LCOE(dict_list_with_kwarg):
    for result_dict, kwarg in dict_list_with_kwarg:
        NVal = len(result_dict[list(result_dict.keys())[0]])
        result_dict['lcoe'] = []
        result_dict['lcoe_cent'] = []
        for i in range(NVal):
            W_dot_des = result_dict['P_ref'][i]
            W_dot_cycle_parasitic_input = W_dot_des * result_dict['fan_power_frac'][i]
            W_dot_net = W_dot_des - W_dot_cycle_parasitic_input
            if W_dot_net != 10:
                print('W_dot_net is not 10')

            W_dot_net_ish = result_dict['W_dot_net_ish'][i] * 1e3           # kWe
            total_installed_cost = result_dict['total_installed_cost'][i]   # $
            capacity_factor = 0.636 # (originally used 0.7)
            FCR = 0.07
            yr = 8760   # hr

            W_system_annual = W_dot_net_ish * yr * capacity_factor # kWe
            LCOE = FCR * total_installed_cost / W_system_annual # $/kWe
            LCOE_cent = LCOE * 100  # c/kWe

            result_dict['lcoe'].append(LCOE)
            result_dict['lcoe_cent'].append(LCOE_cent)

def find_sample_cases(dict_list_with_kwarg, is_multi=False):
    recomp_dict = {}
    partial_dict = {}
    for result_dict, kwarg in dict_list_with_kwarg:
        config_name = result_dict['config_name'][0]
        if config_name.lower() == 'recompression':
            recomp_dict = result_dict
        elif config_name.lower() == 'partial':
            partial_dict = result_dict

    # Define sample bounds
    recomp_frac_bounds = ['recomp_frac', 0.29, 0.32]
    LTR_UA_bounds = ['LTR_UA_calculated', 0.45, 0.9]
    HTR_UA_bounds = ['HTR_UA_calculated', 0.45, 0.9]
    P_MC_IN_bounds = ['P_state_points_0_0', 8.4, 8.7]
    P_PC_IN_bounds = ['P_state_points_10_0', 4.5, 5.5]

    recomp_bounds = [recomp_frac_bounds, LTR_UA_bounds, HTR_UA_bounds, P_MC_IN_bounds]
    partial_bounds = [recomp_frac_bounds, LTR_UA_bounds, HTR_UA_bounds, P_MC_IN_bounds, P_PC_IN_bounds]

    # Initialize sample recomp and partial result dicts
    recomp_sample_dict = {}
    partial_sample_dict = {}
    for key in recomp_dict:
        recomp_sample_dict[key] = []
    for key in partial_dict:
        partial_sample_dict[key] = []

    # Find Recompression sample cases
    NVal_recomp = len(recomp_dict['config_name'])
    for i in range(NVal_recomp):
        
        # Test each bound
        is_sample = True
        for bound_key, bound_lower, bound_upper in recomp_bounds:
            val = recomp_dict[bound_key][i]
            if (val < bound_lower) or (val > bound_upper):
                is_sample = False
                break
        # Save samples
        if is_sample:
            for key in recomp_dict:
                recomp_sample_dict[key].append(recomp_dict[key][i])

            if is_multi == False:
                break

    # Get best recomp case and add to return dict
    sample_dict_list_with_kwarg = []
    recomp_dict_w_kwarg = [recomp_sample_dict, {'label':'Sample ' + recomp_dict['config_name'][0]}]
    sample_dict_list_with_kwarg.append(recomp_dict_w_kwarg)

    # Find partial sample cases
    NVal_partial = len(partial_dict['config_name'])
    for i in range(NVal_partial):
        
        # Test each bound
        is_sample = True
        for bound_key, bound_lower, bound_upper in partial_bounds:
            val = partial_dict[bound_key][i]
            if (val < bound_lower) or (val > bound_upper):
                is_sample = False
                break
        # Save samples
        if is_sample:
            for key in partial_dict:
                partial_sample_dict[key].append(partial_dict[key][i])
            if is_multi == False:
                break
    partial_dict_w_kwarg = [partial_sample_dict, {'label':'Sample ' + partial_dict['config_name'][0]}]
    sample_dict_list_with_kwarg.append(partial_dict_w_kwarg)

    return sample_dict_list_with_kwarg


# Plot Utility

def plot_test(dict_list_with_kwarg):

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
    
    MIN_DT_LTR_label = ["LTR_min_dT", "C", "LTR Min dT"]
    UA_ASSIGNED_LTR_label = ["LTR_UA_assigned", "MW/K", "LTR UA Assigned"]
    UA_CALC_LTR_label = ["LTR_UA_calculated", "MW/K", "LTR UA Calculated"]
    EFF_LTR_label = ["eff_LTR", "", "LTR Effectiveness"]
    MIN_DT_HTR_label = ["HTR_min_dT", "C", "HTR Min dT"]
    UA_ASSIGNED_HTR_label = ["HTR_UA_assigned", "MW/K", "HTR UA Assigned"]
    UA_CALC_HTR_label = ["HTR_UA_calculated", "MW/K", "HTR UA Calculated"]
    EFF_HTR_label = ["eff_HTR", "", "HTR Effectiveness"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]
    
    LTR_UA_assigned_over_calc_label = ["LTR_UA_assigned_over_calc", "", "LTR UA Assigned / Calculated"]
    HTR_UA_assigned_over_calc_label = ["HTR_UA_assigned_over_calc", "", "HTR UA Assigned / Calculated"]

    COST_PER_kW_GROSS_NORM_label = ["cost_per_kWe_gross_norm", "", "Cost per kWe Gross Normalized"]
    COST_PER_kW_NET_NORM_label = ["cost_per_kWe_net_ish_norm", "", "Cost per kWe Net Normalized"]

    CYCLE_cost_label = ["cycle_cost", "M$", "Cycle Cost"]

    LCOE_cent_label = ["lcoe_cent", "\u00A2/kWe", "LCOE"]

     # Pop up variables to show
    label_list = ["config_name", "cycle_config", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total",
                  "eta_rec_thermal_des", "V_tes_htf_total_des",
                  "HTR_UA_des_in", "LTR_UA_des_in", 
                  "HTR_UA_calculated", "LTR_UA_calculated", 
                  "recomp_frac", "bypass_frac",
                  "q_dot_BPX", "BPX_cost_bare_erected",
                  'P_state_points_10_0', 'P_state_points_0_0',
                  'pc_cost_bare_erected', 'pc_W_dot',
                  'pc_cost_equipment', 'm_dot_co2_full']
    
    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "mc_cost_bare_erected", "rc_cost_bare_erected",
    #              "pc_cost_bare_erected", "LTR_cost_bare_erected",
    #              "HTR_cost_bare_erected", "PHX_cost_bare_erected",
    #              "t_cost_bare_erected", "mc_cooler_cost_bare_erected",
    #              "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost",
    #              "cycle_cost", 'm_dot_co2_full'
    #              ]

    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "T_comp_in", "mc_W_dot", "mc_cost_equipment",
    #              "T_turb_in", "t_W_dot", "t_cost_equipment",
    #              "q_dot_rec_des_total", 'm_dot_co2_full']

    print('Plotting...')

    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor

    # $/kWe vs T HTF   
    fig_1, ax1 = plt.subplots(1)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    plt.tight_layout()
    
    # $/kWe vs cycle eff 
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

    # $/kWe vs UA Total
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_TOTAL_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # LTR min dt vs UA calc
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_CALC_LTR_label, MIN_DT_LTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # HTR min dt vs UA calc
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_CALC_HTR_label, MIN_DT_HTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # LTR assigned vs UA calc
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_CALC_LTR_label, UA_ASSIGNED_LTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # HTR assigned vs UA calc
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_CALC_HTR_label, UA_ASSIGNED_HTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # LTR eff vs UA calc
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_CALC_LTR_label, EFF_LTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # HTR eff vs UA calc
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  UA_CALC_HTR_label, EFF_HTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()
    
     # LTR dT vs (UA assigned / calc)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  LTR_UA_assigned_over_calc_label, MIN_DT_LTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # LTR dT vs (UA assigned / calc)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  LTR_UA_assigned_over_calc_label, EFF_LTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # LTR dT vs (UA assigned / calc)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  HTR_UA_assigned_over_calc_label, MIN_DT_HTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)

     # HTR dT vs (UA assigned / calc)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  HTR_UA_assigned_over_calc_label, EFF_HTR_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # HTR dT vs (UA assigned / calc)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  PC_ETA_label, LCOE_cent_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

    # Get Best Values
    best_dict_list_with_kwarg = []
    for dict_kwarg in dict_list_with_kwarg:
        diction = dict_kwarg[0]
        kwarg = copy.deepcopy(dict_kwarg[1])
        if('marker' in kwarg) == False:
            kwarg['marker'] = 'X'
        kwarg['label'] = 'best ' + kwarg['label']
        kwarg['c'] = 'black'
        best_dict = sco2_plot_g3p3_baseline_FINAL.get_best_dict(diction, COST_PER_kW_NET_label[0], False)
        best_dict_list_with_kwarg.append([best_dict, kwarg])
    design_tools.plot_scatter_pts(best_dict_list_with_kwarg, 
                                  PC_ETA_label, COST_PER_kW_NET_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)
    
    # Plot cost breakdown
    dict_index_duo_list = []
    for best_dict_kwarg in best_dict_list_with_kwarg:
        best_dict = best_dict_kwarg[0]
        dict_index_duo_list.append([best_dict, 0])
    design_tools.plot_costs_barchart(dict_index_duo_list, type='sco2')
    design_tools.plot_costs_barchart(dict_index_duo_list, type='system')


    return

def compare_run_sweeps(dict_list_with_kwarg_old,
                       dict_list_with_kwarg_new):
    # Labels
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "PC HTF Outlet Temperature"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]

     # Pop up variables to show
    label_list = ["config_name", "cycle_config", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total",
                  "eta_rec_thermal_des", "V_tes_htf_total_des",
                  "HTR_UA_des_in", "LTR_UA_des_in", 
                  "HTR_UA_calculated", "LTR_UA_calculated", 
                  "recomp_frac", "bypass_frac",
                  "q_dot_BPX", "BPX_cost_bare_erected",
                  'P_state_points_10_0', 'P_state_points_0_0',
                  'pc_cost_bare_erected', 'pc_W_dot',
                  'pc_cost_equipment']
    
    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "mc_cost_bare_erected", "rc_cost_bare_erected",
    #              "pc_cost_bare_erected", "LTR_cost_bare_erected",
    #              "HTR_cost_bare_erected", "PHX_cost_bare_erected",
    #              "t_cost_bare_erected", "mc_cooler_cost_bare_erected",
    #              "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost",
    #              "cycle_cost"
    #              ]

    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "T_comp_in", "mc_W_dot", "mc_cost_equipment",
    #              "T_turb_in", "t_W_dot", "t_cost_equipment",
    #              "q_dot_rec_des_total"]

    print('Plotting...')

    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor

    # $/kWe vs T HTF   
    fig_1, [ax1, ax2] = plt.subplots(1, 2)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg_old],
                                  PC_ETA_label, T_HTF_label, 
                                  show_legend=True, title='Old Data', legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    
     # $/kWe vs T HTF   
    design_tools.plot_scatter_pts([*dict_list_with_kwarg_new],
                                  PC_ETA_label, T_HTF_label, 
                                  show_legend=True, title='New Data', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

def plot_w_sample(dict_list_with_kwarg,
                  sample_list_with_kwarg):
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
    
    MIN_DT_LTR_label = ["LTR_min_dT", "C", "LTR Min dT"]
    UA_ASSIGNED_LTR_label = ["LTR_UA_assigned", "MW/K", "LTR UA Assigned"]
    UA_CALC_LTR_label = ["LTR_UA_calculated", "MW/K", "LTR UA Calculated"]
    EFF_LTR_label = ["eff_LTR", "", "LTR Effectiveness"]
    MIN_DT_HTR_label = ["HTR_min_dT", "C", "HTR Min dT"]
    UA_ASSIGNED_HTR_label = ["HTR_UA_assigned", "MW/K", "HTR UA Assigned"]
    UA_CALC_HTR_label = ["HTR_UA_calculated", "MW/K", "HTR UA Calculated"]
    EFF_HTR_label = ["eff_HTR", "", "HTR Effectiveness"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]
    
    LTR_UA_assigned_over_calc_label = ["LTR_UA_assigned_over_calc", "", "LTR UA Assigned / Calculated"]
    HTR_UA_assigned_over_calc_label = ["HTR_UA_assigned_over_calc", "", "HTR UA Assigned / Calculated"]

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
                  "q_dot_BPX", "BPX_cost_bare_erected",
                  'P_state_points_10_0', 'P_state_points_0_0',
                  'pc_cost_bare_erected', 'pc_W_dot',
                  'pc_cost_equipment', 'm_dot_co2_full']
    
    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "mc_cost_bare_erected", "rc_cost_bare_erected",
    #              "pc_cost_bare_erected", "LTR_cost_bare_erected",
    #              "HTR_cost_bare_erected", "PHX_cost_bare_erected",
    #              "t_cost_bare_erected", "mc_cooler_cost_bare_erected",
    #              "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost",
    #              "cycle_cost", 'm_dot_co2_full'
    #              ]

    #label_list = ["config_name", "W_dot_net_des", "design_eff", 
    #              "T_comp_in", "mc_W_dot", "mc_cost_equipment",
    #              "T_turb_in", "t_W_dot", "t_cost_equipment",
    #              "q_dot_rec_des_total", 'm_dot_co2_full']

    print('Plotting...')

    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor

    # $/kWe vs T HTF   
    fig_1, ax1 = plt.subplots(1)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg, *sample_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    plt.tight_layout()
    
    # $/kWe vs cycle eff 
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg, *sample_list_with_kwarg],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

    # Get Best Values
    best_dict_list_with_kwarg = []
    for dict_kwarg in dict_list_with_kwarg:
        diction = dict_kwarg[0]
        kwarg = copy.deepcopy(dict_kwarg[1])
        if('marker' in kwarg) == False:
            kwarg['marker'] = 'X'
        kwarg['label'] = 'best ' + kwarg['label']
        kwarg['c'] = 'black'
        best_dict = sco2_plot_g3p3_baseline_FINAL.get_best_dict(diction, COST_PER_kW_NET_label[0], False)
        best_dict_list_with_kwarg.append([best_dict, kwarg])
    design_tools.plot_scatter_pts([*best_dict_list_with_kwarg, *sample_list_with_kwarg], 
                                  PC_ETA_label, COST_PER_kW_NET_label,
                                  show_legend=True, title='', legend_loc='upper right',
                                  label_list=label_list)

def plot_paretos(dict_list_with_kwarg, 
                sample_list_with_kwarg,
                best_list_with_kwarg,
                config_filter_list=[],
                plot_title=""):
    

    if True:
        result_dict_list = []
        for result_dict, kwarg in dict_list_with_kwarg:
            result_dict_list.append(result_dict)
        complete_pareto_dict = design_tools.get_min_Y_pareto_multiple(result_dict_list, PC_ETA_label[0], COST_PER_kW_NET_label[0], 50)

        design_tools.plot_scatter_pts([*dict_list_with_kwarg, [complete_pareto_dict, {'label':'pareto'}]],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right')    

        return    


    # Get Pareto for entire data set (this only works if keys are same length)  
    copy_vars = [PC_ETA_label[0], COST_PER_kW_NET_label[0], T_HTF_label[0]]
    complete_dict = {}
    for key in copy_vars:
        complete_dict[key] = []
    for dict_w_kwarg in dict_list_with_kwarg:
        result_dict = dict_w_kwarg[0]
        for key in copy_vars:
            for val in result_dict[key]:
                complete_dict[key].append(val)

    pareto_eta_complete = design_tools.get_min_Y_pareto_dict(complete_dict, PC_ETA_label[0], COST_PER_kW_NET_label[0], 20)
    pareto_T_complete = design_tools.get_min_Y_pareto_dict(complete_dict, T_HTF_label[0], COST_PER_kW_NET_label[0], 20)

    design_tools.plot_scatter_pts([*dict_list_with_kwarg, [pareto_eta_complete, {'label':'pareto'}]],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right')
    
    design_tools.plot_scatter_pts([*dict_list_with_kwarg, [pareto_T_complete, {'label':'pareto'}]],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right')
    
    

def plot_FY25Q1(dict_list_with_kwarg,
                sample_list_with_kwarg,
                best_list_with_kwarg,
                barchart_configs_list,
                plot_title=""):
     # Pop up variables to show
    label_list = ["config_name", "cycle_config", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total",
                  "eta_rec_thermal_des", "V_tes_htf_total_des",
                  "HTR_UA_des_in", "LTR_UA_des_in", 
                  "HTR_UA_calculated", "LTR_UA_calculated", 
                  "recomp_frac", "bypass_frac",
                  "q_dot_BPX", "BPX_cost_bare_erected",
                  'P_state_points_10_0', 'P_state_points_0_0',
                  'pc_cost_bare_erected', 'pc_W_dot',
                  'pc_cost_equipment', 'm_dot_co2_full',
                  'total_installed_cost']
    
    print('Plotting...')

    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor

    # $/kWe vs T HTF   
    fig_1, ax1 = plt.subplots(1)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.minorticks_on()
    ax1.grid(which='minor', linestyle=':', linewidth='0.5') 
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    plt.tight_layout()
    
    # $/kWe vs cycle eff 
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.minorticks_on()
    ax2.grid(which='minor', linestyle=':', linewidth='0.5') 
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

    # $/kWe vs T HTF (with samples)
    fig_1, ax1 = plt.subplots(1)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg,
                                   *sample_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    plt.tight_layout()
    
    # $/kWe vs cycle eff (with samples)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg,
                                   *sample_list_with_kwarg],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

     # LCOE vs T HTF   
    fig_1, ax1 = plt.subplots(1)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_ylim([6,18])
    ax1.minorticks_on()
    ax1.grid(which='minor', linestyle=':', linewidth='0.5') 
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  T_HTF_label, LCOE_cent_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    plt.tight_layout()
    
    # LCOE vs cycle eff 
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_ylim([6,18])
    ax2.minorticks_on()
    ax2.grid(which='minor', linestyle=':', linewidth='0.5') 
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg],
                                  PC_ETA_label, LCOE_cent_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

    # Best cases $/kWe vs eff
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*best_list_with_kwarg, *sample_list_with_kwarg], 
                                  PC_ETA_label, COST_PER_kW_NET_label,
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    
    # Plot cost breakdown
    dict_index_duo_list = []
    for best_dict_kwarg in best_list_with_kwarg:
        best_dict = best_dict_kwarg[0]
        dict_index_duo_list.append([best_dict, 0])
    design_tools.plot_costs_barchart(dict_index_duo_list, type='sco2')
    design_tools.plot_costs_barchart(dict_index_duo_list, type='system')

    # Plot cost breakdown (focused w/ samples)
    dict_index_duo_list_focused = []
    for best_dict_kwarg in best_list_with_kwarg:
        best_dict = best_dict_kwarg[0]
        config_name = best_dict['config_name'][0]
        if(config_name.lower() in barchart_configs_list):
            dict_index_duo_list_focused.append([best_dict, 0])
    dict_index_duo_list_samples = []
    for sample_dict_kwarg in sample_list_with_kwarg:
        sample_dict = sample_dict_kwarg[0]
        kwarg = sample_dict_kwarg[1]
        dict_index_duo_list_samples.append([sample_dict, 0, kwarg])
    design_tools.plot_costs_barchart([*dict_index_duo_list_focused, *dict_index_duo_list_samples], type='sco2')
    design_tools.plot_costs_barchart([*dict_index_duo_list_focused, *dict_index_duo_list_samples], type='system')

    # $/kWe Plot
    design_tools.plot_parasitics_barchart([*dict_index_duo_list_focused, *dict_index_duo_list_samples])

    pass

def plot_select(dict_list_with_kwarg,
                sample_list_with_kwarg,
                best_list_with_kwarg,
                barchart_configs_list,
                plot_title=""):
    
     # Pop up variables to show
    label_list = ["config_name", "cycle_config", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                  "plant_spec_cost", "cycle_cost",
                  "m_dot_htf_cycle_des", "q_dot_in_total",
                  "eta_rec_thermal_des", "V_tes_htf_total_des",
                  "HTR_UA_des_in", "LTR_UA_des_in", 
                  "HTR_UA_calculated", "LTR_UA_calculated", 
                  "recomp_frac", "bypass_frac",
                  "q_dot_BPX", "BPX_cost_bare_erected",
                  'P_state_points_10_0', 'P_state_points_0_0',
                  'pc_cost_bare_erected', 'pc_W_dot',
                  'pc_cost_equipment', 'm_dot_co2_full',
                  'total_installed_cost']
    
    print('Plotting...')

    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor

    # $/kWe vs T HTF (with samples)
    fig_1, ax1 = plt.subplots(1)
    fig_1.set_size_inches(fig_width, fig_height)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg,
                                   *sample_list_with_kwarg],
                                  T_HTF_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax1)
    plt.tight_layout()
    
    # $/kWe vs cycle eff (with samples)
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*dict_list_with_kwarg,
                                   *sample_list_with_kwarg],
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    plt.tight_layout()

    # Best cases $/kWe vs eff
    fig_2, ax2 = plt.subplots(1)
    fig_2.set_size_inches(fig_width, fig_height)
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)
    design_tools.plot_scatter_pts([*best_list_with_kwarg, *sample_list_with_kwarg], 
                                  PC_ETA_label, COST_PER_kW_NET_label,
                                  show_legend=True, title=plot_title, legend_loc='upper right',
                                  label_list=label_list, ax=ax2)
    
    # Plot cost breakdown
    dict_index_duo_list = []
    for best_dict_kwarg in best_list_with_kwarg:
        best_dict = best_dict_kwarg[0]
        dict_index_duo_list.append([best_dict, 0])
    design_tools.plot_costs_barchart(dict_index_duo_list, type='sco2', plot_title=plot_title)
    design_tools.plot_costs_barchart(dict_index_duo_list, type='system', plot_title=plot_title)

    plot_paretos(dict_list_with_kwarg, [], [], barchart_configs_list, plot_title)

    # Plot cost breakdown (focused w/ samples)
    #dict_index_duo_list_focused = []
    #for best_dict_kwarg in best_list_with_kwarg:
    #    best_dict = best_dict_kwarg[0]
    #    config_name = best_dict['config_name'][0]
    #    if(config_name.lower() in barchart_configs_list):
    #        dict_index_duo_list_focused.append([best_dict, 0])
    #dict_index_duo_list_samples = []
    #for sample_dict_kwarg in sample_list_with_kwarg:
    #    sample_dict = sample_dict_kwarg[0]
    #    kwarg = sample_dict_kwarg[1]
    #    dict_index_duo_list_samples.append([sample_dict, 0, kwarg])
    #design_tools.plot_costs_barchart([*dict_index_duo_list_focused, *dict_index_duo_list_samples], type='sco2')
    #design_tools.plot_costs_barchart([*dict_index_duo_list_focused, *dict_index_duo_list_samples], type='system')

    # $/kWe Plot
    #design_tools.plot_parasitics_barchart([*dict_index_duo_list_focused, *dict_index_duo_list_samples])

# Plot methods

def prep_recomp_test():
    
    # Get Filenames
    hardcode = True
    if hardcode:
        filenames, _ = sco2_filenames.get_filenames_baseline(False)
    else:
        filename_htrbp = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 htrbp pkl file")
        filename_recomp = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 recomp pkl file")
        filename_partial = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open g3p3 partial pkl file")
    
    # Load result dicts
    print('Opening pickles...')
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

    # remove simple double recup
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        if config_name.lower() == 'simple double recup':
            result_dict_list.pop(i)
            break
        i += 1

    # Add UA calc / ua assigned key to dicts
    for result_dict in result_dict_list:
        NVal = len(result_dict['config_name'])
        result_dict['LTR_UA_assigned_over_calc'] = []
        result_dict['HTR_UA_assigned_over_calc'] = []
        for i in range(NVal):
            LTR_UA_assigned = result_dict['LTR_UA_assigned'][i]
            LTR_UA_calculated = result_dict['LTR_UA_calculated'][i]
            HTR_UA_assigned = result_dict['HTR_UA_assigned'][i]
            HTR_UA_calculated = result_dict['HTR_UA_calculated'][i]

            LTR_UA_assigned_over_calc = 1 if LTR_UA_calculated == 0 else LTR_UA_assigned / LTR_UA_calculated
            HTR_UA_assigned_over_calc = 1 if HTR_UA_calculated == 0 else HTR_UA_assigned / HTR_UA_calculated

            result_dict['LTR_UA_assigned_over_calc'].append(LTR_UA_assigned_over_calc)
            result_dict['HTR_UA_assigned_over_calc'].append(HTR_UA_assigned_over_calc)

    # make dict_list_with_kwarg
    dict_list_with_kwargs = []
    marker_list = design_tools.get_marker_list()
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        dict_w_kwarg = [result_dict, {'label':config_name, 'marker':marker_list[i]}]
        dict_list_with_kwargs.append(dict_w_kwarg)
        i += 1

    # Add LCOE
    print("Adding LCOE...")
    add_LCOE(dict_list_with_kwargs)

    # Find Sample cases
    print("Getting sample cases...")
    sample_dict_list_w_kwargs = find_sample_cases(dict_list_with_kwargs)

    # Get Best Cases
    print("Finding best $/kWe cases...")
    best_dict_list_with_kwarg = []
    for dict_kwarg in dict_list_with_kwargs:
        diction = dict_kwarg[0]
        kwarg = copy.deepcopy(dict_kwarg[1])
        if('marker' in kwarg) == False:
            kwarg['marker'] = 'X'
        kwarg['label'] = 'Best ' + kwarg['label']
        kwarg['c'] = 'black'
        best_dict = sco2_plot_g3p3_baseline_FINAL.get_best_dict(diction, "cost_per_kWe_net_ish", False)
        best_dict_list_with_kwarg.append([best_dict, kwarg])

    # Select which bar chart configs to show
    barchart_configs_list = ["turbine split flow", "partial intercooling w/o htr", "simple split flow bypass w/o ltr",
                              "simple", "partial w/o htr", "recompression w/o htr"]

    # Plot
    #plot_test(dict_list_with_kwargs)
    plot_FY25Q1(dict_list_with_kwargs, sample_dict_list_w_kwargs, best_dict_list_with_kwarg, barchart_configs_list)
    #plot_paretos(dict_list_with_kwargs, sample_dict_list_w_kwargs, best_dict_list_with_kwarg, barchart_configs_list)
    #plot_w_sample(dict_list_with_kwargs, sample_dict_list_w_kwargs)

def prep_sweep_plot(filename_htrbp = "", filename_recomp = "",
                    filename_tsf = "", filename_partial = "",
                    run_label=""):
    
    # Get Filenames (if necessary)
    filenames = {
        "htr bp": filename_htrbp,
        "recomp": filename_recomp,
        "tsf": filename_tsf,
        "partial": filename_partial
    }

    for sweep_label in filenames:
        if filenames[sweep_label] == "":
            filenames[sweep_label] = askopenfilename(filetypes=[('Pickles', '*.pkl')], title="Open g3p3 " + sweep_label + " pkl file")

    filename_htrbp = filenames["htr bp"]
    filename_recomp = filenames["recomp"]
    filename_tsf = filenames["tsf"]
    filename_partial = filenames["partial"]
    
    # Load result dicts
    print('Opening pickles...')
    result_dict_htrbp = open_pickle(filename_htrbp)
    result_dict_recomp = open_pickle(filename_recomp)
    result_dict_partial = open_pickle(filename_partial)
    result_dict_tsf = open_pickle(filename_tsf)

    input_dict_list = [result_dict_htrbp, result_dict_recomp,
                       result_dict_partial, result_dict_tsf]
    
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

    # remove simple double recup
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        if config_name.lower() == 'simple double recup':
            result_dict_list.pop(i)
            break
        i += 1

    # Add UA calc / ua assigned key to dicts
    for result_dict in result_dict_list:
        NVal = len(result_dict['config_name'])
        result_dict['LTR_UA_assigned_over_calc'] = []
        result_dict['HTR_UA_assigned_over_calc'] = []
        for i in range(NVal):
            LTR_UA_assigned = result_dict['LTR_UA_assigned'][i]
            LTR_UA_calculated = result_dict['LTR_UA_calculated'][i]
            HTR_UA_assigned = result_dict['HTR_UA_assigned'][i]
            HTR_UA_calculated = result_dict['HTR_UA_calculated'][i]

            LTR_UA_assigned_over_calc = 1 if LTR_UA_calculated == 0 else LTR_UA_assigned / LTR_UA_calculated
            HTR_UA_assigned_over_calc = 1 if HTR_UA_calculated == 0 else HTR_UA_assigned / HTR_UA_calculated

            result_dict['LTR_UA_assigned_over_calc'].append(LTR_UA_assigned_over_calc)
            result_dict['HTR_UA_assigned_over_calc'].append(HTR_UA_assigned_over_calc)

    # make dict_list_with_kwarg
    dict_list_with_kwargs = []
    marker_list = design_tools.get_marker_list()
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        dict_w_kwarg = [result_dict, {'label':config_name, 'marker':marker_list[i]}]
        dict_list_with_kwargs.append(dict_w_kwarg)
        i += 1

    # Add LCOE
    print("Adding LCOE...")
    add_LCOE(dict_list_with_kwargs)

    # Find Sample cases
    print("Getting sample cases...")
    sample_dict_list_w_kwargs = find_sample_cases(dict_list_with_kwargs)

    # Get Best Cases
    print("Finding best $/kWe cases...")
    best_dict_list_with_kwarg = []
    for dict_kwarg in dict_list_with_kwargs:
        diction = dict_kwarg[0]
        kwarg = copy.deepcopy(dict_kwarg[1])
        if('marker' in kwarg) == False:
            kwarg['marker'] = 'X'
        kwarg['label'] = 'Best ' + kwarg['label']
        kwarg['c'] = 'black'
        best_dict = sco2_plot_g3p3_baseline_FINAL.get_best_dict(diction, "cost_per_kWe_net_ish", False)
        best_dict_list_with_kwarg.append([best_dict, kwarg])

    # Select which bar chart configs to show
    barchart_configs_list = ["turbine split flow", "partial intercooling w/o htr", "simple split flow bypass w/o ltr",
                              "simple", "partial w/o htr", "recompression w/o htr"]

    # Plot
    plot_select(dict_list_with_kwargs, sample_dict_list_w_kwargs, best_dict_list_with_kwarg, barchart_configs_list, run_label)

def prep_comparison():
    
    filename_htrbp_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250215_171644__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
    filename_recomp_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_163031__recomp_G3P3_collection_10_20250210_180210_000.pkl"
    filename_tsf_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_175940__TSF_G3P3_collection_10_20250210_180908_000.pkl"
    filename_partial_old = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_053648__partial_G3P3_collection_10_20250210_142613_000.pkl"

    filename_htrbp_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
    filename_recomp_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
    filename_tsf_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
    filename_partial_new = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

    filename_list_old = [filename_htrbp_old, filename_recomp_old,
                         filename_tsf_old, filename_partial_old]
    
    filename_list_new = [filename_htrbp_new, filename_recomp_new,
                         filename_tsf_new, filename_partial_new]

    # Load Pickles
    print('Opening pickles...')
    input_dict_list_old = []
    for filename in filename_list_old:
        input_dict_list_old.append(open_pickle(filename))

    input_dict_list_new = []
    for filename in filename_list_new:
        input_dict_list_new.append(open_pickle(filename))

    input_dict_set = [input_dict_list_old, input_dict_list_new]

    dict_list_with_kwarg_set = []

    i = 0
    for input_dict_list in input_dict_set:

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

        # Clear original dict (for memory)
        for input_dict in input_dict_list:
            input_dict.clear()

        # remove simple double recup
        i = 0
        for result_dict in result_dict_list:
            config_name = result_dict['config_name'][0]
            if config_name.lower() == 'simple double recup':
                result_dict_list.pop(i)
                break
            i += 1

        # Add UA calc / ua assigned key to dicts
        for result_dict in result_dict_list:
            NVal = len(result_dict['config_name'])
            result_dict['LTR_UA_assigned_over_calc'] = []
            result_dict['HTR_UA_assigned_over_calc'] = []
            for i in range(NVal):
                LTR_UA_assigned = result_dict['LTR_UA_assigned'][i]
                LTR_UA_calculated = result_dict['LTR_UA_calculated'][i]
                HTR_UA_assigned = result_dict['HTR_UA_assigned'][i]
                HTR_UA_calculated = result_dict['HTR_UA_calculated'][i]

                LTR_UA_assigned_over_calc = 1 if LTR_UA_calculated == 0 else LTR_UA_assigned / LTR_UA_calculated
                HTR_UA_assigned_over_calc = 1 if HTR_UA_calculated == 0 else HTR_UA_assigned / HTR_UA_calculated

                result_dict['LTR_UA_assigned_over_calc'].append(LTR_UA_assigned_over_calc)
                result_dict['HTR_UA_assigned_over_calc'].append(HTR_UA_assigned_over_calc)

        # make dict_list_with_kwarg
        dict_list_with_kwargs = []
        marker_list = design_tools.get_marker_list()
        i = 0
        for result_dict in result_dict_list:
            config_name = result_dict['config_name'][0]
            dict_w_kwarg = [result_dict, {'label':config_name, 'marker':marker_list[i]}]
            dict_list_with_kwargs.append(dict_w_kwarg)
            i += 1

        dict_list_with_kwarg_set.append(dict_list_with_kwargs)

    # Plot
    compare_run_sweeps(*dict_list_with_kwarg_set)


def compare_helio_to_base():
    
    filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
    filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
    filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
    filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"
        
    filename_htrbp_helio = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250215_171644__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
    filename_recomp_helio = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_163031__recomp_G3P3_collection_10_20250210_180210_000.pkl"
    filename_tsf_helio = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_175940__TSF_G3P3_collection_10_20250210_180908_000.pkl"
    filename_partial_helio = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_053648__partial_G3P3_collection_10_20250210_142613_000.pkl"

    # Plot Baseline
    prep_sweep_plot(filename_htrbp, filename_recomp, filename_tsf, filename_partial, run_label="Baseline w/ Inflation")

    # Plot Helio
    prep_sweep_plot(filename_htrbp_helio, filename_recomp_helio, filename_tsf_helio, filename_partial_helio, run_label="Heliostat Cost 127 $/m2")

def test_pareto():
    filenames_baseline, _ = sco2_filenames.get_filenames_baseline(split=True)
    result_dict_list = []
    for filename in filenames_baseline:
        result_dict_list.append(sco2_plot_compare_all.open_pickle_mmap(filename))
    
    # make dict_list_with_kwarg
    dict_list_with_kwargs = []
    marker_list = design_tools.get_marker_list()
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        dict_w_kwarg = [result_dict, {'label':config_name, 'marker':marker_list[i]}]
        dict_list_with_kwargs.append(dict_w_kwarg)
        i += 1

    # Select which bar chart configs to show
    barchart_configs_list = ["turbine split flow", "partial intercooling w/o htr", "simple split flow bypass w/o ltr",
                              "simple", "partial w/o htr", "recompression w/o htr"]


    plot_paretos(dict_list_with_kwargs, [], [], barchart_configs_list, "Test")


if __name__ == "__main__":

    # Define some global labels
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
    
    MIN_DT_LTR_label = ["LTR_min_dT", "C", "LTR Min dT"]
    UA_ASSIGNED_LTR_label = ["LTR_UA_assigned", "MW/K", "LTR UA Assigned"]
    UA_CALC_LTR_label = ["LTR_UA_calculated", "MW/K", "LTR UA Calculated"]
    EFF_LTR_label = ["eff_LTR", "", "LTR Effectiveness"]
    MIN_DT_HTR_label = ["HTR_min_dT", "C", "HTR Min dT"]
    UA_ASSIGNED_HTR_label = ["HTR_UA_assigned", "MW/K", "HTR UA Assigned"]
    UA_CALC_HTR_label = ["HTR_UA_calculated", "MW/K", "HTR UA Calculated"]
    EFF_HTR_label = ["eff_HTR", "", "HTR Effectiveness"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]
    
    LTR_UA_assigned_over_calc_label = ["LTR_UA_assigned_over_calc", "", "LTR UA Assigned / Calculated"]
    HTR_UA_assigned_over_calc_label = ["HTR_UA_assigned_over_calc", "", "HTR UA Assigned / Calculated"]

    COST_PER_kW_GROSS_NORM_label = ["cost_per_kWe_gross_norm", "", "Cost per kWe Gross Normalized"]
    COST_PER_kW_NET_NORM_label = ["cost_per_kWe_net_ish_norm", "", "Cost per kWe Net Normalized"]

    CYCLE_cost_label = ["cycle_cost", "M$", "Cycle Cost"]

    LCOE_cent_label = ["lcoe_cent", "\u00A2/kWe", "LCOE"]

    #plot_pkl_g3p3_via_filedlg()
    prep_recomp_test()
    #compare_helio_to_base()
    #prep_comparison()
    #test_pareto()
    plt.show(block = True)