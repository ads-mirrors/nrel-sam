import pandas as pd 

old_df = pd.read_csv("cec_modules_test_2024-9-11_2024-Nov-16.csv")
new_df = pd.read_csv("cec_modules_test_2025-4-16_2025-Jun-2.csv")
print(old_df)
print(new_df)

old_df = old_df.set_index('Module Name')
new_df = new_df.set_index('Module Name')
print(old_df)
print(new_df)

combined_df = new_df.join(old_df, lsuffix='_py', rsuffix='_ssc')
print(combined_df)

combined_df.to_csv("combined.csv")
        
