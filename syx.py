import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from matplotlib.patches import Circle

m_x=[]
m_y=[]
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
	return np.sqrt((m_x-xc)**2 + (m_y-yc)**2)

def f_2(c):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()
def getCircleModel(x,y):
	global m_x,m_y
	m_x=x
	m_y=y
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

def getInput(objectName,typeList=[],unit="",valueType="s"):
	abbreviation=[]
	title=""
	if valueType=="s":
		if not unit=="":
			unit="(%s)"%unit
		if len(typeList)>0:
			for i in range(len(typeList)):
				if not typeList[i][0] in abbreviation:
					abbreviation.append(typeList[i][0])
				elif not typeList[i][0:2] in abbreviation:
					abbreviation.append(typeList[i][0:2])
				elif not typeList[i][0:3] in abbreviation:
					abbreviation.append(typeList[i][0:3])
				else:
					abbreviation.append(typeList[i])
				title+="%s--%s; "%(typeList[i],abbreviation[i])
			out=raw_input("%s %s: \n(%s):"%(objectName,unit,title))
			if out in abbreviation:
				return typeList[abbreviation.index(out)]
			else :
				return getInput(objectName,typeList,unit,valueType)
		else:
			out=raw_input("%s %s: "%(objectName,unit))
			return out
	elif valueType=="i":
		try:
			if not unit=="":
				unit="(%s)"%unit
			if len(typeList)>0:
				for i in range(len(typeList)):
					if not typeList[i][0] in abbreviation:
						abbreviation.append(typeList[i][0])
					elif not typeList[i][0:2] in abbreviation:
						abbreviation.append(typeList[i][0:2])
					elif not typeList[i][0:3] in abbreviation:
						abbreviation.append(typeList[i][0:3])
					else:
						abbreviation.append(typeList[i])
					title+="%s--%s; "%(typeList[i],abbreviation[i])
				out=int(raw_input("%s %s: \n(%s):"%(objectName,unit,title)))
				if out in abbreviation:
					return typeList[abbreviation.index(out)]
				else :
					return getInput(objectName,typeList)
			else:
				out=int(raw_input("%s %s: "%(objectName,unit)))
				print("out:",type(out))
				return out
		except ValueError:
			print("you have to input integer!")
			return getInput(objectName,typeList,unit,'i')
	elif valueType=="f":
		try:
			if not unit=="":
				unit="(%s)"%unit
			if len(typeList)>0:
				for i in range(len(typeList)):
					if not typeList[i][0] in abbreviation:
						abbreviation.append(typeList[i][0])
					elif not typeList[i][0:2] in abbreviation:
						abbreviation.append(typeList[i][0:2])
					elif not typeList[i][0:3] in abbreviation:
						abbreviation.append(typeList[i][0:3])
					else:
						abbreviation.append(typeList[i])
					title+="%s--%s; "%(typeList[i],abbreviation[i])
				out=float(raw_input("%s %s: \n(%s):"%(objectName,unit,title)))
				if out in abbreviation:
					return typeList[abbreviation.index(out)]
				else :
					return getInput(objectName,typeList)
			else:
				out=float(raw_input("%s %s: "%(objectName,unit)))
				return out
		except ValueError:
			print("you have to input number!")
			return getInput(objectName,typeList,unit,'f')

def checkVariedLane(lineInfo):
    isVaried=False
    for i in range(len(lineInfo)):
        if lineInfo[i][-1]=="variedlane":
            isVaried=True
    return isVaried
def compareLaneSection(section1,section2,takeDistance=False):
    sameSection=True
    if takeDistance:
        return section1==section2
    else:
        if len(section1)==len(section2):
            for i in range(len(section1)):
                if not section1[i][1:]==section2[i][1:]:
                    sameSection=False
            return sameSection
        else:
            return False

def ReadList3L(filename):
	with open(filename,'r') as file:
		data=file.read()
	start=0
	size=data.count("[[")
	allData=[]
	for i in range(size):
		start=data.find("[[",start)+1
		end=data.find("]]",start)
		temp=data[start+0:end+1]
		temp=temp.split('], [')
		temp_new=[]
		for st in temp:
			st=st.replace('[','')
			st=st.replace(']','')
			st=st.replace('\'','')
			st=st.replace(' ','')
			st=st.replace('\n','')
			l=st.split(',')
			temp_new.append(l)
		allData.append(temp_new)
	return allData
def checkSingleSide(LineInfo):
	hasLeft=False
	hasRight=False
	for info in LineInfo:
		if info[1]=="right":
			hasRight=True
		if info[1]=="left":
			hasLeft=True
	if hasRight and hasLeft:
		return False
	else:
		return True
