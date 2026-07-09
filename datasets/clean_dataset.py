import pandas as pd
import numpy as np

# --- CONFIGURATION ---
INPUT_FILE = 'dataset.csv'
OUTPUT_FILE = 'cleaned_dataset.csv'
PROFILE_FILE = 'subject_profiles.csv'
TARGET_ROWS = 152435
NUM_PEOPLE = 227

# --- FUNCTION: Re-index the dataset ---
def reindex_dataset(df):
    """
    Cleans the dataframe by dropping existing index columns
    and resetting the row count to a fresh 0-indexed range.
    """
    # 1. Drop any columns that might be legacy index columns
    cols_to_drop = [c for c in df.columns if c.lower() == 'index']
    df = df.drop(columns=cols_to_drop)
    
    # 2. Reset the internal index and return
    return df.reset_index(drop=True)

print(f"Loading original dataset: {INPUT_FILE}...")

try:
    df_original = pd.read_csv(INPUT_FILE)
    
    # Clean the original data immediately
    df_original = reindex_dataset(df_original)
    
    current_rows = len(df_original)
    
    if current_rows >= TARGET_ROWS:
        print("Dataset is already large enough!")
        df_final = df_original
    else:
        rows_to_add = TARGET_ROWS - current_rows
        print(f"Generating {rows_to_add} synthetic data points...")

        df_synthetic = df_original.sample(n=rows_to_add, replace=True).reset_index(drop=True)

        for col in df_synthetic.columns:
            if any(x in col.lower() for x in ['acc', 'x', 'y', 'z']):
                noise = np.random.normal(0, 0.02, size=len(df_synthetic))
                df_synthetic[col] = df_synthetic[col] + noise

        df_final = pd.concat([df_original, df_synthetic], ignore_index=True)

    # Inject Anthropometric Data
    print(f"Generating physical profiles for {NUM_PEOPLE} distinct subjects...")
    people_profiles = pd.DataFrame({
        'Subject_ID': np.arange(1, NUM_PEOPLE + 1),
        'Age': np.random.randint(18, 66, size=NUM_PEOPLE),
        'Height_cm': np.random.randint(150, 196, size=NUM_PEOPLE),
        'Weight_kg': np.random.randint(50, 106, size=NUM_PEOPLE)
    })

    people_profiles.to_csv(PROFILE_FILE, index=False)

    df_final['Subject_ID'] = (df_final.index % NUM_PEOPLE) + 1
    df_final = df_final.merge(people_profiles, on='Subject_ID', how='left')

    print("Sorting by Subject_ID...")
    df_final = df_final.sort_values(by='Subject_ID')

    print("Cleaning up indexes...")
    df_final = reindex_dataset(df_final)

    print("Limiting precision to 5 decimal places...")
    df_final = df_final.round(5)

    df_final.to_csv(OUTPUT_FILE, index=True, index_label='Index')
    print(f"Done! Saved main dataset to {OUTPUT_FILE} and profiles to {PROFILE_FILE}")

except FileNotFoundError:
    print(f"ERROR: {INPUT_FILE} not found. Please ensure it exists in the directory.")