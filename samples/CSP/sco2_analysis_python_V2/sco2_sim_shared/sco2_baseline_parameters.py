

def get_sco2_G3P3():

    des_par = {}

    # G3P3 Parameters

    # Power
    W_thermo_net = 10.0     # [MWt] Gross thermo output
    W_air_cooler = 0.1      # [MWe] Air Cooler Parasitic
    W_thermo_gross = W_thermo_net + W_air_cooler    #[MWe]
    des_par["W_dot_net_des"] = W_thermo_gross       #[MWe]
    des_par["fan_power_frac"] = W_air_cooler/W_thermo_gross  # [-] Fraction of net cycle power consumed by air cooler fan

    # HTF
    T_HTF_in = 775                          # [C]
    T_turbine_in = 700                      # [C] sco2 turbine inlet temp    
    des_par["T_htf_hot_des"] = T_HTF_in     # [C] HTF design hot temperature (PHX inlet)
    des_par["dT_PHX_hot_approach"] = T_HTF_in - T_turbine_in     # [C/K] Temperature difference between hot HTF and turbine inlet
    des_par["dT_PHX_cold_approach"] = 20     # [C/K] Temperature difference between cold HTF and hot sco2

    des_par["set_HTF_mdot"] = 0

    # Efficiency (ASSUMPTION)
    des_par["eta_isen_t"] = 0.90   # [-] Turbine isentropic efficiency
    des_par["eta_isen_t2"] = 0.90  # [-] Secondary turbine isentropic efficiency
    des_par["eta_isen_mc"] = 0.85  # [-] Main compressor isentropic efficiency
    des_par["eta_isen_pc"] = 0.85  # [-] Precompressor isentropic efficiency
    des_par["eta_isen_rc"] = 0.85  # [-] Recompressor Polytropic efficiency

    # Design Variables
    des_par["is_PR_fixed"] = -7.918     # 0 = No, >0 = fixed pressure ratio at input <0 = fixed LP at abs(input)
    des_par["is_turbine_split_ok"] = -0.431364843
    des_par["is_IP_fixed"] = 0      # partial cooling config: 0 = No, >0 = fixed HP-IP pressure ratio at input, <0 = fixed IP at abs(input)
    des_par["is_bypass_ok"] = -0.114
    des_par["is_recomp_ok"] = -0.35 	# 1 = Yes, 0 = simple cycle only, < 0 = fix f_recomp to abs(input)
    des_par["design_method"] = 2  # [-] 1 = specify efficiency, 2 = specify total recup UA, 3 = Specify each recup design (see inputs below)
    des_par["UA_recup_tot_des"] = 36851.92  # [kW/K] (used when design_method == 2)
    des_par["HTR_UA_des_in"] = 0.77925 * 959.37     # [kW/K] (required if LTR_design_code == 1)
    des_par["LTR_UA_des_in"] = 1.61506 * 112.18     # [kW/K] (required if LTR_design_code == 1)

    des_par["N_nodes_air_cooler_pass"] = 100

    # from Alfani 2021

    # Configuration
    des_par["cycle_config"] = 4  # [1] = RC, [2] = PC, [3] = HTRBP, [4] = TSF

    # Ambient
    des_par["T_amb_des"] = 30  # [C] Ambient temperature at design
    des_par["dT_mc_approach"] = 6.0  # [C] Use 6 here per Neises & Turchi 19. Temperature difference between main compressor CO2 inlet and ambient air

    # Pressure
    des_par["PHX_co2_deltaP_des_in"] = 0.0056  # [kPa] Relative pressure loss
    des_par["deltaP_cooler_frac"] = 0.005  # [-] Fraction of CO2 inlet pressure that is design point cooler CO2 pressure drop
    des_par["is_P_high_fixed"] = 1  # 0 = No, optimize. 1 = Yes (=P_high_limit)
    des_par["P_high_limit"] = 25  # [MPa] Cycle high pressure limit
    
    LP_deltaP = 0.031 # 3.1% from Neises (2023) Influence of air-cooled...
    HP_deltaP = 0.0056 # 0.56% from ^
    des_par["LTR_LP_deltaP_des_in"] = LP_deltaP  # [-]
    des_par["HTR_LP_deltaP_des_in"] = LP_deltaP  # [-]
    des_par["LTR_HP_deltaP_des_in"] = HP_deltaP  # [-]
    des_par["HTR_HP_deltaP_des_in"] = HP_deltaP  # [-]

    # Recuperators
    eff_max = 0.999
        # LTR
    des_par["LTR_design_code"] = 2        # 1 = UA, 2 = min dT, 3 = effectiveness
    des_par["LTR_min_dT_des_in"] = 10.0   # [C] (required if LTR_design_code == 2)
    des_par["LT_recup_eff_max"] = eff_max    # [-] Maximum effectiveness low temperature recuperator

        # HTR
    des_par["HTR_design_code"] = 2        # 1 = UA, 2 = min dT, 3 = effectiveness
    des_par["HTR_min_dT_des_in"] = 10.0   # [C] (required if LTR_design_code == 2)
    des_par["HT_recup_eff_max"] = eff_max  # [-] Maximum effectiveness high temperature recuperator

    des_par["eta_thermal_cutoff"] = 0.2

    # DEFAULTS

    # ADDED to converge LTR and HTR 
    des_par["HTR_n_sub_hx"] = 50
    des_par["LTR_n_sub_hx"] = 50
 
        # System design parameters
    des_par["htf"] = 36  # [-] Bauxite
    des_par["site_elevation"] = 588  # [m] Elevation of Daggett, CA. Used to size air cooler...

    # Convergence and optimization criteria
    des_par["rel_tol"] = 6  # [-] Baseline solver and optimization relative tolerance exponent (10^-rel_tol)

    # Default
    des_par["deltaP_counterHX_frac"] = 0.0054321  # [-] Fraction of CO2 inlet pressure that is design point counterflow HX (recups & PHX) pressure drop
    des_par["deltaT_bypass"] = 0
    
    des_par["yr_inflation"] = 2024

    # NOT USED

    # LTR
    
    
    des_par["LTR_eff_des_in"] = 0.895     # [-] (required if LTR_design_code == 3)
    
    
    # HTR
    des_par["HTR_eff_des_in"] = 0.945      # [-] (required if LTR_design_code == 3)
    

    des_par["eta_thermal_des"] = 0.44  # [-] Target power cycle thermal efficiency (used when design_method == 1)
    

    
    return des_par

def get_design_vars_orig():
    
    design_var_dict = {}
    
    design_var_dict["is_PR_fixed"] = [5, 13]     # MPa
    design_var_dict["UA_recup_tot_des"] = [100, 5000]   # kW/K
    design_var_dict["LTR_UA_split"] = [0,1]
    design_var_dict["is_recomp_ok"] = [0, 0.7]	    # < 0 = fix f_recomp to abs(input)
    design_var_dict["partial_IP"] = [0,0.54]
    design_var_dict["is_bypass_ok"] = [0, 0.99]
    design_var_dict["tsf_split_frac"] = [0, 0.7]

    return design_var_dict

def get_design_vars_opt():
    
    design_var_dict = {}
    
    design_var_dict["is_PR_fixed"] = [3.67, 10.3]     # MPa
    design_var_dict["UA_recup_tot_des"] = [100, 2270]   # kW/K
    design_var_dict["LTR_UA_split"] = [0,1]
    design_var_dict["is_recomp_ok"] = [0, 0.23]	    # < 0 = fix f_recomp to abs(input)
    design_var_dict["partial_IP"] = [0,0.54]
    design_var_dict["is_bypass_ok"] = [0, 0.66]
    design_var_dict["tsf_split_frac"] = [0.389, 0.54]

    return design_var_dict

if __name__ == "__main__":
    pass