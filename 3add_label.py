import pandas as pd

def add_label(file_path, output_path):
 # 读取txt文件
    data = pd.read_csv(file_path, sep="\t")

    # 检查数据格式
    if 'Reactants' in data.columns and 'Products' in data.columns and 'set' in data.columns:
        # 随机打乱数据
        data_shuffled = data.sample(frac=1, random_state=42).reset_index(drop=True)

        # 计算10%的样本数量
        total_samples = len(data_shuffled)
        test_count = valid_count = int(total_samples * 0.1)

        # 修改标签
        data_shuffled.loc[:test_count - 1, 'set'] = 'test'
        data_shuffled.loc[test_count:test_count + valid_count - 1, 'set'] = 'valid'

        # 保存修改后的数据
        data_shuffled.to_csv(output_path, sep="\t", index=False)

        print(f"修改完成！结果已保存到 {output_path}")
    else:
        print("文件格式错误，确保文件包含 'Reactants', 'Products', 和 'set' 列。")

if __name__ == "__main__": 
    add_label('/Users/zhaodongliu/data/ord-data/intermediate.txt', '/Users/zhaodongliu/data/ord-data/retro_llm_labeled.txt')