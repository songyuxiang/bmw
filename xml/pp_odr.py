import numpy as np
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, parse
import fun_write_odr
import copy

tree = parse('sample_road.xodr')
OpenDRIVE = tree.getroot()

# post fill width a

for RoadElement in OpenDRIVE.findall('./road[@id]'):
    road_id = RoadElement.attrib['id']
    if road_id > 1000:
        sh_ln = RoadElement.findall("./lanes/laneSection/right/*[@id='-1']")
        she = RoadElement.findall("./lanes/laneSection/right/*[@id='-1']/width")
        for she_id in range(0, len(she)):
            she[she_id].set("a", "2.0")
            new_she = copy.deepcopy(she[she_id])
            sh_ln[she_id].remove(she[she_id])
            sh_ln[she_id].insert(1, new_she)

# reorganize sequence for lanes
for RoadElement in OpenDRIVE.findall('./road[@id]'):
    road_id = RoadElement.attrib['id']
    sh_ls = RoadElement.findall("./lanes/laneSection")
    she = RoadElement.findall("./lanes/laneSection/left")
    for she_id in range(0, len(she)):
        new_she = copy.deepcopy(she[she_id])
        sh_ls[she_id].remove(she[she_id])
        sh_ls[she_id].insert(0, new_she)

# post fill elevationProfile
for RoadElement in OpenDRIVE.findall('./road[@id]'):
    sh_ln = RoadElement.find("elevationProfile")
    if sh_ln is None:
        sh_ln = SubElement(RoadElement,"elevationProfile")
        she = SubElement(sh_ln, "elevation")
    else:
        she = sh_ln.find("elevation")

    she.set("s", "0.0000000000000000e+00")
    she.set("a", "0.0000000000000000e+00")
    she.set("b", "0.0000000000000000e+00")
    she.set("c", "0.0000000000000000e+00")
    she.set("d", "0.0000000000000000e+00")


    new_she = copy.deepcopy(sh_ln)
    RoadElement.remove(sh_ln)
    RoadElement.insert(3, new_she)


# post fill elevationProfile
for RoadElement in OpenDRIVE.findall('./road[@id]'):
    sh_ln = RoadElement.find("lateralProfile")
    if sh_ln is None:
        sh_ln = SubElement(RoadElement,"lateralProfile")
        she = SubElement(sh_ln, "superelevation")
    else:
        she = sh_ln.find("superelevation")

    she.set("s", "0.0000000000000000e+00")
    she.set("a", "0.0000000000000000e+00")
    she.set("b", "0.0000000000000000e+00")
    she.set("c", "0.0000000000000000e+00")
    she.set("d", "0.0000000000000000e+00")

    new_she = copy.deepcopy(sh_ln)
    RoadElement.remove(sh_ln)
    RoadElement.insert(4, new_she)

# post fill controllers
do_controllers = False
if do_controllers:
    ControllerElement = SubElement(OpenDRIVE,"controller")
    ControlElement = SubElement(ControllerElement, "control")
    ControlElement.set("signalId", "Signal1")
    ControlElement.set("type","1.000.001")


# reorganize sequence for objects object
do_objects = True
if do_objects:
    for RoadElement in OpenDRIVE.findall('./road[@id]'):
        road_id = RoadElement.attrib['id']
        sh_oo = RoadElement.findall("./objects/object")

        she = RoadElement.findall("./objects/object/repeat")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(0, new_she)

        she = RoadElement.findall("./objects/object/outline")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(1, new_she)

        she = RoadElement.findall("./objects/object/material")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(2, new_she)

        she = RoadElement.findall("./objects/object/validity")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(3, new_she)

        she = RoadElement.findall("./objects/object/parkingSpace")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(4, new_she)

do_signals = True
if do_signals:
    # reorganize sequence for signals signal
    for RoadElement in OpenDRIVE.findall('./road[@id]'):
        road_id = RoadElement.attrib['id']
        sh_oo = RoadElement.findall("./signals/signal")

        she = RoadElement.findall("./signals/signal/validity")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(0, new_she)

        she = RoadElement.findall("./signals/signal/dependency")
        for she_id in range(0, len(she)):
            new_she = copy.deepcopy(she[she_id])
            sh_oo[she_id].remove(she[she_id])
            sh_oo[she_id].insert(1, new_she)

    # check validity of width vs border
    for RoadElement in OpenDRIVE.findall('./road[@id]'):
        road_id = RoadElement.attrib['id']
        sh_ln = RoadElement.findall("./lanes/laneSection//lane")

        for sh_ln_id in range(0, len(sh_ln)):
            sh_w = sh_ln[sh_ln_id].find("width")
            sh_b = sh_ln[sh_ln_id].find("border")

            if (sh_w is not None and
                sh_b is not None):
                if (len(sh_w.attrib['a']) == 1 and
                    len(sh_b.attrib['a']) == 1 ):
                    print "Error Must choose width OR border"
                elif (len(sh_w.attrib['a']) == 0 and
                    len(sh_b.attrib['a']) == 1 ):
                    sh_ln[sh_ln_id].remove(sh_w)
                elif (len(sh_w.attrib['a']) == 1 and
                              len(sh_b.attrib['a']) == 0):
                    sh_ln[sh_ln_id].remove(sh_b)
                else:
                    print "Missing width or border"
            else:
                pass

# post fill junction
do_junc=False
if do_junc:
    junction_element = np.genfromtxt(path_in + 'junction_element.csv', delimiter="|", dtype=str)

    sh2 = SubElement(OpenDRIVE,"junction")
    sh2.set('name', 'Junction1')
    sh2.set('id','1')
    for jid in range(1, len(junction_element)):
        row = junction_element[jid]
        sh3 = SubElement(sh2, "connection")
        sh4 = SubElement(sh3, "laneLink")
        sh3.set("id", row[0])
        sh3.set("incomingRoad", row[1])
        sh3.set("connectingRoad", row[2])
        sh3.set("contactPoint", row[3])
        sh4.set("from", row[4])
        sh4.set("to", row[5])

        if (row[0] == "J10" or row[0] == "J2"):
            sh3a = SubElement(sh2,"controller")
            sh3a.set("id", "Signal1")
            sh3a.set("type", "1.000.001")
            sh3a.set("sequence",'1')


# add lengths

#she = OpenDRIVE.findall("./*[@id='1001']")
#she.set("length", 32)
fix_road_length=False
if fix_road_length:
    road_length = 0
    she = OpenDRIVE.findall("./*[@id='1001']//geometry")
    RoadElement = OpenDRIVE.findall("./*[@id='1001']")
    for she_id in range(0, len(she)):
        lengthnow = she[she_id].attrib['length']
        road_length = np.float64(road_length) + np.float64(lengthnow)

    RoadElement[-1].set("length", road_length)


    RoadElementList = OpenDRIVE.findall("./road")
    for rid in range(0, len(RoadElementList)):
        RoadElement = RoadElementList[rid]
        she = RoadElement.findall(".//geometry")
        road_length = 0
        for she_id in range(0, len(she)):
            lengthnow = she[she_id].attrib['length']
            road_length = np.float64(road_length) + np.float64(lengthnow)

        RoadElement.set("length", str(road_length))


fun_write_odr.write_odr_to_csv(OpenDRIVE, "output.xodr")
