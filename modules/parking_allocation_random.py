import pandas as pd
import random
import traci

# allocate parking space and change the space indication color for random allocation zone
def parking_lot_allocation(parking_type_info, a_num_car1, a_num_car2, a_num_truck,
                           b_num_car1, b_num_car2, b_num_truck,
                           c_num_car1, c_num_car2, c_num_truck):
    # allocate parking spaces type to each zone
    # allocate parking spaces type to zone 1 or A
    for i in ['a7', 'a8', 'a11', 'a12', 'a13', 'a14', 'a17', 'a18']:
        for j in ['1', '2', '3', '4', '5']:
            value = 1
            while value == 1:
                random_type = random.choices(['PARK', 'PUDO', 'LUL'],
                                             weights=[a_num_car1 / 40, a_num_car2 / 40,
                                                      a_num_truck / 40], k=1)[0]
                if random_type == 'PARK' and a_num_car1 > 0:
                    a_num_car1 -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
                elif random_type == 'PUDO' and a_num_car2 > 0:
                    a_num_car2 -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
                elif random_type == 'LUL' and a_num_truck > 0:
                    a_num_truck -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0

    # allocate parking spaces type to zone 2 or B
    for i in ['b7', 'b8', 'b11', 'b12', 'b13', 'b14', 'b17', 'b18']:
        for j in ['1', '2', '3', '4', '5']:
            value = 1
            while value == 1:
                random_type = random.choices(['PARK', 'PUDO', 'LUL'],
                                             weights=[b_num_car1 / 40, b_num_car2 / 40,
                                                      b_num_truck / 40], k=1)[0]
                if random_type == 'PARK' and b_num_car1 > 0:
                    b_num_car1 -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
                elif random_type == 'PUDO' and b_num_car2 > 0:
                    b_num_car2 -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
                elif random_type == 'LUL' and b_num_truck > 0:
                    b_num_truck -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0

    # allocate parking spaces type to zone 3 or C
    for i in ['c5', 'c7', 'c8', 'c10']:
        for j in ['1', '2', '3', '4', '5']:
            value = 1
            while value == 1:
                random_type = random.choices(['PARK', 'PUDO', 'LUL'],
                                             weights=[c_num_car1 / 20, c_num_car2 / 20,
                                                      c_num_truck / 20], k=1)[0]
                if random_type == 'PARK' and c_num_car1 > 0:
                    c_num_car1 -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
                elif random_type == 'PUDO' and c_num_car2 > 0:
                    c_num_car2 -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
                elif random_type == 'LUL' and c_num_truck > 0:
                    c_num_truck -= 1
                    parking_type_info[i[0] + 'p' + i[1:] + '_' + j] = random_type
                    value = 0
    # change the space color based on the type
    for key, value in parking_type_info.items():
        if parking_type_info[key] == 'PARK':
            traci.poi.setColor(key, (255, 0, 0))
        elif parking_type_info[key] == 'PUDO':
            traci.poi.setColor(key, (0, 0, 255))
        else:
            traci.poi.setColor(key, (0, 255, 0))