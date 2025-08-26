import sys
import os
import numpy as np
import math
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
import pickle
import multiprocessing

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

from G3P3_analysis.sco2_baseline_sim_FINAL import get_sco2_G3P3
import sco2_cycle_ssc as sco2_solve
import design_point_examples as design_pt
import design_point_tools as design_tools

folder_location = "C:\\Users\\tbrown2\\OneDrive - NREL\\sCO2-CSP 10302.41.01.40\\Notes\\G3P3\\runs\\sandbox\\"

def sum_w_nan(iterable):
    sum_total = 0
    for val in iterable:
        if(math.isnan(val) == False):
            sum_total += val
    return sum_total

def validate_sco2_cost(result_dict):
    
    # Get calculated cost from cmod
    cycle_cost = result_dict['cycle_cost']

    # Get individual costs
    mc_cost_bare_erected = result_dict['mc_cost_bare_erected']
    rc_cost_bare_erected = result_dict['rc_cost_bare_erected']
    pc_cost_bare_erected = result_dict['pc_cost_bare_erected']
    LTR_cost_bare_erected = result_dict['LTR_cost_bare_erected']
    HTR_cost_bare_erected = result_dict['HTR_cost_bare_erected']
    PHX_cost_bare_erected = result_dict['PHX_cost_bare_erected']
    BPX_cost_bare_erected = 0
    if 'BPX_cost_bare_erected' in result_dict: 
        BPX_cost_bare_erected = result_dict['BPX_cost_bare_erected']
    t_cost_bare_erected = result_dict['t_cost_bare_erected']
    t2_cost_bare_erected = 0
    if 't2_cost_bare_erected' in result_dict:
        t2_cost_bare_erected = result_dict['t2_cost_bare_erected']
    mc_cooler_cost_bare_erected = result_dict['mc_cooler_cost_bare_erected']
    pc_cooler_cost_bare_erected = result_dict['pc_cooler_cost_bare_erected']
    piping_inventory_etc_cost = result_dict['piping_inventory_etc_cost']

    # Calculate Cycle cost
    cycle_cost_calc = sum_w_nan([mc_cost_bare_erected, rc_cost_bare_erected, pc_cost_bare_erected, 
                                 LTR_cost_bare_erected, HTR_cost_bare_erected, 
                                 PHX_cost_bare_erected, BPX_cost_bare_erected, 
                                 t_cost_bare_erected, t2_cost_bare_erected,
                                 mc_cooler_cost_bare_erected, 
                                 pc_cooler_cost_bare_erected, piping_inventory_etc_cost])
    
    diff = abs(cycle_cost - cycle_cost_calc)

    if(diff > 0.00001):
        print('cycle cost error')
        return False

    return True


def run_bad_partial():
    default_par = get_sco2_G3P3()

    default_par["cycle_config"] = 2
    default_par["UA_recup_tot_des"] = 100
    default_par["is_recomp_ok"] = -0.7
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 0
    default_par["LTR_UA_des_in"] = 100
    default_par["design_method"] = 3
    default_par["is_PR_fixed"] = -13
    default_par["eta_thermal_cutoff"] = 0.0

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(3)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    # Make Cycle Collection Class
    sim_collection = sco2_solve.C_sco2_sim_result_collection()
    sim_collection.add(c_sco2.m_solve_dict)

    file_name = "bad_partial"
    combined_name = folder_location + file_name + '_' + design_pt.get_time_string() + ".csv"
    sim_collection.write_to_csv(combined_name)

    finished = ""

def test_recomp():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 1
    default_par['is_recomp_ok'] = -0.0
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 65
    default_par["LTR_UA_des_in"] = 35
    default_par["design_method"] = 3

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(3)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    # Make Cycle Collection Class
    sim_collection = sco2_solve.C_sco2_sim_result_collection()
    sim_collection.add(c_sco2.m_solve_dict)

def test_partial():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 2
    default_par['is_recomp_ok'] = -0.1
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 65
    default_par["LTR_UA_des_in"] = 35
    default_par["design_method"] = 3

    #default_par["is_IP_fixed"] = -11 # partial cooling config: 0 = No, >0 = fixed HP-IP pressure ratio at input, <0 = fixed IP at abs(input) [MC_IN]

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(2)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    result_dict = c_sco2.m_solve_dict

    P_PC_IN = result_dict['P_state_points'][10]
    P_PC_OUT = result_dict['P_state_points'][11]
    P_MC_IN = result_dict['P_state_points'][0]
    P_MC_OUT = result_dict['P_state_points'][1]

    x = 0

def test_partial_no_recomp():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 2
    default_par['is_recomp_ok'] = 0.0
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 65
    default_par["LTR_UA_des_in"] = 35
    default_par["design_method"] = 3
    default_par["is_PR_fixed"] = -1.0 * 8
    default_par["is_IP_fixed"] = -1.0 * 10
    
    #default_par["is_IP_fixed"] = -11 # partial cooling config: 0 = No, >0 = fixed HP-IP pressure ratio at input, <0 = fixed IP at abs(input) [MC_IN]

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(2)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    result_dict = c_sco2.m_solve_dict

    P_PC_IN = result_dict['P_state_points'][10]
    P_PC_OUT = result_dict['P_state_points'][11]
    P_MC_IN = result_dict['P_state_points'][0]
    P_MC_OUT = result_dict['P_state_points'][1]

    x = 0


def get_IP_pressure_range():

    result_filename = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_orig\run_10_20241211_113039\partial_G3P3_collection_10_20241211_120938.csv"

    print("Opening " + result_filename)
    sim_collection = sco2_solve.C_sco2_sim_result_collection()
    sim_collection.open_csv(result_filename)
    print(result_filename + " opened")

    NRuns = len(sim_collection.old_result_dict)
    P_IP_frac_min = 1
    P_IP_frac_max = -1
    for i in range(NRuns):
        P_PC_IN = sim_collection.old_result_dict['P_state_points_10_0'][i]
        P_PC_OUT = sim_collection.old_result_dict['P_state_points_11_0'][i]
        P_MC_IN = sim_collection.old_result_dict['P_state_points_0_0'][i]
        P_MC_OUT = sim_collection.old_result_dict['P_state_points_1_0'][i]

        P_max = P_MC_OUT
        P_min = P_PC_IN
        P_IP = P_MC_IN

        P_IP_frac = (P_IP - P_min) / (P_max - P_min)
        
        if(P_IP_frac < P_IP_frac_min):
            P_IP_frac_min = P_IP_frac

        if(P_IP_frac > P_IP_frac_max):
            P_IP_frac_max = P_IP_frac

    x = 0

def test_partial_nodes():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 2
    default_par['is_recomp_ok'] = -0.0
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 637.5
    default_par["LTR_UA_des_in"] = 1912.5
    default_par["design_method"] = 3
    default_par["is_PR_fixed"] = -7
    default_par["is_IP_fixed"] = -7
    default_par["dT_PHX_cold_approach"] = 20

    Npts = 27
    node_list = np.linspace(4, 30, Npts, True, dtype=int)

    node_result_dict = {'nodes':[]}
    label_eta = "eta_thermal_calc"
    label_cost = "cycle_cost"
    label_T_htf = "T_htf_cold_des"
    output_labels = [label_eta, label_cost, label_T_htf]
    for label in output_labels:
        node_result_dict[label] = []



    for nodes in node_list:
        default_par["HTR_n_sub_hx"] = nodes
        default_par["LTR_n_sub_hx"] = nodes

        # Make Cycle class
        c_sco2 = sco2_solve.C_sco2_sim(2)

        # Overwrite Variables
        c_sco2.overwrite_default_design_parameters(default_par)

        # Solve
        c_sco2.solve_sco2_case()

        result_dict = c_sco2.m_solve_dict
        
        node_result_dict["nodes"].append(nodes)
        for label in output_labels:
            node_result_dict[label].append(result_dict[label])

        eta = result_dict[label_eta]
        cost = result_dict[label_cost]
        T_htf = result_dict[label_T_htf]

        y = 0


    x = 0

def test_bad_htrbp():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 3
    default_par['is_recomp_ok'] = 0.0
    default_par['is_bypass_ok'] = 0.0
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 924.691358
    default_par["LTR_UA_des_in"] = 264.1975309
    default_par["design_method"] = 3
    default_par["is_PR_fixed"] = -8.55555
    default_par["T_bypass_target"] = 0 # (not used)
    default_par['yr_inflation'] = 0

    #default_par["is_IP_fixed"] = -11 # partial cooling config: 0 = No, >0 = fixed HP-IP pressure ratio at input, <0 = fixed IP at abs(input) [MC_IN]

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(2)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    result_dict = c_sco2.m_solve_dict

    P_PC_IN = result_dict['P_state_points'][10]
    P_PC_OUT = result_dict['P_state_points'][11]
    P_MC_IN = result_dict['P_state_points'][0]
    P_MC_OUT = result_dict['P_state_points'][1]

    x = 0

def test_simple_cost_htr():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 3
    default_par['is_recomp_ok'] = 0.0
    default_par['is_bypass_ok'] = 0.0
    default_par["LTR_design_code"] = 1
    default_par["HTR_design_code"] = 1
    default_par["HTR_UA_des_in"] = 1733.333
    default_par["LTR_UA_des_in"] = 0
    default_par["design_method"] = 3
    default_par["is_PR_fixed"] = -7.66667
    default_par["T_bypass_target"] = 0 # (not used)

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(3)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    result_dict = c_sco2.m_solve_dict

    if False:
        filename = asksaveasfilename(filetypes =[('Text file', '*.txt')], title="Select save file")
        if filename != "":
            design_tools.write_dict(filename, result_dict, '\t') 

    P_PC_IN = result_dict['P_state_points'][10]
    P_PC_OUT = result_dict['P_state_points'][11]
    P_MC_IN = result_dict['P_state_points'][0]
    P_MC_OUT = result_dict['P_state_points'][1]

    x = 0

def test_recomp_inflation():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 1
    default_par['is_recomp_ok'] = -0.3
    default_par['yr_inflation'] = 0

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(3)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    # Validate Cost
    solve_dict = c_sco2.m_solve_dict
    cost_valid = validate_sco2_cost(solve_dict)
    if cost_valid == False:
        print("Recomp: No inflation run costs do not add up")
        return
    cycle_cost_no_inflation = solve_dict['cycle_cost']

    # Now set inflation
    inflation = 798.8 / 567.5
    default_par["yr_inflation"] = 2024
    c_sco2.overwrite_default_design_parameters(default_par)

    # Re-Solve
    c_sco2.solve_sco2_case()

    # Validate cost with inflation
    solve_dict_inflated = c_sco2.m_solve_dict
    cost_valid_inflated = validate_sco2_cost(solve_dict_inflated)
    if cost_valid_inflated == False:
        print("Recomp: Inflation run costs do not add up")
        return
    cycle_cost_inflated = solve_dict_inflated['cycle_cost']

    # Calculate Ratio
    inflation_ratio_calc = cycle_cost_inflated / cycle_cost_no_inflation

    if(abs((inflation_ratio_calc/inflation)-1) > 0.01):
        print("Recomp inflation does not equal calculated cost ratio")
    else:
        print("Recomp inflation looks good")

def test_partial_inflation():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 2
    default_par['is_recomp_ok'] = -0.3
    default_par['yr_inflation'] = 0

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(2)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    # Validate Cost
    solve_dict = c_sco2.m_solve_dict
    cost_valid = validate_sco2_cost(solve_dict)
    if cost_valid == False:
        print("Partial: No inflation run costs do not add up")
        return
    cycle_cost_no_inflation = solve_dict['cycle_cost']

    # Now set inflation
    inflation = 798.8 / 567.5
    default_par["yr_inflation"] = 2024
    c_sco2.overwrite_default_design_parameters(default_par)

    # Re-Solve
    c_sco2.solve_sco2_case()

    # Validate cost with inflation
    solve_dict_inflated = c_sco2.m_solve_dict
    cost_valid_inflated = validate_sco2_cost(solve_dict_inflated)
    if cost_valid_inflated == False:
        print("Partial: Inflation run costs do not add up")
        return
    cycle_cost_inflated = solve_dict_inflated['cycle_cost']

    # Calculate Ratio
    inflation_ratio_calc = cycle_cost_inflated / cycle_cost_no_inflation

    if(abs((inflation_ratio_calc/inflation)-1) > 0.01):
        print("Partial: inflation does not equal calculated cost ratio")
    else:
        print("Partial: inflation looks good")

def test_htrbp_inflation():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 3
    default_par['is_recomp_ok'] = -0.3
    default_par['is_bypass_ok'] = -0.1
    default_par['T_bypass_target'] = 0
    default_par['yr_inflation'] = 0

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(3)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    # Validate Cost
    solve_dict = c_sco2.m_solve_dict
    cost_valid = validate_sco2_cost(solve_dict)
    if cost_valid == False:
        print("htr bp: No inflation run costs do not add up")
        return
    cycle_cost_no_inflation = solve_dict['cycle_cost']

    # Now set inflation
    inflation = 798.8 / 567.5
    default_par["yr_inflation"] = 2024
    c_sco2.overwrite_default_design_parameters(default_par)

    # Re-Solve
    c_sco2.solve_sco2_case()

    # Validate cost with inflation
    solve_dict_inflated = c_sco2.m_solve_dict
    cost_valid_inflated = validate_sco2_cost(solve_dict_inflated)
    if cost_valid_inflated == False:
        print("htr bp: Inflation run costs do not add up")
        return
    cycle_cost_inflated = solve_dict_inflated['cycle_cost']

    # Calculate Ratio
    inflation_ratio_calc = cycle_cost_inflated / cycle_cost_no_inflation

    if(abs((inflation_ratio_calc/inflation)-1) > 0.01):
        print("htr bp inflation does not equal calculated cost ratio")
    else:
        print("htr bp inflation looks good")

def test_tsf_inflation():
    default_par = get_sco2_G3P3()
    default_par["cycle_config"] = 4
    default_par['yr_inflation'] = 0

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(4)

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(default_par)

    # Solve
    c_sco2.solve_sco2_case()

    # Validate Cost
    solve_dict = c_sco2.m_solve_dict
    cost_valid = validate_sco2_cost(solve_dict)
    if cost_valid == False:
        print("tsf: No inflation run costs do not add up")
        return
    cycle_cost_no_inflation = solve_dict['cycle_cost']

    # Now set inflation
    inflation = 798.8 / 567.5
    default_par["yr_inflation"] = 2024
    c_sco2.overwrite_default_design_parameters(default_par)

    # Re-Solve
    c_sco2.solve_sco2_case()

    # Validate cost with inflation
    solve_dict_inflated = c_sco2.m_solve_dict
    cost_valid_inflated = validate_sco2_cost(solve_dict_inflated)
    if cost_valid_inflated == False:
        print("tsf: Inflation run costs do not add up")
        return
    cycle_cost_inflated = solve_dict_inflated['cycle_cost']

    # Calculate Ratio
    inflation_ratio_calc = cycle_cost_inflated / cycle_cost_no_inflation

    if(abs((inflation_ratio_calc/inflation)-1) > 0.01):
        print("tsf inflation does not equal calculated cost ratio")
    else:
        print("tsf inflation looks good")

def run_sco2_case_from_GUI():
    
    filename = askopenfilename(filetypes =[
            ('All supported', '*.pkl *.txt *.tsv'),
            ('Pickle files', '*.pkl'),
            ('Text files', '*.txt'),
            ('Tab-separated', '*.tsv')],
          title="Open htrbp pkl file")
    _, ext = os.path.splitext(filename)

    result_dict = {}

    match ext:
        case ".txt" | ".tsv":
            result_dict = design_tools.get_dict_from_file_w_STRING(filename)
        case ".pkl":
            with open(filename, 'rb') as f:
                result_dict = pickle.load(f)

    # Get default par
    sim_dict = design_pt.get_sco2_G3P3()

    # Overwrite all keys in sim_dict
    for key in sim_dict:
        if key in result_dict:
            sim_dict[key] = result_dict[key][0]
        else:
            trouble = 0

    # Add missing keys
    sim_dict['T_bypass_target'] = 0
    sim_dict['deltaT_bypass'] = 0

    # Make Cycle class
    c_sco2 = sco2_solve.C_sco2_sim(result_dict['cycle_config'][0])

    # Overwrite Variables
    c_sco2.overwrite_default_design_parameters(sim_dict)            
    
    # Solve
    c_sco2.solve_sco2_case()
    solve_dict = c_sco2.m_solve_dict

    if c_sco2.m_solve_success == False:
        return

    # Add cmod success var
    solve_dict['cmod_success'] = True
    solve_dict['id'] = 0
    solve_dict['filename'] = os.path.basename(filename)

    # Run G3P3
    sys.path.append(r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\Design Point\G3P3_python_design_point")
    import g3p3_design_sim

    manager = multiprocessing.Manager()
    solve_dict_queue = manager.Queue()

    g3p3_design_sim.run_once_solve_dict(solve_dict, solve_dict_queue)
    g3p3_solve_dict = solve_dict_queue.get()

    # Make mega g3p3 dict
    mega_dict = {}
    for sco2_key in solve_dict:
        mega_dict[sco2_key] = solve_dict[sco2_key]
    for g3p3_key in g3p3_solve_dict:
        mega_dict[g3p3_key] = g3p3_solve_dict[g3p3_key]

    # Save
    save_filename = asksaveasfilename(filetypes =[('Text file', '*.txt')], title="Select save file")
    design_tools.write_dict(save_filename, mega_dict, '\t')   
    
        


if __name__ == "__main__":
    #run_bad_partial()
    #test_recomp()
    #test_partial()
    #test_partial_nodes()
    #test_recomp()
    #test_partial_no_recomp()
    #test_simple_cost_htr()
    run_sco2_case_from_GUI()
    #test_recomp_inflation()
    #test_partial_inflation()
    #test_htrbp_inflation()
    #test_tsf_inflation()
    #get_IP_pressure_range()
    #run_bad_partial()