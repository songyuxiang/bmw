def getInput(objectName,typeList=[],unit=""):
	abbreviation=[]
	title=""
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
				bbreviation.append(typeList[i])
			title+="%s--%s; "%(typeList[i],abbreviation[i])
		out=raw_input("%s %s: \n(%s):"%(objectName,unit,title))
		if out in abbreviation:
			return typeList[abbreviation.index(out)]
		else :
			return getInput(objectName,typeList)
	else:
		out=raw_input("%s %s: "%(objectName,unit))
		return out

print(getInput("test",unit="m/s"))