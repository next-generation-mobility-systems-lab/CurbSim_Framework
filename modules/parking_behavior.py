import traci
import random
import numpy as np
from modules.vehicle_generation import select_column
from input.data import link, parking_link, parking_area_list, parking_list

# control vehicles to perform parking
def parking_wizard(step, veh_dict, link, parking_link, parking_area_list,
                   parking_list, parking_buffer, parking_type_info, parking_actual, veh_first_zone, result):
    # simulation starts
    for i in traci.vehicle.getIDList():
        if 'parking' in i:
            # when vehicle appears for the first time
            if i not in veh_dict:
                # store the enter_location_system and temporary_destination/leave_location_system
                start = traci.vehicle.getRoadID(i)
                end = traci.vehicle.getRoute(i)[-1]
                veh_type = traci.vehicle.getTypeID(i)
                last_road_id = traci.vehicle.getRoadID(i)
                # generate parking_zone_sequence
                parking_options = ['a', 'b', 'c']
                want_parking_count_options = [1, 2, 3]

                # first choice
                parking1 = veh_first_zone[i]
                # remove the selected item from parking_options, and adjust the selection probability
                remaining_options = parking_options.copy()
                remaining_options.remove(parking1)
                # adjust the probability
                if parking1 == 'c':
                    # if we choose zone c at the first time, then keep the probability of zone b and c
                    new_probabilities = [0.5, 0.5]
                else:
                    # if we choose zone a or b at the first time,
                    # then the probability of remaining zones are 66.7% and 33.3%
                    new_probabilities = [2 / 3, 1 / 3]
                # second choice
                parking2 = random.choices(remaining_options, new_probabilities, k=1)[0]
                # third choice (choose the remaining one)
                remaining_options.remove(parking2)
                parking3 = remaining_options[0]

                # choice the max_num_of_zones_can_pass_through
                want_parking_count = random.choice(want_parking_count_options)
                while parking2 == parking1:
                    parking2 = random.choice(parking_options)
                # generate the first temporary_destination
                if start == 'ai':
                    if parking1 == 'a':
                        temp_target = random.choice(['ai1', 'ai2', 'ai3'])
                    elif parking1 == 'b':
                        temp_target = random.choice(['bi1', 'bi2'])
                    else:
                        temp_target = random.choice(['ci1', 'ci2', 'ci3'])
                elif start == 'bi':
                    if parking1 == 'a':
                        temp_target = random.choice(['ai4', 'ai5', 'ai6'])
                    elif parking1 == 'b':
                        temp_target = random.choice(['bi5'])
                    else:
                        temp_target = random.choice(['ci4', 'ci5'])
                elif start == 'ci':
                    if parking1 == 'a':
                        temp_target = random.choice(['ai7', 'ai8', 'ai9'])
                    elif parking1 == 'b':
                        temp_target = random.choice(['bi6', 'bi7'])
                    else:
                        temp_target = random.choice(['ci6', 'ci7', 'ci8'])
                else:
                    if parking1 == 'a':
                        temp_target = random.choice(['ai10', 'ai11', 'ai12'])
                    elif parking1 == 'b':
                        temp_target = random.choice(['bi7', 'bi8'])
                    else:
                        temp_target = random.choice(['ci9', 'ci10'])

                if veh_type == 'PARK':
                    # generate parking time (service length) for PARK, triangular distribution
                    parking_time = float(np.random.triangular(left=0, mode=45, right=90, size=1)[0] * 60)
                elif veh_type == 'PUDO':
                    # generate parking time (service length) for PUDO, exponential distribution
                    parking_time = 0
                    while parking_time == 0:
                        parking_time = float(np.random.exponential(scale=5, size=1)[0] * 60)
                else:
                    # generate parking time (service length) for LUL, uniform distribution
                    parking_time = float(np.random.uniform(10, 50, 1)[0] * 60)
                
                # generate search time tolerance
                search_threshold = {
                    'PARK': int(max(np.random.normal(2.5, 1, size=1)[0], 0.5) * 60),
                    'PUDO': int(max(np.random.normal(3, 1, size=1)[0], 0.5) * 60),
                    'LUL': int(max(np.random.normal(4, 1, size=1)[0], 0.5) * 60),
                }

                # get vehicle's intend_parking_block
                if parking1 == 'a':
                    Zone = 1
                elif parking1 == 'b':
                    Zone = 2
                else:
                    Zone = 3
                Time = int(step / 3600) + 1
                Usage = veh_type
                key =(Zone, Time, Usage)
                probabilities = result[key]
                selected_column =select_column(probabilities)      
                veh_dict[i] = {'departure_time': step, 'arrival_time': step,
                               'enter_location_system': start, 'temporary_destination': '', 'leave_location_system': end, 'vehicle_type': veh_type,
                               'parking_zone_sequence': [parking1, parking2, parking3],
                               'intend_parking_block': selected_column,
                               'prone_factor': random.choice([0, 1]), 'whether_went_to_intend_block': False,
                               'max_num_of_zones_can_pass_through': want_parking_count, 'actual_passed_through_zones_num': 0, 'actual_passed_through_zones': '',
                               'whether_parking_success': False,
                               'parking_space_id': '', 'parking_time_legal': parking_time,
                               'cruising_time_threshold_legal': search_threshold[veh_type],
                               'temporary_cruising_time': 0, 'average_cruising_speed': [], 'actual_cruising_time': 0,
                               'selfish_factor': random.choice([0, 1]), 'temporary_whether_illegal_parking': False, 'illegal_behavior_state': 0,
                               'parking_space_type_illegal1': '', 'average_cruising_speed_illegal': [],
                               'actual_cruising_time_illegal': 0, 'final_cruising_time_illegal': 0, 'whether_illegal_parking_success': False}
                
                # let vehicle goes to the first temporary_destination, which is the intended parking block
                traci.vehicle.changeTarget(i, veh_dict[i]['intend_parking_block'])
                veh_dict[i]['temporary_destination'] = veh_dict[i]['intend_parking_block']
                veh_dict[i]['whether_went_to_intend_block'] = True

            # if this is not the first time vehicles have appeared
            else:
                # update the vehicle's arrival_time
                veh_dict[i]['arrival_time'] = step
                edge = traci.vehicle.getRoadID(i)
                road_id = traci.vehicle.getRoadID(i)
                veh_type = veh_dict[i]['vehicle_type']
                parking_area = veh_dict[i]['parking_zone_sequence']
                speed = traci.vehicle.getSpeed(i)
                # If this vehicle passed_through_zones_num is 0/1/2, and does not park successfully,
                # then count the temporary_cruising_time and passed_through_zones_num
                if veh_dict[i]['actual_passed_through_zones_num'] in [0, 1, 2] and edge[0] in ['a', 'b', 'c'] and veh_dict[i][
                    'whether_parking_success'] is False:
                    veh_dict[i]['temporary_cruising_time'] += 1
                    veh_dict[i]['average_cruising_speed'].append(speed)
                # if vehicle does not in the parking zone, set temporary_cruising_time = 0
                elif edge[0] not in ['a', 'b', 'c', ':']:
                    veh_dict[i]['temporary_cruising_time'] = 0
                # record the actual_cruising_time_illegal and average_cruising_speed_illegal
                if veh_dict[i]['temporary_whether_illegal_parking'] is True:
                    if veh_dict[i]['illegal_behavior_state'] == 3 and veh_dict[i]['actual_cruising_time_illegal'] >= veh_dict[i]['cruising_time_threshold_legal'] / 2:
                        pass
                    else:
                        veh_dict[i]['actual_cruising_time_illegal'] += 1
                        veh_dict[i]['average_cruising_speed_illegal'].append(speed)
                # perform illegal behavior, if illegal_behavior_state = 1 and actual_cruising_time_illegal
                # greater than the illegal cruising_time_threshold
                # only allow PUDO and LUL vehicles tranfer to illegal_behavior_state = 2, let PARK leave the system
                if veh_dict[i]['temporary_whether_illegal_parking'] is True and veh_dict[i]['illegal_behavior_state'] == 1 and veh_dict[i][
                    'actual_cruising_time_illegal'] >= veh_dict[i]['cruising_time_threshold_legal'] / 2:
                    if veh_dict[i]['vehicle_type'] != 'PARK':
                        veh_dict[i]['illegal_behavior_state'] = 2
                        traci.vehicle.changeTarget(i, veh_dict[i]['intend_parking_block'])
                        veh_dict[i]['temporary_destination'] = veh_dict[i]['intend_parking_block']
                    else:
                        veh_dict[i]['illegal_behavior_state'] = 3
                        traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                        veh_dict[i]['temporary_destination'] = veh_dict[i]['leave_location_system']                                      
                
                # if vehicle arrive at the temporary_destination, and is not the leave_location_system
                # or for risk adverse users, before they arrive at the intended parking block
                if (edge == veh_dict[i]['temporary_destination'] and edge != veh_dict[i]['leave_location_system']) or (
                    veh_dict[i]['prone_factor'] == 0 and veh_dict[i]['actual_passed_through_zones_num'] == 0 and edge[0] ==
                    veh_dict[i]['parking_zone_sequence'][0]):
                    # for risk adverse users
                    if veh_dict[i]['prone_factor'] == 0 and veh_dict[i]['actual_passed_through_zones_num'] == 0 and edge == veh_dict[i][
                        'intend_parking_block']:
                        veh_dict[i]['prone_factor'] = 2
                    # if vehicle arrive at the blocks
                    if edge in parking_area_list and veh_dict[i]['whether_parking_success'] is False:
                        # do not perform illegal behavior
                        if veh_dict[i]['temporary_whether_illegal_parking'] is False:
                            # if cruising_time greater than cruising_time_threshold_legal
                            if veh_dict[i]['temporary_cruising_time'] >= veh_dict[i]['cruising_time_threshold_legal']:
                                # actual_passed_through_zones_num + 1
                                veh_dict[i]['actual_passed_through_zones_num'] += 1

                                # get the max_num_of_zones_can_pass_through
                                want_parking_count = veh_dict[i]['max_num_of_zones_can_pass_through']

                                # update the illegal behavior data
                                if veh_dict[i]['actual_passed_through_zones_num'] == 1 and random.random() < veh_dict[i]['selfish_factor']:
                                    veh_dict[i]['temporary_whether_illegal_parking'] = True
                                    veh_dict[i]['illegal_behavior_state'] = 1
                                else:
                                    # set temporary_cruising_time as negative value
                                    veh_dict[i]['temporary_cruising_time'] = -30 * 60
                                # if the vehicle has tried to park want_parking_count times and failed to park
                                if want_parking_count == veh_dict[i]['actual_passed_through_zones_num'] and veh_dict[i][
                                    'temporary_whether_illegal_parking'] is False:
                                    traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                                elif want_parking_count > veh_dict[i]['actual_passed_through_zones_num'] and veh_dict[i][
                                    'temporary_whether_illegal_parking'] is False:
                                    # If the vehicle_type is "LUL", leave the system after one attempt
                                    if veh_type == "LUL":
                                        traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                                    else:
                                        # get the next parking zone
                                        current_parking_area = parking_area[veh_dict[i]['actual_passed_through_zones_num'] - 1]
                                        next_parking_area = parking_area[veh_dict[i]['actual_passed_through_zones_num']]
                                        next_one = random.choice(parking_link[current_parking_area + next_parking_area])
                                        traci.vehicle.changeTarget(i, next_one)
                                        veh_dict[i]['temporary_destination'] = next_one
                            # if the temporary_cruising_time is less than cruising_time_threshold_legal, and the car has not parked
                            elif 0 < veh_dict[i]['temporary_cruising_time'] < veh_dict[i]['cruising_time_threshold_legal']:
                                # if the vehicle is already in the parking block, and can park
                                if edge in parking_list:
                                    # get the 5 parking spaces information
                                    parking1 = edge[0] + 'p' + edge[1:] + '_1'
                                    parking2 = edge[0] + 'p' + edge[1:] + '_2'
                                    parking3 = edge[0] + 'p' + edge[1:] + '_3'
                                    parking4 = edge[0] + 'p' + edge[1:] + '_4'
                                    parking5 = edge[0] + 'p' + edge[1:] + '_5'
                                    parking_info = {}
                                    # whether find the appropriate parking space, initialize as false
                                    parking = 0
                                    # merge parking spaces data and buffer area data
                                    for key in [parking1, parking2, parking3, parking4, parking5]:
                                        parking_info[key] = parking_actual[key] + parking_buffer[key]
                                        # if parking is possible and the vehicle_type matches
                                        if parking_info[key] == 0 and veh_dict[i]['vehicle_type'] == parking_type_info[key] and road_id != veh_dict[i]['last_road_id']:
                                            # let vehicle park
                                            traci.vehicle.setParkingAreaStop(i, key, veh_dict[i]['parking_time_legal'])

                                            traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                                            # actual_passed_through_zones_num + 1
                                            veh_dict[i]['actual_passed_through_zones_num'] += 1
                                            # parking successful
                                            veh_dict[i]['whether_parking_success'] = True
                                            # store parking_space_id
                                            veh_dict[i]['parking_space_id'] = key
                                            # store buffer data
                                            parking_buffer[key] = 1
                                            # calculate actual_cruising_time
                                            if veh_dict[i]['actual_passed_through_zones_num'] == 1:
                                                veh_dict[i]['actual_cruising_time'] = veh_dict[i]['temporary_cruising_time']
                                            elif veh_dict[i]['actual_passed_through_zones_num'] == 2 and veh_dict[i]['illegal_behavior_state'] == 0:
                                                veh_dict[i]['actual_cruising_time'] = veh_dict[i]['temporary_cruising_time'] + \
                                                                              veh_dict[i]['cruising_time_threshold_legal']
                                            elif veh_dict[i]['actual_passed_through_zones_num'] == 2 and veh_dict[i]['illegal_behavior_state'] == 2:
                                                veh_dict[i]['actual_cruising_time'] = veh_dict[i]['temporary_cruising_time'] + \
                                                                              veh_dict[i]['cruising_time_threshold_legal'] + \
                                                                              veh_dict[i]['actual_cruising_time_illegal']
                                            elif veh_dict[i]['actual_passed_through_zones_num'] == 3 and veh_dict[i]['illegal_behavior_state'] == 0:
                                                veh_dict[i]['actual_cruising_time'] = veh_dict[i]['temporary_cruising_time'] + \
                                                                              veh_dict[i]['cruising_time_threshold_legal'] * 2
                                            elif veh_dict[i]['actual_passed_through_zones_num'] == 3 and veh_dict[i]['illegal_behavior_state'] == 2:
                                                veh_dict[i]['actual_cruising_time'] = veh_dict[i]['temporary_cruising_time'] + \
                                                                              veh_dict[i]['cruising_time_threshold_legal'] * 2 + \
                                                                              veh_dict[i]['actual_cruising_time_illegal']
                                            # already find appropriate parking space
                                            parking = 1
                                            # jump out of the for loop to prevent vehicles from continuing to park on the road
                                            break
                                    # if the vehicle cannot stop, proceed to the next road
                                    if parking == 0:
                                        if veh_dict[i]['actual_passed_through_zones_num'] == 0 and veh_dict[i]['prone_factor'] == 0:
                                            traci.vehicle.changeTarget(i, veh_dict[i]['intend_parking_block'])
                                            veh_dict[i]['temporary_destination'] = veh_dict[i]['intend_parking_block']
                                        else:
                                            next_one = random.choice(link[edge])
                                            traci.vehicle.changeTarget(i, next_one)
                                            veh_dict[i]['temporary_destination'] = next_one
                                # if the vehicle cannot stop, proceed to the next road
                                else:
                                    if veh_dict[i]['actual_passed_through_zones_num'] == 0 and veh_dict[i]['prone_factor'] == 0:
                                        traci.vehicle.changeTarget(i, veh_dict[i]['intend_parking_block'])
                                        veh_dict[i]['temporary_destination'] = veh_dict[i]['intend_parking_block']
                                    else:
                                        next_one = random.choice(link[edge])
                                        traci.vehicle.changeTarget(i, next_one)
                                        veh_dict[i]['temporary_destination'] = next_one
                            else:
                                pass
                        # perform illegal behavior
                        else:
                            if veh_dict[i]['illegal_behavior_state'] == 1 and veh_dict[i]['actual_cruising_time_illegal'] < veh_dict[i][
                                'cruising_time_threshold_legal'] / 2:
                                # if the vehicle is already in the parking block, and can park
                                if edge in parking_list:
                                    # get the 5 parking spaces information
                                    parking1 = edge[0] + 'p' + edge[1:] + '_1'
                                    parking2 = edge[0] + 'p' + edge[1:] + '_2'
                                    parking3 = edge[0] + 'p' + edge[1:] + '_3'
                                    parking4 = edge[0] + 'p' + edge[1:] + '_4'
                                    parking5 = edge[0] + 'p' + edge[1:] + '_5'
                                    parking_info = {}
                                    # whether find the appropriate parking space, initialize as false
                                    parking = 0
                                    # merge parking spaces data and buffer area data
                                    for key in [parking1, parking2, parking3, parking4, parking5]:
                                        parking_info[key] = parking_actual[key] + parking_buffer[key]
                                        # if parking is possible and the vehicle_type matches
                                        if parking_info[key] == 0:
                                            # let vehicle park
                                            traci.vehicle.setParkingAreaStop(i, key, veh_dict[i]['parking_time_legal'] / 2)

                                            traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                                            # parking successful
                                            veh_dict[i]['whether_parking_success'] = veh_dict[i]['whether_illegal_parking_success'] = True
                                            # does not continue illegal behavior
                                            veh_dict[i]['temporary_whether_illegal_parking'] = False
                                            # store parking_space_id
                                            veh_dict[i]['parking_space_id'] = key
                                            # store parking_space_type_illegal1
                                            veh_dict[i]['parking_space_type_illegal1'] = parking_type_info[key]
                                            # get final_cruising_time_illegal
                                            veh_dict[i]['final_cruising_time_illegal'] = veh_dict[i]['actual_cruising_time_illegal']
                                            # store buffer information
                                            parking_buffer[key] = 1
                                            # calculate actual_cruising_time
                                            veh_dict[i]['actual_cruising_time'] = veh_dict[i]['final_cruising_time_illegal'] + \
                                                                          veh_dict[i]['cruising_time_threshold_legal']
                                            # already find appropriate parking space
                                            parking = 1
                                            # jump out of the for loop to prevent vehicles from continuing to park on the road
                                            break
                                    # if the vehicle cannot stop, proceed to the next road
                                    if parking == 0:
                                        next_one = random.choice(link[edge])
                                        traci.vehicle.changeTarget(i, next_one)
                                        veh_dict[i]['temporary_destination'] = next_one
                                # if the vehicle cannot stop, proceed to the next road
                                else:
                                    next_one = random.choice(link[edge])
                                    traci.vehicle.changeTarget(i, next_one)
                                    veh_dict[i]['temporary_destination'] = next_one
                            # if illegal_behavior_state = 2
                            elif veh_dict[i]['illegal_behavior_state'] == 2:
                                # if vehicle arrives at intend_parking_block, and the illegal parking area has empty space
                                if edge == veh_dict[i]['intend_parking_block'] and traci.parkingarea.getVehicleCount(
                                        edge + '_il') < 8:
                                    # let vehicle park
                                    traci.vehicle.setParkingAreaStop(i, edge + '_il', veh_dict[i]['parking_time_legal'] / 2)

                                    traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                                    # parking successful
                                    veh_dict[i]['whether_parking_success'] = veh_dict[i]['whether_illegal_parking_success'] = True
                                    # does not continue illegal behavior
                                    veh_dict[i]['temporary_whether_illegal_parking'] = False
                                    # store parking_space_id
                                    veh_dict[i]['parking_space_id'] = edge + '_il'
                                    # get final_cruising_time_illegal
                                    veh_dict[i]['final_cruising_time_illegal'] = veh_dict[i]['actual_cruising_time_illegal']
                                    # calculate actual_cruising_time
                                    veh_dict[i]['actual_cruising_time'] = veh_dict[i]['final_cruising_time_illegal'] + \
                                                                  veh_dict[i]['cruising_time_threshold_legal']
                                # if vehicle arrives at intend_parking_block, and the illegal parking area does not have empty space
                                elif edge == veh_dict[i]['intend_parking_block'] and traci.parkingarea.getVehicleCount(
                                        edge + '_il') == 8:
                                    traci.vehicle.changeTarget(i, veh_dict[i]['leave_location_system'])
                                    # parking unsuccessful
                                    veh_dict[i]['whether_parking_success'] = veh_dict[i]['whether_illegal_parking_success'] = False
                                    # does not continue illegal behavior
                                    veh_dict[i]['temporary_whether_illegal_parking'] = False
                                    # get final_cruising_time_illegal
                                    veh_dict[i]['final_cruising_time_illegal'] = veh_dict[i]['actual_cruising_time_illegal']
                    else:
                        pass
                # if the vehicle does not reach its temporary_destination or reaches its destination
                else:
                    pass
                veh_dict[i]['last_road_id'] = road_id
        else:
            pass
