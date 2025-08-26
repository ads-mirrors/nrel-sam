import json

import matplotlib.pyplot as plt

import numpy as np

import matplotlib.lines as mlines
import multiprocessing

import sys
import os

newPath = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')

sys.path.append(newPath)

import sco2_cycle_ssc as sco2_solve
import ssc_inout_v2 as ssc_sim
import sco2_plots as cy_plt

sam_g3p3_dict = json.load(open("sam_gen3_particle_for_tmb.json", 'r'))

# Design or annual simulation?
sam_g3p3_dict["sim_type"] = 2

# Set system design parameters based on cycle - these should NOT be defined in JSON
sam_g3p3_dict["P_ref"] = 11.1        # MWe this should be cycle output *before* cooling parasitics
sam_g3p3_dict["design_eff"] = 0.485  # similarly this should be cycle output before cooling parasitics
sam_g3p3_dict["T_htf_cold_des"] = 555    # C
sam_g3p3_dict["T_htf_hot_des"] = 775     # C
sam_g3p3_dict["plant_spec_cost"] = 1000  # $/kWe where kWe is = P_ref
W_dot_cycle_parasitic_input = 0.02   # MWe - Not used in current cmod setup, but need to track for net parasitics below


# Do some design calcs to size receiver and tower
q_dot_rec = sam_g3p3_dict["P_ref"] / sam_g3p3_dict["design_eff"] * sam_g3p3_dict["solarm"]
design_flux_kwm2 = 500     #kW/m2
A_rec = (q_dot_rec*1.E3) / design_flux_kwm2 
side_rec = A_rec**0.5

h_tower_calc = 15.405*(q_dot_rec**0.4479)  # q_dot_rec in MWt -> from Bill's spreadsheet

# Now set tower height and receiver dimensions
sam_g3p3_dict["h_tower"] = h_tower_calc
sam_g3p3_dict["rec_height"] = [side_rec]
sam_g3p3_dict["rec_width"] = [side_rec]

is_financial = False
g3p3_so_solved_dict = ssc_sim.cmod_particle_from_dict(sam_g3p3_dict, is_financial)  # ssc_sim.cmod_mspt_from_dict(sam_mspt_dict)

is_success = g3p3_so_solved_dict["cmod_success"]    
print ('SSC simulation(s) successful = ', is_success)
if (is_success == 1):

    if g3p3_so_solved_dict["sim_type"] == 1:

        annual_energy = g3p3_so_solved_dict["annual_energy"]
        print ('Annual energy (year 1) = ', annual_energy)
        flip_actual_irr = g3p3_so_solved_dict["flip_actual_irr"]
        print ('Internal rate of return (IRR) = ', flip_actual_irr)
        #print('Rec W_dot = ', g3p3_so_solved_dict["W_dot_rec_pump_rec_share_des"])
        # print('Q TES SAM = ', g3p3_so_solved_dict["Q_tes_des"])
        # print('diff Q TES = ', g3p3_so_solved_dict["Q_tes_des"]/q_tes_calc)
        # print("W_dot_cycle_pump = ", g3p3_so_solved_dict["W_dot_cycle_pump_des"])
        # print("q_dot_rec_des = ", g3p3_so_solved_dict["q_dot_rec_des"])
        # print("solar_mult_calc = ", g3p3_so_solved_dict["solar_mult_calc"])
        print("lcoe real = ", g3p3_so_solved_dict["lcoe_real"])
        print("total installed cost = ", g3p3_so_solved_dict["total_installed_cost"])
        # print("Hot hours revenue fraction = ", g3p3_so_solved_dict["hot_hours_revenue_fraction"])
        # print("All hours revenue fraction = ", g3p3_so_solved_dict["all_hours_revenue_fraction"])
        # print("Hot hours electricity sales = ", g3p3_so_solved_dict["hot_hours_electricity_sales"])
        # print("All hours electricity sales = ", g3p3_so_solved_dict["all_hours_electricity_sales"])

    else:

        "Design from cycle design"
        print("P ref = ", sam_g3p3_dict["P_ref"])
        print("eta = ", sam_g3p3_dict["design_eff"])
        print("T htf cold = ", sam_g3p3_dict["T_htf_cold_des"])
        print("T htf hot = ", sam_g3p3_dict["T_htf_hot_des"])
        print("plant spec cost = ", sam_g3p3_dict["plant_spec_cost"])

        # solar field
        A_sf = g3p3_so_solved_dict["A_sf"][0]
        print("A sf = ", A_sf)

        # receiver
        q_dot_rec_des = g3p3_so_solved_dict["q_dot_rec_des"]
        eta_rec_thermal_des = g3p3_so_solved_dict["eta_rec_thermal_des"]
        P_tower_lift_des = g3p3_so_solved_dict["P_tower_lift_des"]
        Q_transport_loss_des = g3p3_so_solved_dict["Q_transport_loss_des"]
        m_dot_htf_rec_des = g3p3_so_solved_dict["m_dot_htf_rec_des"]
        h_tower = g3p3_so_solved_dict["h_tower_calc"]
        w_rec_calc = g3p3_so_solved_dict["rec_width_calc"][0]
        print("q_dot_rec_des = ", q_dot_rec_des)
        print("eta rec therm = ", eta_rec_thermal_des)
        print("P tower lift = ", P_tower_lift_des)
        print("q transport loss = ", Q_transport_loss_des)
        print("m dot htf rec des = ", m_dot_htf_rec_des)
        print("h tower calc = ", h_tower)
        print("w rec calc = ", w_rec_calc)

        q_dot_rec_per_A_sf = q_dot_rec_des*1E6 / A_sf   # W/m2
        print("q dot rec per A sf W/m2 = ", q_dot_rec_per_A_sf)

        # cycle
        W_dot_cycle_des = g3p3_so_solved_dict["P_ref"]
        m_dot_htf_cycle_des = g3p3_so_solved_dict["m_dot_htf_cycle_des"]
        q_dot_cycle_des = g3p3_so_solved_dict["q_dot_cycle_des"]
        W_dot_cycle_lift_des = g3p3_so_solved_dict["W_dot_cycle_lift_des"]
        W_dot_cycle_cooling_des = g3p3_so_solved_dict["W_dot_cycle_cooling_des"]
        print("W dot cycle des = ", W_dot_cycle_des)
        print("m dot htf cycle des = ", m_dot_htf_cycle_des)
        print("q dot cycle des = ", q_dot_cycle_des)
        print("W dot cycle lift des = ", W_dot_cycle_lift_des)
        print("W dot cycle cooling des = ", W_dot_cycle_cooling_des)

        #TES
        Q_tes_des = g3p3_so_solved_dict["Q_tes_des"]
        V_tes_htf_total_des = g3p3_so_solved_dict["V_tes_htf_total_des"]  # Tank volume
        print("q tes des = ", Q_tes_des)
        print("V tes = ", V_tes_htf_total_des)

        #BOP
        nameplate = g3p3_so_solved_dict["nameplate"]
        W_dot_bop_design = g3p3_so_solved_dict["W_dot_bop_design"]
        W_dot_fixed = g3p3_so_solved_dict["W_dot_fixed"]
        print("nameplate = ", nameplate)
        print("W dot bop des = ", W_dot_bop_design)
        print("W dot fixed = ", W_dot_fixed)

        W_dot_net_ish = W_dot_cycle_des - W_dot_cycle_parasitic_input - W_dot_cycle_lift_des - P_tower_lift_des

        # Costs
        cost_site = g3p3_so_solved_dict["csp.pt.cost.site_improvements"]
        cost_helio = g3p3_so_solved_dict["csp.pt.cost.heliostats"]
        cost_tower = g3p3_so_solved_dict["csp.pt.cost.tower"]
        cost_rec = g3p3_so_solved_dict["csp.pt.cost.receiver"]
        cost_rec_lift = g3p3_so_solved_dict["receiver_lift_cost"]
        cost_storage = g3p3_so_solved_dict["csp.pt.cost.storage"]
        cost_tes_medium = g3p3_so_solved_dict["tes_medium_cost"]
        cost_tes_bin = g3p3_so_solved_dict["tes_bin_cost"]
        cost_tes_lift = g3p3_so_solved_dict["tes_lift_cost"]
        cost_phx_lift = g3p3_so_solved_dict["phx_lift_cost"]
        cost_cycle = g3p3_so_solved_dict["csp.pt.cost.power_block"]
        cost_bop = g3p3_so_solved_dict["csp.pt.cost.bop"]   # should be 0 - sco2 cycle cost model includes PHX
        cost_fossil = g3p3_so_solved_dict["csp.pt.cost.fossil"] # shoud be 0
        cost_direct_sub = g3p3_so_solved_dict["ui_direct_subtotal"]
        cost_contingency = g3p3_so_solved_dict["csp.pt.cost.contingency"]
        cost_direct = g3p3_so_solved_dict["total_direct_cost"]
        cost_indirect = g3p3_so_solved_dict["csp.pt.cost.epc.total"]
        cost_total_installed = g3p3_so_solved_dict["total_installed_cost"]

        print("cost site = ", cost_site)
        print("cost_helio = ", cost_helio)
        print("cost tower = ", cost_tower)
        print("cost rec = ", cost_rec)
        print("cost rec lift = ", cost_rec_lift)
        print("cost storage = ", cost_storage)
        print("cost tes medium = ", cost_tes_medium)
        print("cost tes bin = ", cost_tes_bin)
        print("cost tes lift = ", cost_tes_lift)
        print("cost phx lift = ", cost_phx_lift)
        print("cost cycle = ", cost_cycle)
        print("cost bop = ", cost_bop)
        print("cost fossil = ", cost_fossil)
        print("cost direct sub = ", cost_direct_sub)
        print("cost contingency = ", cost_contingency)
        print("cost direct = ", cost_direct)
        print("cost indirect = ", cost_indirect)
        print("cost total installed = ", cost_total_installed)

        cost_per_kWe_gross = cost_total_installed / (W_dot_cycle_des*1000)
        print("cost per kwe gross $/kwe = ", cost_per_kWe_gross)

        cost_per_kWe_net_ish = cost_total_installed / (W_dot_net_ish*1000)
        print("cost per kwe net ish $/kwe = ", cost_per_kWe_net_ish)


else:
    print ('FAIL FAIL FAIL FAIL FAIL')


