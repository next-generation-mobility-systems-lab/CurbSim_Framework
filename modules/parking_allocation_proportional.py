import pandas as pd
import random
import traci

# allocate parking space and change the space indication color
def parking_lot_allocation(parking_type_info, num):
    # allocate parking spaces type to each zone
    excel_file = pd.ExcelFile('input/space_proportional_allocation.xlsx')

    # create a dictionary to store data
    data_dict = {}

    # for each worksheet
    for sheet_name in excel_file.sheet_names:
        # read the data of the current worksheet
        df = excel_file.parse(sheet_name)

        # for each row
        for index, row in df.iterrows():
            # get values for the zone, time, and usage columns
            zone = row['Zone']
            time = row['Time']
            usage = row['Usage']

            # for the column names that contain 'adjusted'
            for col_name in df.columns:
                if 'adjusted' in col_name and 'sum' not in col_name:
                    # concatenate key values
                    key = f"{zone}_{time}_{usage}_{col_name.split('_')[0]}"

                    # get the value of the corresponding column
                    value = row[col_name]

                    # store the data in the dictionary
                    data_dict[key] = value

    parking_dict = {}
    for spot, car_type in data_dict.items():
        # print(f"{spot}: {car_type}")
        key = spot.split('_')[1] + spot.split('_')[-1]
        parking_dict[key] = [spot.split('_')[-1][0] + 'p' + spot.split('_')[-1][1:] + '_' + '1',
                             spot.split('_')[-1][0] + 'p' + spot.split('_')[-1][1:] + '_' + '2',
                             spot.split('_')[-1][0] + 'p' + spot.split('_')[-1][1:] + '_' + '3',
                             spot.split('_')[-1][0] + 'p' + spot.split('_')[-1][1:] + '_' + '4',
                             spot.split('_')[-1][0] + 'p' + spot.split('_')[-1][1:] + '_' + '5']
   
    for key, value in data_dict.items():
        zone = key.split('_')[0]
        time = key.split('_')[1]
        usage = key.split('_')[2]
        edge = key.split('_')[3]
        # allocate parking space type according to time
        if time == str(num):
            count = value
            parking = time + edge
            # randomly select parking spaces
            spots = random.sample(parking_dict[parking], count)
            # store parking spaces and vehicle types in a dictionary
            for spot in spots:
                parking_type_info[spot] = usage
                # remove the allocated parking space from the parking space list
                parking_dict[parking].remove(spot)

    # change the space color based on the type
    for key, value in parking_type_info.items():
        if parking_type_info[key] == 'PARK':
            traci.poi.setColor(key, (255, 0, 0))
        elif parking_type_info[key] == 'PUDO':
            traci.poi.setColor(key, (0, 0, 255))
        else:
            traci.poi.setColor(key, (0, 255, 0))