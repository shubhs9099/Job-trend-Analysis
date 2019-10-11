from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import xlrd
import csv
try:
	import httplib 
except:
	import http.client as httplib 
 
def has_internet():
	conn = httplib.HTTPConnection("www.google.com", timeout=5)
	try:
		conn.request("HEAD", "/")
		conn.close()
		return True
	except:
		conn.close()
		return False


def job_search(u_job_role,u_location):
	
	page_count=0 #page number offset

	website="https://www.indeed.co.in/jobs?q="
	website+=(u_job_role+"&l="+u_location+"&start="+str(page_count))	
	source=requests.get(website).text
	soup=bs(source,'lxml')
	count_string=soup.find('div',attrs={'id':'searchCount'}).text.strip().split()
	
	job_count=int(count_string[3].replace(",",""))
	print(job_count)
	print("Jobs of your choice are: \n")
	total_pages=101

	curr_page=1 #current page pointer
	data=[]
	while (curr_page<total_pages):
		source=""
		website="https://www.indeed.co.in/jobs?q="
		website+=(u_job_role+"&l="+u_location+"&start="+str(page_count))	
		print(website)
		source=requests.get(website).text
		soup=bs(source,'lxml')
		for job in soup.find_all('div',attrs={'class' : re.compile('jobsearch.*')}):

			temp=[]
			a = job.find(re.compile('.*'),class_='title')
			title = a.find('a')
			if title != None:
				temp.append(title.text.strip())
			else:
				temp.append('Nan')
				#print("Title : " + title)
			
			company = job.find('span',class_='company')
			if company != None:
				temp.append(company.text.strip())
			else:
				temp.append('Nan')
				#print ("Company : " + company)
			
			location = job.find(re.compile('.*'),class_='location')
			if location != None:
				temp.append(location.text.strip())
			else:
				temp.append('Nan')
				#print ("Location : " + location)
			
			salary = job.find(re.compile('.*'),class_='salary')
			if salary != None:
				temp.append(salary.text.strip())
			else:
				temp.append('Nan')
				#print("Salary : " + salary.text.strip())
			
			summary = job.find('div',class_='summary')
			if summary != None:
				temp.append(summary.text.strip())
			else:
				temp.append('Nan')
				#print("Summary : " + summary)

			#details=a.find('a')['href'].strip()
			
			data.append(temp)
		page_count+=10
		curr_page+=1	

	return data 
def main():
		
	data=job_search("","india")
	df=pd.DataFrame(data)
	df.drop_duplicates(subset=None, inplace=True)
	list_rows=["Title","Company","Location","Salary","Summary"]
	df.to_csv('indeed_analysis_india_1.csv',header=list_rows,index=False)
	print("Done")
	# Remove duplicate datas
	'''data=job_search("java+developer","surat")
	list_rows=["Title","Company","Location","Salary","Summary"]
	with open('indeed_analysis_mumbai.csv', 'w+') as xlsFile:
		writer = csv.writer(xlsFile)
		writer.writerow(list_rows)
		writer.writerows(data)'''
	#df.head(10)
	#print (df)
	#else:
	#	print("No internet")
		
main()