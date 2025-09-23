import os
from enum import Enum, auto

# Color List (for plotting)

color_list = [
    "#000000",  # Black
    "#FF7F0E",  # Orange
    "#8C564B",  # Brown
    "#5B9BD5",  # Light Blue
    "#9467BD",  # Purple
    "#2CA02C",  # Green
    "#D62728",  # Red
    "#7F7F7F",  # Gray
    "#BCBD22",  # Olive
    "#17BECF",  # Teal
    "#9E3D41",  # Maroon
    "#E377C2",  # Pink
    "#FFB94A",  # Amber
    "#7B4173",  # Plum
    "#6D9F4B",  # Forest Green
    "#800020",  # Burgundy (swapped with Peach)
    "#6A3D9A",  # Dark Purple
    "#1F77B4",  # Blue (replacing Aqua)
    "#C3B091",  # Taupe
    "#B8860B",  # Dark Goldenrod
    "#008B8B",  # Dark Cyan
    "#D85C8A",  # Rose
    "#2F4F4F",  # Slate Gray
    "#8B8B00",  # Olive Drab
    "#F1A7A0",  # Peach (swapped with Burgundy)
    # Additional 25 colors to double the list
    "#FF69B4",  # Hot Pink
    "#00FF7F",  # Spring Green
    "#4169E1",  # Royal Blue
    "#FFD700",  # Gold
    "#FF6347",  # Tomato
    "#40E0D0",  # Turquoise
    "#EE82EE",  # Violet
    "#FFA500",  # Orange Red
    "#32CD32",  # Lime Green
    "#87CEEB",  # Sky Blue
    "#DDA0DD",  # Plum Light
    "#F0E68C",  # Khaki
    "#FA8072",  # Salmon
    "#20B2AA",  # Light Sea Green
    "#9370DB",  # Medium Purple
    "#3CB371",  # Medium Sea Green
    "#F4A460",  # Sandy Brown
    "#2E8B57",  # Sea Green
    "#4682B4",  # Steel Blue
    "#D2691E",  # Chocolate
    "#6495ED",  # Cornflower Blue
    "#DC143C",  # Crimson
    "#00CED1",  # Dark Turquoise
    "#9400D3",  # Dark Violet
    "#FF1493"   # Deep Pink
]

linestyle_list = ['-', '--', ':']


# Collection of filenames

def get_filenames_baseline(split=False):
    sweep_label = 'Baseline'
    i = 0
    color = color_list[i]

    if split == True:
        filename_list = [
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple.pkl',
                         #r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
            
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl',
                         
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl',

                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                         
                         ]

    else:
        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_eta8085(split=False):
    sweep_label = 'ETA C:80% T:85%'
    i = 1
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\split_config\Partial_w_o_LTR.pkl']

    else:
        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\mega_zG3P3_results_20250213_222001__htrbp_G3P3_collection_10_20250213_001356_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\mega_zG3P3_results_20250214_131242__recomp_G3P3_collection_10_20250213_000233_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\mega_zG3P3_results_20250214_160843__TSF_G3P3_collection_10_20250213_000858_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged\mega_zG3P3_results_20250215_010805__partial_G3P3_collection_10_20250212_210401_001.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_eta8090(split=False):
    sweep_label = 'ETA C:80% T:90%'
    i = 2
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                         ]
    else:
        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\mega_zG3P3_results_20250218_231102__htrbp_G3P3_collection_10_20250212_200704_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\mega_zG3P3_results_20250219_140804__recomp_G3P3_collection_10_20250212_195514_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\mega_zG3P3_results_20250218_171846__TSF_G3P3_collection_10_20250212_200140_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged\mega_zG3P3_results_20250219_121321__partial_G3P3_collection_10_20250212_165328_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_coldapproach40(split=False):
    sweep_label = 'Cold Approach 40 \u00B0C'
    i = 3
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    
    else:
        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\mega_zG3P3_results_20250220_230031__htrbp_G3P3_collection_10_20250220_154104_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\mega_zG3P3_results_20250222_040508__recomp_G3P3_collection_10_20250220_152743_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\mega_zG3P3_results_20250222_053221__TSF_G3P3_collection_10_20250220_153506_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged\mega_zG3P3_results_20250221_142819__partial_G3P3_collection_10_20250220_112415_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_coldapproach60(split=False):
    sweep_label = 'Cold Approach 60 \u00B0C'
    i = 4
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\split_config\HTR_BP.pkl']

    else:
        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\mega_zG3P3_results_20250226_225801__htrbp_G3P3_collection_10_20250225_194404_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\mega_zG3P3_results_20250226_101514__recomp_G3P3_collection_10_20250225_193211_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\mega_zG3P3_results_20250226_134736__TSF_G3P3_collection_10_20250225_193834_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged\mega_zG3P3_results_20250227_135337__partial_G3P3_collection_10_20250225_164104_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_TIT550(split=False):
    sweep_label = 'TIT 550 \u00B0C'
    i = 5
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\mega_zG3P3_results_20250220_072601__htrbp_G3P3_collection_10_20250219_175557_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\mega_zG3P3_results_20250222_100208__recomp_G3P3_collection_10_20250219_173432_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\mega_zG3P3_results_20250222_131614__TSF_G3P3_collection_10_20250219_174556_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged\mega_zG3P3_results_20250221_083140__partial_G3P3_collection_10_20250219_111034_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_TIT625(split=False):
    sweep_label = 'TIT 625 \u00B0C'
    i = 6
    color = color_list[i]

    if split == True:
        filename_list = [r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Partial.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Recompression.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Simple.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\split_config\HTR_BP.pkl"
                         ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\mega_zG3P3_results_20250301_032922__htrbp_G3P3_collection_10_20250228_192547_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\mega_zG3P3_results_20250302_010235__recomp_G3P3_collection_10_20250228_191317_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\mega_zG3P3_results_20250302_023005__TSF_G3P3_collection_10_20250228_192002_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged\mega_zG3P3_results_20250301_142449__partial_G3P3_collection_10_20250228_160546_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]


def get_filenames_heliocost(split=False):
    sweep_label = 'Heliostat 127 $/m2'
    i = 7
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Turbine_Split_Flow_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\split_config\Partial.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250215_171644__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_163031__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_175940__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged\mega_zG3P3_results_20250216_053648__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]


def get_filenames_recup50(split=False):
    sweep_label = 'Recuperator Cost 0.5x'
    i = 8
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\HTR_BP_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                         ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\recup50_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\recup50_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\recup50_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334\recup50_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_recup150(split=False):
    sweep_label = 'Recuperator Cost 1.5x'
    i = 9
    color = color_list[i]

    if split == True:
        filename_list = [r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Partial.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Partial_Intercooling_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Partial_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Partial_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Recompression.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Recompression_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Recompression_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Simple.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Simple_Double_Recup.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Simple_Split_Flow_Bypass.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Turbine_Split_Flow.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\Turbine_Split_Flow_w_o_LTR.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\HTR_BP.pkl',
                         r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\split_config\HTR_BP_w_o_LTR.pkl'
                         ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\recup150_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\recup150_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\recup150_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347\recup150_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_recup1000(split=False):
    sweep_label = 'Recuperator Cost 10x'
    i = 10
    color = color_list[i]

    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Turbine_Split_Flow_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\split_config\Partial_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\recup1000_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\recup1000_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\recup1000_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401\recup1000_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]


def get_filenames_tes50(split=False):
    sweep_label = 'TES Cost 0.5x'
    i = 11
    color = color_list[i]

    if split == True:
        filename_list = [r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\HTR_BP.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\HTR_BP_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Partial.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Partial_Intercooling_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Partial_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Partial_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Recompression.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Recompression_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Recompression_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Simple.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Simple_Double_Recup.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Simple_Split_Flow_Bypass.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Turbine_Split_Flow.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Turbine_Split_Flow_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\split_config\Turbine_Split_Flow_w_o_LTR.pkl"
                         ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\tes50_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\tes50_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\tes50_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314\tes50_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_tes150(split=False):
    sweep_label = 'TES Cost 1.5x'
    i = 12
    color = color_list[i]

    if split == True:
        filename_list = [r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\HTR_BP.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\HTR_BP_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Partial.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Partial_Intercooling_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Partial_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Partial_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Recompression.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Recompression_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Recompression_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Simple.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Simple_Double_Recup.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Simple_Split_Flow_Bypass.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Turbine_Split_Flow.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Turbine_Split_Flow_w_o_HTR.pkl",
                         r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\split_config\Turbine_Split_Flow_w_o_LTR.pkl"
                         ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\tes150_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\tes150_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\tes150_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325\tes150_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_tes1000(split=False):
    sweep_label = 'TES Cost 10x'
    i = 13
    color = color_list[i]

    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\tes1000_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\tes1000_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\tes1000_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001\tes1000_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]


def get_filenames_phxbucklow(split=False):
    sweep_label = 'PHX Buck Low'
    i = 14
    color = color_list[i]

    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Turbine_Split_Flow_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\phxbl0_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\phxbl0_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\phxbl0_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120\phxbl0_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_phxbuckhigh(split=False):
    sweep_label = 'PHX Buck High'
    i = 15
    color = color_list[i]

    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\phxbhi_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\phxbhi_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\phxbhi_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131\phxbhi_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_phxbuckhigh10x(split=False):
    sweep_label = 'PHX Buck High 10x'
    i = 16
    color = color_list[i]

    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\phxh10_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\phxh10_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\phxh10_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756\phxh10_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_helio_phxbuckhigh(split=False):
    sweep_label = 'Helio 127 PHX Buck High'
    i = 17
    color = color_list[i]

    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\helio_phxbhi_mega_zG3P3_results_20250215_171644__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\helio_phxbhi_mega_zG3P3_results_20250216_163031__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\helio_phxbhi_mega_zG3P3_results_20250216_175940__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556\helio_phxbhi_mega_zG3P3_results_20250216_053648__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]


def get_filenames_helio10x(split=False):
    sweep_label = 'Heliostat Cost 10x'
    i = 18
    color = color_list[i]
    
    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\h10_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\h10_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\h10_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534\h10_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]

def get_filenames_helio100x(split=False):
    sweep_label = 'Heliostat Cost 100x'
    i = 19
    color = color_list[i]
    
    if split == True:
        filename_list = [
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\HTR_BP.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\HTR_BP_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Partial.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Partial_Intercooling_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Partial_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Partial_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Recompression.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Recompression_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Recompression_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Simple.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Simple_Double_Recup.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Simple_Split_Flow_Bypass.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Simple_Split_Flow_Bypass_w_o_LTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Turbine_Split_Flow.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Turbine_Split_Flow_w_o_HTR.pkl',
                        r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\split_config\Turbine_Split_Flow_w_o_LTR.pkl'
                        ]
    else:

        filename_htrbp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\h100_mega_zG3P3_results_20250211_175945__htrbp_G3P3_collection_10_20250210_181500_000.pkl"
        filename_recomp = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\h100_mega_zG3P3_results_20250213_025738__recomp_G3P3_collection_10_20250210_180210_000.pkl"
        filename_tsf = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\h100_mega_zG3P3_results_20250213_043907__TSF_G3P3_collection_10_20250210_180908_000.pkl"
        filename_partial = r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731\h100_mega_zG3P3_results_20250212_082014__partial_G3P3_collection_10_20250210_142613_000.pkl"

        filename_list = [filename_htrbp, filename_recomp, filename_tsf, filename_partial]

    return [filename_list, sweep_label, color]


def get_all_files_from_folder(parent_folder, file_extension='.pkl'):

    if os.path.exists(parent_folder):
        all_files = os.listdir(parent_folder)
        # Filter for files with specified extension and create full paths
        filename_list = [os.path.join(parent_folder, f) for f in all_files if f.endswith(file_extension)]
        # Sort the list for consistent ordering
        filename_list.sort()
        return filename_list
    else:
        print(f"Warning: Directory '{parent_folder}' does not exist.")
        return []

def get_filenames_OPT(split=False):
    sweep_label = 'Baseline Optimized Par'
    i = 20
    color = color_list[i]
    
    if split == True:
        parent_folder = r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_OPT\run_10_20250718_164740\mega_slim_pickled_merged\split_config'

    else:
        parent_folder = r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_OPT\run_10_20250718_164740\mega_slim_pickled_merged'

    # Use the separate function to get all files from the parent folder
    filename_list = get_all_files_from_folder(parent_folder)

    return [filename_list, sweep_label, color]

class BASE(Enum):
    
    BASELINE = auto()
    ETA8085 = auto()
    ETA8090 = auto()
    COLDAPP40 = auto()
    COLDAPP60 = auto()

    TIT550 = auto()
    TIT625 = auto()

    HELIO127 = auto()

    RECUP50 = auto()
    RECUP150 = auto()
    RECUP1000 = auto()

    TES50 = auto()
    TES150 = auto()
    TES1000 = auto()

    PHXBUCKLO = auto()
    PHXBUCKHI = auto()
    
    PHXBUCKHI10x = auto()
    HELIO127_PHXBUCKHI = auto()
    HELIO10x = auto()
    HELIO100x = auto()
    BASELINE_OPT = auto()
    

#class BASE(Enum):
#    
#    BASELINE_OPT = auto()
#    ETA8085 = auto()
#    ETA8090 = auto()
#    COLDAPP40 = auto()
#    COLDAPP60 = auto()
#    HELIO127 = auto()
#    PHXBUCKLO = auto()
#    PHXBUCKHI = auto()
#    RECUP50 = auto()
#    RECUP150 = auto()
#    RECUP1000 = auto()
#    TES50 = auto()
#    TES150 = auto()
#    TES1000 = auto()
#    
#    PHXBUCKHI10x = auto()
#    HELIO127_PHXBUCKHI = auto()
#    HELIO10x = auto()
#    HELIO100x = auto()
#    BASELINE = auto()
#    TIT550 = auto()
#    TIT625 = auto()

BASE_dict = {
    BASE.BASELINE: ["Baseline", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_FINAL\run_10_20250210_142612\mega_slim_pickled_merged"],
    BASE.BASELINE_OPT: ["Baseline Opt", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_OPT\run_10_20250718_164740\mega_slim_pickled_merged"],
    BASE.ETA8085: ["ETA C:80% T:85%", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8085\run_10_20250212_210400\mega_slim_pickle_merged"],
    BASE.ETA8090: ["ETA C:80% T:90%", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\baseline_eta8090\run_10_20250212_165328\mega_slim_pickled_merged"],
    BASE.COLDAPP40: ["Cold Approach 40 °C", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach40\run_10_20250220_133225\mega_slim_pickled_merged"],
    BASE.COLDAPP60: ["Cold Approach 60 °C", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\coldapproach60\run_10_20250225_164104\mega_slim_pickled_merged"],
    BASE.TIT550: ["TIT 550 °C", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550\run_10_20250219_111034\mega_slim_pickled_merged"],
    BASE.TIT625: ["TIT 625 °C", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625\run_10_20250228_160546\mega_slim_pickled_merged"],
    BASE.HELIO127: ["Heliostat 127 $/m2", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost SAM Default\run_10_20250210_142612\mega_slim_pickled_merged"],
    BASE.RECUP50: ["Recuperator Cost 0.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 50\recup50_20250310_114334"],
    BASE.RECUP150: ["Recuperator Cost 1.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 150\recup150_20250310_114347"],
    BASE.RECUP1000: ["Recuperator Cost 10x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Recup 1000\recup1000_20250313_144401"],
    BASE.TES50: ["TES Cost 0.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 50\tes50_20250310_120314"],
    BASE.TES150: ["TES Cost 1.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 150\tes150_20250310_120325"],
    BASE.TES1000: ["TES Cost 10x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\TES 1000\tes1000_20250313_143001"],
    BASE.PHXBUCKLO: ["PHX Buck Low", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck Low\phxbl0_20250313_093120"],
    BASE.PHXBUCKHI: ["PHX Buck High", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High\phxbhi_20250313_093131"],
    BASE.PHXBUCKHI10x: ["PHX Buck High 10x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\PHX Buck High 10x\phxh10_20250313_094756"],
    BASE.HELIO127_PHXBUCKHI: ["Helio 127 PHX Buck High", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Helio PHX Buck High\helio_phxbhi_20250313_163556"],
    BASE.HELIO10x: ["Heliostat Cost 10x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 10x\h10_20250325_162534"],
    BASE.HELIO100x: ["Heliostat Cost 100x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\Sensitivity\Heliostat Cost 100x\h100_20250325_162731"],
}

class TIT550(Enum):
    BASELINE = auto()
    ETA8085 = auto()
    ETA8090 = auto()
    COLDAPP40 = auto()
    COLDAPP60 = auto()
    HELIO127 = auto()
    PHXBUCKLO = auto()
    PHXBUCKHI = auto()
    RECUP50 = auto()
    RECUP150 = auto()
    RECUP1000 = auto()
    TES50 = auto()
    TES150 = auto()
    TES1000 = auto()

TIT550_dict = {
    TIT550.BASELINE : [ "TIT550 Optimized", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\mega_slim_pickled_merged'],
    TIT550.ETA8085 : ["TIT550 ETA C:80% T:85%", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_eta8085\run_10_20250718_203708\mega_slim_pickled_merged'],
    TIT550.ETA8090 : ["TIT550 ETA C:80% T:90%", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_eta8090\run_10_20250720_203224\mega_slim_pickled_merged'],
    TIT550.COLDAPP40 : ["TIT550 Cold Approach 40 °C", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_coldapproach40\run_10_20250728_163300\mega_slim_pickled_merged'],
    TIT550.COLDAPP60 : ["TIT550 Cold Approach 60 °C", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_coldapproach60\run_10_20250729_155626\mega_slim_pickled_merged'],
    TIT550.HELIO127 : ["TIT550 Heliostat 127 $/m2", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\helio127_20250721_151340"],
    TIT550.PHXBUCKLO : ["TIT550 PHX Buck Low", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\phxblo_20250721_150724"],
    TIT550.PHXBUCKHI : ["TIT550 PHX Buck High", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\phxbhi_20250721_150739"],
    TIT550.RECUP50 : ["TIT550 Recuperator Cost 0.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\recup50_20250721_150641"],
    TIT550.RECUP150 : ["TIT550 Recuperator Cost 1.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\recup150_20250721_150655"],
    TIT550.RECUP1000 : ["TIT550 Recuperator Cost 10x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\recup1000_20250721_150709"],
    TIT550.TES50 : ["TIT550 TES Cost 0.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\tes50_20250721_150604"],
    TIT550.TES150 : ["TIT550 TES Cost 1.5x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\tes150_20250721_150615"],
    TIT550.TES1000 : ["TIT550 TES Cost 10x", r"C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT550_baseline_OPT\run_10_20250718_113615\post\tes1000_20250721_150627"]

}

class TIT625(Enum):
    BASELINE = auto()
    ETA8085 = auto()
    ETA8090 = auto()
    COLDAPP40 = auto()
    COLDAPP60 = auto()
    HELIO127 = auto()
    PHXBUCKLO = auto()
    PHXBUCKHI = auto()
    RECUP50 = auto()
    RECUP150 = auto()
    RECUP1000 = auto()
    TES50 = auto()
    TES150 = auto()
    TES1000 = auto()

TIT625_dict = {
    TIT625.BASELINE : [ "TIT625 Optimized", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\mega_slim_pickled_merged'],
    TIT625.ETA8085 : ["TIT625 ETA C:80% T:85%", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_eta8085\run_10_20250723_164049\mega_slim_pickled_merged'],
    TIT625.ETA8090 : ["TIT625 ETA C:80% T:90%", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_eta8090\run_10_20250725_165741\mega_slim_pickled_merged'],
    TIT625.COLDAPP40 : ["TIT625 Cold Approach 40 °C", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_coldapproach40\run_10_20250801_092726\mega_slim_pickled_merged'],
    TIT625.COLDAPP60 : ["TIT625 Cold Approach 60 °C", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_coldapproach60\run_10_20250801_192238\mega_slim_pickled_merged'],
    TIT625.HELIO127 : ["TIT625 Heliostat 127 $/m2", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\helio127_20250801_093753'],
    TIT625.PHXBUCKLO : ["TIT625 PHX Buck Low", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\phxblo_20250801_093715'],
    TIT625.PHXBUCKHI : ["TIT625 PHX Buck High", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\phxbhi_20250801_093735'],
    TIT625.RECUP50 : ["TIT625 Recuperator Cost 0.5x", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\recup50_20250801_093615'],
    TIT625.RECUP150 : ["TIT625 Recuperator Cost 1.5x", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\recup150_20250801_093635'],
    TIT625.RECUP1000 : ["TIT625 Recuperator Cost 10x", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\recup1000_20250801_093655'],
    TIT625.TES50 : ["TIT625 TES Cost 0.5x", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\tes50_20250801_093518'],
    TIT625.TES150 : ["TIT625 TES Cost 1.5x", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\tes150_20250801_093538'],
    TIT625.TES1000 : ["TIT625 TES Cost 10x", r'C:\Users\tbrown2\OneDrive - NREL\sCO2-CSP 10302.41.01.40\Notes\G3P3\runs\TIT625_baseline_OPT\run_10_20250721_170456\post\tes1000_20250801_093556'],
    }

def get_file_via_enum(enum, split=False):
    """
    Generic function that works with both BASE and TIT550 enums.
    Automatically determines which dictionary to use based on enum type.
    """
    # Determine which dictionary to use based on enum type
    sweep_id = 0
    if isinstance(enum, BASE):
        config_dict = BASE_dict
        sweep_id = 0
    elif isinstance(enum, TIT625):
        config_dict = TIT625_dict
        sweep_id = 1
    elif isinstance(enum, TIT550):
        config_dict = TIT550_dict
        sweep_id = 2
    
    else:
        raise ValueError(f"Unsupported enum type: {type(enum)}")
    
    folder = config_dict[enum][1]
    sweep_label = config_dict[enum][0]
    color = color_list[enum.value - 1]  # Convert enum to 0-based index
    linestyle = linestyle_list[sweep_id]

    kwarg_dict = {'c':color, 'linestyle':linestyle}

    if split == True:
        folder = os.path.join(folder, "split_config")

    filename_list = get_all_files_from_folder(folder)

    return [filename_list, sweep_label, kwarg_dict]

def get_sweep_label(enum):
    if isinstance(enum, BASE):
        config_dict = BASE_dict
    elif isinstance(enum, TIT550):
        config_dict = TIT550_dict
    else:
        raise ValueError(f"Unsupported enum type: {type(enum)}")
    
    return config_dict[enum][0]
