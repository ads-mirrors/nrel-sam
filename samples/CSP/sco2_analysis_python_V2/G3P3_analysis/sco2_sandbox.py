import sys
import os

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)

from G3P3_analysis.sco2_baseline_sim_w_IP import get_sco2_G3P3
import sco2_cycle_ssc as sco2_solve
import design_point_examples as design_pt

folder_location = "C:\\Users\\tbrown2\\OneDrive - NREL\\sCO2-CSP 10302.41.01.40\\Notes\\G3P3\\runs\\sandbox\\"

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
    default_par['is_recomp_ok'] = -0.1
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




if __name__ == "__main__":
    #run_bad_partial()
    #test_recomp()
    #test_partial()
    #get_IP_pressure_range()
    run_bad_partial()