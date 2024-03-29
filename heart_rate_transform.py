import os
import csv
import argparse
# TAKE IN FILENAME AS AN ARGUMENT


parser = argparse.ArgumentParser()
parser.add_argument(
    "foldername", help="name of folder that has files to be appended to output.csv")
parser.add_argument("output", help="name of file to write to")
args = parser.parse_args()


# class args:
#     foldername = '/home/billyshaw/projects/eb/Heart_rate_varience_transform/heart rate'
#     output = 'output_hr.csv'


list_of_files = os.listdir(args.foldername)
for filenum, filename in enumerate(list_of_files):
    # read in csv file
    with open(os.path.join(args.foldername, filename), 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    # get patient id
    patient_id = filename.split('_')[0]
    # get rows needed
    data = []
    for i, row in enumerate(your_list):
        if i == 63:
            header = row
        if i > 64 and i < 90 and row != []:
            data.append(row)
    desired_column_names = [
        "Mean RR  (ms)",
        "SDNN (ms)",
        "Mean HR (beats/min)",
        "SD HR (beats/min)",
        "Min HR (beats/min)",
        "Max HR (beats/min)",
        "RMSSD (ms)",
        "NNxx (beats)",
        "pNNxx (%)",
        "SDANN (ms)",
        "SDNN index (ms)",
        "RR tri index",
        "TINN (ms)"
    ]

    header_start = [x.strip().split('(')[0].replace(" ", "")
                    for x in header if x.strip() != '']
    header_index_dict = {h: i for i, h in enumerate(header_start)}

    filtered_data = [d for d in data if any(
        [True if (c.lower() in d[0].lower()) else False for c in desired_column_names])]

    # loop through each sublist with a comprehension

    filtered_data1 = [[x.strip() for x in d if x.strip() != '']
                      for d in filtered_data]

    # transpose data
    clean_data = list(map(list, zip(*filtered_data1[:])))
    # make dictionary with column names as keys and column data as values
    header = {row: i for i, row in enumerate(clean_data[0])}
    clean_data_dict = {}
    for i, row in enumerate(header):
        row = row.split('(')[0]

        for j, col in enumerate(clean_data):
            if j == 0:
                clean_data_dict[row] = []
            else:
                clean_data_dict[row].append(col[i])

    # get reverse dict of header_index_dict

    reverse_header_index_dict = {v: k for k, v in header_index_dict.items()}
    sample6 = ["SAMPLE 6", "sample 6", "Sample 6",
               "Sample6", "sample6", "Sample 6(6)", 'SAMPLE6']
    for col in clean_data_dict:
        new_clean_data_dict = {}
        for i, val in enumerate(clean_data_dict[col]):
            new_clean_data_dict[reverse_header_index_dict[i]] = val
        clean_data_dict[col] = new_clean_data_dict

    # clean_data_dict1=clean_data_dict

    for col in clean_data_dict:
        new_clean_data_dict = {}
        for i, val in enumerate(clean_data_dict[col]):
            if reverse_header_index_dict[i] in list(sample6):
                new_clean_data_dict['baseline2'] = clean_data_dict[col][reverse_header_index_dict[i]]

            else:
                new_clean_data_dict[reverse_header_index_dict[i]
                                    ] = clean_data_dict[col][reverse_header_index_dict[i]]
        clean_data_dict[col] = new_clean_data_dict

    output_row = [patient_id]

    for sample in sample6:
        if sample in list(header_index_dict.keys()):
            num = header_index_dict[sample]
            del header_index_dict[sample]
            header_index_dict["baseline2"] = num

    baseline2 = ['baseline_2', 'baseline 2', 'baseline 2(6)']
    for baseline in baseline2:
        if baseline in list(header_index_dict.keys()):
            num = header_index_dict[baseline]
            del header_index_dict[baseline]
            header_index_dict["baseline2"] = num

    if not os.path.exists(args.output):
        output_header_row = ['patient_id']
        file_header_index_dict = header_index_dict.copy()
        for i, row in enumerate(header_index_dict):
            for col in clean_data_dict:
                output_header_row.append(
                    (col+'_'+row).replace(' ', '_').replace(':', '').replace('(', '@').replace(')', '$'))
        with open(args.output, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(output_header_row)

    for i, row in enumerate(file_header_index_dict):
        row = row.split('(')[0]
        for col in clean_data_dict:
            output_row.append(clean_data_dict[col][row])
    # check if output.csv exists

    # append data to output file
    with open(args.output, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(output_row)
