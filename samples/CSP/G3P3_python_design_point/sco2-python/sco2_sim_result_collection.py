# -*- coding: utf-8 -*-
"""
Created on 2024-9-25

@author: tbrown
"""

import csv
import enum
import time
import json
import copy
import math
import numpy as np
import pandas as pd

class C_sco2_sim_result_collection:

    class C_sco2_solve_dict_item:
        def __init__(self, name, type, i, j, value):
            self.name = name
            self.type = type
            self.i = i
            self.j = j
            self.value = value
        
    # 'Public' Methods

    def __init__(self):
        #self.solve_dict_list = []
        #self.flattened_solve_list = []
        self.num_cases = 0
        self.csv_array = []
        self.csv_col_offset = 4
        self.old_result_dict = {}
        self.success_id_vec = []
        self.failure_id_vec = []
        return

    def add(self, solve_dict, is_sco2=True, key_ref=''):
        
        if(('cmod_success' in solve_dict) == False):
            print("WARNING: solve_dict should have cmod_success key")

        # Add config_name
        if(is_sco2 and ('config_name' in solve_dict) == False):
            
            bypass_frac = ''
            if('bypass_frac' in solve_dict):
                bypass_frac = solve_dict["bypass_frac"]
            
            recomp_frac = ''
            if('recomp_frac' in solve_dict):
                recomp_frac = solve_dict["recomp_frac"]

            config_name = self.get_config_name(solve_dict["cycle_config"], recomp_frac, bypass_frac)
            solve_dict["config_name"] = config_name

        #self.solve_dict_list.append(solve_dict)
        self.num_cases = self.num_cases + 1

        self.add_run_to_csv_array(solve_dict, key_ref)

        return

    def write_to_csv(self, file_name):
        #self.csv_array = self.form_csv_array()

        if(len(self.csv_array) == 0):
            print("ERROR: no csv array to save")
            return

        f = open(file_name, "w")
        delimiter = ', '
        for row in self.csv_array:

            N_col = len(row)
            for col in range(N_col):

                val = row[col]
                f.write(str(val))
                
                if(col != N_col - 1):
                    f.write(delimiter)
        
            f.write('\n')
    
        f.close()

        return

    def open_csv(self, file_name):
        # Read in csv array
        self.csv_array = []
        f = open(file_name, "r")
        for row in f:
            items = row.split(',')
            for i in range(len(items)):
                items[i] = items[i].replace(' ', '')
            items[len(items)-1] = items[len(items)-1].replace('\n','')
            self.csv_array.append(items)
        f.close()

        # Fill in missing vals at end of rows
        NVal = len(self.csv_array[0]) - self.csv_col_offset
        for row in self.csv_array:
            N_missing_cols = NVal - (len(row) - self.csv_col_offset)
            for x in range(N_missing_cols):
                row.append('')

        self.num_cases = NVal

        # Add config name (if it doesn't exist)
        config_name_exists = False
        bypass_frac_row_id = 0
        recomp_frac_row_id = 0
        cycle_config_row_id = -1
        NRows = len(self.csv_array)
        for row_id in range(NRows):
            key = self.csv_array[row_id][0]
            if(key == 'config_name'):
                config_name_exists = True
                break
            elif(key == 'bypass_frac'):
                bypass_frac_row_id = row_id
            elif(key == 'recomp_frac'):
                recomp_frac_row_id = row_id
            elif(key == 'cycle_config'):
                cycle_config_row_id = row_id
        if(config_name_exists == False):
            self.csv_array.append(['config_name', 'single', '0', '0'])
            
            for run_id in range(NVal):
                bypass_frac = self.csv_array[bypass_frac_row_id][run_id + self.csv_col_offset]
                if(bypass_frac != ''):
                    bypass_frac = float(bypass_frac)
                
                recomp_frac = self.csv_array[recomp_frac_row_id][run_id + self.csv_col_offset]
                if(recomp_frac != ''):
                    recomp_frac = float(recomp_frac)

                cycle_config = int(float(self.csv_array[cycle_config_row_id][run_id + self.csv_col_offset]))
                config_name = self.get_config_name(cycle_config, recomp_frac, bypass_frac)
                self.csv_array[NRows].append(config_name)


        ## Form dicts for each run (by unflattening)
        #NRuns = len(self.csv_array[0]) - self.csv_col_offset
        #for run in range(NRuns):
        #    solve_dict = self.unflatten(self.csv_array, run)
        #    self.solve_dict_list.append(solve_dict)
        #    self.num_cases = self.num_cases + 1
        #    self.flattened_solve_list.append(self.flatten(solve_dict))

        # Form old result dict
        self.form_old_result_dict_from_csv_array()

        return True

    def get_list_of_dicts(self):
        list_of_dicts = []
        for i in range(self.num_cases):
            list_of_dicts.append(self.unflatten(self.csv_array, i))

        return list_of_dicts

    # 'Internal' Methods

    def add_run_to_csv_array(self, solve_dict, key_ref=''):

        flattened_solve_dict = self.flatten(solve_dict)

        NRun_prev = 0
        if(len(self.csv_array) > 0):
            if(key_ref != ''):
                for row in self.csv_array:
                    if(row[0] == key_ref):
                        NRun_prev = len(row) - self.csv_col_offset
                        break
            else:
                NRun_prev = len(self.csv_array[0]) - self.csv_col_offset

        run_id = NRun_prev # id is at end of row

        # Loop through every item
        for item in flattened_solve_dict:
            
            # Check if row exists
            exists = self.does_row_exist(self.csv_array, item.name, item.type, item.i, item.j)
            row_index = -1
            if(exists == -1):
                row = [item.name, item.type, item.i, item.j]
                for col in range(NRun_prev):
                    row.append('')
                row_index = len(self.csv_array)
                self.csv_array.append(row)
            else:
                row_index = exists
                # Fill missing gaps
                while(len(self.csv_array[row_index]) < run_id + self.csv_col_offset):
                    self.csv_array[row_index].append('')

            # Place value
            self.csv_array[row_index].append(item.value)

    def form_csv_array(self):

        flatten_list_copy = self.flattened_solve_list
        NRun = len(flatten_list_copy)
        csv_array = []
        col_offset = 4

        # Loop through every run
        for run_id in range(NRun):

            # Loop through every item
            for item in flatten_list_copy[run_id]:
                
                # Check if row exists
                exists = self.does_row_exist(csv_array, item.name, item.type, item.i, item.j)
                row_index = -1
                if(exists == -1):
                    row = [item.name, item.type, item.i, item.j]
                    for col in range(NRun):
                        row.append('')
                    row_index = len(csv_array)
                    csv_array.append(row)
                else:
                    row_index = exists

                # Place value
                csv_array[row_index][run_id + col_offset] = item.value

        return csv_array

    def does_row_exist(self, csv_array, name, type, i, j):

        row_id = 0;
        for row in csv_array:
            if(row[0] == name
               and row[1] == type
               and row[2] == i
               and row[3] == j):
                return row_id
            row_id = row_id + 1
        
        return -1

    def get_val_type(self, value):
        if(isinstance(value, list)):

            # matrix
            if(isinstance(value[0], list)):
                return "matrix"
            
            # vector
            else:
                return "vector"

        # single value
        else:
            return "single"

    def flatten(self, solve_dict):
        item_list = []

        for key in solve_dict:

            val = solve_dict[key]
            type_string = self.get_val_type(val)

            if(type_string == "single"):
                item = self.C_sco2_solve_dict_item(key, type_string, 0, 0, val)
                item_list.append(item)

            elif(type_string == "vector"):
                for i in range(len(val)):
                    item = self.C_sco2_solve_dict_item(key, type_string, i, 0, val[i]) 
                    item_list.append(item)

            elif(type_string == "matrix"):
                for i in range(len(val)):
                    for j in range(len(val[i])):
                        item = self.C_sco2_solve_dict_item(key, type_string, i, j, val[i][j])
                        item_list.append(item)

        return item_list
    
    def load_solve_dict_item(self, csv_row, col_id_absolute):
            name = csv_row[0]
            type = csv_row[1]
            i = csv_row[2]
            j = csv_row[3]
            value = csv_row[col_id_absolute]

            return self.C_sco2_solve_dict_item(name, type, i, j, value)

    def unflatten(self, csv_array, col_id):
        # This returns a dict for the specified column of the csv array
        # col_id starts at 0 (there is an offset of 4 for labels)
        
        solve_dict = {}
        dict_item_list = []
        if(len(csv_array[0]) < col_id + self.csv_col_offset):
            return solve_dict

        # Make List of dict items (which contain name, type, i, j, and value)
        for row in csv_array:
            dict_item = self.load_solve_dict_item(row, col_id + self.csv_col_offset)
            #dict_item.load(row, col_id + self.csv_col_offset)
            dict_item_list.append(dict_item)

        # Fill dict with items
        for item in dict_item_list:

            # Convert Value to correct type
            val_converted = self.convert_string(str(item.value))

            if item.type == "single":
                if((item.name in solve_dict) == True):
                    return "problem with " + item.name + " single"
                else:
                    solve_dict[item.name] = val_converted

            elif item.type == "vector":
                if((item.name in solve_dict) == True):
                    # key already exists, extend vector (if necessary)
                    self.extend_vector(solve_dict[item.name], int(item.i) + 1, 'nan')
                    solve_dict[item.name][int(item.i)] = val_converted
                else:
                    # Create key, and size it
                    solve_dict[item.name] = []
                    self.extend_vector(solve_dict[item.name], int(item.i) + 1, 'nan')
                    solve_dict[item.name][int(item.i)] = val_converted

            elif item.type == "matrix":
                if((item.name in solve_dict) == True):
                    # key already exists, extend matrix (if necessary)
                    self.extend_matrix(solve_dict[item.name], int(item.i) + 1, int(item.j) + 1, 'nan')
                    solve_dict[item.name][int(item.i)][int(item.j)] = val_converted
                else:
                    # Create key, and size it
                    solve_dict[item.name] = [[]]
                    self.extend_matrix(solve_dict[item.name], int(item.i) + 1, int(item.j) + 1, 'nan')
                    solve_dict[item.name][int(item.i)][int(item.j)] = val_converted

        return solve_dict

    def extend_vector(self, vec, final_length, fill_val):
        while len(vec) < final_length:
            vec.append(fill_val)

    def extend_matrix(self, mat, NCols, NRows, fill_val):
        # Loop through rows
        for row in range(NRows):
            if(row >= len(mat)):
                mat.append([])

            # Loop through Columns
            for col in range(NCols):
                if(col >= len(mat[row])):
                    mat[row].append(fill_val)

    def convert_string(self, val_string):
        is_dec = val_string.isdecimal()
        if(is_dec):
            return int(val_string)
        else:
            try:
                return float(val_string)
            except:
                return val_string

    def form_old_result_dict_from_csv_array(self, remove_zeros = True):
        if(len(self.csv_array) == 0):
            self.csv_array = self.form_csv_array()

        # get number of values
        NVals = len(self.csv_array[0]) - self.csv_col_offset

        # get eta thermal calc row (this will be used to check if run succeeded)
        eta_vec = []
        success_id_vec = []
        failure_id_vec = []
        success_bool_vec = []
        for row_vec in self.csv_array:
            if(row_vec[0] == "eta_thermal_calc" or row_vec[0] == "design_eff"):
                NVals_row = len(row_vec) - self.csv_col_offset
                for i in range(NVals_row):
                    eta_val = self.convert_string(row_vec[i + self.csv_col_offset])
                    eta_vec.append(eta_val)
                    if(isinstance(eta_val, str) == False):
                        success_id_vec.append(i)
                    else:
                        failure_id_vec.append(i)

                # account for missing data at end of row
                while(len(eta_vec) < NVals):
                    eta_vec.append('')
                    success_bool_vec.append(0)

                break

        self.success_id_vec = success_id_vec
        self.failure_id_vec = failure_id_vec

        num_keys = len(self.csv_array)
        self.old_result_dict = {}
        self.old_result_dict_complete = {}
        row_num = 0
        for row_vec in self.csv_array:
            val_vec = [0] * len(success_id_vec)

            ## Fill in missing data (if necessary)
            #missing_data = NVals - (len(row_vec) - self.csv_col_offset)
            #for i in range(missing_data):
            #    row_vec.append('')

            key_name = ""
            val_type = row_vec[1]
            if(val_type == "single"):
                key_name = row_vec[0]
            else:
                key_name = row_vec[0] + "_" + row_vec[2] + "_" + row_vec[3]

            NVals = len(row_vec) - self.csv_col_offset

            # Collect good results
            count = 0
            for id in success_id_vec:
                val_vec[count] = self.convert_string(row_vec[id + self.csv_col_offset])
                count = count + 1

            self.old_result_dict[key_name] = val_vec

            if(row_num % 50 == 0):
                print(str(round((row_num / num_keys) * 100, 2)) + "% loaded")
            row_num = row_num + 1

        return

    def get_config_name(self, cycle_config, recomp_frac, bypass_frac):

        # Recompresion
        if(cycle_config == 1):
            if(recomp_frac == ''):
                return "recompression"

            if(recomp_frac <= 0.0001):
                return "simple"
            else:
                return "recompression"
        # Partial
        if(cycle_config == 2):
            if(recomp_frac == ''):
                return "partial"
            
            if(recomp_frac <= 0.0001):
                return "partial intercooling"
            else:
                return "partial"
        # TSF
        elif(cycle_config == 4):
            return "turbine split flow"
        #HTR BP
        elif(cycle_config == 3):
            if(bypass_frac == ''):
                return "htr bp"
            if bypass_frac != 0 and recomp_frac <= 0.01:
                return "simple split flow bypass"
            elif recomp_frac <= 0.01 and bypass_frac == 0:
                return "simple"
            elif bypass_frac == 0:
                return "recompression"
            else:
                return "htr bp"
        
        return ""

