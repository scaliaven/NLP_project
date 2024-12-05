import json
import os
from pathlib import Path
from ord_schema.message_helpers import load_message, write_message
from ord_schema.proto import dataset_pb2
from google.protobuf.json_format import MessageToJson
from tqdm import tqdm  # Progress bar library

def extract_smiles(data):
    """
    Extract reactants and products SMILES strings from reaction JSON data.

    Args:
        data (dict): Reaction JSON data.
        
    Returns:
        tuple: (list of reactant SMILES, list of product SMILES)
    """
    reactants_smiles = []
    products_smiles = []

    # Extract reactants
    inputs = data.get('inputs', {})
    for input_key, input_value in inputs.items():
        components = input_value.get('components', [])
        for component in components:
            # Extract components with specific roles
            if component.get('reaction_role') in ['REACTANT', 'REAGENT', 'CATALYST']:
                identifiers = component.get('identifiers', [])
                for identifier in identifiers:
                    if identifier.get('type') == 'SMILES':
                        smiles = identifier.get('value')
                        reactants_smiles.append(smiles)

    # Extract products
    outcomes = data.get('outcomes', [])
    for outcome in outcomes:
        products = outcome.get('products', [])
        for product in products:
            identifiers = product.get('identifiers', [])
            for identifier in identifiers:
                if identifier.get('type') == 'SMILES':
                    smiles = identifier.get('value')
                    products_smiles.append(smiles)

    return reactants_smiles, products_smiles

def convert_to_uspto(reactants, products):
    """
    Convert reactant and product SMILES lists to USPTO format string.

    Args:
        reactants (list): List of reactant SMILES.
        products (list): List of product SMILES.
        
    Returns:
        str: Reaction in USPTO format.
    """
    reactants_part = '.'.join(reactants)
    products_part = '.'.join(products)
    uspto_format = f"{reactants_part}>>{products_part}"
    return uspto_format

def process_pb_gz_file(file_path):
    """
    Process a single .pb.gz file to extract all reactions in USPTO SMILES format.

    Args:
        file_path (Path): Path to the .pb.gz file.
        
    Returns:
        list: List of USPTO SMILES reactions from the file.
    """
    try:
        # Convert Path object to string
        dataset = load_message(str(file_path), dataset_pb2.Dataset)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

    uspto_reactions = []

    for idx, rxn in enumerate(dataset.reactions):
        try:
            rxn_json = json.loads(
                MessageToJson(
                    message=rxn,
                    including_default_value_fields=False,
                    preserving_proto_field_name=True,
                    indent=2,
                    sort_keys=False,
                    use_integers_for_enums=False,
                    descriptor_pool=None,
                    float_precision=None,
                    ensure_ascii=True,
                )
            )
            reactants, products = extract_smiles(rxn_json)
            if not reactants or not products:
                # Skip reactions missing reactants or products
                print(f"Skipping reaction {idx} in {file_path}: Missing reactants or products.")
                continue
            uspto_reaction = convert_to_uspto(reactants, products)
            uspto_reactions.append(uspto_reaction)
        except Exception as e:
            print(f"Error processing reaction {idx} in {file_path}: {e}")
            continue  # Skip the faulty reaction

    return uspto_reactions

def traverse_directory(input_dir):
    """
    Traverse the specified directory to find all .pb.gz files.

    Args:
        input_dir (Path): Path to the input directory.
        
    Returns:
        list: List of paths to .pb.gz files.
    """
    pb_gz_files = list(input_dir.rglob('*.pb.gz'))
    return pb_gz_files

def main(f1,f2):
    # Input directory and output file paths
    input_directory = Path(f1)  # Update as needed
    output_txt = Path(f2)  # Output file path

    # Find all .pb.gz files
    pb_gz_files = traverse_directory(input_directory)
    print(f"Found {len(pb_gz_files)} .pb.gz files.")

    total_reactions = 0
    uspto_all = []

    # Process all .pb.gz files
    for pb_gz_file in tqdm(pb_gz_files, desc="Processing .pb.gz files"):
        uspto_reactions = process_pb_gz_file(pb_gz_file)
        uspto_all.extend(uspto_reactions)
        total_reactions += len(uspto_reactions)

    # Write to output text file
    with open(output_txt, 'w', encoding='utf-8') as f:
        for uspto in uspto_all:
            f.write(uspto + '\n')

    print(f"Processed {len(pb_gz_files)} files, extracted {total_reactions} reactions.")
    print(f"The {output_txt} file has been written.")

if __name__ == "__main__":
    main('/Users/zhaodongliu/data/ord-data/data','/Users/zhaodongliu/data/uspto_reactions.txt')