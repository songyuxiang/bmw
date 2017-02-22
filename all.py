import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from matplotlib.patches import Circle
from syx import *


#load data
all_lanes_info=ReadList3L("all_lanes_info.txt")
section_pt=[]
pointX=[]
pointY=[]
pointZ=[]
point3D=[]
tangent3D=[]
tangentX=[]
tangentY=[]
tangentZ=[]
with open("points3D.txt",'r') as file:
	data_point3D=file.readlines()
for line in data_point3D:
	line=line.split(',')
	pointX.append(float(line[0]))
	pointY.append(float(line[1]))
	pointZ.append(float(line[2]))
	point3D.append([float(line[0]),float(line[1]),float(line[2])])
with open("tangent3D.txt",'r') as file:
	data_tangent3D=file.readlines()
for line in data_tangent3D:
	line=line.split(',')
	tangentX.append(float(line[0]))
	tangentY.append(float(line[1]))
	tangentZ.append(float(line[2]))
	tangent3D.append([float(line[0]),float(line[1]),float(line[2])])

for i in range(len(all_lanes_info)-1):
    if not compareLaneSection(all_lanes_info[i],all_lanes_info[i+1]):
        section_pt.append([i,pointX[i],pointY[i],pointZ[i]])

#input
road_name=getInput("road name")

id_current=getInput("corrent road id",valueType="i")
current_road_type=getInput("current road type",["motorway","rural","town","low" "speed","pedestrian","bicycle","unknown"])
current_road_jonctionID=getInput("current jonction ID",valueType='i')
speed_max=getInput("max speed",unit="km/h",valueType="f")/3.6
pre_road_type=getInput("predecessor road type",typeList=["road","jonction"])
pre_road_id=getInput("predecessor road id ",valueType="i")
pre_road_contactPt=getInput("predecessor road contact point",typeList=["start","end"])
successsor_road_type=getInput("successsor road type",typeList=["road","jonction"])
successsor_road_id=getInput("successsor road id",valueType="i")
successsor_road_contactPt=getInput("successsor road contact point",typeList=["start","end"])
neighor_road_side=getInput("neighor road side",typeList=["left","right"])
neighor_road_id=getInput("neighor road id",valueType="i")
neighor_road_direction=getInput("neighor road direction",typeList=["same","opposite"]) 



output_final=open("database.csv",'w+')
header="id|Niv_1|Niv_2|Niv_3|Niv_4|Niv_5|Niv_6|Niv_7|Niv_8|attribute|valeur|"

print>>output_final,header
print>>output_final,"%d|road||||||||name|%s|"%(id_current,road_name)
#print>>output_final,"%d|road||||||||length|%f|double precision|"%(id_current,cumulateLength)
print>>output_final,"%d|road||||||||id|%d|"%(id_current,id_current)
print>>output_final,"%d|road||||||||junction|%d|"%(id_current,current_road_jonctionID)
print>>output_final,"%d|road|link|predecessor||||||elementType|%s|"%(id_current,pre_road_type)
print>>output_final,"%d|road|link|predecessor||||||elementId|%d|"%(id_current,pre_road_id)
print>>output_final,"%d|road|link|predecessor||||||contactPoint|%s|"%(id_current,pre_road_contactPt)


print>>output_final,"%d|road|link|successor||||||elementType|%s|"%(id_current,successsor_road_type)
print>>output_final,"%d|road|link|successor||||||elementId|%d|"%(id_current,successsor_road_id)
print>>output_final,"%d|road|link|successor||||||contactPoint|%s|"%(id_current,successsor_road_contactPt)
print>>output_final,"%d|road|link|neighbor||||||side|%s|"%(id_current,neighor_road_side)
print>>output_final,"%d|road|link|neighbor||||||elementId|%d|"%(id_current,neighor_road_id)
print>>output_final,"%d|road|link|neighbor||||||direction|%s|"%(id_current,neighor_road_direction)
print>>output_final,"%d|road|type|speed||||||max|%d|"%(id_current,speed_max)
print>>output_final,"%d|road|type|speed||||||unit|m/s|"%id_current
print>>output_final,"%d|road|type|||||||s|%f|"%(id_current,0)
print>>output_final,"%d|road|type|||||||type|%s|"%(id_current,current_road_type)





size=len(pointX)
start=0
pointsNb=500
threshold=0.02
lengthUnit=0.1
end=pointsNb
polylinePointX=[]
polylinePointY=[]
circlePointX=[]
circlePointY=[]
linePointX=[]
linePointY=[]
cumulateLength=0
while start<size:
	x,y=rotateAndTranslate(pointX[start:end],pointY[start:end],0,-pointX[start],-pointY[start])
	#y=pointY[start:end]
	
	#test with polyline model
	para_polyline,p_polyline,gap_polyline=getPolylineModel(x,y)
	para_circle,gap_circle=getCircleModel(x,y)
	para_line,p_line,gap_line=getLineModel(x,y)
	if max(gap_polyline)>threshold and max(gap_circle)>threshold and max(gap_line)>threshold:
		#print("out of threshold")
		end=end-1
		continue

	##Use polyline model
	if max(gap_polyline)<max(gap_circle) and max(gap_polyline)<max(gap_line):
		print>>output_final,"%d|road|planView|geometry||||||s|%f|"%(id_current,cumulateLength)
		
		polylinePointX.extend(x)
		polylinePointY.extend(y)
		polylineLength=(len(x)-1)*lengthUnit
		cumulateLength=cumulateLength+polylineLength
		hdg=getOrientation(tangentX[start],tangentY[start])
		testX=np.array(x)
		testY=testX**3*para_polyline[0]+testX**2*para_polyline[1]
		plt.plot(testX,testY,'-')
		#plt.show()
		print>>output_final,"%d|road|planView|geometry||||||x|%f|"%(id_current,pointX[start])
		print>>output_final,"%d|road|planView|geometry||||||y|%f|"%(id_current,pointY[start])
		print>>output_final,"%d|road|planView|geometry||||||hdg|%f|"%(id_current,hdg)
		print>>output_final,"%d|road|planView|geometry||||||length|%f|"%(id_current,polylineLength)
		print>>output_final,"%d|road|planView|geometry|poly3|||||a|%f|"%(id_current,0)
		print>>output_final,"%d|road|planView|geometry|poly3|||||b|%f|"%(id_current,0)
		print>>output_final,"%d|road|planView|geometry|poly3|||||c|%f|"%(id_current,para_polyline[1])
		print>>output_final,"%d|road|planView|geometry|poly3|||||d|%f|"%(id_current,para_polyline[0])
		start=end-1
		end=start+pointsNb
		if(start+4>size):
			break
		else:
			if(end>size):
				end=size

	
	##Use line model
	elif max(gap_line)<=max(gap_polyline) and max(gap_line)<=max(gap_circle):
		print>>output_final,"%d|road|planView|geometry||||||s|%f|"%(id_current,cumulateLength)

		linePointX.extend(x)
		linePointY.extend(y)
		polylineLength=(len(x)-1)*lengthUnit
		cumulateLength=cumulateLength+polylineLength
		hdg=getOrientation(tangentX[start],tangentY[start])
		testX=np.array(x)
		testY=testX*para_polyline[0]
		plt.plot(testX,testY,'.')
		#plt.show()
		print>>output_final,"%d|road|planView|geometry||||||x|%f|"%(id_current,pointX[start])
		print>>output_final,"%d|road|planView|geometry||||||y|%f|"%(id_current,pointY[start])
		print>>output_final,"%d|road|planView|geometry||||||hdg|%f|"%(id_current,hdg)
		print>>output_final,"%d|road|planView|geometry||||||length|%f|"%(id_current,polylineLength)
		print>>output_final,"%d|road|planView|geometry|line|||||||"%id_current
		start=end-1
		end=start+pointsNb
		if(start+4>size):
			break
		else:
			if(end>size):
				end=size

	##Use arc model
	elif max(gap_circle)<max(gap_line) and max(gap_circle)<max(gap_polyline):
		print>>output_final,"%d|road|planView|geometry||||||s|%f|"%(id_current,cumulateLength)
		
		circlePointX.extend(x)
		circlePointY.extend(y)
		circlelineLength=(len(x)-1)*lengthUnit
		cumulateLength=cumulateLength+circlelineLength
		hdg=getOrientation(tangentX[start],tangentY[start])
		sign=getArcSign(tangentX[start],tangentY[start],para_circle[0],para_circle[1])
		plt.plot(x,y,'*')
		#plt.show()
		
		print>>output_final,"%d|road|planView|geometry||||||x|%f|"%(id_current,pointX[start])
		print>>output_final,"%d|road|planView|geometry||||||y|%f|"%(id_current,pointY[start])
		print>>output_final,"%d|road|planView|geometry||||||hdg|%f|"%(id_current,hdg)
		print>>output_final,"%d|road|planView|geometry||||||length|%f|"%(id_current,circlelineLength)
		print>>output_final,"%d|road|planView|geometry|arc|||||curvature|%f|"%(id_current,1/para_circle[2])		
		start=end-1
		end=start+pointsNb
		if(start+4>size):
			break
		else:
			if(end>size):
				end=size

# profilNb=2
# for i in range(profilNb):
# 	print>>output_final,"%d|road|elevationProfile|elevation||||||s|%f|double precision. Units meters. Non-negative. Start position (s-coordinate)|"%(id_current,0)	
# 	print>>output_final,"%d|road|elevationProfile|elevation||||||a|%f|double precision. Units meters. Positive or negative|"%(id_current,0)	
# 	print>>output_final,"%d|road|elevationProfile|elevation||||||b|%f|double precision. Dimensionless. Positive or negative.|"%(id_current,0)	
# 	print>>output_final,"%d|road|elevationProfile|elevation||||||c|%f|double precision. Units 1/m. Positive or negative|"%(id_current,0)	
# 	print>>output_final,"%d|road|elevationProfile|elevation||||||d|%f|double precision. Units 1/m2. Positive or negative|"%(id_current,0)	
# 	print>>output_final,"%d|road|lateralProfile|superelevation||||||s|%f|double precision. Units meters. Non-negative. Start position (s-coordinate)|"%(id_current,0)	
# 	print>>output_final,"%d|road|lateralProfile|superelevation||||||a|%f|double precision. Units radians. Positive or negative. Superelevation at s=0|"%(id_current,0)	
# 	print>>output_final,"%d|road|lateralProfile|superelevation||||||b|%f|double precision. Units radians/meter. Positive or negative.|"%(id_current,0)	
# 	print>>output_final,"%d|road|lateralProfile|superelevation||||||c|%f|double precision. Units radians/m2. Positive or negative|"%(id_current,0)	
# 	print>>output_final,"%d|road|lateralProfile|superelevation||||||d|%f|double precision. Units radians/m3. Positive or negative|"%(id_current,0)	

laneSectionNb=len(section_pt)+1
sectionStartPos=0
sectionS=0
for i in range(laneSectionNb):
	try:
		sectionPts=point3D[sectionStartPos:section_pt[i][0]]
		sectionLanesInfo=all_lanes_info[sectionStartPos:section_pt[i][0]]
	except IndexError:
		sectionPts=point3D[sectionStartPos:size]
		sectionLanesInfo=all_lanes_info[sectionStartPos:size]
	s=len(sectionPts)*lengthUnit
	try:
		sectionStartPos=section_pt[i][0]
	except IndexError:
		sectionStartPos=size
	lane_id=0
	# lane_offset_s=0
	# lane_offset_a=0
	# lane_offset_b=0
	# lane_offset_c=0
	# lane_offset_d=0

	# print>>output_final,"%d|road|lanes|laneOffset||||||s|%f|"%(id_current,lane_offset_s)
	# print>>output_final,"%d|road|lanes|laneOffset||||||a|%f|"%(id_current,lane_offset_a)
	# print>>output_final,"%d|road|lanes|laneOffset||||||b|%f|"%(id_current,lane_offset_b)
	# print>>output_final,"%d|road|lanes|laneOffset||||||c|%f|"%(id_current,lane_offset_c)
	# print>>output_final,"%d|road|lanes|laneOffset||||||d|%f|"%(id_current,lane_offset_d)
	lane_section_s=sectionS
	sectionS=sectionS+s
	lane_section_singleSide=""
	print>>output_final,"%d|road|lanes|laneSection||||||s|%f|"%(id_current,lane_section_s)
	
	if checkSingleSide(sectionLanesInfo[0]):
		lane_section_singleSide="true"
	else:
		lane_section_singleSide="false"
	print>>output_final,"%d|road|lanes|laneSection||||||singleSide|%s|"%(id_current,lane_section_singleSide)
	if not checkVariedLane(sectionLanesInfo[0]):
		for lane in	sectionLanesInfo[0]:
			if lane[1]=="center":
				center_lane_id=0
				center_lane_type=lane[5]
				print>>output_final,"%d|road|lanes|laneSection|center|lane||||type|%s|"%(id_current,center_lane_type)	
				print>>output_final,"%d|road|lanes|laneSection|center|lane||||id|%d|"%(id_current,center_lane_id)	
				#to add# print>>output_final,"%d|road|lanes|laneSection|center|lane||||level|%s|True = flat. Do not apply superelevation. False=apply crossfall and superelevation|"%(id_current,"true")	
				#to add# center_lane_prodecessor_id=raw_input("center lane prodecessor id ",'i')
				center_lane_prodecessor_id=0
				print>>output_final,"%d|road|lanes|laneSection|center|lane|link|predecessor||id|%d|"%(id_current,center_lane_prodecessor_id)	
				#to add# center_lane_successor_id=raw_input("Center lane successor id",'i')
				center_lane_successor_id=0
				print>>output_final,"%d|road|lanes|laneSection|center|lane|link|successor||id|%d|"%(id_current,center_lane_successor_id)	
				#to add# center_lane_roadmark_offset=float(raw_input("center lane roadmark offset : ")or 0)
				center_lane_roadmark_offset=0
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||sOffset|%f|"%(id_current,center_lane_roadmark_offset)	

				center_lane_roadmark_type=lane[3]
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||type|%s|"%(id_current,center_lane_roadmark_type)	
				center_lane_roadmark_weight=lane[4]

				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||weight|%s|"%(id_current,center_lane_roadmark_weight)	
				
				 #to add#
				center_lane_roadmark_color="standard"
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||color|%s|"%(id_current,center_lane_roadmark_color)	
				center_lane_roadmark_material="standard"
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||material|%s|"%(id_current,center_lane_roadmark_material)	
	
				center_lane_roadmark_width=float(lane[2])
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||width|%f|"%(id_current,center_lane_roadmark_width)
				center_lane_roadmark_laneChange="none"
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||laneChange|%s|"%(id_current,center_lane_roadmark_laneChange)
				center_lane_roadmark_height=0
				print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||height|%f|"%(id_current,center_lane_roadmark_height)

	#didn't use roadmark type name/width/line

	####
	#### right lane
			if lane[1]=="right":
				right_lane_type=lane[5]
				right_lane_id=0-lane_id
				print>>output_final,"%d|road|lanes|laneSection|right|lane||||type|%s|"%(id_current,right_lane_type)	
				print>>output_final,"%d|road|lanes|laneSection|right|lane||||id|%d|"%(id_current,right_lane_id)	
				# print>>output_final,"%d|road|lanes|laneSection|right|lane||||level|%s|True = flat. Do not apply superelevation. False=apply crossfall and superelevation|"%(id_current,"true")	
				right_lane_predecessor_id=right_lane_id
				print>>output_final,"%d|road|lanes|laneSection|right|lane|link|predecessor||id|%d|"%(id_current,right_lane_predecessor_id)	
				right_lane_successor_id=right_lane_id
				print>>output_final,"%d|road|lanes|laneSection|right|lane|link|successor||id|%d|"%(id_current,right_lane_successor_id)	
				right_lane_width_sOffset=0
				print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||sOffset|%f|"%(id_current,right_lane_width_sOffset)
				right_lane_width_a=-float(lane[0])
				right_lane_width_b=0
				right_lane_width_c=0
				right_lane_width_d=0
				print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||a|%f|"%(id_current,right_lane_width_a)
				print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||b|%f|"%(id_current,right_lane_width_b)
				print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||c|%f|"%(id_current,right_lane_width_c)
				print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||d|%f|"%(id_current,right_lane_width_d)
				# right_lane_border_sOffset=0
				# print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||sOffset|%f|"%(id_current,right_lane_border_sOffset)
				# #question:what's this
				# right_lane_border_a=0
				# right_lane_border_b=0
				# right_lane_border_c=0
				# right_lane_border_d=0
				# print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||a|%f|"%(id_current,right_lane_border_a)
				# print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||b|%f|"%(id_current,right_lane_border_b)
				# print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||c|%f|"%(id_current,right_lane_border_c)
				# print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||d|%f|"%(id_current,right_lane_border_d)


				right_lane_roadmark_offset=0
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||sOffset|%f|"%(id_current,right_lane_roadmark_offset)	
				# to add
				right_lane_roadmark_type=lane[3]

				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||type|%s|"%(id_current,right_lane_roadmark_type)	
				right_lane_roadmark_weight=lane[4]
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||weight|%s|"%(id_current,right_lane_roadmark_weight)	
				
				right_lane_roadmark_color="standard"
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||color|%s|"%(id_current,right_lane_roadmark_color)	
				right_lane_roadmark_material="standard"
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||material|%s|"%(id_current,right_lane_roadmark_material)	
				right_lane_roadmark_width=float(lane[2])
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||width|%f|"%(id_current,right_lane_roadmark_width)
				right_lane_roadmark_laneChange="none"
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||laneChange|%s|"%(id_current,right_lane_roadmark_laneChange)
				
				right_lane_roadmark_height=0
				print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||height|%f|"%(id_current,right_lane_roadmark_height)
				#don't have roadmark type
				#don't have material/visibility/speed/access/height/rule

			lane_id=lane_id+1
	# else:
	# 	size=len(X)
	# 	start=0
	# 	end=30
	# 	for i in range(len(all_lanes_info))
	# 	while start<size:
	# 		x,y=rotateAndTranslate(X[start:end],Y[start:end],0,-X[start],-Y[start])
	# 		para_polyline,p_polyline,gap_polyline=getPolylineModel(x,y)
	# 		if max(gap_polyline)>threshold :
	# 			end=end-1
	# 			continue

# objectNb=3
# for i in range(objectNb):
# 	object_type=getInput("object type",typeList=["guiderails","road divider","sign gantries","reflector posts","emergency phones","traffic light","stop line","traffic islands","bicycle / pedestrian crossing","parking lot"])
	
# 	print>>output_final,"%d|road|objects|object||||||type|%s||"%(id_current,object_type)
# 	object_name=getInput("object name") 
# 	print>>output_final,"%d|road|objects|object||||||name|%s||"%(id_current,object_name)
# 	object_id=getInput("object id ","i") 
# 	print>>output_final,"%d|road|objects|object||||||id|%d|."%(id_current,object_id)
# 	object_s=float(raw_input("object s : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||s|%f|"%(id_current,object_s)
# 	object_t=float(raw_input("object t : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||t|%f|"%(id_current,object_t)
# 	object_zOffset=float(raw_input("object zOffset : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||zOffset|%f|"%(id_current,object_zOffset)
# 	object_validLength=float(raw_input("object validLength : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||validLength|%f|"%(id_current,object_validLength)
# 	object_orientation=float(raw_input("object orientation : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||orientation|%f|"%(id_current,object_orientation)
# 	object_length=float(raw_input("object length : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||length|%f|"%(id_current,object_length)
# 	object_width=float(raw_input("object width : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||width|%f|"%(id_current,object_width)
# 	object_radius=float(raw_input("object radius : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||radius|%f|"%(id_current,object_radius)
# 	object_height=float(raw_input("object height : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||height|%f|"%(id_current,object_height)
# 	object_hdg=float(raw_input("object hdg : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||hdg|%f|"%(id_current,object_hdg)
# 	object_pitch=float(raw_input("object pitch : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||pitch|%f|"%(id_current,object_pitch)
# 	object_roll=float(raw_input("object roll : ") or 0)
# 	print>>output_final,"%d|road|objects|object||||||roll|%f|"%(id_current,object_roll)
# ## no repeat/outline/material/validity/parkingspace/
# hasTunnel=raw_input("is there tunnel?(y/n):") or "y"
# if hasTunnel=="y":
# 	tunnel_name=raw_input("tunnel name : ") or "test tunnel"
# 	print>>output_final,"%d|road|objects|tunnel||||||name|%s|"%(id_current,tunnel_name)
# 	tunnel_s=float(raw_input("tunnel s : ") or 0)
# 	print>>output_final,"%d|road|objects|tunnel||||||s|%f|"%(id_current,tunnel_s)
# 	tunnel_length=float(raw_input("tunnel length : ") or 0)
# 	print>>output_final,"%d|road|objects|tunnel||||||length|%f|"%(id_current,tunnel_length)
# 	tunnel_id=int(raw_input("tunnel id : ") or 0)
# 	print>>output_final,"%d|road|objects|tunnel||||||id|%d|"%(id_current,tunnel_id)
# 	tunnel_lighting=float(raw_input("tunnel lighting : ") or 0)
# 	print>>output_final,"%d|road|objects|tunnel||||||lighting|%f|"%(id_current,tunnel_lighting)
# 	tunnel_daylight=float(raw_input("tunnel daylight : ") or 0)
# 	print>>output_final,"%d|road|objects|tunnel||||||daylight|%f|"%(id_current,tunnel_daylight)
# 	tunnel_type=raw_input("tunnel type : standard(s)/underpass(u) ") or "s"
# 	if tunnel_type=='u':
# 		tunnel_type="underpass"
# 	else:
# 		tunnel_type="standard"
# 	print>>output_final,"%d|road|objects|tunnel||||||type|%s|"%(id_current,tunnel_type)
# 	tunnel_fromLane=int(raw_input("tunnel from lane id : ") or 1)
# 	print>>output_final,"%d|road|objects|tunnel|validity|||||fromLane|%d|"%(id_current,tunnel_fromLane)
# 	tunnel_toLane=int(raw_input("tunnel to lane id : ") or 2)
# 	print>>output_final,"%d|road|objects|tunnel|validity|||||toLane|%d|"%(id_current,tunnel_toLane)
# hasBridge=raw_input("is there bridge?(y/n)") or "y"
# if hasBridge=="y":
# 	bridge_name=raw_input("bridge name : ") or "test bridge"
# 	print>>output_final,"%d|road|objects|bridge||||||name|%s|"%(id_current,bridge_name)
# 	bridge_s=float(raw_input("bridge s : ") or 0)
# 	print>>output_final,"%d|road|objects|bridge||||||s|%f|"%(id_current,bridge_s)
# 	bridge_length=float(raw_input("bridge length : ") or 0)
# 	print>>output_final,"%d|road|objects|bridge||||||length|%f|"%(id_current,bridge_length)
# 	bridge_id=int(raw_input("bridge id : ") or 0)
# 	print>>output_final,"%d|road|objects|bridge||||||id|%d|"%(id_current,bridge_id)
# 	bridge_type=raw_input("bridge type : wood(w)/brick(b)/steel(s)/concrete(c) ") or "b"
# 	if bridge_type=='w':
# 		bridge_type="wood"
# 	elif bridge_type=='s':
# 		bridge_type="steel"
# 	elif bridge_type=='c':
# 		bridge_type="concrete"
# 	else:
# 		bridge_type="brick"
# 	print>>output_final,"%d|road|objects|bridge||||||type|%s|"%(id_current,bridge_type)
# hasSignal=raw_input("is there signal?(y/n)") or "y"
# if hasSignal=="y":
# 	signal_name=raw_input("signal name : ") or "test signal"
# 	print>>output_final,"%d|road|signals|signal||||||name||%s|"%(id_current,signal_name)
# 	signal_s=float(raw_input("signal s : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||s|%f|"%(id_current,signal_s)
# 	signal_t=float(raw_input("signal t : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||t|%f|"%(id_current,signal_t)
# 	signal_id=int(raw_input("signal id : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||id|%f|"%(id_current,signal_id)
# 	signal_dynamic=raw_input("bridge dynamic : (y/n)") or "no"
# 	if signal_dynamic=="y":
# 		signal_dynamic="yes"
# 	else:
# 		signal_dynamic="no"
# 	print>>output_final,"%d|road|signals|signal||||||dynamic|%s||"%(id_current,signal_dynamic)
# 	signal_orientation=raw_input("bridge orientation : (+/-)") or ""
# 	if signal_orientation=="+":
# 		signal_orientation="+"
# 	else:
# 		signal_orientation="-"
# 	print>>output_final,"%d|road|signals|signal||||||orientation|%s||"%(id_current,signal_orientation)
# 	signal_zOffset=float(raw_input("signal zOffset : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||zOffset|%f|"%(id_current,signal_zOffset)
# 	signal_country=raw_input("country:") or "DEU"
# 	print>>output_final,"%d|road|signals|signal||||||country|%s|ISO 3166 alpha-3 Country Code|"%(id_current,signal_country)
# 	signal_type=raw_input("signal type:") or "310"
# 	print>>output_final,"%d|road|signals|signal||||||type|%s|ISO 3166 alpha-3 Country Code|"%(id_current,signal_type)
# 	signal_value=float(raw_input("signal value : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||value|%f|"%(id_current,signal_value)
# 	signal_unit=raw_input("unit:(m/km/mile)") or "m"
# 	print>>output_final,"%d|road|signals|signal||||||unit|%s|"%(id_current,signal_unit)
# 	signal_height=float(raw_input("signal height : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||height|%s|"%(id_current,signal_height)
# 	signal_width=float(raw_input("signal width : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||width|%s|"%(id_current,signal_width)

# 	signal_hOffset=float(raw_input("signal hOffset : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||hOffset|%s|"%(id_current,signal_hOffset)
# 	signal_pitch=float(raw_input("signal pitch : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||pitch|%s|"%(id_current,signal_pitch)
# 	signal_roll=float(raw_input("signal roll : ") or 0)
# 	print>>output_final,"%d|road|signals|signal||||||roll|%s|"%(id_current,signal_roll)

# 	signal_text=raw_input("text:") or ""
# 	print>>output_final,"%d|road|signals|signal||||||text|%s|"%(id_current,signal_text)
file.close()
output_final.close()