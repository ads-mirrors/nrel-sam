def get_core_var_list():
    # Define variables needed for plotting

    sco2_input_vars = [
        "T_htf_hot_des", "dT_PHX_hot_approach", 
        "UA_recup_tot_des", "LTR_design_code", "LTR_UA_des_in", "LTR_min_dT_des_in", "LT_recup_eff_max", "LTR_n_sub_hx",
        "HTR_design_code", "HTR_UA_des_in", "HTR_min_dT_des_in", "HT_recup_eff_max", "HTR_n_sub_hx",
        "cycle_config", "is_recomp_ok", "is_PR_fixed", "is_IP_fixed", "eta_isen_rc", "eta_isen_pc", "eta_isen_t",
        "dT_PHX_cold_approach", "fan_power_frac" 
    ]

    #state_point_labels = ["T_state_points", "P_state_points", "h_state_points", "s_state_points"]

    #state_point_Ts_labels = ["T_LTR_HP_data","s_LTR_HP_data","T_HTR_HP_data","s_HTR_HP_data",
    #                         "T_PHX_data","s_PHX_data","T_HTR_LP_data","s_HTR_LP_data",
    #                         "T_LTR_LP_data","s_LTR_LP_data","T_main_cooler_data","s_main_cooler_data",
    #                         "T_pre_cooler_data","s_pre_cooler_data", "T_turb_in"]
    
    #state_point_Ph_labels = ["P_t_data","h_t_data","P_mc_data","h_mc_data",
    #                         "P_rc_data","h_rc_data","P_pc_data","h_pc_data",
    #                         "P_t2_data","h_t2_data"]

    sco2_solve_vars = ["config_name", "W_dot_net_des", "design_eff", "eta_thermal_calc", "T_htf_cold_des", 
                    "plant_spec_cost", "cycle_cost",
                    "m_dot_htf_cycle_des", "q_dot_in_total",
                    "eta_rec_thermal_des", "V_tes_htf_total_des",
                    "HTR_UA_des_in", "LTR_UA_des_in", 
                    "HTR_UA_calculated", "LTR_UA_calculated", 
                    "recomp_frac", "bypass_frac",
                    "q_dot_BPX", "BPX_cost_bare_erected",
                    'P_state_points_10_0', 'P_state_points_0_0',
                    'pc_cost_bare_erected', 'pc_W_dot',
                    'pc_cost_equipment', 'm_dot_co2_full', 'recup_total_UA_calculated'
                    ]
    
    g3p3_solve_vars = ['total_installed_cost', "csp.pt.cost.storage", "csp.pt.cost.heliostats",
                       'cost_per_kWe_net_ish']


    return [*sco2_input_vars, #*state_point_labels, *state_point_Ts_labels, *state_point_Ph_labels,
            *sco2_solve_vars, *g3p3_solve_vars]


def get_sco2_cost_info_list():

    cycle_cost_info = ['cycle_cost', 'M$', 'Cycle Cost']
    cost_labels = [["mc_cost_bare_erected", "M$", "Main Compressor Cost"],
                    ["rc_cost_bare_erected", "M$", "Recompressor Cost"],
                    ["pc_cost_bare_erected", "M$", "Precompressor Cost"],
                    ["LTR_cost_bare_erected", "M$", "LTR Cost"],
                    ["HTR_cost_bare_erected", "M$", "HTR Cost"],
                    ["PHX_cost_bare_erected", "M$", "Primary Heat Exchanger Cost"],
                    ["BPX_cost_bare_erected", "M$", "Bypass Heat Exchanger Cost"],
                    ["t_cost_bare_erected", "M$", "Turbine Cost"],
                    ["t2_cost_bare_erected", "M$", "Second Turbine Cost"],
                    ["mc_cooler_cost_bare_erected", "M$", "Main Air Cooler Cost"],
                    ["pc_cooler_cost_bare_erected", "M$", "Precompressor Air Cooler Cost"],
                    ["piping_inventory_etc_cost", "M$", "Piping etc Cost"]
                    ]
    
    return [cycle_cost_info, *cost_labels]

def get_csp_cost_info_list():

    total_installed_cost = ["total_installed_cost", "$", "Total Installed Cost"]
    cost_labels = [["csp.pt.cost.site_improvements", "$", "Site Improvements Cost"],
                       ["csp.pt.cost.heliostats", "$", "Heliostats Cost"],
                       ["csp.pt.cost.tower", "$", "Tower Cost"],
                       ["csp.pt.cost.receiver", "$", "Receiver Cost"],
                       ["receiver_lift_cost", "$", "Receiver Lift Cost"],
                       ["csp.pt.cost.storage", "$", "TES Cost"],
                       ["csp.pt.cost.power_block", "$", "Power Block Cost"],
                       ["heater_cost", "$", "Heater Cost"],
                       ["csp.pt.cost.bop", "$", "BOP Cost"],
                       ["csp.pt.cost.fossil", "$", "Fossil Backup Cost"]]
    
    return [total_installed_cost, *cost_labels]

def get_sco2_design_vars_info_list():
    sco2_vars = [["UA_recup_tot_des", "kW/K", "Total Assigned Conductance"],
                 ["LTR_UA_des_in", "", "LTR UA"], 
                 ["HTR_UA_des_in", "", "HTR UA Assigned"],
                 ["is_PR_fixed", "", "Pressure Ratio"], 
                 ["is_IP_fixed", "", "Intermediate Pressure Ratio"], 
                 ["is_recomp_ok", "", "Recompression Fraction"], 
                 ["is_turbine_split_ok", "", "Turbine Split Fraction"],
                 ["is_bypass_ok", "", "Bypass Fraction"]]
    return sco2_vars