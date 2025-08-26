import sys
import os
import copy
import matplotlib.pyplot as plt
from tkinter.filedialog import asksaveasfilename
from matplotlib import gridspec

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentDir)
exampleFolder = os.path.join(parentDir, 'example')
coreFolder = os.path.join(parentDir, 'core')
g3p3PlottingFolder = os.path.join(parentDir, 'G3P3_analysis_plotting')
sys.path.append(exampleFolder)
sys.path.append(coreFolder)
sys.path.append(g3p3PlottingFolder)

import sco2_filenames
import data_utility
import design_point_tools as design_tools
from sco2_filenames import BASE

FIG_WIDTH_SMALL = 3.54331   # [in] 90 mm
FIG_WIDTH_MED = 5.51181     # [in] 140 mm
FIG_WIDTH_FULL = 7.48031    # [in] 190 mm
FONT_SIZE_FIG = 7           # figure font size

def write_array_to_file(list_list_data, filename=None):
    
    if filename == None:
        filename = asksaveasfilename(confirmoverwrite=True, filetypes =[('Txt Files', '*.txt')], title="Save?")
    if filename == '':
        return
    
    delimiter = '\t'

    N_col = len(list_list_data[0])
    N_row = len(list_list_data)

    f = open(filename, "w")

    for row in range(N_row):

        for col in range(N_col):
            val = list_list_data[row][col]
            f.write(val)
            
            if(col != N_col - 1):
                f.write(delimiter)
        
        f.write('\n')
    
    f.close()


def plot_comparisons(list_of_best_dict_list_w_kwarg, sweep_label_list, show_sweep_list, Y_info,
                     show_config_list=[], is_norm=False, figsize=None):
    if figsize == None:
        figsize = (6,2.69)
    fontsize = 7

    local_list_best_dict_list_w_kwarg = []
    sweep_label_to_index = {d: i for i, d in enumerate(sweep_label_list)}

    for sweep_label in show_sweep_list:
        index = sweep_label_to_index.get(sweep_label)
        local_list_best_dict_list_w_kwarg.append(list_of_best_dict_list_w_kwarg[index])
    
    design_tools.plot_sweep_cost_comparison(local_list_best_dict_list_w_kwarg, show_sweep_list, show_config_list, Y_info, 
                                            disk_load=True, figsize=figsize, fontsize=fontsize, is_norm=is_norm,
                                            shorten_config_label=True)

def plot_comparisons_duo(list_of_best_dict_list_w_kwarg, sweep_label_list, show_sweep_list, Y_info,
                         show_config_list=[], figsize=(6,2.69), bottom_padding=0.24):
    # Create figure
    fig = plt.figure(figsize=figsize)

    # Set explicit figure margins
    plt.subplots_adjust(
        left=0.10,    # Left margin: 10% of figure width
        right=0.97,  # Right margin: 15% of figure width
        bottom=bottom_padding, # Bottom margin: 15% of figure height
        top=0.98,     # Top margin: 10% of figure height,
        wspace=0.01,
        hspace=0.08
    )

    # Create gridspec with a fixed width ratio
    legend_width_ratio = 0.20  # 20% of figure width for legend
    gs = gridspec.GridSpec(2, 2, width_ratios=[1-legend_width_ratio, legend_width_ratio])

    # Create axes
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[1,0])
    legend_ax = fig.add_subplot(gs[:,1])
    legend_ax.axis('off')

    #fig, (ax1, ax2) = plt.subplots(2,1, figsize=figsize)

    local_list_best_dict_list_w_kwarg = []
    sweep_label_to_index = {d: i for i, d in enumerate(sweep_label_list)}

    for sweep_label in show_sweep_list:
        index = sweep_label_to_index.get(sweep_label)
        local_list_best_dict_list_w_kwarg.append(list_of_best_dict_list_w_kwarg[index])
    
    
    design_tools.plot_sweep_cost_comparison(local_list_best_dict_list_w_kwarg, show_sweep_list, show_config_list, Y_info, 
                                            disk_load=True, figsize=figsize, fontsize=FONT_SIZE_FIG, is_norm=False,
                                            shorten_config_label=True, ax=ax1, showX=False, show_legend=False)
    
    design_tools.plot_sweep_cost_comparison(local_list_best_dict_list_w_kwarg, show_sweep_list, show_config_list, Y_info, 
                                            disk_load=True, figsize=figsize, fontsize=FONT_SIZE_FIG, is_norm=True,
                                            shorten_config_label=True, ax=ax2, show_legend=False)
    
    # Collect handles and labels from both axes
    handles1, labels1 = ax1.get_legend_handles_labels()
    #handles2, labels2 = ax2.get_legend_handles_labels()

    # Add shared legend to the right of the plots, halfway between them
    #fig.legend(handles1, labels1, loc='center right', bbox_to_anchor=(1.0, 0.5), fontsize=fontsize)
    legend = legend_ax.legend(handles1, labels1, loc='center left', fontsize=FONT_SIZE_FIG)
    
    plt.draw()
    # Adjust layout to make space for the legend
    #plt.tight_layout()  # Leave space on the right for the legend



def make_optimal_table(list_of_best_dict_list_w_kwarg, sweep_label_list, show_sweep_list):
    
    # Variables
    T_HTF_COLD_info = ["T_htf_cold_des", "C", "HTF Cold Temperature"]
    CYCLE_COST_info = ["cycle_cost", "M$", "Cycle Cost"]
    COST_PER_kW_info = ["cost_per_kWe_net_ish", "$/kWe", "System Cost per Net Power"]
    PC_ETA_info = ["eta_thermal_calc", "", "PC Thermal Efficiency"]
    
    # Make Table
    row_list = []
    first_row = ["Sensitivity Parameter", "Config", "Cycle Eff", "HTF dT", "$/kWe", "Simple $/kWe"]
    row_list.append(first_row)
    sweep_label_to_index = {d: i for i, d in enumerate(sweep_label_list)}
    for sweep_local in show_sweep_list:

        index = sweep_label_to_index.get(sweep_local)
        best_dict_list_w_kwarg = list_of_best_dict_list_w_kwarg[index]

        # Get Best Config
        min_dict = {}
        simple_dict = {}
        min_cost_per_power = float('inf')
        for result_dict, kwarg in best_dict_list_w_kwarg:
            config_name = result_dict['config_name'][0]
            cost_per_power = result_dict[COST_PER_kW_info[0]][0]

            if config_name == "Simple":
                simple_dict = result_dict
            
            if cost_per_power < min_cost_per_power:
                min_dict = result_dict
                min_cost_per_power = cost_per_power

        # Get Data
        min_config_reduced = design_tools.shorten_config(min_dict['config_name'][0])
        min_eff = min_dict['eta_thermal_calc'][0]
        min_HTF_dT = min_dict["T_htf_hot_des"][0] - min_dict["T_htf_cold_des"][0]
        min_cost_per_power = min_cost_per_power
        simple_cost_per_power = simple_dict[COST_PER_kW_info[0]][0]

        # Make Row
        row = []
        row.append(sweep_local)
        row.append(min_config_reduced)
        row.append(str(min_eff * 100))
        row.append(str(min_HTF_dT))
        row.append(str(min_cost_per_power))
        row.append(str(simple_cost_per_power))

        row_list.append(row)

    # Save data
    write_array_to_file(row_list)
    x = 0
        



def make_comparison_plots():
    presplit = True
    
    enum_list = [BASE.BASELINE, BASE.ETA8085, BASE.ETA8090,
                 BASE.COLDAPP40, BASE.COLDAPP60,
                 BASE.TIT550, BASE.TIT625,
                 BASE.HELIO127,
                 BASE.RECUP50, BASE.RECUP150,
                 BASE.TES50, BASE.TES150,
                 BASE.PHXBUCKLO, BASE.PHXBUCKHI]

    filenames_list_w_label = []
    for enum in enum_list:
        filenames_list_w_label.append(sco2_filenames.get_file_via_enum(enum, presplit))

    #filenames_list_w_label = [filenames_baseline_w_label]

    key_list = ["cycle_config", "config_name",
                "recomp_frac", "bypass_frac",
                "LTR_UA_calculated", "HTR_UA_calculated",
                "cost_per_kWe_net_ish", "eta_thermal_calc", 
                "T_htf_hot_des", "T_htf_cold_des",
                "cycle_cost",
                "mc_cooler_q_dot", "pc_cooler_q_dot",
                "id", "UA_BPX", "BPX_cost_equipment", "T_htf_bp_out_des",
                "q_dot_in_total", "mc_cooler_q_dot", "pc_cooler_q_dot",
                "is_bypass_ok", "UA_BPX", "HTR_cost_equipment", "LTR_cost_equipment",
                "eta_thermal_net_less_cooling_des"
                ]

    # Open Files
    output = data_utility.open_file_set_w_label(filenames_list_w_label, key_list)
    list_of_dict_list_w_kwargs = output[0]
    list_of_best_dict_list_with_kwarg = output[1]
    final_sweep_labels = output[2]

    # Variables
    T_HTF_COLD_info = ["T_htf_cold_des", "°C", "HTF Cold Temperature"]
    CYCLE_COST_info = ["cycle_cost", "M$", "Cycle Cost"]
    COST_PER_kW_info = ["cost_per_kWe_net_ish", "$/kWe", "System Specific Cost (SSC)\n"]
    PC_ETA_info = ["eta_thermal_calc", "", "PC Thermal Efficiency"]
    UA_CALC_info = ["recup_total_UA_calculated", "MW/K", "Recup Total UA"]

    # Configs to be plotted
    show_config_list = ['Simple', 'Simple Split Flow Bypass w/o LTR', 'Simple Split Flow Bypass', 
                        'Recompression', 'Recompression w/o LTR', 'Recompression w/o HTR',
                        'HTR BP', 'HTR BP w/o LTR', 
                        'Partial', 'Partial w/o HTR', 'Partial w/o LTR', 'Partial Intercooling w/o HTR',
                        'Turbine Split Flow']

    # Make Optimal Table
    #make_optimal_table(list_of_best_dict_list_with_kwarg, final_sweep_labels, final_sweep_labels)
    
    figsize_local = (6,2.9)
    figsize_double = (FIG_WIDTH_FULL, 4.0)

    # Plot Approach Temperatures
    #T_PHX_sweep_labels = [filenames_baseline_w_label[1], 
    #                      filenames_coldapproach40_w_label[1], filenames_coldapproach60_w_label[1],
    #                      filenames_TIT550_w_label[1], filenames_TIT625_w_label[1]]
    
    T_PHX_sweep_labels = [sco2_filenames.get_sweep_label(BASE.BASELINE), 
                          sco2_filenames.get_sweep_label(BASE.COLDAPP40),
                          sco2_filenames.get_sweep_label(BASE.COLDAPP60),
                          sco2_filenames.get_sweep_label(BASE.TIT550),
                          sco2_filenames.get_sweep_label(BASE.TIT625)]

    plot_comparisons_duo(list_of_best_dict_list_with_kwarg, final_sweep_labels, T_PHX_sweep_labels, COST_PER_kW_info, show_config_list,
                     figsize=figsize_double)
    
    # Plot Isentropic Efficiencies
    #ISEN_sweep_labels = [filenames_baseline_w_label[1], 
    #                     filenames_eta8085_w_label[1], filenames_eta8090_w_label[1]]
    ISEN_sweep_labels = [sco2_filenames.get_sweep_label(BASE.BASELINE), 
                         sco2_filenames.get_sweep_label(BASE.ETA8085), 
                         sco2_filenames.get_sweep_label(BASE.ETA8090)]
    plot_comparisons_duo(list_of_best_dict_list_with_kwarg, final_sweep_labels, ISEN_sweep_labels, COST_PER_kW_info, show_config_list,
                     figsize=figsize_double)
    
    # Plot PHX Costs
    #COST_PHX_sweep_labels = [filenames_baseline_w_label[1], 
    #                         filenames_phxbucklow_w_label[1], filenames_phxbuckhigh_w_label[1]]
    COST_PHX_sweep_labels = [sco2_filenames.get_sweep_label(BASE.BASELINE), 
                             sco2_filenames.get_sweep_label(BASE.PHXBUCKLO), 
                             sco2_filenames.get_sweep_label(BASE.PHXBUCKHI)]

    plot_comparisons_duo(list_of_best_dict_list_with_kwarg, final_sweep_labels, COST_PHX_sweep_labels, COST_PER_kW_info, show_config_list,
                     figsize=figsize_double)
    
    # Plot "Other" Costs
    #COST_other_sweep_labels = [filenames_baseline_w_label[1], 
    #                         filenames_heliocost_w_label[1], 
    #                         filenames_recup50_w_label[1], filenames_recup150_w_label[1],
    #                         filenames_tes50_w_label[1], filenames_tes150_w_label[1]]
    COST_other_sweep_labels = [sco2_filenames.get_sweep_label(BASE.BASELINE), 
                             sco2_filenames.get_sweep_label(BASE.HELIO127), 
                             sco2_filenames.get_sweep_label(BASE.RECUP50),
                             sco2_filenames.get_sweep_label(BASE.RECUP150),
                             sco2_filenames.get_sweep_label(BASE.TES50),
                             sco2_filenames.get_sweep_label(BASE.TES150)]
    plot_comparisons_duo(list_of_best_dict_list_with_kwarg, final_sweep_labels, COST_other_sweep_labels, COST_PER_kW_info, show_config_list,
                     figsize=figsize_double)

    # Plot All
    plot_comparisons_duo(list_of_best_dict_list_with_kwarg, final_sweep_labels, final_sweep_labels, COST_PER_kW_info, show_config_list,
                     figsize=(FIG_WIDTH_FULL, 5), bottom_padding=0.2)
    
    plt.rcParams['savefig.dpi'] = 1000
    plt.show(block=True)
    

if __name__ == "__main__":
    make_comparison_plots()