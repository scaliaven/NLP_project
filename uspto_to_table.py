import pandas as pd
import numpy as np

def parse_smiles_reaction(smiles_reaction):
    """
    Splits a SMILES reaction string into reactants and products.
    
    Args:
        smiles_reaction (str): SMILES reaction string separated by '>>'.
    
    Returns:
        tuple: (reactants, products)
    """
    try:
        reactants, products = smiles_reaction.split('>>')
        reactants = reactants.strip()
        products = products.strip()
        return reactants, products
    except ValueError:
        print(f"Invalid reaction format: {smiles_reaction}")
        return None, None

def convert_and_split_smiles(input_file, final_output_file):
    """
    Converts SMILES reactions to a structured table with Reactants, Products, and Set,
    and adjusts the 'set' column to assign 10% as 'test' and another 10% as 'valid'.
    
    Args:
        input_file (str): Path to the input file containing SMILES reactions.
        output_file (str): Path to the intermediate TSV file with extracted columns.
        final_output_file (str): Path to the final TSV file after adjusting 'set'.
        dataset_set (str): The initial dataset category to assign (default: 'train').
    """
    # Step 1: Extract reactants and products from SMILES reaction
    data = {
        'Reactants': [],
        'Products': [],
        'set': []
    }

    with open(input_file, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            reactants, products = parse_smiles_reaction(line)
            if reactants and products:
                data['Reactants'].append(reactants)
                data['Products'].append(products)
                data['set'].append('0')
            else:
                print(f"Skipping line {line_num} due to invalid format.")

    df = pd.DataFrame(data)

    # Step 2: Shuffle and split data into train, test, and valid sets
    if 'Reactants' in df.columns and 'Products' in df.columns and 'set' in df.columns:
        # Random shuffle
        data_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

        # Calculate 10% samples
        total_samples = len(data_shuffled)
        test_count = valid_count = int(total_samples * 0.1)

        # Update 'set' column
        data_shuffled.loc[:test_count - 1, 'set'] = 'test'
        data_shuffled.loc[test_count:test_count + valid_count - 1, 'set'] = 'valid'

        # Save final output
        data_shuffled.to_csv(final_output_file, sep='\t', index=False)
        print(f"Final adjustment complete. Output saved to {final_output_file}")
    else:
        print("Data format error: Ensure the file contains 'Reactants', 'Products', and 'set' columns.")

if __name__ == "__main__":
    # Define file paths and dataset category
    input_file = '/Users/zhaodongliu/Documents/GitHub/NLP_project/retro.txt'          # 原始 SMILES 文件路径
    final_output = '/Users/zhaodongliu/Documents/GitHub/NLP_project/retro_111.txt' # 最终输出文件路径

    # Call the function
    convert_and_split_smiles(input_file, final_output)