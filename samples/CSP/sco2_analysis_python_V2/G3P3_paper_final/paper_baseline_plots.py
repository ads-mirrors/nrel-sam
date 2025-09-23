import sys
import os
import copy
import matplotlib.pyplot as plt
from tkinter.filedialog import asksaveasfilename
import math
import numpy as np

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
g3p3PlottingFolder = os.path.join(parentDir, 'G3P3_analysis_plotting')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)
sys.path.append(g3p3PlottingFolder)

import sco2_filenames
import data_utility
import design_point_tools as design_tools
import sco2_varnames
import paper_comparison_plots
from sco2_filenames import BASE
from sco2_filenames import TIT550
from sco2_filenames import TIT625

FIG_WIDTH_SMALL = 3.54331   # [in] 90 mm
FIG_WIDTH_MED = 5.51181     # [in] 140 mm
FIG_WIDTH_FULL = 7.48031    # [in] 190 mm
FONT_SIZE_FIG = 7           # figure font size

COST_PER_kW_info = ["cost_per_kWe_net_ish", "$/kWe", "System Specific Cost (SSC)\n"]
kCOST_PER_kW_info = ["kcost_per_kWet_ish", "k$/kWe", "System Specific Cost (SSC)\n"]

LTR_UA_CALC_info = ["LTR_UA_calculated", "MW/K", "LTR Conductance"]
HTR_UA_CALC_info = ["HTR_UA_calculated", "MW/K", "HTR Conductance"]
LTR_UA_FRAC_info = ["LTR_UA_frac", "", "LTR Conductance Fraction of Total"]
BP_FRAC_DISP_info = ["bp_frac_disp", "", "Bypass Fraction"]
RECOMP_FRAC_info = ["recomp_frac", "", "Recompression Fraction"]
RECUP_EFF_AVG_info = ["recup_eff_avg", "", "Average Recuperator Effectiveness"]
HTR_EFF_info = ["eff_HTR", "", "HTR Effectiveness"]

def write_array_to_file(list_list_data, filename=None):
    
    if filename == None:
        filename = asksaveasfilename(confirmoverwrite=True, filetypes =[('Txt Files', '*.txt')], title="Save?")
    if filename == '':
        return
    
    delimiter = '\t'

    N_col = len(list_list_data[0])
    N_row = len(list_list_data)

    f = open(filename, "w")

    for row in range(N_row):

        for col in range(N_col):
            val = list_list_data[row][col]
            f.write(val)
            
            if(col != N_col - 1):
                f.write(delimiter)
        
        f.write('\n')
    
    f.close()


def plot_sco2_dual_paretos(dict_list_w_kwarg, X_info, Y1_info, Y2_info, config_list=[]):
    pareto_list_w_kwarg_Y1 = []
    pareto_list_w_kwarg_Y2 = []

    map_index_to_config_name = {}
    i = 0
    for result_dict, kwarg in dict_list_w_kwarg:
        config_name = result_dict['config_name'][0]
        map_index_to_config_name[config_name] = i
        i += 1

    for config_name in config_list:
        index = map_index_to_config_name[config_name]
        result_dict, kwarg = dict_list_w_kwarg[index]
 
        if config_name in config_list:
            pareto_dict_Y1 = design_tools.get_min_Y_pareto_dict(result_dict, X_info[0], Y1_info[0], 50)
            pareto_dict_Y2 = design_tools.get_min_Y_pareto_dict(result_dict, X_info[0], Y2_info[0], 50)
            pareto_kwarg = copy.deepcopy(kwarg)

            # Remove Preset Color and Marker
            pareto_kwarg.pop('c', None)
            pareto_kwarg.pop('marker', None)

            pareto_list_w_kwarg_Y1.append([pareto_dict_Y1, pareto_kwarg])
            pareto_list_w_kwarg_Y2.append([pareto_dict_Y2, pareto_kwarg])

    with plt.rc_context({'font.size': FONT_SIZE_FIG}):
        fig_combined, (ax1, ax2) = plt.subplots(1,2, figsize=(FIG_WIDTH_FULL, 2.75), 
                                                sharey=False,
                                                gridspec_kw={
                                                'wspace': 0.25,
                                                })

        design_tools.plot_scatter_pts(
                    pareto_list_w_kwarg_Y1
                    , 
                    X_info, Y1_info, show_legend=False,
                    ax=ax1, disk_load=True)
        
        design_tools.plot_scatter_pts(
                    pareto_list_w_kwarg_Y2
                    , 
                    X_info, Y2_info, show_legend=True,
                    legend_loc='outside right',
                    ax=ax2,
                    shorten_legend=True, disk_load=True)
        

        # Set explicit figure margins
        fig_combined.subplots_adjust(
            left=0.07,    # Left margin: 10% of figure width
            right=0.78,  # Right margin: 15% of figure width (leave space for legend)
            bottom=0.15, # Bottom margin: 15% of figure height
            top=0.98      # Top margin: 10% of figure height
        )

        #plt.tight_layout()

def plot_full_data(dict_list_w_kwarg, X_info, Y_info, config_list=[]):
    dict_list_w_kwarg_local = []

    for result_dict, kwarg in dict_list_w_kwarg:

        config_name = result_dict['config_name'][0]
        if config_name in config_list:
            kwarg_local = copy.deepcopy(kwarg)

            # Remove Preset Color and Marker
            kwarg_local.pop('c', None)
            kwarg_local.pop('marker', None)

            dict_list_w_kwarg_local.append([result_dict, kwarg_local])

    with plt.rc_context({'font.size': FONT_SIZE_FIG}):
        fig, ax1 = plt.subplots(figsize=(FIG_WIDTH_FULL, 3.27))

        design_tools.plot_scatter_pts(
                    dict_list_w_kwarg_local
                    , 
                    X_info, Y_info, show_legend=True,
                    legend_loc='outside right',
                    ax=ax1,
                    shorten_legend=True,
                    disk_load=True)
        
        plt.tight_layout()

def plot_full_w_pareto(dict_list_w_kwarg, X_info, Y_info, config_list):
    dict_list_w_kwarg_local = []
    pareto_list_w_kwarg_local = []

    map_index_to_config_name = {}
    i = 0
    for result_dict, kwarg in dict_list_w_kwarg:
        config_name = result_dict['config_name'][0]
        map_index_to_config_name[config_name] = i
        i += 1

    for config_name in config_list:
        index = map_index_to_config_name[config_name]
        result_dict, kwarg = dict_list_w_kwarg[index]

        if config_name in config_list:
            pareto_dict_Y = design_tools.get_min_Y_pareto_dict(result_dict, X_info[0], Y_info[0], 50)
            # Remove Preset Color and Marker
            kwarg_local = copy.deepcopy(kwarg)
            kwarg_local.pop('c', None)
            kwarg_local.pop('marker', None)

            dict_list_w_kwarg_local.append([result_dict, kwarg_local])
            pareto_list_w_kwarg_local.append([pareto_dict_Y, kwarg_local])

    with plt.rc_context({'font.size': FONT_SIZE_FIG}):
        fig_combined, (ax1, ax2) = plt.subplots(1,2, figsize=(FIG_WIDTH_FULL, 2.75), 
                                                sharey=False,
                                                gridspec_kw={
                                                'wspace': 0.1,
                                                })

        design_tools.plot_scatter_pts(
                    dict_list_w_kwarg_local
                    , 
                    X_info, Y_info, show_legend=False,
                    ax=ax1, disk_load=True)
        
        design_tools.plot_scatter_pts(
                    pareto_list_w_kwarg_local
                    , 
                    X_info, Y_info, show_legend=True,
                    legend_loc='outside right',
                    ax=ax2,
                    shorten_legend=True, disk_load=True)
        
        # Set second plot Y axis limits to first, remove label
        #y_min, y_max = ax1.get_ylim()
        #ax2.set_ylim(y_min, y_max)
        ax2.set_ylabel("")

        # Set explicit figure margins
        fig_combined.subplots_adjust(
            left=0.07,    # Left margin: 10% of figure width
            right=0.78,  # Right margin: 15% of figure width (leave space for legend)
            bottom=0.15, # Bottom margin: 15% of figure height
            top=0.98      # Top margin: 10% of figure height
        )


def plot_config_comparison(best_list_w_kwarg, Y1_info, Y2_info=[], config_list=[]):
    figsize_global = (5, 2.69)
    fontsize_global = 6
    with plt.rc_context({'font.size': fontsize_global}):
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y1_info, Y2_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)

def plot_config_comparison_duo(best_list_w_kwarg, Y1_info, Y2_info, Y3_info, Y4_info,
                               config_list):
    figsize_global = (FIG_WIDTH_MED, 4.5)
    fontsize_global = FONT_SIZE_FIG
    with plt.rc_context({'font.size': fontsize_global}):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize_global)
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y1_info, Y2_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global,
                                                   ax=ax1, showX=False, legend_loc='lower center')
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y3_info, Y4_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global,
                                                   ax=ax2, legend_loc='lower center')

def plot_config_comparison_4(best_list_w_kwarg, Y1_info, Y2_info, Y3_info, Y4_info,
                               config_list):
    figsize_global = (FIG_WIDTH_MED, 6)
    fontsize_global = FONT_SIZE_FIG
    colors = ['black']
    with plt.rc_context({'font.size': fontsize_global}):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=figsize_global)

        
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y1_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global,
                                                   ax=ax1, showX=False, legend_loc='lower center', show_legend = False, colors=colors)
        ax1.set_yticks([5900,6000,6100,6200,6300])
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y2_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global,
                                                   ax=ax2, showX=False, legend_loc='lower center', show_legend = False, colors=colors)
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y3_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global,
                                                   ax=ax3, showX=False, legend_loc='lower center', show_legend = False, colors=colors)
        ax3.set_yticks([0.41,0.42,0.43,0.44,0.45])
        design_tools.plot_config_comparison_single(best_list_w_kwarg, config_list, Y4_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global,
                                                   ax=ax4, legend_loc='lower center', show_legend = False, colors=colors)
        ax4.set_yticks([300,350,400,450,500])


def plot_single_config_zoom_in(dict_list_w_kwarg, show_config_name, X_info, Y1_info, Y2_info):
    pareto_dict_w_kwarg_Y1 = []

    for result_dict, kwarg in dict_list_w_kwarg:

        config_name = result_dict['config_name'][0]
        if show_config_name == config_name:
            pareto_dict_Y1 = design_tools.get_min_Y_pareto_dict(result_dict, X_info[0], Y1_info[0], 50)
            pareto_kwarg = copy.deepcopy(kwarg)

            # Remove Preset Color and Marker
            pareto_kwarg.pop('c', None)
            pareto_kwarg.pop('marker', None)

            pareto_dict_w_kwarg_Y1 = [pareto_dict_Y1, pareto_kwarg]
            break

    with plt.rc_context({'font.size': FONT_SIZE_FIG}):
        fig_combined, ax1 = plt.subplots(1, figsize=(FIG_WIDTH_SMALL, 2.62), sharey=False)

        design_tools.plot_scatter_pts_dual_Y(pareto_dict_w_kwarg_Y1[0], X_info, Y1_info, Y2_info, 
                                             title="Recompression Cycle", show_legend=True, legend_loc="upper center",
                                             show_line=True,
                                             ax1=ax1
                                             )
        plt.tight_layout()

def plot_barcharts(best_dict_list_w_kwarg, config_list):
    
    # Plot cost breakdown
    fontsize = FONT_SIZE_FIG
    figsize = (FIG_WIDTH_FULL, 3.27)

    dict_index_duo_list = []
    for config_name in config_list:
        for best_dict_kwarg in best_dict_list_w_kwarg:
            best_dict = best_dict_kwarg[0]
            config_name_local = best_dict['config_name'][0]
            if config_name == config_name_local:
                dict_index_duo_list.append([best_dict, 0])
                break
    design_tools.plot_costs_barchart(dict_index_duo_list, type='sco2', plot_title="Cycle Cost Comparison", fontsize=fontsize, figsize=figsize, shorten_config_label=True)
    design_tools.plot_costs_barchart(dict_index_duo_list, type='system', plot_title="System Cost Comparison", fontsize=fontsize, figsize=figsize, shorten_config_label=True)

def generate_table(best_dict_list_w_kwarg, show_config_list):
    
    # Select Vars to show
    var_info_list = sco2_varnames.get_baseline_table_info_list()

    # Load complete cases from disk
    dict_list_complete = []
    for result_dict_partial, _ in best_dict_list_w_kwarg:
        # Load complete case from disk
        filename = result_dict_partial['run_filename'][0]
        run_id = result_dict_partial['run_id'][0]
        result_dict_complete = design_tools.get_single_case_disk(filename, run_id)
        dict_list_complete.append(result_dict_complete)

    # Map config_name to index of list
    config_name_to_index = {d["config_name"][0]: i for i, d in enumerate(dict_list_complete)}
    
    # Organize Data
    table_data_inner = []
    label_list = []
    unit_list = []
    for var_info in var_info_list:
        var = var_info[0]
        var_unit = var_info[1]
        var_label = var_info[2]

        label_list.append(var_label)
        unit_list.append(var_unit)

        row_data = []
        for config in show_config_list:
            index = config_name_to_index.get(config)
            result_dict_complete = dict_list_complete[index]

            row_val_formatted = "-"
            if var in result_dict_complete:
                row_val = result_dict_complete[var][0]
                
                if row_val != '':
                    if math.isnan(row_val):
                        row_val_formatted = "-"
                    else:
                        row_val_formatted = "{:.8f}".format(row_val)
                else:
                    row_val_formatted = row_val
            
            row_data.append(row_val_formatted)
        table_data_inner.append(row_data)

    # Wrap config labels
    show_config_list_wrapped = []
    for config_name in show_config_list:
        show_config_list_wrapped.append(design_tools.shorten_config(config_name))

    # Undo wrapping
    #show_config_list_wrapped = show_config_list

    # Put together table data
    table_data_complete = []
    table_first_row = ["", "Unit", *show_config_list_wrapped]
    table_data_complete.append(table_first_row)
    for i, row_data in enumerate(table_data_inner):
        label = label_list[i]
        unit = unit_list[i]
        row_complete = [label, unit, *row_data]
        table_data_complete.append(row_complete)

    # Save Table
    write_array_to_file(table_data_complete)

def plot_appendix_sco2_pars(dict_list_w_kwarg, XY_info_list, config_list=[]):
    
    N_plots = len(XY_info_list)

    N_col = 2
    N_row = math.ceil(N_plots / N_col)
    
    fig_height = 2.75 * N_row

    Y_min_manual = 5.5
    Y_max_manual= 14

    with plt.rc_context({'font.size': FONT_SIZE_FIG}):
        fig_combined, axes_collection = plt.subplots(N_row, N_col, figsize=(FIG_WIDTH_FULL, fig_height), 
                                                sharey=False,
                                                gridspec_kw={
                                                'wspace': 0.15,
                                                })

        if N_row == 1:
            axes_collection = axes_collection.reshape(1, -1)

        # Make unused axis invisible
        if N_plots % 2 != 0:
            axes_collection[N_row - 1, N_col - 1].set_visible(False)


        for i_plot in range(N_plots):

            i_row = math.floor(i_plot / N_col)
            i_col = i_plot % N_col
            axis_local = axes_collection[i_row, i_col]

            X_info_local = XY_info_list[i_plot][0]
            Y_info_local = XY_info_list[i_plot][1]
            pareto_list_w_kwarg_local = []

            map_index_to_config_name = {}
            i = 0
            for result_dict, kwarg in dict_list_w_kwarg:
                config_name = result_dict['config_name'][0]
                map_index_to_config_name[config_name] = i
                i += 1

            for config_name in config_list:
                index = map_index_to_config_name[config_name]
                result_dict, kwarg = dict_list_w_kwarg[index]
        
                if config_name in config_list:
                    pareto_dict_local = design_tools.get_min_Y_pareto_dict(result_dict, X_info_local[0], Y_info_local[0], 50)
                    pareto_kwarg_local = copy.deepcopy(kwarg)

                    # Remove Preset Color and Marker
                    pareto_kwarg_local.pop('c', None)
                    pareto_kwarg_local.pop('marker', None)

                    pareto_list_w_kwarg_local.append([pareto_dict_local, pareto_kwarg_local])            

            if i_plot == 0:
                _, new_kwarg_list = design_tools.plot_scatter_pts(
                            pareto_list_w_kwarg_local, 
                            X_info_local, Y_info_local, show_legend=False,
                            ax=axis_local, disk_load=True,
                            shorten_legend=True)
            
                # Extract legend handles and labels
                legend_handles, legend_labels = axis_local.get_legend_handles_labels()

                legend_labels = [design_tools.shorten_config(label) for label in legend_labels]
            else:
                design_tools.plot_scatter_pts(
                            pareto_list_w_kwarg_local
                            , 
                            X_info_local, Y_info_local, show_legend=False,
                            ax=axis_local, disk_load=True,
                            shorten_legend=True)
            
            # Set Y-axis limits for each plot
            axis_local.set_ylim(Y_min_manual, Y_max_manual)
        
            # Remove Y label if same as left label
            if i_col == 1 and Y_info_local[2] == XY_info_list[i_plot-1][1][2]:
                axis_local.set_ylabel("")

            # Create a single legend for the entire figure
            fig_combined.legend(legend_handles, legend_labels, 
                           loc='center right', 
                           bbox_to_anchor=(0.99, 0.5))

            # Set explicit figure margins
            fig_combined.subplots_adjust(
                left=0.07,    # Left margin: 10% of figure width
                right=0.78,  # Right margin: 15% of figure width (leave space for legend)
                bottom=0.1, # Bottom margin: 15% of figure height
                top=0.98      # Top margin: 10% of figure height
            )

        #plt.tight_layout()

def add_missing_vars(list_of_dict_list_w_kwargs):

    print('Adding vars...')

    for dict_list_w_kwarg in list_of_dict_list_w_kwargs:
        for result_dict, kwarg in dict_list_w_kwarg:

            result_dict[kCOST_PER_kW_info[0]] = []
            result_dict[LTR_UA_FRAC_info[0]] = []
            result_dict[BP_FRAC_DISP_info[0]] = []
            result_dict[RECUP_EFF_AVG_info[0]] = []

            NVal = len(result_dict[COST_PER_kW_info[0]])
            for i in range(NVal):

                # $/kW
                cost_per_kW = result_dict[COST_PER_kW_info[0]][i]           # $/kW
                result_dict[kCOST_PER_kW_info[0]].append(cost_per_kW / 1e3) # k$/kW

                # LTR/HTR split
                ltr_ua = result_dict[LTR_UA_CALC_info[0]][i]
                htr_ua = result_dict[HTR_UA_CALC_info[0]][i]
                if math.isnan(ltr_ua): ltr_ua = 0
                if math.isnan(htr_ua): htr_ua = 0
                ltr_ua_frac = ltr_ua / (ltr_ua + htr_ua)
                result_dict[LTR_UA_FRAC_info[0]].append(ltr_ua_frac)

                # Bypass
                bp_frac_disp = 0
                cycle_config = result_dict['cycle_config'][i]
                if cycle_config == 3:
                    bp_ua = result_dict["UA_BPX"][i]
                    if bp_ua == '0.0': bp_ua = 0
                    if math.isnan(bp_ua): bp_ua = 0
                    if bp_ua > 0: 
                        bp_frac_disp = result_dict["bypass_frac"][i]
                result_dict[BP_FRAC_DISP_info[0]].append(bp_frac_disp)
                
                # Recup effectiveness
                eff_vec = []
                if ltr_ua > 0: eff_vec.append(result_dict['eff_LTR'][i])
                if htr_ua > 0: eff_vec.append(result_dict['eff_HTR'][i])
                if len(eff_vec) > 0:
                    eff_avg = np.mean(eff_vec)
                else:
                    eff_avg = 0
                result_dict[RECUP_EFF_AVG_info[0]].append(eff_avg)

def make_baseline_plots():
    
    file_enum = BASE.BASELINE
    #file_enum = TIT550.BASELINE
    
    filenames_baseline_w_label = sco2_filenames.get_file_via_enum(file_enum, True)
    
    filenames_list_w_label = [filenames_baseline_w_label]

    key_list = ["cycle_config", "config_name",
                "recomp_frac", "bypass_frac",
                "LTR_UA_calculated", "HTR_UA_calculated",
                "cost_per_kWe_net_ish", "eta_thermal_calc", "T_htf_cold_des",
                "cycle_cost", "csp.pt.cost.heliostats",
                "csp.pt.cost.storage", "recup_total_UA_calculated",
                "T_htf_hot_des", 
                "mc_cost_bare_erected", "rc_cost_bare_erected",
                "pc_cost_bare_erected", "LTR_cost_bare_erected",
                "HTR_cost_bare_erected", "PHX_cost_bare_erected",
                "BPX_cost_bare_erected", "t_cost_bare_erected",
                "t2_cost_bare_erected", "mc_cooler_cost_bare_erected",
                "pc_cooler_cost_bare_erected", "piping_inventory_etc_cost",
                "csp.pt.cost.site_improvements", "csp.pt.cost.heliostats",
                "csp.pt.cost.tower", "csp.pt.cost.receiver",
                "receiver_lift_cost", "csp.pt.cost.storage",
                "csp.pt.cost.power_block", "heater_cost",
                "csp.pt.cost.bop", "csp.pt.cost.fossil",
                "ui_direct_subtotal",
                "UA_recup_tot_des", "LTR_UA_des_in", "HTR_UA_des_in",
                "is_PR_fixed", "is_IP_fixed", "is_recomp_ok",
                "is_turbine_split_ok", "is_bypass_ok",
                "HTR_cost_equipment", "LTR_cost_equipment",
                "recup_total_cost_equipment",
                "mc_cooler_q_dot", "pc_cooler_q_dot",
                "id", "UA_BPX", "BPX_cost_equipment", "T_htf_bp_out_des",
                "q_dot_in_total", "mc_cooler_q_dot", "pc_cooler_q_dot",
                "eff_LTR", "eff_HTR"]

    output = data_utility.open_file_set_w_label(filenames_list_w_label, key_list)
    list_of_dict_list_w_kwargs = output[0]
    list_of_best_dict_list_with_kwarg = output[1]
    final_sweep_labels = output[2]

    # Configs to be plotted
    show_config_list = ['Simple', 'Simple Split Flow Bypass w/o LTR', 'Simple Split Flow Bypass',  
                        'Recompression', 'Recompression w/o LTR', 'Recompression w/o HTR',
                        'HTR BP', 'HTR BP w/o LTR', 
                        'Partial', 'Partial w/o HTR', 'Partial w/o LTR', 'Partial Intercooling w/o HTR',
                        'Turbine Split Flow']
    
    #show_config_list = ['Simple', 'Simple Split Flow Bypass w/o LTR', 'Simple Split Flow Bypass',  
    #                    'Recompression', 'Recompression w/o LTR', 'Recompression w/o HTR',
    #                    'HTR BP', 'HTR BP w/o LTR', 
    #                    'Partial', 'Partial w/o HTR', 'Partial w/o LTR', 'Partial Intercooling w/o HTR',
    #                    'Partial HX flip', 'Partial w/o HTR HX flip',
    #                    'Turbine Split Flow', 'Turbine Split Flow HX flip']

    # Variables
    T_HTF_COLD_info = ["T_htf_cold_des", "°C", "HTF Cold Temperature"]
    CYCLE_COST_info = ["cycle_cost", "M$", "Cycle Cost"]
    COST_PER_kW_info = ["cost_per_kWe_net_ish", "$/kWe", "System Specific Cost (SSC)\n"]
    kCOST_PER_kW_info = ["kcost_per_kWet_ish", "k$/kWe", "System Specific Cost (SSC)\n"]
    PC_ETA_info = ["eta_thermal_calc", "", "PC Thermal Efficiency"]
    UA_CALC_info = ["recup_total_UA_calculated", "MW/K", "Total Recuperator Conductance"]
    BP_info = ["is_bypass_ok", "", "Bypass Fraction"]
    RC_info = ["is_recomp_ok", "", "Recompression Fraction"]

    # Add k$/kWe 
    add_missing_vars(list_of_dict_list_w_kwargs)

    print('Plotting...')
    # Make Table
    #generate_table(list_of_best_dict_list_with_kwarg[0], show_config_list)
    
    # Plot Paretos
    plot_sco2_dual_paretos(list_of_dict_list_w_kwargs[0], PC_ETA_info, T_HTF_COLD_info, CYCLE_COST_info, show_config_list)

    # Plot Full Data
    #plot_full_data(list_of_dict_list_w_kwargs[0], PC_ETA_info, kCOST_PER_kW_info, show_config_list)
    plot_full_w_pareto(list_of_dict_list_w_kwargs[0], PC_ETA_info, kCOST_PER_kW_info, show_config_list)
    #plot_full_w_pareto(list_of_dict_list_w_kwargs[0], UA_CALC_info, kCOST_PER_kW_info, show_config_list)

    # Plot Baseline
    #plot_config_comparison(list_of_best_dict_list_with_kwarg[0], COST_PER_kW_info, CYCLE_COST_info, show_config_list)
    #plot_config_comparison(list_of_best_dict_list_with_kwarg[0], PC_ETA_info, T_HTF_COLD_info, show_config_list)

    #plot_config_comparison_duo(list_of_best_dict_list_with_kwarg[0], COST_PER_kW_info, CYCLE_COST_info,
    #                           PC_ETA_info, T_HTF_COLD_info, show_config_list)
    
    plot_config_comparison_4(list_of_best_dict_list_with_kwarg[0], COST_PER_kW_info, CYCLE_COST_info,
                               PC_ETA_info, T_HTF_COLD_info, show_config_list)

    # Plot Recompression Specific
    plot_single_config_zoom_in(list_of_dict_list_w_kwargs[0], "Recompression", 
                               PC_ETA_info, COST_PER_kW_info, UA_CALC_info)
    
    #plot_single_config_zoom_in(list_of_dict_list_w_kwargs[0], "Recompression", 
    #                           PC_ETA_info, COST_PER_kW_info, HTR_EFF_info)

    # Plot Bar Plots
    bar_configs = ["Simple", 'Simple Split Flow Bypass w/o LTR', "Recompression w/o HTR", 
                   "HTR BP w/o LTR", "Partial w/o LTR", "Partial Intercooling w/o HTR",
                   "Turbine Split Flow"]
    #bar_configs = ['Simple', 'Simple Split Flow Bypass', 'Simple Split Flow Bypass w/o LTR', 
    #                    'Recompression', 'Recompression w/o LTR', 'Recompression w/o HTR',
    #                    'HTR BP', 'HTR BP w/o LTR', 
    #                    'Partial', 'Partial w/o HTR', 'Partial w/o LTR', 'Partial Intercooling w/o HTR',
    #                    'Turbine Split Flow']
    plot_barcharts(list_of_best_dict_list_with_kwarg[0], bar_configs)

    # Appendix sco2 parameters
    plot_appendix_sco2_pars(list_of_dict_list_w_kwargs[0], 
                            [[UA_CALC_info, kCOST_PER_kW_info], [LTR_UA_FRAC_info, kCOST_PER_kW_info],
                             [RECOMP_FRAC_info, kCOST_PER_kW_info], [BP_FRAC_DISP_info, kCOST_PER_kW_info]
                             ],
                            show_config_list)


    #T_PHX_sweep_labels = [filenames_baseline_w_label[1]]
    #paper_comparison_plots.plot_comparisons_duo(list_of_best_dict_list_with_kwarg, final_sweep_labels, T_PHX_sweep_labels, COST_PER_kW_info, show_config_list)


    plt.rcParams['savefig.dpi'] = 1000
    plt.show(block=True)


if __name__ == "__main__":
    make_baseline_plots()