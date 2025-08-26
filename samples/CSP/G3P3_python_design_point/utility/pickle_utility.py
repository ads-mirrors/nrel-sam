import sys
import os
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pickle
import re

newPath = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')
    sys.path.append(newPath)
    examplePath = os.path.join(os.path.dirname(newPath), 'example')
    sys.path.append(examplePath)

import sco2_cycle_ssc as sco2_solve
import design_point_tools as design_tools

# Utility Functions

def remove_cases(result_dict, key, val_min, supress_print=True):
    # remove all cases with key value below val
    remove_id_list = []
    id = 0
    if (key in result_dict) == False:
        return {}

    for val in result_dict[key]:
        if((val == '') or val <= val_min):
            remove_id_list.append(id)
        id += 1

    total_keys = len(list(result_dict.keys()))
    i = 0
    for key in result_dict:
        if(supress_print==False):
            percent = (i / total_keys) * 100
            print("Removing " + str(round(percent, 2)) + "% complete")
        result_dict[key] = [i for j, i in enumerate(result_dict[key]) if j not in remove_id_list]
        i += 1

    return result_dict

def pickle_slim_result_dict(filename_list, key_to_remove, min_val=0):
    # remove all results below a certain value
    #COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    #key_to_remove = "T_htf_cold_des"
    ##key_to_remove = COST_PER_kW_NET_label[0]
    #min_val = 0
#
    ## Open files
    #window = tk.Tk()
    #filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Select csv(s) to slim and pickle")
    #filename_list = []
    #for filename in filename_tuple:
    #    filename_list.append(filename)

    save_folder_name = "slim_pickled"
    
    for filename in filename_list:

        file_basename = os.path.basename(filename)
        file_basename_no_ext, py_ext = os.path.splitext(file_basename)
        folder_name = os.path.dirname(filename)

        filename_pickle_save = folder_name + "//" + save_folder_name + "//" + file_basename_no_ext + ".pkl"

        sim_collection = sco2_solve.C_sco2_sim_result_collection()
        sim_collection.open_csv(filename)

        result_dict_slim = remove_cases(sim_collection.old_result_dict, key_to_remove, min_val, supress_print=False)
        if(result_dict_slim == {}):
            print("Empty dictionary " + filename)
            continue

        save_folder_path = os.path.dirname(filename_pickle_save)
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

        with open(filename_pickle_save, "wb") as f:
            pickle.dump(result_dict_slim, f)

        x = 0

def sanitize_filename(filename):
    pattern = r'[^\w\-]'

    # Replace invalid characters with an underscore
    sanitized_filename = re.sub(pattern, '_', filename)

    return sanitized_filename


# Main Functions

def pickle_result_dict():
    window = tk.Tk()
    filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Select csv(s) to pickle")
    filename_list = []
    for filename in filename_tuple:
        filename_list.append(filename)

    save_folder_name = "pickled"

    for filename in filename_list:

        file_basename = os.path.basename(filename)
        file_basename_no_ext, py_ext = os.path.splitext(file_basename)
        folder_name = os.path.dirname(filename)

        filename_pickle_save = folder_name + "//" + save_folder_name + "//" + file_basename_no_ext + ".pkl"

        sim_collection = sco2_solve.C_sco2_sim_result_collection()
        sim_collection.open_csv(filename)

        save_folder_path = os.path.dirname(filename_pickle_save)
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

        with open(filename_pickle_save, "wb") as f:
            pickle.dump(sim_collection.old_result_dict, f)

        x = 0

def open_pickle():
    filename_tuple = askopenfilenames(filetypes =[('Pickles', '*.pkl')], title="Select pkl to open")
    filename_list = []
    for filename in filename_tuple:
        filename_list.append(filename)

    for filename in filename_list:

        with open(filename, 'rb') as f:
            my_dict = pickle.load(f)

        x = 0

def open_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def combine_pickles():
    filename_tuple = askopenfilenames(filetypes =[('Pickles', '*.pkl')], title="Select pkls to combine")
    filename_list = []

    # Get result dict from files
    result_dict_list = []
    for filename in filename_tuple:
        with open(filename, 'rb') as f:
            my_dict = pickle.load(f)
            result_dict_list.append(my_dict)

    if(len(result_dict_list) == 0):
        print("nothing to do")
        return

    # Get save name
    file_basename = os.path.basename(filename_tuple[0])
    file_basename_no_ext, py_ext = os.path.splitext(file_basename)
    folder_name = os.path.dirname(filename_tuple[0])

    save_folder_name = "pickled_merged"
    #filename_pickle_save = folder_name + "//" + save_folder_name + "//" + file_basename_no_ext + ".pkl"
    filename_pickle_save = os.path.join(folder_name, save_folder_name, file_basename_no_ext + ".pkl")

    save_folder_path = os.path.dirname(filename_pickle_save)
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    # Check dictionaries have the same keys
    mismatch_keys = []

    master_keys = list(result_dict_list[0].keys())
    for result_dict in result_dict_list:
        master_keys = list(set(master_keys + list(result_dict.keys())))
    for result_dict in result_dict_list:
        for key in master_keys:
            if((key in result_dict) == False):
                print("mismatched dict keys: " + key)
                mismatch_keys.append(key)
                



    # Calculate correct number of final runs
    Nruns = 0
    test_key = master_keys[0]
    for result_dict in result_dict_list:
        Nruns += len(result_dict[test_key])

    # Combine result dictionaries
    final_result_dict = result_dict_list[0]
    for i in range(1,len(result_dict_list)):
        for key in final_result_dict:
            len_1 = len(final_result_dict[key])
            len_2 = len(result_dict_list[i][key])
            len_new = len_1 + len_2

            final_result_dict[key].extend(result_dict_list[i][key])

            if(len_new != len(final_result_dict[key])):
                asdf = 0

    # Save pickle
    with open(filename_pickle_save, "wb") as f:
        pickle.dump(final_result_dict, f)

def pickle_slim_sco2():
    # remove all results below a certain value
    key_to_remove = "T_htf_cold_des"
    min_val = 0

    # Open files
    window = tk.Tk()
    filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Select sco2 csv(s) to slim and pickle")
    filename_list = []
    for filename in filename_tuple:
        filename_list.append(filename)
    pickle_slim_result_dict(filename_list, key_to_remove, min_val)

def pickle_slim_g3p3():
    # remove all results below a certain value
    COST_PER_kW_NET_label = ["cost_per_kWe_net_ish", "$/kWe", "Cost per kWe Net"]
    key_to_remove = COST_PER_kW_NET_label[0]
    min_val = 0

    # Open files
    window = tk.Tk()
    filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Select g3p3 csv(s) to slim and pickle")
    filename_list = []
    for filename in filename_tuple:
        filename_list.append(filename)
    pickle_slim_result_dict(filename_list, key_to_remove, min_val)

def split_mega_g3p3_sco2_by_config():
    filename_tuple = askopenfilenames(filetypes =[('Pickles', '*.pkl')], title="Select pkl to open")
    filename_list = []
    for filename in filename_tuple:
        filename_list.append(filename)

    # Open Pickles
    print('Opening pickles...')
    input_dict_list = []
    for filename in filename_list:
        input_dict_list.append(open_pickle(filename))

    # Rename config names
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

            if (cycle_config == 3) and (bypass_frac == ''):
                x = 0

            result_dict['config_name'][i] = sco2_solve.get_config_name(cycle_config, recomp_frac, bypass_frac, is_LTR, is_HTR)

    # Split by config name
    print("Splitting dictionaries by config_name...")
    result_dict_list = design_tools.split_by_config_name(input_dict_list)

    # Make save folder (if it doesn't exist)
    parent_folder = os.path.dirname(filename_list[0])
    save_folder_path = os.path.join(parent_folder, 'split_config')
    if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

    # Save files
    for result_dict in result_dict_list:
        config_name = result_dict['config_name'][0]
        config_name_sanitized = sanitize_filename(config_name)

        save_filename = save_folder_path + '//' + config_name_sanitized + '.pkl'

        with open(save_filename, "wb") as f:
            pickle.dump(result_dict, f)

        x = 0


        


if __name__ == "__main__":
    #display_eff()
    #plot_sweep()
    #plot_via_filedlg()
    #pickle_result_dict()
    #combine_and_pickle()
    #combine_pickles()
    #pickle_slim_sco2()
    #pickle_slim_g3p3()
    #open_pickle()
    split_mega_g3p3_sco2_by_config()