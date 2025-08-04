import random
import csv
import traci
import numpy as np
import sumolib

# Select a list based on probability (i.e. intend_parking_block)
def select_column(probabilities):
    rand_num = random.random()
    cum_prob = 0
    for col_name, prob in probabilities.items():
        cum_prob += prob
        if rand_num <= cum_prob:
            return col_name
    return list(probabilities.keys())[-1]


# generate vehicles (PARK, PUDO, LUL)
def generate_vehicle_flow(file_path):
    # read csv file and store data into a dictionary named data
    data = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # get headers of the csv file

        # get names and index
        vehicle_types = header[2:]  # get the headers/columns name of vehicle types
        zone_index = 0
        time_index = 1

        # read data by line and store into a dictionary named data
        for row in reader:
            zone = row[zone_index]
            time = int(row[time_index])
            for vehicle_type, value in zip(vehicle_types, row[2:]):
                key = f"{zone}_{time}_{vehicle_type}"
                data[key] = float(value)

    # generate 16 possible routes
    for i in ['ai', 'bi', 'ci', 'di']:
        for j in ['ao', 'bo', 'co', 'do']:
            traci.route.add(i[0] + j[0], [i, j])

    # store vehicle's first parking zone
    veh_first_zone = {}
    # generate vehicle by 'data' dictionary
    for key, value in data.items():
        zone = key.split('_')[0]
        time_interval = int(key.split('_')[1])
        typeid = key.split('_')[2]
        count = value
        # if count equals 0, skip current loop
        if count == 0:
            continue
        # start and end time of traffic flow
        start = (time_interval - 1) * 3600
        end = time_interval * 3600

        # generate a list to store the vehicles' generation time
        event_list = []

        for i in range(1000):
            # Poison's arrival
            time_interval = random.expovariate(count / 60)
            start += int(time_interval * 60)
            # if the sum greater than 60min, break
            if start >= end:
                break
            else:
                # update event list
                event_list.append(start)

        for i in range(len(event_list)):
            depart = event_list[i]
            veh_id = 'parking_' + key + '_' + str(i)
            # add vehicle
            traci.vehicle.add(veh_id, routeID=random.choice(
                ['aa', 'ab', 'ac', 'ad', 'ba', 'bb', 'bc', 'bd', 'ca', 'cb', 'cc', 'cd', 'da', 'db', 'dc', 'dd']),
                              typeID=typeid, depart=depart)
            veh_first_zone[veh_id] = zone.lower()
    return veh_first_zone


# generate background traffic
def generate_background_flow(file_path, num):
    # read csv file and store data into a dictionary named data
    data = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # get headers of the csv file

        vehicle_types = header[2:]  # get the headers/columns name of vehicle types
        zone_index = 0
        time_index = 1

        # read data by line and store into a dictionary named data
        for row in reader:
            zone = row[zone_index]
            time = int(row[time_index])
            for vehicle_type, value in zip(vehicle_types, row[2:]):
                key = f"{zone}_{time}_{vehicle_type}"
                data[key] = float(value)

    # get network information
    net = sumolib.net.readNet("net.xml")
    edge_list = list(net.getEdges())

    # generate vehicle by 'data' dictionary
    for key, value in data.items():
        print(key, value)
        zone = key.split('_')[0]
        time_interval = int(key.split('_')[1])
        typeid = 'BT'
        count = value
        # if count equals 0, skip current loop
        if count == 0:
            continue
        # start and end time of traffic flow
        start = (time_interval - 1) * 3600
        end = time_interval * 3600

        # generate a list to store the vehicles' generation time
        event_list = []

        for i in range(3000):
            # Poison's arrival
            time_interval = random.expovariate(num * count / 60)
            start += int(time_interval * 60)
            # if the sum greater than 60min, break
            if start >= end:
                break
            else:
                # update event list
                event_list.append(start)
        for i in range(len(event_list)):
            depart = event_list[i]
            veh_id = 'background_' + key + '_' + str(i)

            state = True
            while state is True:
                # obtain edges and coordinates
                from_edge = random.choice(edge_list).getID()
                from_x, from_y = net.getEdge(from_edge).getShape()[0]
                to_edge = random.choice(edge_list).getID()
                to_x, to_y = net.getEdge(to_edge).getShape()[0]
                if True:
                    try:
                        routes = traci.simulation.findRoute(from_edge, to_edge).edges
                        # judgement condition
                        specified_zone = zone.lower()
                        have_zone = False
                        have_zone_other = False
                        abc = ['a', 'b', 'c']
                        abc.remove(specified_zone)
                        for edge in routes:
                            if specified_zone == edge[0] and edge not in ['ai', 'ao', 'bi', 'bo', 'ci', 'co', 'di',
                                                                          'do'] and edge[1] != 'i':
                                have_zone = True
                            if (abc[0] == edge[0] or abc[1] == edge[0]) and edge[0:2] != 'cl':
                                have_zone_other = True

                        # whether satisfy the condition
                        if have_zone is True and have_zone_other is False:
                            # create route and vehicle based on the vehicles' generation time in the list
                            traci.route.add(veh_id, list(routes))
                            traci.vehicle.add(veh_id, routeID=veh_id, typeID=typeid, depart=depart)
                            state = False
                        else:
                            continue
                    except:
                        continue
                else:
                    pass