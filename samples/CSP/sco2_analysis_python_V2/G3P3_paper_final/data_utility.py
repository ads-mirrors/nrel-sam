import os
import sys
import psutil
from multiprocessing import Manager
import concurrent.futures
import mmap
import psutil
import pickle
import copy
import gc

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

import sco2_cycle_ssc as sco2_solve
import design_point_tools as design_tools
import sco2_plot_g3p3_baseline_FINAL

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

        NVal = len(return_dict["config_name"])
        return_dict["run_id"] = []
        return_dict["run_filename"] = []
        for col_id in range(NVal):
            return_dict["run_id"].append(col_id)
            return_dict["run_filename"].append(filename)

        mm.close()
        return return_dict

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

def open_file_set_w_label(filenames_list_w_label, key_list=[]):

    list_of_dict_list_w_kwargs = []
    list_of_best_dict_list_with_kwarg = []
    final_sweep_labels = []

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

    return list_of_dict_list_w_kwargs, list_of_best_dict_list_with_kwarg, final_sweep_labels