import sys
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import pickle

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

from G3P3_analysis.sco2_baseline_sim_w_IP import get_sco2_G3P3
import sco2_cycle_ssc as sco2_solve
import design_point_examples as design_pt
import design_point_tools as design_tools
import sco2_plot_sandbox as plot_sandbox


def plot_sweep(htrbp_result_dict, recomp_result_dict,
               tsf_result_dict, partial_result_dict):
    
    # Variables to Display
    ETA_label = ["eta_thermal_calc", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    print("Splitting by config type...")

    # HTR BP (only comes from htr bp file)
    htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict],
                                                            "config_name", "htr bp")

    # Recompression (comes from recomp and htr bp)
    recomp_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict, 
                                                            recomp_result_dict],  
                                                            "config_name", "recompression")

    # Simple (from recomp and htr bp)
    simple_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict, 
                                                            recomp_result_dict],  
                                                            "config_name", "simple")

    # Simple w/ htr bypass (from htr bp only)
    simple_htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_result_dict],
                                                            "config_name", "simple split flow bypass")
    
    # Partial (only comes from partial file)
    partial_compiled_dict = design_tools.combine_dict_by_key([partial_result_dict],
                                                            "config_name", "partial")

    # Partial Intercooling (only comes from partial file)
    partial_ic_compiled_dict = design_tools.combine_dict_by_key([partial_result_dict],
                                                            "config_name", "partial intercooling")

    

    # Create Cycle Split T HTF Pareto
    print("Forming split cycle T HTF pareto fronts...")
    htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
    tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_result_dict, ETA_label[0], T_HTF_label[0], True, False)

    P_MC_IN = 'P_state_points_0_0'
    P_PC_IN = 'P_state_points_10_0'
    z_label_list = [["recomp_frac", "", "Recomp Frac"], 
                    [P_MC_IN, "MPa", "P MC IN"], 
                    [P_PC_IN, "MPa", "P PC IN"],
                    ["bypass_frac", "", "Bypass Frac"], 
                    ["is_turbine_split_ok", "", "Turbine Split Frac"],
                    ["recup_total_UA_calculated", "MW/K", "Total Recup Conductance"], 
                    ["HTR_UA_calculated", "MW/K", "HTR Conductance"],
                    ["LTR_UA_calculated", "MW/K", "LTR Conductance"]]

    # Plot
    plot_sandbox.plot_z_axis(simple_compiled_dict, ETA_label, T_HTF_label, z_label_list, title="Simple")
    plt.show(block = True)

    plot_sandbox.plot_z_axis(simple_htrbp_compiled_dict, ETA_label, T_HTF_label, z_label_list, title="Simple BP")
    plt.show(block = True)

    plot_sandbox.plot_z_axis(recomp_compiled_dict, ETA_label, T_HTF_label, z_label_list, title="Recomp")
    plt.show(block = True)

    plot_sandbox.plot_z_axis(htrbp_compiled_dict, ETA_label, T_HTF_label, z_label_list, title="HTR BP")
    plt.show(block = True)

    plot_sandbox.plot_z_axis(partial_ic_compiled_dict, ETA_label, T_HTF_label, z_label_list, title="Partial IC")
    plt.show(block = True)

    plot_sandbox.plot_z_axis(partial_compiled_dict, ETA_label, T_HTF_label, z_label_list, title="Partial")
    plt.show(block = True)

    plot_sandbox.plot_z_axis(tsf_result_dict, ETA_label, T_HTF_label, z_label_list, title="TSF")
    plt.show(block = True)

    htrbp_legend_label = "recompression \nw/ htr bypass"
    recomp_legend_label = "recompression"
    simple_legend_label = "simple"
    simple_bp_legend_label = "simple w/ bypass"
    partial_legend_label = "partial cooling"
    partial_ic_legend_label = "simple intercooling"
    tsf_legend_label = "turbine split flow"
    design_tools.plot_scatter_pts([
                    [simple_compiled_dict, {'label':simple_legend_label, 'marker':'.'}],
                    [simple_htrbp_compiled_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                    [recomp_compiled_dict, {'label':recomp_legend_label, 'marker':'.'}],
                    [htrbp_compiled_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                    [partial_ic_compiled_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                    [partial_compiled_dict, {'label':partial_legend_label, 'marker':'.'}],          
                    [tsf_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
                    ], 
                    ETA_label, T_HTF_label, show_legend=True)

    # Pareto (Temp vs ETA)
    design_tools.plot_scatter_pts([
                [simple_compiled_T_HTF_pareto_dict, {'label':simple_legend_label, 'marker':'.'}],
                [simple_htrbp_compiled_T_HTF_pareto_dict, {'label':simple_bp_legend_label, 'marker':'.'}],             
                [recomp_compiled_T_HTF_pareto_dict, {'label':recomp_legend_label, 'marker':'.'}],
                [htrbp_compiled_T_HTF_pareto_dict, {'label':htrbp_legend_label, 'marker':'.'}],
                [partial_ic_compiled_T_HTF_pareto_dict, {'label':partial_ic_legend_label, 'marker':'.'}],
                [partial_compiled_T_HTF_pareto_dict, {'label':partial_legend_label, 'marker':'.'}],          
                [tsf_T_HTF_pareto_dict, {'label':tsf_legend_label, 'marker':'.'}]
                ], 
                ETA_label, T_HTF_label, show_legend=False)

def plot_pkl_via_filedlg():
    
    window = tk.Tk()
    htrbp_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open htrbp pkl file")
    recomp_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open recomp pkl file")
    tsf_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open tsf pkl file")
    partial_filename = askopenfilename(filetypes =[('Pickles', '*.pkl')], title="Open partial pkl file")

    filename_list = [htrbp_filename, recomp_filename,
                     tsf_filename, partial_filename]
    result_dict_list = []

    for filename in filename_list:
        with open(filename, 'rb') as f:
            result_dict = pickle.load(f)
        result_dict_list.append(result_dict)
    
    plot_sweep(*result_dict_list)

def plot_pkl_via_hardcode():
    window = tk.Tk()
    htrbp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\htrbp_G3P3_collection_10_20250103_192511_000.pkl"
    recomp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\recomp_G3P3_collection_10_20250103_190235_000.pkl"
    tsf_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\TSF_G3P3_collection_10_20250103_191443_000.pkl"
    partial_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250103_132839\pickled_merged\partial_G3P3_collection_10_20250103_132840_000.pkl"

    filename_list = [htrbp_filename, recomp_filename,
                     tsf_filename, partial_filename]
    result_dict_list = []

    for filename in filename_list:
        with open(filename, 'rb') as f:
            result_dict = pickle.load(f)
        result_dict_list.append(result_dict)
    
    plot_sweep(*result_dict_list)


def plot_test():
    window = tk.Tk()
    htrbp_filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Open htrbp save file(s)")
    htrbp_filename_list = []
    for filename in htrbp_filename_tuple:
        htrbp_filename_list.append(filename)

    htrbp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv_list(htrbp_filename_list)

if __name__ == "__main__":
    plot_pkl_via_hardcode()
    plt.show(block = True)