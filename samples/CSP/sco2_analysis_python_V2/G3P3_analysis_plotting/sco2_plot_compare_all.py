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
import sco2_filenames
from multiprocessing import Manager
import gc
import mmap
import psutil

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
g3p3paperfinalFolder = os.path.join(parentDir, 'G3P3_paper_final')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)
sys.path.append(g3p3paperfinalFolder)

import sco2_cycle_ssc as sco2_solve
import design_point_examples as design_pt
import design_point_tools as design_tools
import sco2_varnames
import sco2_plot_sandbox as plot_sandbox
from sco2_plot_g3p3_baseline_FINAL import open_pickle
import sco2_plot_g3p3_baseline_FINAL
import concurrent.futures
from tkinter.filedialog import asksaveasfilename
import sco2_filenames
from sco2_filenames import BASE
from sco2_filenames import TIT550 
from sco2_filenames import TIT625
import data_utility

figsize_global = (11, 6)
fontsize_global = 9

def get_all_keys(list_of_dicts):
    all_keys = set()
    for d in list_of_dicts:
        all_keys.update(d.keys())
    return list(all_keys)

def open_pickle_mmap(filename, keys=[]):
    with open(filename, 'rb') as f:
        # Memory map the file
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        full_dict = pickle.load(mm)
        return_dict = full_dict

        if len(keys) > 0:
            #partial_dict = {k: full_dict[k] for k in keys if k in full_dict}
            partial_dict = {}
            for dict_key in full_dict:
                for key in keys:
                    if key in dict_key:
                        partial_dict[dict_key] = full_dict[dict_key]

            return_dict = partial_dict

        run_id = 0
        NVal = len(partial_dict["config_name"])
        partial_dict["run_id"] = []
        partial_dict["run_filename"] = []
        for col_id in range(NVal):
            partial_dict["run_id"].append(col_id)
            partial_dict["run_filename"].append(filename)

            # Debug
            basename = os.path.basename(filename)
            if basename == "Simple.pkl":
                if col_id == 988:
                    x = 0

        mm.close()
        return return_dict

def plot_comparison(list_of_dict_list_w_kwarg):



    pass

def plot_pareto(list_of_dict_list_w_kwarg, final_sweep_labels, config_list=[]):

    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]

    pareto_list_w_kwarg = []

    i = 0
    for result_dict_list_w_kwarg in list_of_dict_list_w_kwarg:

        result_dict_list = []
        for result_dict, kwarg in result_dict_list_w_kwarg:

            if (len(config_list) > 0 and (result_dict['config_name'][0] in config_list) == False):
                continue
            result_dict_list.append(result_dict)

        pareto_dict = design_tools.get_min_Y_pareto_multiple(result_dict_list, PC_ETA_label[0], COST_PER_kW_NET_label[0], 50)
        kwarg_local = {'label':final_sweep_labels[i], 'marker':'.'}
        if 'c' in result_dict_list_w_kwarg[0][1]:
            kwarg_local['c'] = result_dict_list_w_kwarg[0][1]['c']
        pareto_list_w_kwarg.append([pareto_dict, kwarg_local])
        i += 1


    design_tools.plot_scatter_pts(pareto_list_w_kwarg,
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, legend_loc='upper right',show_line=True,
                                  disk_load=True, title="All config pareto")   

    design_tools.plot_scatter_pts(pareto_list_w_kwarg,
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, legend_loc='upper right',show_line=True,
                                  disk_load=True, title="All config pareto", is_norm=True)    

def plot_sco2_pareto(dict_list_w_kwarg, config_list, X_info, Y_info):
    
    pareto_list_w_kwarg = []
    local_dict_list_w_kwarg = []

    # First plot full sweep (to get markers, colors)
    i = 0
    for result_dict, kwarg in dict_list_w_kwarg:

        # Remove Preset Color and Marker
        kwarg_local = copy.deepcopy(kwarg)
        kwarg_local.pop('c', None)
        kwarg_local.pop('marker', None)

        local_dict_list_w_kwarg.append([result_dict, kwarg_local])
        i += 1

    _, new_kwarg_list = design_tools.plot_scatter_pts(
        local_dict_list_w_kwarg
        , 
        X_info, Y_info, show_legend=True, legend_loc="outside right")
    plt.tight_layout()

    # Now plot pareto with correct colors and markers
    i = 0
    for result_dict, kwarg in dict_list_w_kwarg:

        config_name = result_dict['config_name'][0]
        if config_name in config_list:
            #pareto_dict = design_tools.get_pareto_dict(result_dict, X_info[0], Y_info[0], True, False)
            pareto_dict = design_tools.get_min_Y_pareto_dict(result_dict, X_info[0], Y_info[0], 50)
            pareto_kwarg = new_kwarg_list[i]

            pareto_list_w_kwarg.append([pareto_dict, pareto_kwarg])

        i += 1   

    design_tools.plot_scatter_pts(
                pareto_list_w_kwarg
                , 
                X_info, Y_info, show_legend=True)
    plt.tight_layout()
    
def plot_sco2_vars(dict_list_w_kwarg, sweep_label=''):

    sco2_design_vars = sco2_varnames.get_sco2_design_vars_info_list()
    sco2_design_vars = [
        ["mc_cooler_q_dot", "MW", "MC Cooler"],
        ["pc_cooler_q_dot", "MW", "PC Cooler"]
    ]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]

    # Remove preset color and marker from kwargs
    new_dict_list_w_kwarg = []
    for result_dict, kwarg in dict_list_w_kwarg:
        kwarg_local = copy.deepcopy(kwarg)
        kwarg_local.pop('c', None)
        kwarg_local.pop('marker', None)
        new_dict_list_w_kwarg.append([result_dict, kwarg_local])

    # Loop through vars, making plot for each design variable
    for var_info in sco2_design_vars:
        title = var_info[2] + ' (' + sweep_label +')'
        design_tools.plot_scatter_pts(new_dict_list_w_kwarg,
            var_info, COST_PER_kW_NET_label, 
            show_legend=True, legend_loc='upper right',show_line=False,
            disk_load=True, title=title, is_norm=False)



def plot_all(list_of_dict_list_w_kwarg, final_sweep_labels, Y_info = None):
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]

    if Y_info == None:
        Y_info = COST_PER_kW_NET_label

    sweep_dict_list_w_kwarg = []

    # Loop through every sweep
    i = 0
    for result_dict_list_w_kwarg in list_of_dict_list_w_kwarg:

        # Make sweep dict
        sweep_dict = {}
        keys = get_all_keys([item[0] for item in result_dict_list_w_kwarg]) # Get all keys
        for key in keys:
            sweep_dict[key] = []

        # Loop through every config data in sweep data
        
        for result_dict, kwarg in result_dict_list_w_kwarg:

            # Copy data to sweep dict
            NVal = len(result_dict["config_name"])
            for key in sweep_dict:
                if key in result_dict:
                    sweep_dict[key].extend(result_dict[key])
                else:
                    sweep_dict[key].extend(NVal * [''])

        local_kwarg = {'label':final_sweep_labels[i], 'marker':'.'}
        if 'c' in result_dict_list_w_kwarg[0][1]:
            local_kwarg['c'] = result_dict_list_w_kwarg[0][1]['c']

        sweep_dict_list_w_kwarg.append([sweep_dict, local_kwarg])

        i += 1

    design_tools.plot_scatter_pts(sweep_dict_list_w_kwarg,
        PC_ETA_label, Y_info, 
        show_legend=True, legend_loc='upper right',show_line=False,
        disk_load=True, title="All config data", is_norm=False) 

def plot_error(list_of_dict_list_w_kwarg, final_sweep_labels, X_info, Y_info):
    sweep_dict_list_w_kwarg = []

    # Loop through every sweep
    i = 0
    for result_dict_list_w_kwarg in list_of_dict_list_w_kwarg:

        # Change color of series
        local_result_dict_list_w_kwarg = []
        j = 0
        for result_dict, kwarg in result_dict_list_w_kwarg:
            local_kwarg = copy.deepcopy(kwarg)
            local_kwarg['c'] = sco2_filenames.color_list[j]

            local_result_dict_list_w_kwarg.append([result_dict, local_kwarg])
            j += 1

        design_tools.plot_scatter_pts(local_result_dict_list_w_kwarg,
            X_info, Y_info, 
            show_legend=True, legend_loc='upper right',show_line=False,
            disk_load=True, title=final_sweep_labels[i], is_norm=False) 
        
        i += 1

    


def plot_barcharts(best_dict_list_w_kwarg, config_list):
    
    # Plot cost breakdown
    dict_index_duo_list = []
    for config_name in config_list:
        for best_dict_kwarg in best_dict_list_w_kwarg:
            best_dict = best_dict_kwarg[0]
            config_name_local = best_dict['config_name'][0]
            if config_name == config_name_local:
                dict_index_duo_list.append([best_dict, 0])
                break
    design_tools.plot_costs_barchart(dict_index_duo_list, type='sco2', plot_title="Cycle Cost Comparison", fontsize=fontsize_global, figsize=figsize_global)
    design_tools.plot_costs_barchart(dict_index_duo_list, type='system', plot_title="System Cost Comparison", fontsize=fontsize_global, figsize=figsize_global)

def plot_pareto_spec_config(list_of_dict_list_w_kwarg, final_sweep_labels, config_list, Y_label=[]):
    
    # Define X and Y Labels
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]

    if Y_label == "recup_over_cycle":
        recup_var = "recup_total_cost_equipment"
        cycle_var = "cycle_cost"
        recup_over_cycle = "recup_over_cycle"

        for result_dict_list_w_kwarg in list_of_dict_list_w_kwarg:
            for result_dict, kwarg in result_dict_list_w_kwarg:
                NVal = len(result_dict[recup_var])
                result_dict[recup_over_cycle] = []
                for i in range(NVal):
                    recup = result_dict[recup_var][i]
                    cycle = result_dict[cycle_var][i]
                    r_frac = recup/cycle
                    result_dict[recup_over_cycle].append(r_frac)

        Y_label = [recup_over_cycle, "", "Recup Cost over Cycle"]

    if len(Y_label) == 0:
        Y_label = COST_PER_kW_NET_label

    for config_name in config_list:

        # Get cycle config from each data set
        config_spec_result_dict_list_w_kwarg = []
        for result_dict_list_w_kwarg in list_of_dict_list_w_kwarg:
            for result_dict, kwarg in result_dict_list_w_kwarg:
                local_config_name = result_dict['config_name'][0]
                if local_config_name == config_name:
                    config_spec_result_dict_list_w_kwarg.append([result_dict, kwarg])
                    break
        if len(config_spec_result_dict_list_w_kwarg) != len(final_sweep_labels):
            print("mismatch")
            return
        
        # $/kWe vs T HTF   
        size_factor = 6
        fig_width = 1.35 * size_factor
        fig_height = 1 * size_factor
        fig_1, [ax1, ax2] = plt.subplots(1, 2)
        fig_1.set_size_inches(1.5 * fig_width, fig_height)
        ax1.xaxis.grid(True)
        ax1.yaxis.grid(True)
        ax1.minorticks_on()
        ax1.grid(which='minor', linestyle=':', linewidth='0.5') 
        ax1.set_axisbelow(True)

        ax2.xaxis.grid(True)
        ax2.yaxis.grid(True)
        ax2.minorticks_on()
        ax2.grid(which='minor', linestyle=':', linewidth='0.5') 
        ax2.set_axisbelow(True)


        # Get Pareto Front for each result dict        
        pareto_dict_w_kwarg_list = []
        i = 0
        for result_dict, kwarg in config_spec_result_dict_list_w_kwarg:
            pareto_dict = design_tools.get_min_Y_pareto_dict(result_dict, PC_ETA_label[0], COST_PER_kW_NET_label[0], 100)
            kwarg_local = {'label':final_sweep_labels[i], 'marker':'.'}
            if 'c' in kwarg:
                kwarg_local['c'] = kwarg['c']

            pareto_dict_w_kwarg_list.append([pareto_dict, kwarg_local])
            i += 1
        
        design_tools.plot_scatter_pts(pareto_dict_w_kwarg_list,
                                  PC_ETA_label, Y_label, 
                                  show_legend=True, legend_loc='upper right',show_line=True,
                                  title=config_name, disk_load=True, is_norm=False, ax=ax1)   

        design_tools.plot_scatter_pts(pareto_dict_w_kwarg_list,
                                  PC_ETA_label, Y_label, 
                                  show_legend=True, legend_loc='upper right',show_line=True,
                                  title=config_name + " Normalized", disk_load=True, is_norm=True, ax=ax2) 

        fig_1.canvas.manager.set_window_title("Cycle: " + config_name)
        plt.tight_layout()   
        
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

def get_all_enum():
    enum_base = [BASE.BASELINE_OPT, BASE.ETA8085, BASE.ETA8090, 
                BASE.COLDAPP40, BASE.COLDAPP60, 
                BASE.HELIO127,
                BASE.RECUP50, BASE.RECUP150,
                BASE.TES50, BASE.TES150,
                BASE.PHXBUCKLO, BASE.PHXBUCKHI]
    
    enum_TIT625 = [TIT625.BASELINE, TIT625.ETA8085, TIT625.ETA8090, 
                TIT625.COLDAPP40, TIT625.COLDAPP60, 
                TIT625.HELIO127,
                TIT625.RECUP50, TIT625.RECUP150,
                TIT625.TES50, TIT625.TES150,
                TIT625.PHXBUCKLO, TIT625.PHXBUCKHI]

    enum_TIT550 = [TIT550.BASELINE, TIT550.ETA8085, TIT550.ETA8090, 
                TIT550.COLDAPP40, TIT550.COLDAPP60, 
                TIT550.HELIO127,
                TIT550.RECUP50, TIT550.RECUP150,
                TIT550.TES50, TIT550.TES150,
                TIT550.PHXBUCKLO, TIT550.PHXBUCKHI]
    
    enum_all = enum_base
    enum_all.extend(enum_TIT625)
    enum_all.extend(enum_TIT550)
    

    return enum_all
    
    

def test_compare():

    presplit = True
    enum_list = [BASE.BASELINE, BASE.ETA8085, BASE.ETA8090, 
                BASE.COLDAPP40, BASE.COLDAPP40, 
                BASE.TIT550, BASE.TIT625,
                BASE.HELIO127,
                BASE.RECUP50, BASE.RECUP150, BASE.RECUP1000,
                BASE.TES50, BASE.TES150, BASE.TES1000,
                BASE.PHXBUCKLO, BASE.PHXBUCKHI,
                BASE.PHXBUCKHI10x,
                BASE.HELIO127_PHXBUCKHI,
                BASE.HELIO10x, BASE.HELIO100x]

    enum_list = [BASE.BASELINE, BASE.ETA8085, BASE.ETA8090, 
                BASE.COLDAPP40, BASE.COLDAPP40, 
                BASE.TIT550, BASE.TIT625,
                BASE.HELIO127,
                BASE.RECUP50, BASE.RECUP150,
                BASE.TES50, BASE.TES150,
                BASE.PHXBUCKLO, BASE.PHXBUCKHI]

    enum_list = [BASE.BASELINE]

    

    enum_list = [TIT550.BASELINE, TIT550.ETA8085]

    enum_list = [TIT550.BASELINE, TIT550.ETA8085, TIT550.ETA8090,
                 TIT550.RECUP50, TIT550.RECUP150,
                TIT550.TES50, TIT550.TES150,
                TIT550.PHXBUCKLO, TIT550.PHXBUCKHI]

    enum_list = [BASE.BASELINE, TIT550.BASELINE, TIT625.BASELINE]

    enum_list = [TIT625.BASELINE, TIT625.ETA8085, TIT625.ETA8090]
    #enum_list = [BASE.BASELINE, BASE.BASELINE_OPT]
    
    enum_list = [TIT550.BASELINE, TIT550.COLDAPP40, TIT550.COLDAPP60]

    enum_list = [TIT550.BASELINE, TIT550.ETA8085, TIT550.ETA8090,
                 TIT550.COLDAPP40, TIT550.COLDAPP60, 
                 TIT550.HELIO127, 
                 TIT550.PHXBUCKLO, TIT550.PHXBUCKHI,
                 TIT550.RECUP50, TIT550.RECUP150, TIT550.RECUP1000,
                 TIT550.TES50, TIT550.TES150, TIT550.TES1000]

    enum_list = [TIT625.BASELINE, TIT625.ETA8085, TIT625.ETA8090,
                 TIT625.COLDAPP40, TIT625.COLDAPP60, TIT625.HELIO127, 
                 TIT625.PHXBUCKLO, TIT625.PHXBUCKHI,
                 TIT625.RECUP50, TIT625.RECUP150, TIT625.RECUP1000,
                 TIT625.TES50, TIT625.TES150, TIT625.TES1000]
    #enum_list = [BASE.BASELINE, TIT625.BASELINE, TIT625.COLDAPP40, TIT625.COLDAPP60,
    #             TIT550.BASELINE, TIT550.COLDAPP40, TIT550.COLDAPP60]

    enum_list = [BASE.BASELINE_OPT, TIT550.BASELINE, TIT625.BASELINE]

    #enum_list = [BASE.PHXBUCKLO, BASE.PHXBUCKHI,
    #             TIT625.PHXBUCKLO, TIT625.PHXBUCKHI,
    #             TIT550.PHXBUCKLO, TIT550.PHXBUCKHI]
    #enum_list = [TIT625.RECUP150]
    enum_list = get_all_enum()

    enum_list = [BASE.BASELINE, BASE.ETA8085, BASE.ETA8090,
                 BASE.COLDAPP40, BASE.COLDAPP60,
                 BASE.TIT550, BASE.TIT625,
                 BASE.HELIO127,
                 BASE.RECUP50, BASE.RECUP150,
                 BASE.TES50, BASE.TES150,
                 BASE.PHXBUCKLO, BASE.PHXBUCKHI]

    #enum_list = [BASE.COLDAPP60]

    filenames_list_w_label = []
    for enum in enum_list:
        filenames_list_w_label.append(sco2_filenames.get_file_via_enum(enum, presplit))

    list_of_dict_list_w_kwargs = []
    list_of_best_dict_list_with_kwarg = []
    final_sweep_labels = []

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
                "q_dot_in_total", "mc_cooler_q_dot", "pc_cooler_q_dot"]

    output = data_utility.open_file_set_w_label(filenames_list_w_label, key_list)
    list_of_dict_list_w_kwargs = output[0]
    list_of_best_dict_list_with_kwarg = output[1]
    final_sweep_labels = output[2]

    # Set kwarg for best dict list
    

    print('Plotting...')

    show_config_list = ['Simple', 'Simple Split Flow Bypass', 'Simple Split Flow Bypass w/o LTR', 
                        'Recompression', 'Recompression w/o LTR', 'Recompression w/o HTR',
                        'HTR BP', 'HTR BP w/o LTR', 
                        'Partial', 'Partial w/o HTR', 'Partial w/o LTR', 'Partial Intercooling w/o HTR',
                        'Turbine Split Flow']

    COST_PER_kW_info = ["cost_per_kWe_net_ish", "$/kWe", "System Cost per Net Power"]
    PC_ETA_info = ["eta_thermal_calc", "", "PC Thermal Efficiency"]
    T_HTF_COLD_info = ["T_htf_cold_des", "C", "HTF Cold Temperature"]
    CYCLE_COST_info = ["cycle_cost", "M$", "Cycle Cost"]
    HELIO_COST_info = ["csp.pt.cost.heliostats", "$", "Heliostat Cost"]
    TES_COST_info = ["csp.pt.cost.storage", "$", "Storage Cost"]
    BP_FRAC_info = ["bypass_frac", "", "Bypass Frac Input"]
    Q_ERROR_info = ["q_error", "MWt", "Q_error"]

    # Save sweep table to file
    if False:
        show_config_table_list = show_config_list
        var_info_list = [COST_PER_kW_info, PC_ETA_info, T_HTF_COLD_info, 
                         *sco2_varnames.get_sco2_cost_info_list(), *sco2_varnames.get_csp_cost_info_list()]

        for best_dict_list_with_kwarg in list_of_best_dict_list_with_kwarg:
            #table_data = design_tools.show_sweep_table(best_dict_list_with_kwarg, show_config_table_list, var_info_list)
            #write_array_to_file(table_data)
            design_tools.show_sweep_table(best_dict_list_with_kwarg, show_config_table_list, var_info_list, fontsize=7)
            x = 0

    # sco2 paretos
    if False:
        config_list = ["Turbine Split Flow"]
        for dict_list_w_kwarg in list_of_dict_list_w_kwargs:
            plot_sco2_pareto(dict_list_w_kwarg, config_list, PC_ETA_info, T_HTF_COLD_info)
            plot_sco2_pareto(dict_list_w_kwarg, config_list, PC_ETA_info, COST_PER_kW_info)

    # sco2 design variables
    if False:
        for dict_list_w_kwarg, sweep_label in zip(list_of_dict_list_w_kwargs, final_sweep_labels):
            plot_sco2_vars(dict_list_w_kwarg, sweep_label)

    # Cost Bar Plots
    if False:
        config_list_cost_plot = ["Simple", "Simple Split Flow Bypass w/o LTR",
                                "Recompression", "HTR BP", "Partial w/o HTR",
                                "Turbine Split Flow"]
        for best_dict_list_w_kwarg in list_of_best_dict_list_with_kwarg:
            plot_barcharts(best_dict_list_w_kwarg, config_list_cost_plot)

    # Pareto by config
    if False:
        Y_label = ["recup_total_cost_equipment", "M$", "Recup Cost"]
        Y_label = "recup_over_cycle"
        Y_label = ["cycle_cost", "M$", "Cycle Cost"]
        Y_label = ["UA_recup_tot_des", "MW/K", "Recup Total Conductance"]
        plot_pareto_spec_config(list_of_dict_list_w_kwargs, final_sweep_labels, show_config_list, Y_label=COST_PER_kW_info)
    
    # Plot Error
    if True:
        plot_error(list_of_dict_list_w_kwargs, final_sweep_labels, COST_PER_kW_info, Q_ERROR_info)

    # Sweep Comparison
    if False:
        plot_pareto(list_of_dict_list_w_kwargs, final_sweep_labels, show_config_list)
        plot_all(list_of_dict_list_w_kwargs, final_sweep_labels)
        

        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, COST_PER_kW_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, COST_PER_kW_info, disk_load=True, is_norm=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, PC_ETA_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, T_HTF_COLD_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, CYCLE_COST_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, HELIO_COST_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, TES_COST_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, BP_FRAC_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)

    

        
    plt.show(block = True)


if __name__ == "__main__":
    test_compare()
