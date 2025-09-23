
def calc_errors(full_dict, return_dict):
    
    # Full dict has ALL keys
    # Return dict is a partial dict that we'll assign error keys to

    NVal = len(full_dict['cycle_config'])

    return_dict['is_LTR_flip'] = []
    return_dict['is_HTR_flip'] = []
    return_dict['energy_balance_error'] = []
    return_dict['ltr_temp_down'] = []
    return_dict['htr_temp_down'] = []

    for i in range(NVal):

        T_mc_in = full_dict['T_state_points_0_0'][i]
        T_mc_out = full_dict['T_state_points_1_0'][i]
        T_ltr_hp_out = full_dict['T_state_points_2_0'][i]
        T_mixer_out = full_dict['T_state_points_3_0'][i]
        T_htr_hp_out = full_dict['T_state_points_4_0'][i]
        T_turb_in = full_dict['T_state_points_5_0'][i]
        T_turb_out = full_dict['T_state_points_6_0'][i]
        T_htr_lp_out = full_dict['T_state_points_7_0'][i]
        T_ltr_lp_out = full_dict['T_state_points_8_0'][i]
        T_rc_out = full_dict['T_state_points_9_0'][i]
        T_pc_in = full_dict['T_state_points_10_0'][i]
        T_pc_out = full_dict['T_state_points_11_0'][i]
        T_bypass_out = full_dict['T_state_points_12_0'][i]
        T_mixer2_out = full_dict['T_state_points_13_0'][i]
        T_turb2_out = full_dict['T_state_points_14_0'][i]

        cycle_config = full_dict['cycle_config'][i]

        # Check temperatures at heat exchangers
        is_LTR_flip = 0
        is_HTR_flip = 0
        ltr_temp_down = 0
        htr_temp_down = 0
        match(cycle_config):
            
            # Recompression
            case(1):

                # LTR cold side hotter than hot side
                if T_mc_out > T_htr_lp_out:
                    is_LTR_flip = 1

                # HTR cold side hotter than hot side
                if T_mixer_out > T_turb_out:
                    is_HTR_flip = 1

                # LTR temps wrong direction
                if T_mc_out > T_ltr_hp_out:
                    ltr_temp_down = 1
                if T_htr_lp_out < T_ltr_lp_out:
                    ltr_temp_down = 1

                # HTR temps wrong direction
                if T_mixer_out > T_htr_hp_out:
                    htr_temp_down = 1
                if T_turb_out < T_htr_lp_out:
                    htr_temp_down = 1

            # Partial
            case(2):

                # LTR cold side hotter than hot side
                if T_mc_out > T_htr_lp_out:
                    is_LTR_flip = 1

                # HTR cold side hotter than hot side
                if T_mixer_out > T_turb_out:
                    is_HTR_flip = 1

                # LTR temps wrong direction
                if T_mc_out > T_ltr_hp_out:
                    ltr_temp_down = 1
                if T_htr_lp_out < T_ltr_lp_out:
                    ltr_temp_down = 1

                # HTR temps wrong direction
                if T_mixer_out > T_htr_hp_out:
                    htr_temp_down = 1
                if T_turb_out < T_htr_lp_out:
                    htr_temp_down = 1

            # HTR Bypass
            case(3):

                # LTR cold side hotter than hot side
                if T_mc_out > T_htr_lp_out:
                    is_LTR_flip = 1

                # HTR cold side hotter than cold side
                if T_htr_hp_out > T_turb_out:
                    is_HTR_flip = 1

                # LTR temps wrong direction
                if T_mc_out > T_ltr_hp_out:
                    ltr_temp_down = 1
                if T_htr_lp_out < T_ltr_lp_out:
                    ltr_temp_down = 1

                # HTR temps wrong direction
                if T_mixer_out > T_htr_hp_out:
                    htr_temp_down = 1
                if T_turb_out < T_htr_lp_out:
                    htr_temp_down = 1

            # TSF
            case(4):

                # LTR cold side hotter than hot side
                if (T_mc_out > T_turb2_out):
                    is_LTR_flip = 1

                # HTR cold side hotter than hot side
                if (T_mc_out > T_turb_out):
                    is_HTR_flip = 1

                # LTR temps wrong direction
                if T_mc_out > T_ltr_hp_out:
                    ltr_temp_down = 1
                if T_turb2_out < T_ltr_lp_out:
                    ltr_temp_down = 1

                # HTR temps wrong direction
                if T_mc_out > T_htr_hp_out:
                    htr_temp_down = 1
                if T_turb_out < T_htr_lp_out:
                    htr_temp_down = 1

        # Calculate energy balance error
        eta_thermal_calc = full_dict['eta_thermal_calc'][i]
        q_dot_in_total = full_dict['q_dot_in_total'][i]
        mc_cooler_q_dot = full_dict['mc_cooler_q_dot'][i]
        pc_cooler_q_dot = full_dict['pc_cooler_q_dot'][i]
        energy_balance_error = (q_dot_in_total * (1 - eta_thermal_calc)) - (mc_cooler_q_dot + pc_cooler_q_dot)


        return_dict['is_LTR_flip'].append(is_LTR_flip)
        return_dict['is_HTR_flip'].append(is_HTR_flip)
        return_dict['ltr_temp_down'].append(ltr_temp_down)
        return_dict['htr_temp_down'].append(htr_temp_down)
        return_dict['energy_balance_error'].append(energy_balance_error)
    
    


