# -*- coding: utf-8 -*-

import sys
import os
import json

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
simsharedFolder = os.path.join(parentDir, 'sco2_sim_shared')
sys.path.append(simsharedFolder)

import sco2_baseline_parameters as sco2_pars
import sco2_sim_core


# Global variables
eta_cutoff = 0.2
N_per_batch = 50000

def initialize_global_var():
    local_var_dict = {}

    json_file_path = os.path.join(parentDir, 'local_var.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            local_var_dict = json.load(json_file)

    return local_var_dict

# Methods to run all sweeps

def run_case():

    # Get global variables
    global_var_dict = initialize_global_var()

    # Get baseline parameters
    default_par = sco2_pars.get_sco2_G3P3()

    # Modify baseline for TIT 550
    T_turbine_in = 550  # [C]
    default_par["dT_PHX_hot_approach"] = default_par["T_htf_hot_des"] - T_turbine_in

    # Get design variable ranges
    design_var_dict = sco2_pars.get_design_vars_opt()

    # Set Number of runs, and name
    n_par = 10
    run_name = "TIT550_baseline_OPT"
    run_g3p3 = True

    # Run sco2 sweeps
    save_file_names = sco2_sim_core.run_all_sweeps(n_par, run_name, default_par, design_var_dict,
                                 global_var_dict, run_g3p3)


# Main function

if __name__ == "__main__":

    run_case()

