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
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

import sco2_cycle_ssc as sco2_solve
import design_point_examples as design_pt
import design_point_tools as design_tools
import sco2_varnames
import sco2_plot_sandbox as plot_sandbox
from sco2_plot_g3p3_baseline_FINAL import open_pickle
import sco2_plot_g3p3_baseline_FINAL
import concurrent.futures
from tkinter.filedialog import asksaveasfilename

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

        mm.close()
        return return_dict

def plot_comparison(list_of_dict_list_w_kwarg):



    pass

def plot_pareto(list_of_dict_list_w_kwarg, final_sweep_labels):

    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]

    pareto_list_w_kwarg = []

    i = 0
    for result_dict_list_w_kwarg in list_of_dict_list_w_kwarg:

        result_dict_list = []
        for result_dict, kwarg in result_dict_list_w_kwarg:
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
        X_info, Y_info, show_legend=True)


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
    
def plot_sco2_vars(dict_list_w_kwarg, sweep_label=''):

    sco2_design_vars = sco2_varnames.get_sco2_design_vars_info_list()
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



def plot_all(list_of_dict_list_w_kwarg, final_sweep_labels):
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]

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
        PC_ETA_label, COST_PER_kW_NET_label, 
        show_legend=True, legend_loc='upper right',show_line=False,
        disk_load=True, title="All config data", is_norm=False) 

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

def plot_pareto_spec_config(list_of_dict_list_w_kwarg, final_sweep_labels, config_list):
    
    # Define X and Y Labels
    PC_ETA_label = ["eta_thermal_calc", "", "PC Efficiency"]
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    UA_TOTAL_label = ["recup_total_UA_calculated", "MW/K", "Total UA Calculated"]

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
                                  PC_ETA_label, COST_PER_kW_NET_label, 
                                  show_legend=True, legend_loc='upper right',show_line=True,
                                  title=config_name, disk_load=True, is_norm=False, ax=ax1)   

        design_tools.plot_scatter_pts(pareto_dict_w_kwarg_list,
                                  PC_ETA_label, COST_PER_kW_NET_label, 
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

def process_sweep_fileset(filenames, sweep_label):
    # Open files, split by config name
    # Return dict list with kwarg, best cases?

    # Open Pickles
    print('Opening pickles...')
    input_dict_list = []
    for filename in filenames:
        input_dict_list.append(open_pickle(filename))
    
    # Rename config names
    print('Naming cycles...')
    is_new_config_names = False
    presplit = True
    for result_dict in input_dict_list:
        NVal = len(result_dict[list(result_dict.keys())[0]])
        if('config_name' in result_dict == False):
            result_dict['config_name'] = []
            for i in range(NVal):
                result_dict['config_name'].append('')
        
        prev_config_name = result_dict['config_name'][0]

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

            new_config_name = sco2_solve.get_config_name(cycle_config, recomp_frac, bypass_frac, is_LTR, is_HTR)

            if new_config_name != result_dict['config_name'][i]:
                result_dict['config_name'][i] = new_config_name
                is_new_config_names = True

            if result_dict['config_name'][i] != prev_config_name:
                presplit = False

    # Check if 

    # Split by config name
    if presplit == True:
        print("Skipping dictionary splitting by config name...")
        result_dict_list = input_dict_list
    else:
        print("Splitting dictionaries by config_name...")
        result_dict_list = design_tools.split_by_config_name_optimized(input_dict_list)

        # Clear original dict (for memory)
        for input_dict in input_dict_list:
            input_dict.clear()

    # make dict_list_with_kwarg
    dict_list_with_kwargs = []
    marker_list = design_tools.get_marker_list()
    i = 0
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        dict_w_kwarg = [result_dict, {'label':config_name, 'marker':marker_list[i]}]
        dict_list_with_kwargs.append(dict_w_kwarg)
        i += 1

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



    return [dict_list_with_kwargs, best_dict_list_with_kwarg, sweep_label]

def process_sweep_fileset_optimized(filenames, sweep_label, color, result_queue, key_list):
    # Open files, split by config name
    # Return dict list with kwarg, best cases?

    # Open Pickles
    print('Opening pickles...')
    input_dict_list = []

    # Track memory before and after operations
    print(f"Memory before loading: {psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB")

    for filename in filenames:
        #input_dict_list.append(open_pickle(filename))
        input_dict_list.append(open_pickle_mmap(filename, key_list))

    # Rename config names
    print('Naming cycles...')
    is_new_config_names = False
    presplit = True
    for result_dict in input_dict_list:
        NVal = len(result_dict[list(result_dict.keys())[0]])
        if('config_name' in result_dict == False):
            result_dict['config_name'] = []
            for i in range(NVal):
                result_dict['config_name'].append('')
        
        prev_config_name = result_dict['config_name'][0]

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

            if bypass_frac == '':
                bypass_frac = 0

            new_config_name = sco2_solve.get_config_name(cycle_config, recomp_frac, bypass_frac, is_LTR, is_HTR)

            if new_config_name != result_dict['config_name'][i]:
                result_dict['config_name'][i] = new_config_name
                is_new_config_names = True

            if result_dict['config_name'][i] != prev_config_name:
                presplit = False

    # Split by config name
    if presplit == True:
        print("Skipping dictionary splitting by config name...")
        result_dict_list = input_dict_list
    else:
        print("Splitting dictionaries by config_name...")
        result_dict_list = design_tools.split_by_config_name_optimized(input_dict_list)

        # Clear original dict (for memory)
        for input_dict in input_dict_list:
            input_dict.clear()


    # Make dict_list_with_kwarg
    dict_list_with_kwargs = []
    marker_list = design_tools.get_marker_list()
    for i, result_dict in enumerate(result_dict_list):
        config_name = result_dict['config_name'][0]
        dict_w_kwarg = [result_dict, {'label': config_name, 
                                      'marker': marker_list[i],
                                      'c':color}]
        dict_list_with_kwargs.append(dict_w_kwarg)

    # Get Best Cases
    print("Finding best $/kWe cases...")
    best_dict_list_with_kwarg = []
    for dict_kwarg in dict_list_with_kwargs:
        diction = dict_kwarg[0]
        kwarg = copy.deepcopy(dict_kwarg[1])
        kwarg.setdefault('marker', 'X')
        kwarg['label'] = 'Best ' + kwarg['label']
        kwarg['c'] = color
        best_dict = sco2_plot_g3p3_baseline_FINAL.get_best_dict_optimized(diction, "cost_per_kWe_net_ish", False)
        best_dict_list_with_kwarg.append([best_dict, kwarg])

     # Put the result in the queue
    result_queue.put([dict_list_with_kwargs, best_dict_list_with_kwarg, sweep_label])
    #result_queue.put([result_dict_list])

    # Clear memory
    del input_dict_list
    del result_dict_list
    input_dict_list = None
    gc.collect()

    print(f"Memory after cleanup: {psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB")
    #del dict_list_with_kwargs
    #del best_dict_list_with_kwarg
    #
    
    return


def test_compare():

    presplit = True

    filenames_baseline_w_label = sco2_filenames.get_filenames_baseline(split=presplit)
    filenames_eta8085_w_label = sco2_filenames.get_filenames_eta8085(split=presplit)
    filenames_eta8090_w_label = sco2_filenames.get_filenames_eta8090(split=presplit)
    filenames_coldapproach40_w_label = sco2_filenames.get_filenames_coldapproach40(split=presplit)
    filenames_coldapproach60_w_label = sco2_filenames.get_filenames_coldapproach60(split=presplit)
    filenames_TIT550_w_label = sco2_filenames.get_filenames_TIT550(split=presplit)
    filenames_TIT625_w_label = sco2_filenames.get_filenames_TIT625(split=presplit)
    filenames_heliocost_w_label = sco2_filenames.get_filenames_heliocost(split=presplit)
    filenames_recup50_w_label = sco2_filenames.get_filenames_recup50(split=presplit)
    filenames_recup150_w_label = sco2_filenames.get_filenames_recup150(split=presplit)
    filenames_recup1000_w_label = sco2_filenames.get_filenames_recup1000(split=presplit)
    filenames_tes50_w_label = sco2_filenames.get_filenames_tes50(split=presplit)
    filenames_tes150_w_label = sco2_filenames.get_filenames_tes150(split=presplit)
    filenames_tes1000_w_label = sco2_filenames.get_filenames_tes1000(split=presplit)
    filenames_phxbucklow_w_label = sco2_filenames.get_filenames_phxbucklow(split=presplit)
    filenames_phxbuckhigh_w_label = sco2_filenames.get_filenames_phxbuckhigh(split=presplit)
    filenames_phxbuckhigh10x_w_label = sco2_filenames.get_filenames_phxbuckhigh10x(split=presplit)
    filenames_helio_phxbuckhigh_w_label = sco2_filenames.get_filenames_helio_phxbuckhigh(split=presplit)
    filenames_helio10x_w_label = sco2_filenames.get_filenames_helio10x(split=presplit)
    filenames_helio100x_w_label = sco2_filenames.get_filenames_helio100x(split=presplit)

    filenames_list_w_label = [filenames_baseline_w_label, filenames_eta8085_w_label, filenames_eta8090_w_label, 
                              filenames_coldapproach40_w_label, filenames_coldapproach60_w_label, 
                              filenames_TIT550_w_label, filenames_TIT625_w_label,
                              filenames_heliocost_w_label,
                              filenames_recup50_w_label, filenames_recup150_w_label, filenames_recup1000_w_label,
                              filenames_tes50_w_label, filenames_tes150_w_label, filenames_tes1000_w_label,
                              filenames_phxbucklow_w_label, filenames_phxbuckhigh_w_label,
                              filenames_phxbuckhigh10x_w_label,
                              filenames_helio_phxbuckhigh_w_label,
                              filenames_helio10x_w_label, filenames_helio100x_w_label]
    
    filenames_list_w_label = [filenames_baseline_w_label, filenames_eta8085_w_label, filenames_eta8090_w_label, 
                              filenames_coldapproach40_w_label, filenames_coldapproach60_w_label, 
                              filenames_TIT550_w_label, filenames_TIT625_w_label,
                              filenames_heliocost_w_label,
                              filenames_recup50_w_label, filenames_recup150_w_label,
                              filenames_tes50_w_label, filenames_tes150_w_label,
                              filenames_phxbucklow_w_label, filenames_phxbuckhigh_w_label,
                              filenames_helio_phxbuckhigh_w_label]

    #filenames_list_w_label = [filenames_baseline_w_label, filenames_heliocost_w_label]

    

    #filenames_list_w_label = [filenames_baseline_w_label]

    #filenames_list_w_label = [filenames_TIT550_w_label]
#
    #filenames_list_w_label = [filenames_baseline_w_label,
    #                          filenames_recup50_w_label, filenames_recup150_w_label]
#
    #filenames_list_w_label = [filenames_baseline_w_label,
    #                          filenames_tes50_w_label, filenames_tes150_w_label]
#
    #filenames_list_w_label = [filenames_baseline_w_label,
    #                          filenames_helio10x_w_label, filenames_helio100x_w_label]
    #
    #filenames_list_w_label = [filenames_baseline_w_label,
    #                          filenames_eta8085_w_label, filenames_eta8090_w_label]
#
    #filenames_list_w_label = [filenames_baseline_w_label, 
    #                          filenames_TIT550_w_label, filenames_TIT625_w_label,]

    #filenames_list_w_label = [filenames_baseline_w_label, 
    #                          filenames_coldapproach40_w_label, filenames_coldapproach60_w_label,
    #                          filenames_TIT550_w_label, filenames_TIT625_w_label,]
#
    #filenames_list_w_label = [filenames_baseline_w_label, filenames_phxbucklow_w_label, filenames_phxbuckhigh_w_label]
#
    #filenames_list_w_label = [filenames_baseline_w_label, filenames_recup50_w_label, filenames_recup150_w_label, filenames_recup1000_w_label,
    #                          filenames_tes50_w_label, filenames_tes150_w_label, filenames_tes1000_w_label,
    #                          filenames_helio10x_w_label, filenames_helio100x_w_label]
#
    #filenames_list_w_label = [filenames_baseline_w_label, filenames_TIT550_w_label, filenames_TIT625_w_label]

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
                "is_turbine_split_ok", "is_bypass_ok"]

    #key_list = sco2_varnames.get_core_var_list()

    # Create a queue to hold the results
    with Manager() as manager:
        result_queue = manager.Queue()

        with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(process_sweep_fileset_optimized, filenames_w_label[0], filenames_w_label[1], filenames_w_label[2], 
                                       result_queue, key_list) 
                       for filenames_w_label in filenames_list_w_label]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Collect all results from the queue
        while not result_queue.empty():
            dict_list_w_kwargs, best_dict_list_with_kwarg, sweep_label = result_queue.get()
            list_of_dict_list_w_kwargs.append(dict_list_w_kwargs)
            list_of_best_dict_list_with_kwarg.append(best_dict_list_with_kwarg)
            final_sweep_labels.append(sweep_label)

        # Create mapping based on the original order in filenames_list_w_label
        label_order = [label for _, label, _ in filenames_list_w_label]
        expected_order = {label: idx for idx, label in enumerate(label_order)}

        # Sort the collected results to match the original order
        sorted_indices = []
        for i, label in enumerate(final_sweep_labels):
            sorted_indices.append(expected_order[label])

        # Apply sorting to all three lists
        list_of_dict_list_w_kwargs = [x for _, x in sorted(zip(sorted_indices, list_of_dict_list_w_kwargs))]
        list_of_best_dict_list_with_kwarg = [x for _, x in sorted(zip(sorted_indices, list_of_best_dict_list_with_kwarg))]
        final_sweep_labels = [x for _, x in sorted(zip(sorted_indices, final_sweep_labels))]

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
        config_list = ["Simple", "Recompression", "HTR BP", "Partial", "Turbine Split Flow"]
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
    if True:
        plot_pareto_spec_config(list_of_dict_list_w_kwargs, final_sweep_labels, show_config_list)
    
    # Sweep Comparison
    if True:
        plot_pareto(list_of_dict_list_w_kwargs, final_sweep_labels)
        plot_all(list_of_dict_list_w_kwargs, final_sweep_labels)

        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, COST_PER_kW_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, COST_PER_kW_info, disk_load=True, is_norm=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, PC_ETA_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, T_HTF_COLD_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, CYCLE_COST_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, HELIO_COST_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)
        design_tools.plot_sweep_cost_comparison(list_of_best_dict_list_with_kwarg, final_sweep_labels, show_config_list, TES_COST_info, disk_load=True, figsize=figsize_global, fontsize=fontsize_global)

    

        
    plt.show(block = True)


if __name__ == "__main__":
    test_compare()
