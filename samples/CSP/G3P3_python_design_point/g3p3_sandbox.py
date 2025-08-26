import numpy as np

import matplotlib.lines as mlines
import multiprocessing
from functools import partial
import time
import datetime
import sys
import os
from tkinter.filedialog import askopenfilenames
import tkinter as tk
import pandas as pd

sys.path.append("sco2-python")

newPath = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')

import sco2_sim_result_collection as sco2_result_collection
import g3p3_annual_sim_refactored as g3p3_case

folder_location = "C:\\Users\\tbrown2\\Desktop\\sco2_python\\G3P3\\design point\\"
Nproc = 1

# Simulation Functions

def run_failed_good_case():

    P_ref_MWe = 10.1 # MWe
    design_eff = 0.49
    T_htf_cold_des_C = 530.1827 # C
    T_htf_hot_des_C = 775 # C
    plant_spec_cost_per_kWe = 1961.515 # $/kWe
    W_dot_cycle_parasitic_input_MWe = 0.1 # MWe

    result_dict = g3p3_case.run_g3p3_case(P_ref_MWe, design_eff, T_htf_cold_des_C, T_htf_hot_des_C,
                                         plant_spec_cost_per_kWe, W_dot_cycle_parasitic_input_MWe, suppress_print=False)

    x = 0
    return

def run_passed_good_case():

    P_ref_MWe = 10.1 # MWe
    design_eff = 0.488
    T_htf_cold_des_C = 529.5359 # C
    T_htf_hot_des_C = 775 # C
    plant_spec_cost_per_kWe = 1919.212 # $/kWe
    W_dot_cycle_parasitic_input_MWe = 0.1 # MWe

    result_dict = g3p3_case.run_g3p3_case(P_ref_MWe, design_eff, T_htf_cold_des_C, T_htf_hot_des_C,
                                         plant_spec_cost_per_kWe, W_dot_cycle_parasitic_input_MWe, suppress_print=False)

    x = 0
    return

def test_heliostat_cost():
    P_ref_MWe = 10.1 # MWe
    design_eff = 0.488
    T_htf_cold_des_C = 529.5359 # C
    T_htf_hot_des_C = 775 # C
    plant_spec_cost_per_kWe = 1919.212 # $/kWe
    W_dot_cycle_parasitic_input_MWe = 0.1 # MWe

    # Modify heliostat cost
    overwrite_dict = {}
    heliostat_spec_cost_baseline = 75

    heliostat_spec_cost = 10 * heliostat_spec_cost_baseline
    overwrite_dict["heliostat_spec_cost"] = heliostat_spec_cost
    
    # Run
    result_dict = g3p3_case.run_g3p3_case(P_ref_MWe, design_eff, T_htf_cold_des_C, T_htf_hot_des_C,
                                         plant_spec_cost_per_kWe, W_dot_cycle_parasitic_input_MWe, suppress_print=False,
                                         overwrite_dict=overwrite_dict)

    x = 0
    return

if __name__ == "__main__":
    test_heliostat_cost()


