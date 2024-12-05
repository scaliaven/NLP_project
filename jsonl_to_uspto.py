import json, random

# Open the JSONL file
def main(f1, f2):
    with open(f1, 'r', encoding='utf-8') as file:
        input_smiless, pred_smiless = [], []
        for line in file:
            # Parse each line as JSON
            data = json.loads(line.strip())
            input_smiles = data.get('input', '')
            gold_smiles = data.get('gold', '')
            pred_smiles = '; '.join(data.get('pred', []))
            
            if gold_smiles in pred_smiles:
                input_smiless.append(input_smiles)
                pred_smiless.append(gold_smiles)

            else:
                input_smiless.append(input_smiles)
                apd = random.choice(pred_smiles.split(';'))
                pred_smiless.append(apd)

    with open(f2, 'w', encoding='utf-8') as f:
        for i in range(len(input_smiless)):
            f.write(f'{input_smiless[i]}>>{pred_smiless[i]}\n')

    print(f" {len(input_smiless)} reactions have been written to {f2}.")
        

if __name__ == "__main__":
    main('/Users/zhaodongliu/data/ord-data/retrosynthesis.jsonl', '/Users/zhaodongliu/data/ord-data/hhj.txt')