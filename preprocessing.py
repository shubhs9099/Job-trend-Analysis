import pandas as pd
import csv
import re

# for indeed salary field

data=pd.read_csv('indeed_analysis_surat.csv')
df=pd.DataFrame(data)
for  index in df.index:
	temp=df['Salary'][index]
	temp=temp.replace(',','')
	temp=temp.replace('₹','').strip()
	if(temp!='Nan'):
		flag = 0
		# pos=temp.index("-")
		if "year" in temp:
			flag = 1
		if "month" in temp:
			flag = 2
		#temp = re.findall("\d+", temp )
		avg=0
		temp=temp.replace('a month','').strip()
		temp=temp.replace('a year','').strip()
		x = temp.split('-')
		#print(x)
		if flag==1:
			if(len(x)>1):
				avg=(int(x[0].strip())+int(x[1].strip()))/2
				print(avg)
		if flag==2:
			if len(x)>1 :
				avg=(int(x[0].strip())+int(x[1].strip()))/2
				avg*=12
				print(avg)
		print(avg)
		df['Salary'][index]=avg

df.to_csv('indeed_analysis_india_1.csv')


# for shine experoence field
'''
data=pd.read_csv('shine_analysis_all_2.csv')
df=pd.DataFrame(data)
for index in df.index :
	temp=df['Experience'][index]
	try:
		temp=temp.replace('>','')
		temp=temp.replace('Yrs','')
		temp=temp.replace('Yr','').strip()
		exp=0
		if len(temp)>0:
			exp=int(temp[0].strip())	
		else :
			exp=0
		df['Experience'][index]=exp
	except:
		pass
	print(df['Experience'][index], " ", index)
df.to_csv('shine_analysis_all_2.csv') '''