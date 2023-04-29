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
        if (i > 19 and i < 24) or (i > 13 and i < 17) and row != []:
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
    clean_data = list(map(list, zip(*filtered_data1[0:5])))
    # make dictionary with column names as keys and column data as values
    header = {row: i for i, row in enumerate(clean_data[0])}
    clean_data_dict = {}
    for i, row in enumerate(header):
        for j, col in enumerate(clean_data):
            if j == 0:
                clean_data_dict[row] = []
            else:
                clean_data_dict[row].append(col[i])

    output_row = [patient_id]
    for i, row in enumerate(header_index_dict):
        for col in clean_data_dict:
            output_row.append(clean_data_dict[col][i])

    # check if output.csv exists

    if not os.path.exists(args.output):

        output_header_row = ['patient_id']
        for i, row in enumerate(header_index_dict):
            for col in clean_data_dict:
                output_header_row.append(
                    (col+'_'+row).replace(' ', '_').replace(':', ''))
        with open(args.output, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(output_header_row)

    # append data to output file
    with open(args.output, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(output_row)
