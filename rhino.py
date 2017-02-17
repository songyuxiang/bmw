import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

all_lanes_info=[]
section_pt=[]
size=len(plans)

for i in range(size):
    line_info=[]
    for c in c1:
        intersect=rs.PlaneCurveIntersection(plans[i],c)
        if not intersect==None:
            
            for inter in intersect:
                info=[]
                d=rs.Distance(inter[1],truck_pts[i])
                info.append(str(d))
                info.append("125")
                info.append("broken")
                info.append("standard")
                info.append("driving")
                line_info.append(info)
    for c in c2:
        intersect=rs.PlaneCurveIntersection(plans[i],c)
        if not intersect==None:
            
            for inter in intersect:
                info=[]
                d=rs.Distance(inter[1],truck_pts[i])
                info.append(str(d))
                info.append("125")
                info.append("solid")
                info.append("standard")
                info.append("special1")
                line_info.append(info)
    for c in c3:
        intersect=rs.PlaneCurveIntersection(plans[i],c)
        if not intersect==None:
            
            for inter in intersect:
                info=[]
                d=rs.Distance(inter[1],truck_pts[i])
                info.append(str(d))
                info.append("300")
                info.append("solid")
                info.append("standard")
                info.append("driving")
                line_info.append(info)
    for c in c4:
        intersect=rs.PlaneCurveIntersection(plans[i],c)
        if not intersect==None:
            
            for inter in intersect:
                info=[]
                d=rs.Distance(inter[1],truck_pts[i])
                info.append(str(d))
                info.append("300")
                info.append("broken")
                info.append("standard")
                info.append("driving")
                line_info.append(info)
    for i in range(len(line_info)):
        for j in range(len(line_info)-1):
            if abs(float(line_info[j][0])-float(line_info[j+1][0]))<0.05:
                line_info.remove(line_info[j+1])
    for i in range(len(line_info)):
        for j in range(len(line_info)-1):
            if(float(line_info[j][0])>float(line_info[j+1][0])):
                l=line_info[j+1]
                line_info[j+1]=line_info[j]
                line_info[j]=l
    all_lanes_info.append(line_info)
for i in range(len(all_lanes_info)-1):
    if len(all_lanes_info[i])!=len(all_lanes_info[i+1]):
        section_pt.append(truck_pts[i])
    else:
        for j in range(len(all_lanes_info[i])):
            if abs(float(all_lanes_info[i][j][0])-float(all_lanes_info[i+1][j][0]))>0.1:
                section_pt.append(truck_pts[i])
