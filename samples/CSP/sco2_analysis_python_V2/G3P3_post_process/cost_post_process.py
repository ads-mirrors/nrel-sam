import math
import os
import sys
import pickle
import json


parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
plottingDir = os.path.join(parentDir, "G3P3_analysis_plotting")
sys.path.append(plottingDir)
exampleDir = os.path.join(parentDir, "example")
sys.path.append(exampleDir)

import sco2_filenames
from sco2_plot_g3p3_baseline_FINAL import open_pickle
import design_point_examples as design_pt
import phx_costs

global_var_dict = {}
g3p3_json_dict = {}
is_global_var = False

def initialize_global_var():
    local_var_dict = {}

    json_file_path = os.path.join(parentDir, 'local_var.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            local_var_dict = json.load(json_file)

    global global_var_dict
    global is_global_var
    global_var_dict = local_var_dict
    is_global_var = True

    g3p3_json_filename = global_var_dict["g3p3_json_filename"]
    with open(g3p3_json_filename, 'r') as json_file:
        local_g3p3_json = json.load(json_file)

    global g3p3_json_dict
    g3p3_json_dict = local_g3p3_json

tol = 0.0001

# Utility Functions

def sum_w_NaN(result_dict, id, keys):
    val_sum = 0
    for key in keys:
        if key in result_dict:
            val = result_dict[key][id]
            if val != '':
                if math.isnan(val) == False:
                    val_sum += val
    return val_sum

def compare_vals(val1, val2, tol):
    if val1 == val2:
        return True
    
    if (val1 == 0) or (val2 == 0):
        if abs(val1 - val2) > tol:
            return False
        else:
            return True
        
    if abs((val1/val2) - 1) > tol:
        return False
    
    return True


def calculate_cycle_cost(result_dict, id):

    # Recalculates sco2 cycle costs and returns dict of results

    recup_equip_vars = ["LTR_cost_equipment", "HTR_cost_equipment"]
    recup_bare_erected_vars = ["LTR_cost_bare_erected", "HTR_cost_bare_erected"]

    cycle_vars = ["mc_cost_bare_erected", "rc_cost_bare_erected",
                  "pc_cost_bare_erected", "PHX_cost_bare_erected",
                  "BPX_cost_bare_erected", "t_cost_bare_erected",
                  "t2_cost_bare_erected", "mc_cooler_cost_bare_erected",
                  "pc_cooler_cost_bare_erected","piping_inventory_etc_cost", 
                  *recup_bare_erected_vars]
    
    # Calculate Cycle Cost
    cycle_cost_M = sum_w_NaN(result_dict, id, cycle_vars)    # M$

    # Calculate cycle specific cost
    cycle_cost = cycle_cost_M * 1e6                     # $
    W_dot_net_des_MW = result_dict["W_dot_net_des"][id] # MW
    W_dot_net_des_kW = W_dot_net_des_MW * 1000          # kW
    cycle_spec_cost = cycle_cost / W_dot_net_des_kW     # $/kW

    # Calculate cycle specific cost thermal
    eta_thermal_calc = result_dict["eta_thermal_calc"][id]
    cycle_spec_cost_thermal = cycle_cost / (W_dot_net_des_kW / eta_thermal_calc)    # $/kW

    # Calculate Recuperator equipment and bare erected total cost
    recup_total_cost_equipment = sum_w_NaN(result_dict, id, recup_equip_vars)
    recup_total_cost_bare_erected = sum_w_NaN(result_dict, id, recup_bare_erected_vars)


    # Assign return dict
    return_dict = {}
    return_dict["cycle_cost"] = cycle_cost_M                            # M$
    return_dict["cycle_spec_cost"] = cycle_spec_cost                    # $/kW
    return_dict["cycle_spec_cost_thermal"] = cycle_spec_cost_thermal    # $/kW
    return_dict["recup_total_cost_equipment"] = recup_total_cost_equipment          # M$
    return_dict["recup_total_cost_bare_erected"] = recup_total_cost_bare_erected    # M$

    return_dict["plant_spec_cost"] = cycle_spec_cost                    # $/kW
    return_dict["csp.pt.cost.power_block"] = cycle_cost                 # $

    return return_dict

def calculate_system_installed_cost(result_dict, id, back_calc):

    # Define keys that sum to ui direct subtotal
    ui_direct_subtotal_vars = ["csp.pt.cost.site_improvements", "csp.pt.cost.heliostats",
                               "csp.pt.cost.tower", "csp.pt.cost.receiver",
                               "receiver_lift_cost", "csp.pt.cost.storage",
                               "csp.pt.cost.power_block", "heater_cost",
                               "csp.pt.cost.bop", "csp.pt.cost.fossil"]
    
    # Calculate ui direct subtotal
    ui_direct_subtotal_calc = sum_w_NaN(result_dict, id, ui_direct_subtotal_vars) # $
    
    # Calculate contingency cost (csp.pt.cost.contingency)
    csp_pt_cost_contingency_calc = (g3p3_json_dict["contingency_rate"] / 100.0) * ui_direct_subtotal_calc

    # Calculate total direct cost
    total_direct_cost_calc = ui_direct_subtotal_calc + csp_pt_cost_contingency_calc # $

    # Back Calculate total land area (if necessary)
    if back_calc == True:

        sales_tax_cost_backcalc = (total_direct_cost_calc 
                           * (g3p3_json_dict["sales_tax_frac"] / 100.0) 
                           * (g3p3_json_dict["sales_tax_rate"] / 100.0))           # $

        total_indirect_cost_backcalc = (result_dict["total_installed_cost"][id] 
                                        - result_dict["total_direct_cost"][id])

        total_land_cost_backcalc = (total_indirect_cost_backcalc
                                    - result_dict["csp.pt.cost.epc.total"][id]
                                    - sales_tax_cost_backcalc)

        nameplate = result_dict["nameplate"][id]                    # MWe
        plant_net_capacity_calc = nameplate                         # MWe

        total_land_area_backcalc = (total_land_cost_backcalc 
                           - (total_direct_cost_calc * (g3p3_json_dict["csp.pt.cost.plm.percent"]/100))
                           - (plant_net_capacity_calc * 1e6 * g3p3_json_dict["csp.pt.cost.plm.per_watt"])
                           - g3p3_json_dict["csp.pt.cost.plm.fixed"]) / g3p3_json_dict["land_spec_cost"]    # acre
        
        # Assign back calculated values to result dict
        back_calc_dict = {}
        back_calc_dict["csp.pt.cost.sales_tax.total"] = sales_tax_cost_backcalc
        back_calc_dict["total_indirect_cost"] = total_indirect_cost_backcalc
        back_calc_dict["csp.pt.cost.plm.total"] = total_land_cost_backcalc
        back_calc_dict["total_land_area"] = total_land_area_backcalc
        for key in back_calc_dict:
            if (key in result_dict) == False:
                result_dict[key] = []
            while len(result_dict[key]) < id + 1:
                result_dict[key].append('')
            result_dict[key][id] = back_calc_dict[key]

    # Calculate total land cost
    nameplate = result_dict["nameplate"][id]                    # MWe
    system_capacity = nameplate * 1e3                           # kWe
    plant_net_capacity_calc = system_capacity * 1e-3            # MWe
    total_land_cost_calc = ((result_dict["total_land_area"][id] * g3p3_json_dict["land_spec_cost"])
                            + (total_direct_cost_calc * (g3p3_json_dict["csp.pt.cost.plm.percent"]/100))
                            + (plant_net_capacity_calc * 1e6 * g3p3_json_dict["csp.pt.cost.plm.per_watt"])
                            + g3p3_json_dict["csp.pt.cost.plm.fixed"])         # $

    # Calculate EPC and Owner cost
    epc_and_owner_cost_calc = ((result_dict["total_land_area"][id] * g3p3_json_dict["csp.pt.cost.epc.per_acre"])
                               + (total_direct_cost_calc * g3p3_json_dict["csp.pt.cost.epc.percent"] / 100)
                               + (plant_net_capacity_calc * 1e6 * g3p3_json_dict["csp.pt.cost.epc.per_watt"])
                               + g3p3_json_dict["csp.pt.cost.epc.fixed"])      # $

    # Calculate sales tax cost
    sales_tax_cost_calc = (total_direct_cost_calc 
                           * (g3p3_json_dict["sales_tax_frac"] / 100.0) 
                           * (g3p3_json_dict["sales_tax_rate"] / 100.0))           # $

    # Calculate Total Indirect Cost
    total_indirect_cost_calc = total_land_cost_calc + epc_and_owner_cost_calc + sales_tax_cost_calc  # $

    # Calculate Total Installed Cost
    total_installed_cost_calc = total_direct_cost_calc + total_indirect_cost_calc   # $

    # Calculate Estimated Installed Cost per cap
    estimated_installed_cost_per_cap_calc = total_installed_cost_calc / (plant_net_capacity_calc * 1e3)  # $/kWe

    # Calculate Receiver flux per solar field area
    q_dot_rec_per_A_sf_calc = (result_dict["q_dot_rec_des_total"][id] * 1e6) / result_dict["A_sf"][id]  # W/m2

    # Calculate W_dot_net_ish
    W_dot_cycle_parasitic_input = result_dict["W_dot_net_des"][id] * result_dict["fan_power_frac"][id]  # MWe
    P_tower_lift_des_spec = result_dict["P_tower_lift_des"][id] / result_dict["solarm"][id]             # MWe
    W_dot_net_ish_calc = (result_dict["P_ref"][id] - result_dict["W_dot_cycle_lift_des"][id] 
                          - W_dot_cycle_parasitic_input - P_tower_lift_des_spec)                        # MWe

    # Calculate $/kWe
    cost_per_kWe_gross_calc = total_installed_cost_calc / (result_dict["W_dot_net_des"][id] * 1e3)      # $/kWe
    cost_per_kWe_net_ish_calc = total_installed_cost_calc / (W_dot_net_ish_calc * 1e3)                  # $/kWe

    # Assign return dict
    return_dict = {}
    return_dict["ui_direct_subtotal"] = ui_direct_subtotal_calc             # $
    return_dict["csp.pt.cost.contingency"] = csp_pt_cost_contingency_calc   # $
    return_dict["total_direct_cost"] = total_direct_cost_calc               # $
    return_dict["csp.pt.cost.plm.total"] = total_land_cost_calc             # $
    return_dict["csp.pt.cost.epc.total"] = epc_and_owner_cost_calc          # $
    return_dict["csp.pt.cost.sales_tax.total"] = sales_tax_cost_calc        # $
    return_dict["total_indirect_cost"] = total_indirect_cost_calc           # $
    return_dict["total_installed_cost"] = total_installed_cost_calc         # $
    #return_dict["csp.pt.cost.installed_per_capacity"] = estimated_installed_cost_per_cap_calc    # $/kWe
    return_dict["q_dot_rec_per_A_sf"] = q_dot_rec_per_A_sf_calc             # W/m2
    return_dict["W_dot_net_ish"] = W_dot_net_ish_calc                       # MWe
    return_dict["cost_per_kWe_gross"] = cost_per_kWe_gross_calc             # $/kWe
    return_dict["cost_per_kWe_net_ish"] = cost_per_kWe_net_ish_calc         # $/kWe

    return return_dict

def is_phx_carlson(result_dict, id):

    UA_PHX = result_dict["UA_PHX"][id] * 1e6          # W/K
    phx_cost_equip_new, phx_cost_bare_erected_new = phx_costs.carlson_2021(UA_PHX, 0, 0)    # $

    phx_cost_equip_new = phx_cost_equip_new / 1e6                           # M$
    phx_cost_bare_erected_new = phx_cost_bare_erected_new / 1e6             # M$

    phx_cost_equip_orig = result_dict["PHX_cost_equipment"][id]             # M$
    phx_cost_bare_erected_orig = result_dict["PHX_cost_bare_erected"][id]   # M$

    if compare_vals(phx_cost_equip_orig, phx_cost_equip_new, tol) == False:
        print("Original not carlson")
        return False
    if compare_vals(phx_cost_bare_erected_orig, phx_cost_bare_erected_new, tol) == False:
        print("Original not carlson")
        return False
    
    if "BPX_cost_equipment" in result_dict:
        if result_dict["BPX_cost_equipment"][id] > 0:
            UA_BPX = result_dict["UA_BPX"][id] * 1e6           # MW/K
            bpx_cost_equip_new, bpx_cost_bare_erected_new = phx_costs.carlson_2021(UA_BPX, 0, 0)    # $

            bpx_cost_equip_new = bpx_cost_equip_new / 1e6                           # M$
            bpx_cost_bare_erected_new = bpx_cost_bare_erected_new / 1e6             # M$

            bpx_cost_equip_orig = result_dict["BPX_cost_equipment"][id]             # M$
            bpx_cost_bare_erected_orig = result_dict["BPX_cost_bare_erected"][id]   # M$

            if compare_vals(bpx_cost_equip_orig, bpx_cost_equip_new, tol) == False:
                print("Original not carlson")
                return False
            if compare_vals(bpx_cost_bare_erected_orig, bpx_cost_bare_erected_new, tol) == False:
                print("Original not carlson")
                return False
            
    return True
    

###################

# Changes the cost of specfied keys, and updates sco2 total cost, and csp installed costs
# Check that the tests are using the correct values (recup or TES)
def change_csp_cost(result_dict, cost_keys, cost_factor, change_type=""):

    # Loop through each case
    NVal = len(result_dict["cycle_config"])
    for id in range(NVal):
        success = result_dict["cmod_success"][id]
        if success != True:
            continue
        # Validate sco2 cycle cost
        cycle_cost_orig = result_dict["cycle_cost"][id] # M$
        cycle_cost_no_recup_orig = (cycle_cost_orig 
                                    - result_dict["LTR_cost_bare_erected"][id] 
                                    - result_dict["HTR_cost_bare_erected"][id]) # M$
        cycle_cost_dict_orig = calculate_cycle_cost(result_dict, id)
        for key in cycle_cost_dict_orig:
            orig = result_dict[key][id]
            validate = cycle_cost_dict_orig[key]
            if compare_vals(orig, validate, tol) == False:
                print("Mismatch sco2 cycle cost validation")
                return

        # Validate system total installed cost
        ui_direct_subtotal_orig = result_dict["ui_direct_subtotal"][id]     # $
        ui_direct_subtotal_no_cycle_cost_orig = ui_direct_subtotal_orig - (cycle_cost_orig * 1e6)   # $
        ui_direct_subtotal_no_tes_orig = ui_direct_subtotal_orig - result_dict["csp.pt.cost.storage"][id]   # $
        ui_direct_subtotal_no_helio_orig = ui_direct_subtotal_orig - result_dict["csp.pt.cost.heliostats"][id]   # $
        system_cost_dict_orig = calculate_system_installed_cost(result_dict, id, True)
        for key in system_cost_dict_orig:
            orig = result_dict[key][id]
            validate = system_cost_dict_orig[key]
            if compare_vals(orig, validate, tol) == False:
                print("Mismatch Total Installed Cost validation")
                return


        # Modify cost
        for key in cost_keys:
            val_orig = result_dict[key][id]
            val_new = val_orig * cost_factor
            result_dict[key][id] = val_new

        # Recalculate cycle Cost
        cycle_cost_dict_new = calculate_cycle_cost(result_dict, id)

        # Apply new cycle costs
        for key in cycle_cost_dict_new:
            result_dict[key][id] = cycle_cost_dict_new[key]
        cycle_cost_new = result_dict["cycle_cost"][id]

        # Recalculate System Cost
        system_cost_dict_new = calculate_system_installed_cost(result_dict, id, False)

        # Apply new system costs
        for key in system_cost_dict_new:
            result_dict[key][id] = system_cost_dict_new[key]
        ui_direct_subtotal_new = result_dict["ui_direct_subtotal"][id]

        if change_type == "recup":
            # Special test for recuperator
            cycle_cost_no_recup_new = (cycle_cost_new 
                                        - result_dict["LTR_cost_bare_erected"][id] 
                                        - result_dict["HTR_cost_bare_erected"][id])
            ui_direct_subtotal_no_cycle_cost_new = ui_direct_subtotal_new - (cycle_cost_new * 1e6)   # $
            if compare_vals(cycle_cost_no_recup_orig, cycle_cost_no_recup_new, tol) == False:
                print("Cycle costs minus recup do not equal")
                return
            if compare_vals(ui_direct_subtotal_no_cycle_cost_orig, ui_direct_subtotal_no_cycle_cost_new, tol) == False:
                print("UI direct subtotal minus cycle cost do not equal")
                return

        if change_type == "tes":
            # Test total installed cost without power cycle
            ui_direct_subtotal_no_tes_new = ui_direct_subtotal_new - (result_dict["csp.pt.cost.storage"][id])   # $
            if compare_vals(ui_direct_subtotal_no_tes_orig, ui_direct_subtotal_no_tes_new, tol) == False:
                print("UI direct subtotal cost minus tes cost do not equal")
                return
            
        elif change_type == "helio":
            # Test ui direct subtotal without heliostat field
            ui_direct_subtotal_no_helio_new = ui_direct_subtotal_new - (result_dict["csp.pt.cost.heliostats"][id])  # $
            if compare_vals(ui_direct_subtotal_no_helio_orig, ui_direct_subtotal_no_helio_new, tol) == False:
                print("UI direct subtotal cost minus helio cost do not equal")
                return

    return result_dict

# Changes the cost of phx, and updates sco2 total cost and csp installed costs
def change_phx_cost(result_dict, phx_cost_func):

    # Loop through each case
    NVal = len(result_dict["cycle_config"])
    for id in range(NVal):
        success = result_dict["cmod_success"][id]
        if success != True:
            continue

        is_BP = False
        if "BPX_cost_equipment" in result_dict:
            if result_dict["BPX_cost_equipment"][id] > 0:
                is_BP == True

        # Validate sco2 cycle cost
        cycle_cost_orig = result_dict["cycle_cost"][id] # M$
        cycle_cost_no_phx_bpx_orig = cycle_cost_orig - result_dict["PHX_cost_bare_erected"][id]  # M$
        if is_BP:
            cycle_cost_no_phx_bpx_orig -= result_dict["BPX_cost_bare_erected"][id]               # M$
                                    
        cycle_cost_dict_orig = calculate_cycle_cost(result_dict, id)
        for key in cycle_cost_dict_orig:
            orig = result_dict[key][id]
            validate = cycle_cost_dict_orig[key]
            if compare_vals(orig, validate, tol) == False:
                print("Mismatch sco2 cycle cost validation")
                return

        # Validate system total installed cost
        ui_direct_subtotal_orig = result_dict["ui_direct_subtotal"][id]     # $
        ui_direct_subtotal_no_cycle_cost_orig = ui_direct_subtotal_orig - (cycle_cost_orig * 1e6)   # $
        system_cost_dict_orig = calculate_system_installed_cost(result_dict, id, True)
        for key in system_cost_dict_orig:
            orig = result_dict[key][id]
            validate = system_cost_dict_orig[key]
            if compare_vals(orig, validate, tol) == False:
                print("Mismatch Total Installed Cost validation")
                return

        # Modify Costs
        U = 350 # W/m2 K
        inflation_yr = 2024

        # First check if phx costs are carlson
        carlson_flag = is_phx_carlson(result_dict, id)
        if carlson_flag == False:
            print("Not carlson original")
            return

        # Modify PHX
        UA_PHX = result_dict["UA_PHX"][id]          # MW/K
        phx_cost_equip, phx_cost_bare_erected = phx_cost_func(UA_PHX * 1e6, U, inflation_yr)  # $ 
        result_dict["PHX_cost_equipment"][id] = phx_cost_equip / 1e6                # M$
        result_dict["PHX_cost_bare_erected"][id] = phx_cost_bare_erected / 1e6      # M$
        
        # Modify BPX
        if is_BP:
            UA_bpx = result_dict["UA_BPX"][id]          # MW/K
            bpx_cost_equip, bpx_cost_bare_erected = phx_cost_func(UA_bpx * 1e6, U, inflation_yr)  # $ 
            result_dict["BPX_cost_equipment"][id] = bpx_cost_equip / 1e6                # M$
            result_dict["BPX_cost_bare_erected"][id] = bpx_cost_bare_erected / 1e6      # M$

        # Recalculate cycle Cost
        cycle_cost_dict_new = calculate_cycle_cost(result_dict, id)

        # Apply new cycle costs
        for key in cycle_cost_dict_new:
            result_dict[key][id] = cycle_cost_dict_new[key]
        cycle_cost_new = result_dict["cycle_cost"][id]

        # Recalculate System Cost
        system_cost_dict_new = calculate_system_installed_cost(result_dict, id, False)

        # Apply new system costs
        for key in system_cost_dict_new:
            result_dict[key][id] = system_cost_dict_new[key]
        ui_direct_subtotal_new = result_dict["ui_direct_subtotal"][id]

        # Special test for recuperator
        cycle_cost_no_phx_bpx_new = cycle_cost_new - result_dict["PHX_cost_bare_erected"][id]  # M$
        if is_BP:
            cycle_cost_no_phx_bpx_new -= result_dict["BPX_cost_bare_erected"][id]               # M$
        if compare_vals(cycle_cost_no_phx_bpx_orig, cycle_cost_no_phx_bpx_new, tol) == False:
            print("Cycle costs minus PHX(s) do not equal")
            return
        
        # Test total installed cost without power cycle
        ui_direct_subtotal_no_cycle_cost_new = ui_direct_subtotal_new - (cycle_cost_new * 1e6)   # $
        if compare_vals(ui_direct_subtotal_no_cycle_cost_orig, ui_direct_subtotal_no_cycle_cost_new, tol) == False:
            print("UI direct subtotal cost minus pb cost do not equal")
            return

    return result_dict  

# Handles file IO and calls change_csp_cost or change_phx_cost
def modify_baseline(cost_keys, cost_factor, mod_name, change_type="", phx_cost_func=None, filenames=[]):

    # Get baseline filenames (if necessary)
    if len(filenames) == 0:
        filenames, _ = sco2_filenames.get_filenames_baseline(split=False)

    # Open cases
    result_dict_list = []
    for filename in filenames:
        result_dict_list.append(open_pickle(filename))

    # Modify result dicts
    result_dict_modified_list = []
    for result_dict in result_dict_list:

        if phx_cost_func == None:
            result_dict_modified = change_csp_cost(result_dict, cost_keys, cost_factor, change_type)
        else:
            result_dict_modified = change_phx_cost(result_dict, phx_cost_func)

        if result_dict_modified == None:
            print("Conversion Failed")
            return
        result_dict_modified_list.append(result_dict_modified)
    
    # Save result dicts
    parent_folder = os.path.dirname(filenames[0])
    folder_name = mod_name + "_" + design_pt.get_time_string()
    save_folder_path = os.path.join(parent_folder, folder_name)
    if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

    for i in range(len(filenames)):
        filename = filenames[i]
        save_dict = result_dict_modified_list[i]

        file_basename = mod_name + "_" + os.path.basename(filename)
        save_filename = os.path.join(save_folder_path, file_basename)

        with open(save_filename, "wb") as f:
            pickle.dump(save_dict, f)


    return

###################

def post_process_recup():

    # Define vars to change
    recup_vars = ["LTR_cost_equipment", "LTR_cost_bare_erected",
                "HTR_cost_equipment", "HTR_cost_bare_erected"]

    #modify_baseline(recup_vars, 0.5, "recup50", "recup")
    #modify_baseline(recup_vars, 1.5, "recup150", "recup")
    modify_baseline(recup_vars, 10, "recup1000", "recup")

    x = 0

def post_process_tes():

    # Define vars to change
    tes_vars = ["csp.pt.cost.storage"]

    #modify_baseline(tes_vars, 0.5, "tes50", "tes")
    #modify_baseline(tes_vars, 1.5, "tes150", "tes")
    modify_baseline(tes_vars, 10, "tes1000", "tes")

    x = 0

def post_process_phx():
    #modify_baseline([], None, "phx", "phxbl0", phx_costs.buck_low_2021)
    #modify_baseline([], None, "phx", "phxbhi", phx_costs.buck_high_2021)
    modify_baseline([], None, "phxh10", "phx", phx_costs.buck_highx10_2021)

def post_process_helio_phx():
    helio_filenames, _ = sco2_filenames.get_filenames_heliocost(split=False)

    modify_baseline([], None, "1", "phx", phx_costs.buck_high_2021, helio_filenames)

def post_process_helio():
    # Define vars to change
    helio_vars = ["csp.pt.cost.heliostats"]

    #modify_baseline(recup_vars, 0.5, "recup50", "recup")
    #modify_baseline(recup_vars, 1.5, "recup150", "recup")
    modify_baseline(helio_vars, 100, "h100", "helio")

if __name__ == "__main__":
    initialize_global_var()
    #post_process_tes()
    #post_process_recup()
    #post_process_phx()
    #post_process_helio_phx()
    post_process_helio()
    pass