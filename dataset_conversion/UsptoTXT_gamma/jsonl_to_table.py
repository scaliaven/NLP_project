import json, random
import pandas as pd

# Open the JSONL file
def main(f1, f2):
    with open(f1, 'r', encoding='utf-8') as file:
        input_smiless, pred_smiless, golden_smiless = [], [], []
        for line in file:
            # Parse each line as JSON
            data = json.loads(line.strip())
            input_smiles = data.get('input', '')
            gold_smiles = data.get('gold', '')
            golden_smiless.append(gold_smiles)
            try:
                pred_smiles = data.get('output', [])

                flag = False
                # for i in pred_smiles:
                #     # print(i)
                #     # print(i.split('</SMILES>'))
                #     # break
                #     for j in i.split('<SMILES>', 1)[-1].split('</SMILES>'):
                #         if gold_smiles in j:
                #             input_smiless.append(input_smiles)
                #             pred_smiless.append(gold_smiles)
                #             flag = True
                #             break
                #     if flag:
                #         break   

                if not flag:
                    input_smiless.append(input_smiles)

                    apd = random.choice(pred_smiles).split('<SMILES>', 1)[-1].split('</SMILES>')
                    for k in range(len(apd)):
                        if "</s><unk><unk><unk>" in apd[k]:
                            apd.pop(k)
                    pred_smiless.append(random.choice(apd))
            except:
                continue
            

    # print(type(gold_smiles))



    data = {
        'Reactants': [],
        'Golden': [],
        'Products': [],
        'set': []
    }
    for i in range(len(input_smiless)):
        data['Reactants'].append(input_smiless[i])
        data['Products'].append(pred_smiless[i])
        data['set'].append('train')
        data['Golden'].append(golden_smiless[i])

    df = pd.DataFrame(data)

    # Step 2: Shuffle and split data into train, test, and valid sets
    if 'Reactants' in df.columns and 'Products' in df.columns and 'set' in df.columns and 'Golden' in df.columns:
        # Random shuffle
        data_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

        # Calculate 10% samples
        total_samples = len(data_shuffled)
        test_count = valid_count = int(total_samples * 0.1)

        # Update 'set' column
        data_shuffled.loc[:test_count - 1, 'set'] = 'test'
        data_shuffled.loc[test_count:test_count + valid_count - 1, 'set'] = 'valid'

        # Save final output
        data_shuffled.to_csv(f2, sep='\t', index=False)
        print(f"Final adjustment complete. Output saved to {f2}")
    else:
        print("Data format error: Ensure the file contains 'Reactants', 'Products', and 'set' columns.")

        

if __name__ == "__main__":
    main('/Users/zhaodongliu/Documents/GitHub/NLP_project/retrosynthesis.jsonl', '/Users/zhaodongliu/Documents/GitHub/NLP_project/retro_111.txt')