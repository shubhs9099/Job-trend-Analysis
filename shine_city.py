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
	page_count=3001
	website = 'https://www.shine.com/job-search/'
	website+=(role+"-jobs-in-"+city+'-'+str(page_count))
	page = requests.get(website).text
	soup= bs(page, 'lxml')
	
	#jobs_count=int(soup.find('em',{'id':'id_resultCount'}).text.replace(",",""))
	#print(jobs_count)

	data=[]
	total_pages=4500#150000/20

	while (page_count<total_pages):

		website = 'https://www.shine.com/job-search/'
		website+=(role+"-jobs-in-"+city+'-'+str(page_count))
		page = requests.get(website).text
		soup= bs(page, 'lxml')
		print(website)

		for job in soup.find_all('li',attrs={'class' : re.compile('search_listing cls_jobsnippet ')}):

			temp=[]
			a = job.find('li',class_='snp cls_jobtitle')

			title = a.find('h3')
			if title != None:
				#print("Title : " + title.text.strip())
				temp.append(title.text.strip())
			else:
				temp.append("Nan")
			
			company = job.find('li',class_='snp_cnm cls_cmpname cls_jobcompany')
			if company != None:
				#print ("Company : " + company.text.strip())
				temp.append(company.text.strip())
			else:
				temp.append("Nan")
					
			experience=job.find('span',class_="snp_yoe cls_jobexperience")
			if experience!=None:
				#print("Experience required : "+experience.text.strip())
				temp.append(experience.text.strip())
			else:
				temp.append("Nan")

			location = job.find('em',class_='snp_loc')
			if location != None:
				#print ("Location : " + location.text.strip())
				temp.append(location.text.strip())
			else:
				temp.append("Nan")
			skills = job.find('div',class_='sk jsrp cls_jobskill')

			if skills != None:
				#print("skills required : " + skills.text.strip())
				temp.append(skills.text.strip())
			else:
				temp.append("Nan")

			summary = job.find('li',class_='srcresult')
			if summary != None:
				#print("Summary : " + summary.text.strip())
				temp.append(summary.text.strip())
			else:
				temp.append("Nan")

			data.append(temp)
		page_count+=1

	return data
			
		
def main():
	if has_internet():
		'''job_role=input("Enter the Job Role \n")
		job_role.replace(' ','-')
		location=input("Enter the location \n")
		job_search(job_role+'-jobs-in-'+location)'''
		data=job_search("","")
		df=pd.DataFrame(data)
		df.drop_duplicates(subset=None, inplace=True)
		list_rows=["Title","Company","Experience","Location","Skills","Summary"]
		df.to_csv('shine_analysis_all_3.csv',header=list_rows,index=False)
		print("Done")
	else:
		print("No internet")
		
main()