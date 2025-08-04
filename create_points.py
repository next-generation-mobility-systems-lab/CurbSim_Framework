from xml.etree import ElementTree as ET


def create_poi():
    # create a root tag
    additional = ET.Element("additional")

    # parse the XML file
    tree = ET.parse('parking_space.add.xml')
    root = tree.getroot()

    # for each parkingArea node
    for parking_area in root.findall('parkingArea'):
        # extract the id attribute
        parking_area_id = parking_area.get('id')
        if 'cp5' in parking_area_id or 'cp7' in parking_area_id:
            # extract the x and y attributes of the space node
            space = parking_area.find('space')
            x = str(float(space.get('x')) + 3)
            y = str(float(space.get('y')) + 4)

            # generate data in points.add.xml file to create node poi
            poi = ET.Element('poi',
                             {'id': parking_area_id, 'color': "red", 'layer': '202.00', 'x': x,
                              'y': y})

            # add to the routes root directory
            additional.append(poi)
        elif 'cp8' in parking_area_id or 'cp10' in parking_area_id:
            # extract the x and y attributes of the space node
            space = parking_area.find('space')
            x = str(float(space.get('x')) - 3)
            y = str(float(space.get('y')) + 4)

            # generate data in points.add.xml file to create node poi
            poi = ET.Element('poi',
                             {'id': parking_area_id, 'color': "red", 'layer': '202.00', 'x': x,
                              'y': y})

            # add to the routes root directory
            additional.append(poi)
        else:
            # extract the x and y attributes of the space node
            space = parking_area.find('space')
            x = space.get('x')
            y = str(float(space.get('y')) + 9)

            # generate data in points.add.xml file to create node poi
            poi = ET.Element('poi',
                             {'id': parking_area_id, 'color': "red", 'layer': '202.00', 'x': x,
                              'y': y})

            # add to the routes root directory
            additional.append(poi)

    # save file
    tree = ET.ElementTree(additional)
    tree.write("points.add.xml", encoding='utf-8')


if __name__ == '__main__':
    create_poi()
