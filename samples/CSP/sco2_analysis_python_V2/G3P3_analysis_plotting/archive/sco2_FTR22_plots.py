import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import copy

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
grandparentDir = os.path.dirname(parentDir)
exampleFolder = os.path.join(grandparentDir, 'example')
coreFolder = os.path.join(grandparentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

import design_point_tools as design_tools
import sco2_cycle_ssc as sco2_solve
import sco2_filenames
import sco2_plot_compare_all
import sco2_plot_g3p3_baseline_FINAL

def tsf_plots():

    # Get Baseline file names
    filenames_baseline, _ = sco2_filenames.get_filenames_baseline(split=True)
    tsf_result_dict = {}

    # Open TSF dictionary
    for filename in filenames_baseline:
        result_dict = sco2_plot_compare_all.open_pickle_mmap(filename)
        config_name = result_dict['config_name'][0]
        if(config_name == "Turbine Split Flow"):
            tsf_result_dict = result_dict
            break

    # Make turbine split flow variable
    tsf_result_dict["turbine_split_fraction"] = []
    for val in tsf_result_dict["is_turbine_split_ok"]:
        tsf_result_dict["turbine_split_fraction"].append(val * -1)

    # Plot Efficiency against design variables
    design_vars = [["turbine_split_fraction", "-", "Turbine Split Fraction"],
                   ["P_state_points_0_0", "MPa", "Minimum Pressure"],
                   ["recup_total_UA_calculated", "MW/K", "Total Recuperator Conductance"],
                   ["recup_LTR_UA_frac", "-", "LTR Conductance / Total"]]
    
    # $/kWe vs T HTF   
    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor
    fig_1, axs = plt.subplots(2,2)
    fig_1.set_size_inches(fig_width, fig_height)

    i = 0
    for design_var_info in design_vars:
        row = int(np.floor(i / 2))
        col = i % 2

        ax = axs[row, col]

        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        ax.set_axisbelow(True)

        design_tools.plot_scatter_pts([[tsf_result_dict, {'marker':'.'}]],
                                    design_var_info, PC_ETA_label,
                                    show_legend=False, title='', legend_loc='upper right',
                                    ax=ax)
        
        i += 1

    # Adjust layout to make room for the title
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust the bottom, left, right, and top margins

    fig_1.suptitle('Turbine Split Flow')


    # $/kWe vs T HTF   
    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor
    fig_2, ax2 = plt.subplots()
    fig_2.set_size_inches(fig_width, fig_height)

    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_axisbelow(True)

    design_tools.plot_scatter_pts([[tsf_result_dict, {'marker':'.'}]],
                                PC_ETA_label, T_HTF_label,
                                show_legend=False, title='', legend_loc='upper right',
                                ax=ax2)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust the bottom, left, right, and top margins

    fig_2.suptitle('Turbine Split Flow')

    pass

def htrbp_plots(Y_info):
    # Get Baseline file names
    filenames_baseline, _ = sco2_filenames.get_filenames_baseline(split=True)
    
    config_list = ["HTR BP", "Recompression", "Simple", 
                   "Simple Split Flow Bypass", "Simple Split Flow Bypass w/o LTR",
                   "Simple Split Flow Bypass w/o HTR"]

    # Get specific dictionaries
    result_dict_list_w_kwarg = []
    for filename in filenames_baseline:
        result_dict = sco2_plot_compare_all.open_pickle_mmap(filename)
        config_name = result_dict['config_name'][0]

        
        kwarg = {"label":config_name, "marker":"."}
        result_dict_list_w_kwarg.append([result_dict, kwarg])
        continue

        if(config_name in config_list):
            kwarg = {"label":config_name, "marker":"."}
            result_dict_list_w_kwarg.append([result_dict, kwarg])

    # Get Paretos
    pareto_dict_list_w_kwarg = []
    X_label = PC_ETA_label[0]
    for result_dict, _ in result_dict_list_w_kwarg:
        config_name = result_dict["config_name"][0]
        kwarg = {"label":config_name + " pareto", "marker":"."}
        pareto = design_tools.get_min_Y_pareto_dict(result_dict, X_label, Y_info[0], 30)
        pareto_dict_list_w_kwarg.append([pareto, kwarg])

    # Plot
    size_factor = 6
    fig_width = 1.35 * size_factor
    fig_height = 1 * size_factor
    fig_1, ax = plt.subplots()
    fig_1.set_size_inches(fig_width, fig_height)

    i = 0
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    design_tools.plot_scatter_pts(pareto_dict_list_w_kwarg,
                                PC_ETA_label, Y_info,
                                show_legend=True, title='', legend_loc='upper right',
                                ax=ax)

def baseline_plots():
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
        input_dict_list.append(sco2_plot_compare_all.open_pickle_mmap(filename))
        
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

    # Find Sample cases
    #print("Getting sample cases...")
    #sample_dict_list_w_kwargs = find_sample_cases(dict_list_with_kwargs)

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

    best_dict_list_with_kwarg_sorted = sorted(best_dict_list_with_kwarg, 
                                          key=lambda x: x[0]["cost_per_kWe_net_ish"], 
                                          reverse=False)


    # Select which bar chart configs to show
    barchart_configs_list = ["turbine split flow", "partial intercooling w/o htr", "simple split flow bypass w/o ltr",
                              "simple", "partial w/o htr", "recompression w/o htr"]

    # Plot

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

    tsf_plots()
    #baseline_plots()
    #htrbp_plots(COST_PER_kW_NET_label)
    #htrbp_plots(T_HTF_label)
    #htrbp_plots(CYCLE_cost_label)
    plt.show(block=True)