import pandas as pd
import json

# Load the dataset
input_file = 'data.csv'  # Adjust the path as needed
df = pd.read_csv(input_file)

# Display first few rows to understand the structure of the dataset
print("Dataset Preview:")
print(df.head())


# Function to parse the JSON from 'contracts' column
def parse_contracts(contract_json_str):
    try:
        # Convert JSON string to dictionary/list
        contract_data = json.loads(contract_json_str)

        # Initialize features dictionary
        features = {}

        # Check if the contract_data is a list and contains dictionaries
        if isinstance(contract_data, list) and all(isinstance(contract, dict) for contract in contract_data):
            # Example feature: count of contracts
            features['total_contracts'] = len(contract_data)

            # Example feature: total contract value (assuming each contract has a 'value' key)
            features['total_value'] = sum([contract.get('value', 0) for contract in contract_data])

            # Example feature: count of active contracts (assuming each contract has a 'status' key)
            features['num_active_contracts'] = sum(
                1 for contract in contract_data if contract.get('status') == 'active')
        else:
            # If the structure is unexpected, set default values
            features = {'total_contracts': 0, 'total_value': 0, 'num_active_contracts': 0}

        return features

    except (json.JSONDecodeError, TypeError) as e:
        # Return default values in case of errors
        return {'total_contracts': 0, 'total_value': 0, 'num_active_contracts': 0}


# Parse the 'contracts' column and calculate features
contract_features = df['contracts'].apply(parse_contracts)

# Convert the dictionary results into separate columns
contract_features_df = pd.json_normalize(contract_features)

# Concatenate the new features with the original dataframe
df_final = pd.concat([df, contract_features_df], axis=1)

# Drop the 'contracts' column if no longer needed
df_final = df_final.drop(columns=['contracts'])

# Save the resulting dataset to a new CSV file
output_file = 'contract_features.csv'
df_final.to_csv(output_file, index=False)

print(f"Features successfully extracted and saved to {output_file}")
