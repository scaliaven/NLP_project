import pandas as pd

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

def convert_smiles_to_table(input_file, output_file, dataset_set):
    """
    Converts SMILES reactions to a structured table with Reactants, Products, and Set.
    
    Args:
        input_file (str): Path to the input file containing SMILES reactions.
        output_file (str): Path to the output TSV file.
        dataset_set (str): The dataset category to assign (e.g., 'train', 'test').
    """
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
                data['set'].append(dataset_set)
            else:
                print(f"Skipping line {line_num} due to invalid format.")

    df = pd.DataFrame(data)
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Conversion complete. Output saved to {output_file}")

if __name__ == "__main__":
    # Set file paths and dataset category directly
    input_file = '/Users/zhaodongliu/data/ord-data/retro_llm.txt'   # 输入文件路径
    output_file = '/Users/zhaodongliu/data/ord-data/intermediate.txt' # 输出文件路径
    dataset_set = 'train'         # 数据集类别（如 'train', 'test', 'valid'）

    convert_smiles_to_table(input_file, output_file, dataset_set)