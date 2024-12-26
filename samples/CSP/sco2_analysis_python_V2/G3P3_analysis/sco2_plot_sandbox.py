import sys
import os
import matplotlib.pyplot as plt

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

def plot_z_axis(result_dict, X_info, Y_info, Z_info_list, title=""):

    for Z_info in Z_info_list:
        Z_label = ''
        if(isinstance(Z_info, list)):
            Z_label = Z_info[0]
        else:
            Z_label = Z_info

        if(Z_label in result_dict):
            design_tools.plot_scatter_pts([           
                            [result_dict, {'label':'test', 'marker':'.'}],
                            ], 
                            X_info, Y_info, Z_info, show_legend=False, title=title)

    pass

def plot_split(result_dict, split_key, X_info, Y_info, title=""):

    dict_key_list = design_tools.split_by_key(result_dict, split_key)
    recomp_eff_pareto_list = []
    for diction in dict_key_list:
        pareto = design_tools.get_pareto_dict(diction, X_info[0], Y_info[0], True, False)
        dict_w_kargs = [pareto, {'label':diction[split_key][0]}]
        recomp_eff_pareto_list.append(dict_w_kargs)

    design_tools.plot_scatter_pts(          
        recomp_eff_pareto_list
        , 
        X_info, Y_info, show_legend=True, title=title)

    pass

def display_complete():
    # Define original data
    tsf_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\TSF_G3P3_collection_10_20241209_171618.csv"
    recomp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241219_105932\recomp_G3P3_collection_10_20241219_110636.csv"
    partial_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_w_IP\run_10_20241218_121515\partial_G3P3_collection_10_20241218_172723.csv"
    htrbp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_10_20241209_164644\htrbp_G3P3_collection_10_20241209_182054.csv"

    is_reduced = False
    if is_reduced:
        tsf_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_5_20241209_163643\TSF_G3P3_collection_5_20241209_163832.csv"
        recomp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_5_20241209_163643\recomp_G3P3_collection_5_20241209_163812.csv"
        partial_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_w_IP\run_5_20241218_093200\partial_G3P3_collection_5_20241218_093801.csv"
        htrbp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline\run_5_20241209_163643\htrbp_G3P3_collection_5_20241209_164028.csv"

    print("Opening htrbp...")
    htrbp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv(htrbp_filename)
    print("HTR BP opened")

    print("Opening recomp...")
    recomp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_filename)
    print("Recomp open")

    print("Opening tsf...")
    tsf_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    tsf_sim_collection.open_csv(tsf_filename)
    print("TSF opened")

    print("Opening partial...")
    partial_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    partial_sim_collection.open_csv(partial_filename)
    print("Partial opened")

    # Variables to Display
    ETA_label = ["eta_thermal_calc", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    # Split Dicts by 'Actual' config name
    if True:
        print("Splitting by config type...")

        # HTR BP (only comes from htr bp file)
        htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict],
                                                                "config_name", "htr bp")

        # Recompression (comes from recomp and htr bp)
        recomp_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict, 
                                                                recomp_sim_collection.old_result_dict],  
                                                                "config_name", "recompression")

        # Simple (from recomp and htr bp)
        simple_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict, 
                                                                recomp_sim_collection.old_result_dict],  
                                                                "config_name", "simple")

        # Simple w/ htr bypass (from htr bp only)
        simple_htrbp_compiled_dict = design_tools.combine_dict_by_key([htrbp_sim_collection.old_result_dict],
                                                                "config_name", "simple split flow bypass")
        
        # Partial (only comes from partial file)
        partial_compiled_dict = design_tools.combine_dict_by_key([partial_sim_collection.old_result_dict],
                                                                "config_name", "partial")

        # Partial Intercooling (only comes from partial file)
        partial_ic_compiled_dict = design_tools.combine_dict_by_key([partial_sim_collection.old_result_dict],
                                                                "config_name", "partial intercooling")

        

        # Create Cycle Split T HTF Pareto
        print("Forming split cycle T HTF pareto fronts...")
        htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(htrbp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
        recomp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(recomp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
        simple_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
        simple_htrbp_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(simple_htrbp_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
        partial_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
        partial_ic_compiled_T_HTF_pareto_dict = design_tools.get_pareto_dict(partial_ic_compiled_dict, ETA_label[0], T_HTF_label[0], True, False)
        tsf_T_HTF_pareto_dict = design_tools.get_pareto_dict(tsf_sim_collection.old_result_dict, ETA_label[0], T_HTF_label[0], True, False)

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
    #plot_z_axis(htrbp_sim_collection.old_result_dict, ETA_label, T_HTF_label, z_label_list, title="HTR BP")
    #plt.show(block = True)

    #plot_z_axis(recomp_sim_collection.old_result_dict, ETA_label, T_HTF_label, z_label_list, title="Recomp")
    #plt.show(block = True)

    #plot_z_axis(partial_sim_collection.old_result_dict, ETA_label, T_HTF_label, z_label_list, title="Partial")
    #plt.show(block = True)

    #plot_z_axis(tsf_sim_collection.old_result_dict, ETA_label, T_HTF_label, z_label_list, title="TSF")
    #plt.show(block = True)

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
                    [tsf_sim_collection.old_result_dict, {'label':tsf_legend_label, 'marker':'.'}]
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


def display_eff():
    # Define original data
    tsf_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\eff\run_5_20241218_202504\TSF_G3P3_collection_5_20241218_205118.csv"
    recomp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\eff\run_5_20241218_202504\recomp_G3P3_collection_5_20241218_205035.csv"
    partial_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\eff\run_5_20241218_202504\partial_G3P3_collection_5_20241218_204843.csv"
    htrbp_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\eff\run_5_20241218_202504\htrbp_G3P3_collection_5_20241218_205717.csv"

    print("Opening htrbp...")
    htrbp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    htrbp_sim_collection.open_csv(htrbp_filename)
    print("HTR BP opened")

    print("Opening recomp...")
    recomp_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    recomp_sim_collection.open_csv(recomp_filename)
    print("Recomp open")

    print("Opening tsf...")
    tsf_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    tsf_sim_collection.open_csv(tsf_filename)
    print("TSF opened")

    print("Opening partial...")
    partial_sim_collection = sco2_solve.C_sco2_sim_result_collection()
    partial_sim_collection.open_csv(partial_filename)
    print("Partial opened")

    # Variables to Display
    ETA_label = ["eta_thermal_calc", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    plot_split(htrbp_sim_collection.old_result_dict, "eta_isen_mc", ETA_label, T_HTF_label, "htr bp")  
    plot_split(recomp_sim_collection.old_result_dict, "eta_isen_mc", ETA_label, T_HTF_label, "recomp")
    plot_split(tsf_sim_collection.old_result_dict, "eta_isen_mc", ETA_label, T_HTF_label, "tsf")
    plot_split(partial_sim_collection.old_result_dict, "eta_isen_mc", ETA_label, T_HTF_label, "partial")

    if False:
        recomp_eff_list = design_tools.split_by_key(recomp_sim_collection.old_result_dict, "eta_isen_mc")
        recomp_eff_pareto_list = []
        for recomp_dict in recomp_eff_list:
            pareto = design_tools.get_pareto_dict(recomp_dict, ETA_label[0], T_HTF_label[0], True, False)
            dict_w_kargs = [pareto, {'label':'test'}]
            recomp_eff_pareto_list.append(dict_w_kargs)

        
        design_tools.plot_scatter_pts(          
            recomp_eff_pareto_list
            , 
            ETA_label, T_HTF_label, show_legend=False)




if __name__ == "__main__":
    #display_eff()
    display_complete()
    plt.show(block = True)