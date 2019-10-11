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


def job_search(role,city):
	offset=0
	#100
	website = 'https://www.freshersworld.com/jobs/jobsearch/'
	website+=(role+'-jobs-in-'+city+"?&limit=50&offset="+str(offset))	
	page = requests.get(website).text
	soup= bs(page, 'lxml')
	data=[]
	jobs_count=soup.find('span',{'class':'number-of-jobs'}).text
	print(jobs_count)
	total_pages=int(jobs_count)/50

	page_count=1
	while (page_count<total_pages):

		website = 'https://www.freshersworld.com/jobs/jobsearch/'
		website+=(role+'-jobs-in-'+city+"?&limit=50&offset="+str(offset))	
		page = requests.get(website).text
		soup= bs(page, 'lxml')
		print(website)
		for job in soup.find_all('div',class_=re.compile("col-md-12 col-lg-12 col-xs-12 padding-none job-container.*")): 
			
			temp=[]
			tc=job.find('div',class_="col-md-12 col-xs-12 col-lg-12 padding-none left_move_up")
			
			if tc!=None:

				
				temp.append(tc.find('div').text.strip())

				title=tc.find('a').text	
				if title != None:
					
					temp.append(title.strip())
				else:
					temp.append("Nan")
				

				qualifications=tc.find('span',class_="bold_elig").text
				
				if qualifications!=None:
					
					temp.append(qualifications.strip())
				else:
					temp.append("Nan")
				desc=job.find('span',class_="desc").text
				if desc!=None:
					
					temp.append(desc.strip())
				else:
					temp.append("Nan")	
				location=job.find('a',class_="bold_font")
				if location!=None:
					
					temp.append(location.text.strip())
				else:
					temp.append("Nan")

				data.append(temp)
		page_count+=1
		offset+=50
	return data

def main():
	if has_internet():
		'''job_role=input("Enter the Job Role \n")
		job_role.replace(' ','-')
		location=input("Enter the location \n")'''
		data=job_search("","")
		df=pd.DataFrame(data)
		df.drop_duplicates(subset=None, inplace=True)
		list_rows=["Title","Company","Qualifications","Description","Location"]
		df.to_csv('fw_analysis_india.csv',header=list_rows,index=False)
		print("Done")
	else:
		print("No internet")
		
main()