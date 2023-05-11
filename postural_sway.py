import os
import csv
import argparse
# TAKE IN FILENAME AS AN ARGUMENT


parser = argparse.ArgumentParser()
parser.add_argument(
    "foldername", help="name of folder that has files to be appended to output.csv")
parser.add_argument("output", help="name of file to write to")
args = parser.parse_args()

# print foldername


list_of_files = os.listdir(args.foldername)
for filename in list_of_files:
    # read in csv file
    data_list = open(os.path.join(args.foldername, filename), 'r').readlines()
    your_list = [[x.replace("\n", "")] for x in data_list[:-2]]
    your_list = [x[0].split(',') for x in your_list]
    # get patient id
    patient_id = filename.split('_')[0]
    # get rows needed
    data = []
    for i, row in enumerate(your_list):
        if i == 9:
            header = [x.split('-')[1] if "-" in x else x for x in row]
            header = header[1:]
        if (i > 17 and i < 23) or (i > 11 and i < 17) and row != []:
            data.append(row)
    # desired_column_names=[
    #    "MEAN HR",
    #    "SD HR",
    #    "RMSSD",
    #    "RR tri index",
    # ]

    header = [x.strip() for x in header if x.strip() != '']
    header_index_dict = {h: i for i, h in enumerate(header)}

    # data = [d for d in data if any([True if (c.lower() in d[0].lower()) else False for c in desired_column_names])]

    # loop through each sublist with a comprehension

    filtered_data1 = [[x.strip() for x in d if x.strip() != ''] for d in data]

    # transpose data
    clean_data = list(map(list, zip(*filtered_data1[:])))
    # make dictionary with column names as keys and column data as values
    header = {row: i for i, row in enumerate(clean_data[0])}
    clean_data_dict = {}
    for i, row in enumerate(header):
        for j, col in enumerate(clean_data):
            if j == 0:
                clean_data_dict[row] = []
            else:
                clean_data_dict[row].append(col[i])

    reverse_header_index_dict = {v: k for k, v in header_index_dict.items()}

    for col in clean_data_dict:
        new_clean_data_dict = {}
        for i, val in enumerate(clean_data_dict[col]):
            new_clean_data_dict[reverse_header_index_dict[i]] = val
        clean_data_dict[col] = new_clean_data_dict

    # check if output.csv exists

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

    output_row = [patient_id]
    for i, row in enumerate(file_header_index_dict):
        for col in clean_data_dict:
            output_row.append(clean_data_dict[col][row])

    # append data to output file
    with open(args.output, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(output_row)
