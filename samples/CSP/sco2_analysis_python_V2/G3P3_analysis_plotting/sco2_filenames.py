# Color List (for plotting)
color_list = [
    "#FF5733",
    "#33FF57",
    "#5733FF",
    "#F2C037",
    "#37F2C0",
    "#C037F2",
    "#FF8533",
    "#33FF85",
    "#8533FF",
    "#FF3385",
    "#3385FF",
    "#85FF33",
    "#C033FF",
    "#33C0FF",
    "#FF33C0",
    "#FFB833",
    "#33B8FF",
    "#B833FF",
    "#FF33B8",
    "#B8FF33"
]

color_list = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', 
                  '#c2c2f0', '#ffb3e6', '#c4e17f', '#76d7c4', 
                  '#ff7f50', '#87ceeb', '#da70d6', '#ffa07a', 
                  '#20b2aa', '#778899', '#b0c4de', '#ff6347', 
                  '#40e0d0', '#ff69b4', "#FF33B8",
    "#B8FF33"]




color_list = [
    "#1A5A7C",  # Dark Blue
    "#D46A09",  # Dark Orange
    "#2A7D32",  # Dark Green
    "#A6231E",  # Dark Red
    "#6A4C91",  # Dark Purple
    "#6F4F44",  # Dark Brown
    "#9E2B73",  # Dark Pink
    "#585858",  # Dark Gray
    "#8C8D1D",  # Olive Green
    "#137A8C",  # Dark Teal
    "#9D2E30",  # Dark Maroon
    "#4C6B3C",  # Dark Forest Green
    "#D77C27",  # Dark Amber
    "#5A2A56",  # Dark Plum
    "#4C7E99",  # Dark Light Blue
    "#7CAEA5",  # Dark Aqua
    "#D1655F",  # Dark Peach
    "#5A2A6F",  # Dark Dark Purple
    "#6A5D89",  # Dark Lavender
    "#9E8C5A"   # Dark Taupe
]

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
    "#F1A7A0"   # Peach (swapped with Burgundy)
]




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

