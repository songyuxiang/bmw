import numpy as np
import matplotlib.pyplot as plt
from scipy      import optimize
from matplotlib.patches import Circle

def getLeastSquare(list):
	x=0
	for i in list:
		x=i**2+x
	return np.sqrt(x)
def getPolylineModel(x,y):
	z_polyline = np.polyfit(x, y, 3)
	p_polyline=np.poly1d(z_polyline)
	gap_polyline=np.abs(y-p_polyline(x))
	return z_polyline,p_polyline,gap_polyline
def calc_R(xc, yc):
	""" calculate the distance of each 2D points from the center (xc, yc) """
	return np.sqrt((x-xc)**2 + (y-yc)**2)

def f_2(c):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()
def getCircleModel(x,y):
	x_m = np.mean(x)
	y_m = np.mean(y)
	# calculation of the reduced coordinates
	u = x - x_m
	v = y - y_m
	center_estimate = x_m, y_m
	center_2, ier = optimize.leastsq(f_2, center_estimate)

	xc_2, yc_2 = center_2
	Ri_2       = calc_R(*center_2)
	R_2        = Ri_2.mean()
	residu_2   = sum((Ri_2 - R_2)**2)
	parameters=[xc_2,yc_2,R_2]
	gap=np.sqrt((x-xc_2)**2+(y-yc_2)**2)-R_2
	return parameters,gap
def getLineModel(x,y):
	z_line = np.polyfit(x, y, 1)
	p_line=np.poly1d(z_line)
	gap_line=np.abs(y-p_line(x))
	return z_line,p_line,gap_line
def getOrientation(x,y):
	orientation=0
	if x>=0:
	  	if y>=0:
			rientation=np.arctan(y/x)
		else:
			orientation=2*np.pi-np.arctan(-y/x)
	else :
		if y>=0:
			orientation=np.pi-np.arctan(-y/x)
		else:
			orientation=np.pi+np.arctan(y/x)

	return orientation

def rotateAndTranslate(x_list,y_list,angle=0,x0=0,y0=0):
	x_t=[]
	y_t=[]
	if len(x_list)!=len(y_list):
		print("Error:x_list has to have the same size of y_list")
	else:
		size=len(x_list)
		for i in range(size):
			x_t.append(x_list[i]*np.cos(angle)-y_list[i]*np.sin(angle)+x0)
			y_t.append(x_list[i]*np.sin(angle)+y_list[i]*np.cos(angle)+y0)
	return x_t,y_t
def getArcSign(tanX,tanY,centerX,centerY):
	oriTan=getOrientation(tanX,tanY)
	oriCenter=getOrientation(centerX,centerY)
	if oriTan-oriCenter>np.pi:
		oriCenter=oriCenter+np.pi*2
	if oriCenter-oriTan>np.pi:
		oriTan=oriTan+np.pi*2
	if oriTan>oriCenter:
		return "-"
	if oriTan<oriCenter:
		return "+"




#input
road_name=raw_input("road name : ") or "route test"
id_current=int(raw_input("current road id : ") or 1) 
current_road_type=raw_input("current road type  (motorway(m);rural(r);town(t);low speed(l);pedestrian (p);bicycle(b);unknown(u) : ") or "m"
if current_road_type=="m" or current_road_type=="M":
	current_road_type="motorway"
elif current_road_type=="t" or current_road_type=="T":
	current_road_type="town"
elif current_road_type=="l" or current_road_type=="L":
	current_road_type="lowSpeed"
elif current_road_type=="p" or current_road_type=="P":
	current_road_type="pedestrian"
elif current_road_type=="b" or current_road_type=="B":
	current_road_type="bicycle"
elif current_road_type=="u" or current_road_type=="U":
	current_road_type="unknown"
elif current_road_type=="r" or current_road_type=="R":
	current_road_type="rural"
else :
	print("Error: you have to take a option!")
try:
	speed_max=float(raw_input("max speed (km/h) : ") or 50)/3.6
except:
	print("You have to enter a number!")
pre_road_type=raw_input("predecessor road name (road(r),jonction(j)) : ") or "r"
if pre_road_type=="r" or pre_road_type=="R":
	pre_road_type="road"
if pre_road_type=="j" or pre_road_type=="J":
	pre_road_type="jonction"

pre_road_id=int(raw_input("predecessor road id : ") or 2) 
pre_road_contactPt=raw_input("predecessor road contact point (start(s),end(e)) :")
if pre_road_contactPt=="s" or pre_road_contactPt=="S":
	pre_road_contactPt="start"
if pre_road_contactPt=="e" or pre_road_contactPt=="E":
	pre_road_contactPt="end"

successsor_road_type=raw_input("successsor road name (road(r),jonction(j)) : ") or "r"
if successsor_road_type=="r" or pre_road_type=="R":
	successsor_road_type="road"
if successsor_road_type=="j" or pre_road_type=="J":
	successsor_road_type="jonction"

successsor_road_id=int(raw_input("successsor road id : ") or 3)
successsor_road_contactPt=raw_input("successsor road contact point (start(s),end(e)) :") or "s"
if successsor_road_contactPt=="s" or successsor_road_contactPt=="S":
	successsor_road_contactPt="start"
if successsor_road_contactPt=="e" or successsor_road_contactPt=="E":
	successsor_road_contactPt="end"

neighor_road_side=raw_input("neighor road side (left(l),right(r)) : ") or "l"
if successsor_road_type=="l" or pre_road_type=="L":
	successsor_road_type="left"
if successsor_road_type=="r" or pre_road_type=="R":
	successsor_road_type="right"

neighor_road_id=int(raw_input("neighor road id : ") or 4)
neighor_road_direction=raw_input("neighor road direction (same(s),opposite(o)) :") or "s"
if successsor_road_contactPt=="s" or successsor_road_contactPt=="S":
	successsor_road_contactPt="same"
if successsor_road_contactPt=="o" or successsor_road_contactPt=="O":
	successsor_road_contactPt="opposite"




output_final=open("database.csv",'w+')
header="id|Niv_1|Niv_2|Niv_3|Niv_4|Niv_5|Niv_6|Niv_7|Niv_8|attribute|valeur|comments|comments2"

print>>output_final,header
print>>output_final,"%d|road||||||||name|%s|string|"%(id_current,road_name)
#print>>output_final,"%d|road||||||||length|%f|double precision|"%(id_current,cumulateLength)
print>>output_final,"%d|road||||||||id|%d|Unique Non-negative integer|"%(id_current,id_current)
print>>output_final,"%d|road||||||||junction||integer or alphanumeric. Use -1 for none|"%(id_current)
print>>output_final,"%d|road|link|predecessor||||||elementType|%s||"%(id_current,pre_road_type)
print>>output_final,"%d|road|link|predecessor||||||elementID|%d|integer or alphanumeric|"%(id_current,pre_road_id)
print>>output_final,"%d|road|link|predecessor||||||contactPoint|%s||"%(id_current,pre_road_contactPt)


print>>output_final,"%d|road|link|successor||||||elementType|%s||"%(id_current,successsor_road_type)
print>>output_final,"%d|road|link|successor||||||elementID|%d|integer or alphanumeric|"%(id_current,successsor_road_id)
print>>output_final,"%d|road|link|successor||||||contactPoint|%s||"%(id_current,successsor_road_contactPt)
print>>output_final,"%d|road|link|neighbor||||||side|%s||"%(id_current,neighor_road_side)
print>>output_final,"%d|road|link|neighbor||||||elementID|%d|integer or alphanumeric|"%(id_current,neighor_road_id)
print>>output_final,"%d|road|link|neighbor||||||direction|%s||"%(id_current,neighor_road_direction)
print>>output_final,"%d|road|type|speed||||||max|%d|Meters/sec in integer otherwise drop-menu option. Speed limit.|"%(id_current,speed_max)
print>>output_final,"%d|road|type|speed||||||unit|m/s|optional|"%id_current
print>>output_final,"%d|road|type|||||||s|%f|double precision. Non-negative|"%(id_current,0)
print>>output_final,"%d|road|type|||||||type|%s||"%(id_current,current_road_type)





output=open("geometry.csv",'w+')
print>>output,"Type;Parameters;x;y;length;s;hdg"
pointX=[]
pointY=[]
tangentX=[]
tangentY=[]
with open("point3D",'r') as file:
	data_point3D=file.readlines()
for line in data_point3D:
	line=line.split(',')
	pointX.append(float(line[0]))
	pointY.append(float(line[1]))
with open("tan3D",'r') as file:
	data_tangent3D=file.readlines()
for line in data_tangent3D:
	line=line.split(',')
	tangentX.append(float(line[0]))
	tangentY.append(float(line[1]))	
size=len(pointX)
start=0
pointsNb=100
threshold=0.01
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
		print>>output_final,"%d|road|planView|geometry||||||s|%f|Meters, double precision. Non-negative|"%(id_current,cumulateLength)
		
		polylinePointX.extend(x)
		polylinePointY.extend(y)
		polylineLength=(len(x)-1)*lengthUnit
		cumulateLength=cumulateLength+polylineLength
		hdg=getOrientation(tangentX[start],tangentY[start])
		testX=np.array(x)
		testY=testX**3*para_polyline[0]+testX**2*para_polyline[1]
		plt.plot(testX,testY,'-')
		#plt.show()
		print>>output,"polyline"+';'+"a=0,b=0,c=%s,d=%s"%(str(para_polyline[1]),str(para_polyline[0]))+';'+str(pointX[start])+';'+str(pointY[start])+';'+str(polylineLength)+';'+str(cumulateLength)+';'+str(hdg)
		print>>output_final,"%d|road|planView|geometry||||||x|%f|Meters, double precision. Positve or negative|"%(id_current,pointX[start])
		print>>output_final,"%d|road|planView|geometry||||||y|%f|Meters, double precision. Positve or negative|"%(id_current,pointY[start])
		print>>output_final,"%d|road|planView|geometry||||||hdg|%f|Radians, double precision, positve or negative|"%(id_current,hdg)
		print>>output_final,"%d|road|planView|geometry||||||length|%f|Meters, double precision. Non-negative|"%(id_current,polylineLength)
		print>>output_final,"%d|road|planView|geometry|poly3|||||a|%f|double precision. Units meters|"%(id_current,0)
		print>>output_final,"%d|road|planView|geometry|poly3|||||b|%f|double precision. Dimensionless|"%(id_current,0)
		print>>output_final,"%d|road|planView|geometry|poly3|||||c|%f|double precision. Units 1/m. Positive or negative|"%(id_current,para_polyline[1])
		print>>output_final,"%d|road|planView|geometry|poly3|||||d|%f|double precision. Units 1/m2. Positive or negative|"%(id_current,para_polyline[0])
		start=end-1
		end=start+pointsNb
		if(start+4>size):
			break
		else:
			if(end>size):
				end=size

	
	##Use line model
	elif max(gap_line)<=max(gap_polyline) and max(gap_line)<=max(gap_circle):
		print>>output_final,"%d|road|planView|geometry||||||s|%f|Meters, double precision. Non-negative|"%(id_current,cumulateLength)

		linePointX.extend(x)
		linePointY.extend(y)
		polylineLength=(len(x)-1)*lengthUnit
		cumulateLength=cumulateLength+polylineLength
		hdg=getOrientation(tangentX[start],tangentY[start])
		testX=np.array(x)
		testY=testX*para_polyline[0]
		plt.plot(testX,testY,'.')
		#plt.show()
		print>>output,"line"+';'+"a=%s,b=%s"%(str(para_line[1]),str(para_line[0]))+';'+str(pointX[start])+';'+str(pointY[start])+';'+str(polylineLength)+';'+str(cumulateLength)+';'+str(hdg)
		print>>output_final,"%d|road|planView|geometry||||||x|%f|Meters, double precision. Positve or negative|"%(id_current,pointX[start])
		print>>output_final,"%d|road|planView|geometry||||||y|%f|Meters, double precision. Positve or negative|"%(id_current,pointY[start])
		print>>output_final,"%d|road|planView|geometry||||||hdg|%f|Radians, double precision, positve or negative|"%(id_current,hdg)
		print>>output_final,"%d|road|planView|geometry||||||length|%f|Meters, double precision. Non-negative|"%(id_current,polylineLength)
		print>>output_final,"%d|road|planView|geometry|line|||||"%id_current
		start=end-1
		end=start+pointsNb
		if(start+4>size):
			break
		else:
			if(end>size):
				end=size

	##Use arc model
	elif max(gap_circle)<max(gap_line) and max(gap_circle)<max(gap_polyline):
		print>>output_final,"%d|road|planView|geometry||||||s|%f|Meters, double precision. Non-negative|"%(id_current,cumulateLength)
		
		circlePointX.extend(x)
		circlePointY.extend(y)
		circlelineLength=(len(x)-1)*lengthUnit
		cumulateLength=cumulateLength+circlelineLength
		hdg=getOrientation(tangentX[start],tangentY[start])
		sign=getArcSign(tangentX[start],tangentY[start],para_circle[0],para_circle[1])
		plt.plot(x,y,'*')
		#plt.show()
		
		print>>output,"arc"+';'+"curvature=%s%s"%(sign,str(1/para_circle[2]))+';'+str(pointX[start])+';'+str(pointY[start])+';'+str(circlelineLength)+';'+str(cumulateLength)+';'+str(hdg)
		print>>output_final,"%d|road|planView|geometry||||||x|%f|Meters, double precision. Positve or negative|"%(id_current,pointX[start])
		print>>output_final,"%d|road|planView|geometry||||||y|%f|Meters, double precision. Positve or negative|"%(id_current,pointY[start])
		print>>output_final,"%d|road|planView|geometry||||||hdg|%f|Radians, double precision, positve or negative|"%(id_current,hdg)
		print>>output_final,"%d|road|planView|geometry||||||length|%f|Meters, double precision. Non-negative|"%(id_current,circlelineLength)
		print>>output_final,"%d|road|planView|geometry|arc|||||curvature|%f|double precision. Units 1/m. Positive or negative|"%(id_current,1/para_circle[2])		
		start=end-1
		end=start+pointsNb
		if(start+4>size):
			break
		else:
			if(end>size):
				end=size

profilNb=2
for i in range(profilNb):
	print>>output_final,"%d|road|elevationProfile|elevation||||||s|%f|double precision. Units meters. Non-negative. Start position (s-coordinate)|"%(id_current,0)	
	print>>output_final,"%d|road|elevationProfile|elevation||||||a|%f|double precision. Units meters. Positive or negative|"%(id_current,0)	
	print>>output_final,"%d|road|elevationProfile|elevation||||||b|%f|double precision. Dimensionless. Positive or negative.|"%(id_current,0)	
	print>>output_final,"%d|road|elevationProfile|elevation||||||c|%f|double precision. Units 1/m. Positive or negative|"%(id_current,0)	
	print>>output_final,"%d|road|elevationProfile|elevation||||||d|%f|double precision. Units 1/m2. Positive or negative|"%(id_current,0)	
	print>>output_final,"%d|road|lateralProfile|superelevation||||||s|%f|double precision. Units meters. Non-negative. Start position (s-coordinate)|"%(id_current,0)	
	print>>output_final,"%d|road|lateralProfile|superelevation||||||a|%f|double precision. Units radians. Positive or negative. Superelevation at s=0|"%(id_current,0)	
	print>>output_final,"%d|road|lateralProfile|superelevation||||||b|%f|double precision. Units radians/meter. Positive or negative.|"%(id_current,0)	
	print>>output_final,"%d|road|lateralProfile|superelevation||||||c|%f|double precision. Units radians/m2. Positive or negative|"%(id_current,0)	
	print>>output_final,"%d|road|lateralProfile|superelevation||||||d|%f|double precision. Units radians/m3. Positive or negative|"%(id_current,0)	

laneNb=3
for i in range(laneNb):

	#to add in type
	center_lane_type=raw_input("Center lane's type : (None(n)/Driving(d)/Stop(s)/Shoulder(sh)/Biking(b)/)") or "d"
	if center_lane_type=='d':
		center_lane_type="driving"
	elif center_lane_type=='s':
		center_lane_type="stop"
	elif center_lane_type=='n':
		center_lane_type="none"
	elif center_lane_type=='sh':
		center_lane_type="shoulder"
	elif center_lane_type=='b':
		center_lane_type="biking"
	else:
		center_lane_type="none"
	certer_lane_id=int(raw_input("Center lane's id : ") or 1)
	print>>output_final,"%d|road|lanes|laneSection|center|lane||||type|%s||"%(id_current,center_lane_type)	
	print>>output_final,"%d|road|lanes|laneSection|center|lane||||id|%d|integer or alphanumeric|"%(id_current,certer_lane_id)	
	print>>output_final,"%d|road|lanes|laneSection|center|lane||||level|%s|True = flat. Do not apply superelevation. False=apply crossfall and superelevation|"%(id_current,"True")	
	center_lane_prodecessor_id=int(raw_input("center lane prodecessor id : ") or 2)
	print>>output_final,"%d|road|lanes|laneSection|center|lane|link|predecessor||id|%d|integer or alphanumeric|"%(id_current,center_lane_prodecessor_id)	
	center_lane_psuccessor_id=int(raw_input("Center lane successor id : ") or 3)
	print>>output_final,"%d|road|lanes|laneSection|center|lane|link|successor||id|%d|integer or alphanumeric|"%(id_current,center_lane_psuccessor_id)	
	center_lane_roadmark_offset=float(raw_input("center lane roadmark offset : ")or 0)
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||sOffset|%f|"%(id_current,center_lane_roadmark_offset)	
	# to add
	center_lane_roadmark_type=raw_input("center lane roadmark type : (none(n)/solid(s)/broken(b)") or "n"
	if center_lane_roadmark_type=='n':
		center_lane_roadmark_type="none"
	elif center_lane_roadmark_type=='s':
		center_lane_roadmark_type="solid"
	elif center_lane_roadmark_type=='b':
		center_lane_roadmark_type="broken"
	else:
		center_lane_roadmark_type="none"
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||type|%s|||"%(id_current,center_lane_roadmark_type)	
	center_lane_roadmark_weight=raw_input("center lane roadmark weight : (standard(s)/bold(b))") or 's'
	if center_lane_roadmark_weight=='s':
		center_lane_roadmark_weight="standard"
	elif center_lane_roadmark_weight=='b':
		center_lane_roadmark_weight="bold"
	else:
		center_lane_roadmark_weight="standard"
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||type|%s|||"%(id_current,center_lane_roadmark_weight)	
	center_lane_roadmark_color=raw_input("center lane roadmark color : (standard(s)/blue(b)/green(g)/red(r))") or "s"
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||material|%s|"%(id_current,center_lane_roadmark_color)	
	center_lane_roadmark_material="standard"
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||color|%s||"%(id_current,center_lane_roadmark_material)	
	center_lane_roadmark_width=float(raw_input("center roadmark width : ") or 0.5)
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||width|%f|||"%(id_current,center_lane_roadmark_width)
	center_lane_roadmark_laneChange=raw_input("center roadmark lane change : (increase(i)/decrease(d)/both(b)/none(n))") or "n"
	if center_lane_roadmark_laneChange=='i':
		center_lane_roadmark_laneChange="increase"
	elif center_lane_roadmark_laneChange=='d':
		center_lane_roadmark_laneChange="decrease"
	elif center_lane_roadmark_laneChange=='b':
		center_lane_roadmark_laneChange="both"
	elif center_lane_roadmark_laneChange=="n":
		center_lane_roadmark_laneChange="none"
	else:
		center_lane_roadmark_laneChange="none"
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||laneChange|%s|"%(id_current,center_lane_roadmark_laneChange)
	center_lane_roadmark_height=float(raw_input("center roadmark height : ") or 0.5)
	print>>output_final,"%d|road|lanes|laneSection|center|lane|roadMark|||height|%f|"%(id_current,center_lane_roadmark_height)

	#didn't use roadmark type name/width/line

	####
	#### right lane

	right_lane_type=raw_input("right lane's type : (None(n)/Driving(d)/Stop(s)/Shoulder(sh)/Biking(b)/)") or "d"
	if right_lane_type=='d':
		right_lane_type="driving"
	elif right_lane_type=='s':
		right_lane_type="stop"
	elif right_lane_type=='n':
		right_lane_type="none"
	elif right_lane_type=='sh':
		right_lane_type="shoulder"
	elif right_lane_type=='b':
		right_lane_type="biking"
	else:
		right_lane_type="none"
	right_lane_id=int(raw_input("right lane's id : ") or 1)
	print>>output_final,"%d|road|lanes|laneSection|right|lane||||type|%s||"%(id_current,right_lane_type)	
	print>>output_final,"%d|road|lanes|laneSection|right|lane||||id|%d|integer or alphanumeric|"%(id_current,right_lane_id)	
	print>>output_final,"%d|road|lanes|laneSection|right|lane||||level|%s|True = flat. Do not apply superelevation. False=apply crossfall and superelevation|"%(id_current,"True")	
	right_lane_prodecessor_id=int(raw_input("right lane prodecessor id : ") or 2)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|link|predecessor||id|%d|integer or alphanumeric|"%(id_current,right_lane_prodecessor_id)	
	right_lane_psuccessor_id=int(raw_input("right lane successor id : ") or 3)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|link|successor||id|%d|integer or alphanumeric|"%(id_current,right_lane_psuccessor_id)	
	right_lane_width_sOffset=float(raw_input("right lane's width sOffset : ") or 0)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||sOffset|%f|"%(id_current,right_lane_width_sOffset)
	right_lane_width_a=float(raw_input("right lane width a :") or 0.15)
	right_lane_width_b=float(raw_input("right lane width b :") or 0)
	right_lane_width_c=float(raw_input("right lane width c :") or 0)
	right_lane_width_d=float(raw_input("right lane width d :") or 0)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||a|%f|"%(id_current,right_lane_width_a)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||b|%f|"%(id_current,right_lane_width_b)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||c|%f|"%(id_current,right_lane_width_c)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|width|||d|%f|"%(id_current,right_lane_width_d)
	right_lane_border_sOffset=float(raw_input("right lane's border sOffset : ") or 0)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||sOffset|%f|"%(id_current,right_lane_border_sOffset)
	right_lane_border_a=float(raw_input("right lane border a :") or 0.15)
	right_lane_border_b=float(raw_input("right lane border b :") or 0)
	right_lane_border_c=float(raw_input("right lane border c :") or 0)
	right_lane_border_d=float(raw_input("right lane border d :") or 0)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||a|%f|"%(id_current,right_lane_border_a)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||b|%f|"%(id_current,right_lane_border_b)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||c|%f|"%(id_current,right_lane_border_c)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|border|||d|%f|"%(id_current,right_lane_border_d)


	right_lane_roadmark_offset=float(raw_input("right lane roadmark offset : ")or 0)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||sOffset|%f|"%(id_current,right_lane_roadmark_offset)	
	# to add
	right_lane_roadmark_type=raw_input("right lane roadmark type : (none(n)/solid(s)/broken(b)") or "n"
	if right_lane_roadmark_type=='n':
		right_lane_roadmark_type="none"
	elif right_lane_roadmark_type=='s':
		right_lane_roadmark_type="solid"
	elif right_lane_roadmark_type=='b':
		right_lane_roadmark_type="broken"
	else:
		right_lane_roadmark_type="none"
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||type|%s|||"%(id_current,right_lane_roadmark_type)	
	right_lane_roadmark_weight=raw_input("right lane roadmark weight : (standard(s)/bold(b))") or 's'
	if right_lane_roadmark_weight=='s':
		right_lane_roadmark_weight="standard"
	elif right_lane_roadmark_weight=='b':
		right_lane_roadmark_weight="bold"
	else:
		right_lane_roadmark_weight="standard"
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||type|%s|||"%(id_current,right_lane_roadmark_weight)	
	right_lane_roadmark_color=raw_input("right lane roadmark color : (standard(s)/blue(b)/green(g)/red(r))") or "s"
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||material|%s|"%(id_current,right_lane_roadmark_color)	
	right_lane_roadmark_material="standard"
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||color|%s||"%(id_current,right_lane_roadmark_material)	
	right_lane_roadmark_width=float(raw_input("right roadmark width : ") or 0.5)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||width|%f|||"%(id_current,right_lane_roadmark_width)
	right_lane_roadmark_laneChange=raw_input("right roadmark lane change(increase(i)/(decrease(d)/both(b)/none(n))) : ") or "n"
	if right_lane_roadmark_laneChange=='i':
		right_lane_roadmark_laneChange="increase"
	elif right_lane_roadmark_laneChange=='d':
		right_lane_roadmark_laneChange="decrease"
	elif right_lane_roadmark_laneChange=='b':
		right_lane_roadmark_laneChange="both"
	elif right_lane_roadmark_laneChange=="n":
		right_lane_roadmark_laneChange="none"
	else:
		right_lane_roadmark_laneChange="none"
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||laneChange|%s|"%(id_current,right_lane_roadmark_laneChange)
	right_lane_roadmark_height=float(raw_input("right roadmark height : ") or 0.5)
	print>>output_final,"%d|road|lanes|laneSection|right|lane|roadMark|||height|%f|"%(id_current,right_lane_roadmark_height)
	#don't have roadmark type
	#don't have material/visibility/speed/access/height/rule

objectNb=3
for i in range(objectNb):
	object_type=raw_input("object type : guiderails(g)/road divider(d)/reflector posts(r)/emergency phones(e)/traffic light(l)/stop line(s)/traffic islands(i)/Bicycle(b) / pedestrian crossing(p)") or 'l'
	if object_type=='g':
		object_type="guiderails"
	elif object_type=='d':
		object_type="road divider"
	elif object_type=='g':
		object_type="guiderails"
	elif object_type=='r':
		object_type="reflector posts"
	elif object_type=='l':
		object_type="traffic light"
	elif object_type=='e':
		object_type="emergency phones"
	elif object_type=='s':
		object_type="stop line"
	elif object_type=='i':
		object_type="traffic islands"
	elif object_type=='b':
		object_type="Bicycle"
	elif object_type=='p':
		object_type="pedestrian crossing"
	else:
		object_type="traffic light"
	print>>output_final,"%d|road|objects|object||||||type|%s||"%(id_current,object_type)
	object_name=raw_input("object name : ") or "test object"
	print>>output_final,"%d|road|objects|object||||||name|%s|name of object|"%(id_current,object_name)
	object_id=int(raw_input("object name : ") or 1)
	print>>output_final,"%d|road|objects|object||||||id|%d|unique ID."%(id_current,object_id)
	object_s=float(raw_input("object s : ") or 0)
	print>>output_final,"%d|road|objects|object||||||s|%f|"%(id_current,object_s)
	object_t=float(raw_input("object t : ") or 0)
	print>>output_final,"%d|road|objects|object||||||t|%f|"%(id_current,object_t)
	object_zOffset=float(raw_input("object zOffset : ") or 0)
	print>>output_final,"%d|road|objects|object||||||zOffset|%f|"%(id_current,object_zOffset)
	object_validLength=float(raw_input("object validLength : ") or 0)
	print>>output_final,"%d|road|objects|object||||||validLength|%f|"%(id_current,object_validLength)
	object_orientation=float(raw_input("object orientation : ") or 0)
	print>>output_final,"%d|road|objects|object||||||orientation|%f|"%(id_current,object_orientation)
	object_length=float(raw_input("object length : ") or 0)
	print>>output_final,"%d|road|objects|object||||||length|%f|"%(id_current,object_length)
	object_width=float(raw_input("object width : ") or 0)
	print>>output_final,"%d|road|objects|object||||||width|%f|"%(id_current,object_width)
	object_radius=float(raw_input("object radius : ") or 0)
	print>>output_final,"%d|road|objects|object||||||radius|%f|"%(id_current,object_radius)
	object_height=float(raw_input("object height : ") or 0)
	print>>output_final,"%d|road|objects|object||||||height|%f|"%(id_current,object_height)
	object_hdg=float(raw_input("object hdg : ") or 0)
	print>>output_final,"%d|road|objects|object||||||hdg|%f|"%(id_current,object_hdg)
	object_pitch=float(raw_input("object pitch : ") or 0)
	print>>output_final,"%d|road|objects|object||||||pitch|%f|"%(id_current,object_pitch)
	object_roll=float(raw_input("object roll : ") or 0)
	print>>output_final,"%d|road|objects|object||||||roll|%f|"%(id_current,object_roll)
## no repeat/outline/material/validity/parkingspace/
hasTunnel=raw_input("is there tunnel?(y/n):") or "y"
if hasTunnel=="y":
	tunnel_name=raw_input("tunnel name : ") or "test tunnel"
	print>>output_final,"%d|road|objects|tunnel||||||name|%s|"%(id_current,tunnel_name)
	tunnel_s=float(raw_input("tunnel s : ") or 0)
	print>>output_final,"%d|road|objects|tunnel||||||s|%f|"%(id_current,tunnel_s)
	tunnel_length=float(raw_input("tunnel length : ") or 0)
	print>>output_final,"%d|road|objects|tunnel||||||length|%f|"%(id_current,tunnel_length)
	tunnel_id=int(raw_input("tunnel id : ") or 0)
	print>>output_final,"%d|road|objects|tunnel||||||id|%d|"%(id_current,tunnel_id)
	tunnel_lighting=float(raw_input("tunnel lighting : ") or 0)
	print>>output_final,"%d|road|objects|tunnel||||||lighting|%f|"%(id_current,tunnel_lighting)
	tunnel_daylight=float(raw_input("tunnel daylight : ") or 0)
	print>>output_final,"%d|road|objects|tunnel||||||daylight|%f|"%(id_current,tunnel_daylight)
	tunnel_type=raw_input("tunnel type : standard(s)/underpass(u) ") or "s"
	if tunnel_type=='u':
		tunnel_type="underpass"
	else:
		tunnel_type="standard"
	print>>output_final,"%d|road|objects|tunnel||||||type|%s|"%(id_current,tunnel_type)
	tunnel_fromLane=int(raw_input("tunnel from lane id : ") or 1)
	print>>output_final,"%d|road|objects|tunnel|validity|||||fromLane|%d|"%(id_current,tunnel_fromLane)
	tunnel_toLane=int(raw_input("tunnel to lane id : ") or 2)
	print>>output_final,"%d|road|objects|tunnel|validity|||||toLane|%d|"%(id_current,tunnel_toLane)
hasBridge=raw_input("is there bridge?(y/n)") or "y"
if hasBridge=="y":
	bridge_name=raw_input("bridge name : ") or "test bridge"
	print>>output_final,"%d|road|objects|bridge||||||name|%s|"%(id_current,bridge_name)
	bridge_s=float(raw_input("bridge s : ") or 0)
	print>>output_final,"%d|road|objects|bridge||||||s|%f|"%(id_current,bridge_s)
	bridge_length=float(raw_input("bridge length : ") or 0)
	print>>output_final,"%d|road|objects|bridge||||||length|%f|"%(id_current,bridge_length)
	bridge_id=int(raw_input("bridge id : ") or 0)
	print>>output_final,"%d|road|objects|bridge||||||id|%d|"%(id_current,bridge_id)
	bridge_type=raw_input("bridge type : wood(w)/brick(b)/steel(s)/concrete(c) ") or "b"
	if bridge_type=='w':
		bridge_type="wood"
	elif bridge_type=='s':
		bridge_type="steel"
	elif bridge_type=='c':
		bridge_type="concrete"
	else:
		bridge_type="brick"
	print>>output_final,"%d|road|objects|bridge||||||type|%s|"%(id_current,bridge_type)
hasSignal=raw_input("is there signal?(y/n)") or "y"
if hasSignal=="y":
	signal_name=raw_input("signal name : ") or "test signal"
	print>>output_final,"%d|road|signals|signal||||||name||%s|"%(id_current,signal_name)
	signal_s=float(raw_input("signal s : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||s|%f|"%(id_current,signal_s)
	signal_t=float(raw_input("signal t : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||t|%f|"%(id_current,signal_t)
	signal_id=int(raw_input("signal id : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||id|%f|"%(id_current,signal_id)
	signal_dynamic=raw_input("bridge dynamic : (y/n)") or "no"
	if signal_dynamic=="y":
		signal_dynamic="yes"
	else:
		signal_dynamic="no"
	print>>output_final,"%d|road|signals|signal||||||dynamic|%s||"%(id_current,signal_dynamic)
	signal_orientation=raw_input("bridge orientation : (+/-)") or ""
	if signal_orientation=="+":
		signal_orientation="+"
	else:
		signal_orientation="-"
	print>>output_final,"%d|road|signals|signal||||||orientation|%s||"%(id_current,signal_orientation)
	signal_zOffset=float(raw_input("signal zOffset : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||zOffset|%f|"%(id_current,signal_zOffset)
	signal_country=raw_input("country:") or "DEU"
	print>>output_final,"%d|road|signals|signal||||||country|%s|ISO 3166 alpha-3 Country Code|"%(id_current,signal_country)
	signal_type=raw_input("signal type:") or "310"
	print>>output_final,"%d|road|signals|signal||||||type|%s|ISO 3166 alpha-3 Country Code|"%(id_current,signal_type)
	signal_value=float(raw_input("signal value : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||value|%f|"%(id_current,signal_value)
	signal_unit=raw_input("unit:(m/km/mile)") or "m"
	print>>output_final,"%d|road|signals|signal||||||unit|%s|"%(id_current,signal_unit)
	signal_height=float(raw_input("signal height : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||height|%s|"%(id_current,signal_height)
	signal_width=float(raw_input("signal width : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||width|%s|"%(id_current,signal_width)

	signal_hOffset=float(raw_input("signal hOffset : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||hOffset|%s|"%(id_current,signal_hOffset)
	signal_pitch=float(raw_input("signal pitch : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||pitch|%s|"%(id_current,signal_pitch)
	signal_roll=float(raw_input("signal roll : ") or 0)
	print>>output_final,"%d|road|signals|signal||||||roll|%s|"%(id_current,signal_roll)

	signal_text=raw_input("text:") or ""
	print>>output_final,"%d|road|signals|signal||||||text|%s|"%(id_current,signal_text)
file.close()
output.close()
output_final.close()