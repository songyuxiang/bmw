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
	
def ReadList2L(filename):
	with open(filename,'r') as file:
		data=file.read()
	temp=data.split('], [')
	
	temp_new=[]
	for st in temp:
		st=st.replace('[','')
		st=st.replace(']','')
	 	st=st.replace('\'','')
		st=st.replace(' ','')
		st=st.replace('\n','')
		st=st.replace('\r','')
		l=st.split(',')
		temp_new.append(l)
		# print(len(l))
	return temp_new

a=ReadList2L("./test.txt")
print(a[0][0])