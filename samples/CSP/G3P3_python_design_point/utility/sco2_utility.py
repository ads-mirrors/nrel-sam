import sys
import os
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import pickle
from concurrent.futures import ProcessPoolExecutor, as_completed

newPath = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')
    sys.path.append(newPath)
    newPath_example = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/example')
    sys.path.append(newPath_example)
    sys.path.append(parentDir)

import sco2_cycle_ssc as sco2_solve
import design_point_tools as design_tools
import g3p3_design_sim as g3p3_design
import sco2_sim_result_collection as sco2_result_collection
import pickle_utility

def retrieve_single_sco2_case():
    # Load G3P3 csv with a SINGLE case
    # Retreive the associated sco2 case, and save it

    # Open files
    window = tk.Tk()
    filename = askopenfilename(filetypes =[('CSV Files', '*.txt')], title="Select g3p3 txt")
    dir = os.path.dirname(filename)

    result_dict = design_tools.get_dict_from_file_w_STRING(filename)

    #result_dict = sim_collection.old_result_dict
    is_list = isinstance(result_dict[list(result_dict.keys())[0]], list)
    if(is_list):
        if(len(result_dict[list(result_dict.keys())[0]]) > 1):
            print('g3p3 file must contain ONE case')
            return
    
    # Get sco2 filename
    file_key = 'sco2_filename'
    id_key = 'id'
    if((file_key in result_dict) == False):
        print("Missing key " + file_key)
    if((id_key in result_dict) == False):
        print("Missing key " + id_key)
    sco2_filename_short = result_dict[file_key][0]
    sco2_filename = os.path.join(dir, sco2_filename_short)
    sco2_id = result_dict[id_key][0]

    # Open sco2 file
    #sco2_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    #sco2_sim_collection.open_csv(sco2_filename)

    sco2_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
    sco2_sim_collection.open_csv(sco2_filename)

    list_of_dicts = g3p3_design.convert_result_dict_to_list(sco2_sim_collection.old_result_dict)

    # Get specific sco2 case
    sco2_result_dict = list_of_dicts[sco2_id]
    eta_sco2 = sco2_result_dict['eta_thermal_calc']
    eta_g3p3 = result_dict['design_eff'][0]

    if(eta_sco2 != eta_g3p3):
        print('eta do not match')
        return

    T_htf_sco2 = sco2_result_dict['T_htf_cold_des']
    T_htf_g3p3 = result_dict['T_htf_cold_des'][0]

    if(T_htf_sco2 != T_htf_g3p3):
        print('Temperatures do not match')
        return

    # Save sco2 case
    sco2_save_collection = sco2_result_collection.C_sco2_sim_result_collection()
    sco2_save_collection.add(sco2_result_dict)
    save_filename = asksaveasfilename(filetypes =[('CSV Files', '*.csv')], title="Select save sco2 csv")
    sco2_save_collection.write_to_csv(save_filename)

def compare_g3p3_sco2_case(g3p3_result_dict, g3p3_index, sco2_result_dict_single):

    compare_var_list = [['design_eff', 'eta_thermal_calc'],
                   ['T_htf_cold_des', 'T_htf_cold_des'],
                   ['cycle_cost', 'cycle_cost'],
                   ['q_dot_in_total', 'q_dot_in_total'],
                   ['cycle_config', 'cycle_config'],
                   ['is_recomp_ok', 'is_recomp_ok'],
                   ['is_PR_fixed', 'is_PR_fixed'],
                   ['is_bypass_ok', 'is_bypass_ok'],
                   ['is_IP_fixed', 'is_IP_fixed'],
                   ['is_turbine_split_ok', 'is_turbine_split_ok']]
    

    for compare_duo in compare_var_list:
        g3p3_val = g3p3_result_dict[compare_duo[0]][g3p3_index]
        sco2_val = sco2_result_dict_single[compare_duo[1]]

        diff = abs(g3p3_val - sco2_val)

        if(diff > 0.0001):
            print('case mismatch')
            return False
        
    return True

def process_single_filename(filename):
    """
    Process a single filename for parallel execution.
    Returns True if successful, False if there was an error.
    """
    try:
        dir = os.path.dirname(filename)
        file_basename = os.path.basename(filename)
        file_basename_no_ext, py_ext = os.path.splitext(file_basename)
        combined_foldername = 'mega'
        save_filename_basename_no_ext = 'mega_' + file_basename_no_ext
        save_filename_csv = os.path.join(dir, combined_foldername, save_filename_basename_no_ext + '.csv')

        sim_collection = sco2_solve.C_sco2_sim_result_collection()
        sim_collection.open_csv(filename)
        old_result_dict = sim_collection.old_result_dict

        # Check length of every variable
        NVal = len(old_result_dict[list(old_result_dict.keys())[0]])
        for key in old_result_dict:
            if(len(old_result_dict[key]) != NVal):
                print(f'length mismatch in {filename}')
                return False

        # Check dict has file_key keys
        file_key = 'sco2_filename'
        id_key = 'id'
        if((file_key in old_result_dict) == False):
                print(f"Missing key {file_key} in {filename}")
                return False
        if((id_key in old_result_dict) == False):
            print(f"Missing key {id_key} in {filename}")
            return False
        
        # Make list of sco2 cases
        sco2_filename_current = ""
        list_of_sco2_dicts = []

        # Declare mega combined result_dict
        mega_result_collection = sco2_result_collection.C_sco2_sim_result_collection()
        
        print(f"Processing {filename} with {NVal} cases...")

        # Loop through every case
        for g3p3_index in range(NVal):
            sco2_filename_short = old_result_dict[file_key][g3p3_index]
            sco2_filename = os.path.join(dir, sco2_filename_short)
            sco2_id = old_result_dict[id_key][g3p3_index]

            if(sco2_filename != sco2_filename_current):
                # Open sco2 file
                sco2_sim_collection = sco2_result_collection.C_sco2_sim_result_collection()
                sco2_sim_collection.open_csv(sco2_filename)
                list_of_sco2_dicts = g3p3_design.convert_result_dict_to_list(sco2_sim_collection.old_result_dict)
                sco2_filename_current = sco2_filename

            # Get specific sco2 case
            sco2_result_dict = list_of_sco2_dicts[sco2_id]

            # Validate sco2 case corresponds with g3p3
            case_match = compare_g3p3_sco2_case(old_result_dict, g3p3_index, sco2_result_dict)

            if(case_match == False):
                print(f"case mismatch in {filename} at index {g3p3_index}")
                return False
            
            # Add all sco2 keys to combined dict
            mega_local_dict = {}
            for sco2_key in sco2_result_dict:
                mega_local_dict[sco2_key] = sco2_result_dict[sco2_key]
            # Add all g3p3 keys to combined dict
            for g3p3_key in old_result_dict:
                mega_local_dict[g3p3_key] = old_result_dict[g3p3_key][g3p3_index]

            mega_result_collection.add(mega_local_dict)

            if(g3p3_index % 100 == 0):
                print(f"{filename}: {round((g3p3_index / NVal) * 100, 2)}% combined")

        # Save sco2 case
        save_folder_path = os.path.dirname(save_filename_csv)
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
        mega_result_collection.write_to_csv(save_filename_csv)
        
        print(f"Successfully processed {filename} -> {save_filename_csv}")
        return True
        
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return False

def make_mega_g3p3_sco2_csv():
    # Open files
    window = tk.Tk()
    filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Select g3p3 csv(s) to combine with sco2")
    filename_list = []
    for filename in filename_tuple:
        filename_list.append(filename)

    # Process files in parallel
    max_workers = min(len(filename_list), os.cpu_count(), 3)  # Limit workers to avoid overwhelming system
    print(f"Processing {len(filename_list)} files in parallel using {max_workers} workers...")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all filename processing tasks
        future_to_filename = {executor.submit(process_single_filename, filename): filename for filename in filename_list}
        
        # Process completed futures as they finish
        successful_files = 0
        failed_files = 0
        
        for future in as_completed(future_to_filename):
            filename = future_to_filename[future]
            try:
                result = future.result()
                if result:
                    successful_files += 1
                    print(f"✓ Completed: {os.path.basename(filename)}")
                else:
                    failed_files += 1
                    print(f"✗ Failed: {os.path.basename(filename)}")
                    
            except Exception as e:
                failed_files += 1
                print(f"✗ Exception processing {os.path.basename(filename)}: {str(e)}")
    
    print(f"\nProcessing complete: {successful_files} successful, {failed_files} failed")


if __name__ == "__main__":
    #retrieve_single_sco2_case()
    make_mega_g3p3_sco2_csv()