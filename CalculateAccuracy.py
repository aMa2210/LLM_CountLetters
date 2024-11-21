import json
import string
import csv
import os
import re
# Change prefix to choose model

# path_prefix = 'Results/LoRA/GPT4o-mini/'
# text = 'GPT4o-mini'
# path_prefix = 'Results/LoRA/LLaMA3.1-8B/'
# text = 'LLaMA3.1-8B'
# path_prefix = 'Results/LoRA/Gemma2-9B/'
# text = 'Gemma2-9B'
path_prefix = 'Results/LoRA/Mistral-7B/'
text = 'Mistral-7B'

# Change 'result_files' and 'validation_file' simultaneously to choose english/spanish datasets

result_files = ['result_eng_ori.json', 'result_eng_ftby1k.json', 'result_eng_ftby2k.json', 'result_eng_ftby5k.json',
                'result_eng_ftby10k.json']
validation_file = 'Words/Validation_Data.json'
csv_output_path = "Letter_Accuracy_Eng.csv"

# result_files = ['result_spa_ori.json','result_spa_ftby1k.json','result_spa_ftby2k.json','result_spa_ftby5k.json','result_spa_ftby10k.json']
# validation_file = 'Words/Validation_Data_Spanish.json'
# csv_output_path = "Letter_Accuracy_Spa.csv"

letter_stats = {letter: {"correct": 0, "total": 0} for letter in string.ascii_lowercase}

num_correct = 0

for result_file in result_files:
    match = re.search(r'(_[^.]+)\.json', result_file)

    model_name = text+match.group(1)

    with open(path_prefix + result_file, "r") as file_a:
        data_a = json.load(file_a)

    with open(validation_file, "r") as file_b:
        data_b = json.load(file_b)

    for key, value in data_a.items():  # Parse the JSON-formatted value in file a from a string into a dictionary to compare
        try:
            data_a[key] = json.loads(value)
        except:
            # print('errorKey: ' + key)
            pass

    for key in data_a:
        if key in data_b:
            value_a = data_a[key]
            value_b = data_b[key]
            if value_a == value_b:
                num_correct += 1

            if isinstance(value_a, dict):
                for letter in string.ascii_lowercase:
                    if letter in value_b:
                        letter_stats[letter]["total"] += 1
                        if letter in value_a and value_a[letter] == value_b[letter]:
                            letter_stats[letter]["correct"] += 1

        else:
            print(f"Key '{key}' exists only in file a")
    print(result_file + ' accuracy: ' + str(num_correct / 10000))


    accuracy_data = {}
    for letter, stats in letter_stats.items():
        if stats["total"] > 0:
            accuracy = stats["correct"] / stats["total"]
            accuracy_data[letter] = round(accuracy * 100,2)
            # print(f"'{letter}' accuracy: {accuracy:.2%} ({stats['correct']} out of {stats['total']})")
        else:
            accuracy_data[letter] = None
            # print(f"'{letter}' accuracy: No data available")

    if not os.path.exists(csv_output_path):
        # 如果文件不存在，创建文件并写入表头
        with open(csv_output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # 写入表头（第一列为字母，其他列为模型名称）
            header = ["Letter"] + [model_name]
            writer.writerow(header)
            # 写入字母及其对应的准确率
            for letter in string.ascii_lowercase:
                writer.writerow([letter, accuracy_data.get(letter, "No data")])
    else:
        # 如果文件已存在，读取现有内容并添加新模型的数据
        with open(csv_output_path, mode="r", newline="", encoding="utf-8") as file:
            reader = list(csv.reader(file))

        # 更新表头和数据
        header = reader[0]
        if model_name in header:
            print(f"Model '{model_name}' already exists in the CSV file.")
        else:
            # 添加新模型列
            header.append(model_name)
            for i, letter in enumerate(string.ascii_lowercase, start=1):
                if i < len(reader):  # 更新已有行
                    reader[i].append(accuracy_data.get(letter, "No data"))
                else:  # 如果没有该字母的行，则添加新行
                    reader.append([letter] + [""] * (len(header) - 2) + [accuracy_data.get(letter, "No data")])

            # 写回更新后的内容
            with open(csv_output_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(reader)


    num_correct = 0
    letter_stats = {letter: {"correct": 0, "total": 0} for letter in string.ascii_lowercase}
