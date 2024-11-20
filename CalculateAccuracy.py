import json
import string

# Change prefix to choose model

path_prefix = 'Results/LoRA/GPT4o-mini/'
# path_prefix = 'Results/LoRA/Gemma2-9B/'
# path_prefix = 'Results/LoRA/LLaMA3.1-8B/'
# path_prefix = 'Results/LoRA/Mistral-7B/'

# Change 'result_files' and 'validation_file' simultaneously to choose english/spanish datasets

# result_files = ['result_eng_ori.json', 'result_eng_ftby1k.json', 'result_eng_ftby2k.json', 'result_eng_ftby5k.json',
#                 'result_eng_ftby10k.json']
# validation_file = 'Words/Validation_Data.json'

result_files = ['result_spa_ori.json','result_spa_ftby1k.json','result_spa_ftby2k.json','result_spa_ftby5k.json','result_spa_ftby10k.json']
validation_file = 'Words/Validation_Data_Spanish.json'


letter_stats = {letter: {"correct": 0, "total": 0} for letter in string.ascii_lowercase}

num_correct = 0

for result_file in result_files:
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
    for letter, stats in letter_stats.items():
        if stats["total"] > 0:
            accuracy = stats["correct"] / stats["total"]
            print(f"'{letter}' accuracy: {accuracy:.2%} ({stats['correct']} out of {stats['total']})")
        else:
            print(f"'{letter}' accuracy: No data available")

    num_correct = 0
    letter_stats = {letter: {"correct": 0, "total": 0} for letter in string.ascii_lowercase}
