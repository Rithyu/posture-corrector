import pandas as pd

# 1. Load the dataset
print("Loading dataset...")
df = pd.read_csv('cleaned_dataset.csv')

# 2. Filter out redundant columns
# We drop 'index' and the Thigh sensor axes (Ax2, Ay2, Az2) since your node is on the back/neck.
# If you want to keep the thigh data for a different model, just remove them from this drop list.
columns_to_drop = ['index', 'Ax2', 'Ay2', 'Az2']
df_clean = df.drop(columns=columns_to_drop)

# Rename the chest/back columns to standard Edge Impulse naming conventions
df_clean = df_clean.rename(columns={'Ax1': 'accX', 'Ay1': 'accY', 'Az1': 'accZ'})

# 3. Add a simulated timestamp column (Edge Impulse strictly requires this)
# Assuming the data was recorded at ~50Hz (20 milliseconds per reading)
df_clean.insert(0, 'timestamp', range(0, len(df_clean) * 20, 20))

# 4. Split the data into separate files based on the Posture Label
# The dataset uses numbers (0.0, 1.0, 2.0, 5.0) for labels. 
unique_labels = df_clean['label'].unique()
print(f"Found {len(unique_labels)} unique posture labels: {unique_labels}")

# Create a separate, clean CSV for every single posture state
for label in unique_labels:
    # Extract only the rows for this specific posture
    df_subset = df_clean[df_clean['label'] == label].copy()
    
    # Drop the label column now, because the file NAME will act as the label in Edge Impulse
    df_subset = df_subset.drop(columns=['label'])
    
    # Restart the timestamp for each new file so it starts at 0 ms
    df_subset['timestamp'] = range(0, len(df_subset) * 20, 20)
    
    # Save the file (e.g., "posture_state_5.0.csv")
    filename = f"posture_state_{int(label)}.csv"
    df_subset.to_csv(filename, index=False)
    print(f"✅ Saved clean file: {filename} ({len(df_subset)} samples)")

print("\n🎉 DONE! You can now upload these individual files directly into Edge Impulse.")