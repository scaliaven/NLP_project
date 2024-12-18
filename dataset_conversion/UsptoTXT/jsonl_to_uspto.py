import json, random

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
                for i in pred_smiles:
                    # print(i)
                    # print(i.split('</SMILES>'))
                    # break
                    for j in i.split('<SMILES>', 1)[-1].split('</SMILES>'):
                        if gold_smiles in j:
                            input_smiless.append(input_smiles)
                            pred_smiless.append(gold_smiles)
                            flag = True
                            break
                    if flag:
                        break   

                if not flag:
                    input_smiless.append(input_smiles)

                    apd = random.choice(pred_smiles).split('<SMILES>', 1)[-1].split('</SMILES>')
                    for k in range(len(apd)):
                        if "</s><unk><unk><unk>" in apd[k]:
                            apd.pop(k)
                    pred_smiless.append(random.choice(apd))
            except:
                continue
                    

    with open(f2, 'w', encoding='utf-8') as f:
        for i in range(len(input_smiless)):
            f.write(f'{input_smiless[i]}>>{pred_smiless[i]}\n')

    print(f" {len(input_smiless)} reactions have been written to {f2}.")
        

if __name__ == "__main__":
    main('/Users/zhaodongliu/Documents/GitHub/NLP_project/retrosynthesis.jsonl', '/Users/zhaodongliu/Documents/GitHub/NLP_project/retro0.txt')