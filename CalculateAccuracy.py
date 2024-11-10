import json


result_files = ['Results/results_ori.json', 'Results/results_ft1k.json','Results/results_ft2k.json',
                'Results/results_ft5k.json','Results/results_ft10k.json']

# result_files = ['Results/results_ori_Spanish.json', 'Results/results_ft1k_Spanish.json',
#                 'Results/results_ft2k_Spanish.json', 'Results/results_ft5k_Spanish.json',
#                 'Results/results_ft10k_Spanish.json']

validation_file = 'Words/Validation_Data.json'
# validation_file = 'Words/Validation_Data_Spanish.json'


num_correct = 0

for result_file in result_files:
    with open(result_file, "r") as file_a:
        data_a = json.load(file_a)

    with open(validation_file, "r") as file_b:
        data_b = json.load(file_b)

    for key, value in data_a.items():  # Parse the JSON-formatted value in file a from a string into a dictionary to compare
        try:
            data_a[key] = json.loads(value)
        except:
            pass
            # print('errorKey: ' + key)

    for key in data_a:
        if key in data_b:
            value_a = data_a[key]
            value_b = data_b[key]
            if value_a == value_b:
                num_correct += 1
        else:
            print(f"Key '{key}' exists only in file a")
    print(result_file+' accuracy: '+str(num_correct / 10000))
    num_correct = 0
