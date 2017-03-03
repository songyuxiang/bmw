import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from matplotlib.patches import Circle
from syx import *

def getGeoMode(pointX,pointY,lengthUnit,tolerance,sectinoPointNumber,rotation=True,tangentX=[],tangentY=[]):
	size=len(pointX)
	start=0
	end=sectinoPointNumber
	while start<size:
		sectionData={}
		if rotation==True:
			x,y=rotateAndTranslate(pointX[start:end],pointY[start:end],0,-pointX[start],-pointY[start])
			para_polyline,p_polyline,gap_polyline=getPolylineModel(x,y)
			para_circle,gap_circle=getCircleModel(x,y)
			para_line,p_line,gap_line=getLineModel(x,y)
			if max(gap_polyline)>threshold and max(gap_circle)>threshold and max(gap_line)>threshold:
				end=end-1
				continue
			if max(gap_polyline)<max(gap_circle) and max(gap_polyline)<max(gap_line):
				if len(tangentX)>0 and len(tangentY)>0:
					hdg=getOrientation(tangentX[start],tangentY[start])