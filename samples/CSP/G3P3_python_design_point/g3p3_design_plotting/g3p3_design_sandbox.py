# Plot the g3p3 results, y axis HTF temp, x axis sco2 efficiency
# Z axis highlight which runs pass and fail (cmod_success)

import sys
import os
from tkinter.filedialog import askopenfilenames
import tkinter as tk
import matplotlib.pyplot as plt


sys.path.append("sco2-python")

newPath = ""
newPath_example = ""
core_loc = "local_git"

if(core_loc == "local_git"):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    parentDir2 = os.path.dirname(parentDir)
    newPath = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/core')
    newPath_example = os.path.join(parentDir2, 'C:/Users/tbrown2/Documents/repos/sam_dev/sam/samples/CSP/sco2_analysis_python_V2/example')
    sys.path.append(newPath_example)


import sco2_sim_result_collection as sco2_result_collection
import design_point_tools as design_tools

def plot_sco2_results(filenames):

    result_dict_list = []

    # Loop through each sco2 config
    for filename in filenames:
        filename_stripped = os.path.basename(filename)
        print("Opening " + filename_stripped + "...")
        sco2_collection = sco2_result_collection.C_sco2_sim_result_collection()
        sco2_collection.open_csv(filename)
        print("sco2 file open")

        
        result_dict_list.append([sco2_collection.old_result_dict, {'label':filename_stripped, 'marker':'.'}])

    # Variables to Display
    ETA_label = ["eta_thermal_calc", "", "Cycle Thermal Efficiency"]
    T_HTF_label = ["T_htf_cold_des", "C", "HTF Outlet Temperature"]
    COST_label = ["cycle_cost", "M$", "Cycle Cost"]

    design_tools.plot_scatter_pts(      
                    result_dict_list
                    , 
                    ETA_label, T_HTF_label, ["cmod_success","","Success/Failure"],show_legend=False)
    
def plot_sco2_fileopendlg():

    window = tk.Tk()

    window.mainloop()
    filename_tuple = askopenfilenames(filetypes =[('CSV Files', '*.csv')], title="Open sco2 results csv")
    
    filenames = []
    for filename in filename_tuple:
        filenames.append(filename)

    if(len(filenames) > 0):
        plot_sco2_results(filenames)


if __name__ == "__main__":
    plot_sco2_fileopendlg()
    plt.show(block = True)