from io import StringIO
from datetime import date
import numpy as np 
# import matplotlib.pyplot as plt 
import requests as req 
import csv


def arrangeData(country_names, data):
	#pass the whole country name and data(i.e. unsorted) it will short the copied name of country into one
	#unsorted : the data contains information of different states of country so to get the data of a country need this processing.
	
	#removing the repeated country names, to get the available name of country
	filter_country_names = list(dict.fromkeys(country_names))
	
	#loop to add all the data under same country name (but presented at different states)
	filtered_data = []
	for country in filter_country_names:
		count = 0
		for i in np.where(country_names == country):
			count = int(count) + data[i].astype(np.int)
		filtered_data.append(np.sum(count))

	#return value with country colum and data column sorted.
	value = []
	for i in range(len(filter_country_names)):
		c = [filter_country_names[i]] + [filtered_data[i]]
		value.append(c)

	# print(value)
	return np.array(value)


#for todays date
today = date.today()
#url to get the csv file 
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+today.strftime("%m")+'-'+str(int(today.strftime("%d"))-1)+today.strftime("-%Y")+".csv"
print(url)

#requesting data from the url
response = req.get(url)
if response.status_code == 200:
	print('Sucessfully retrived file')
elif response.status_code == 404:
	print('Failed request.')
	print('exiting program.')
	return 0

#parsing the retrive csv 
csv_file = StringIO(response.text)
csv_file = csv.reader(csv_file, delimiter = ',')

dataset = []
for row in csv_file:
	dataset.append(row)
dataset = np.array(dataset)

#the name of the country in the dataset
country_names = dataset[1:,3]
#the update time of the data
data_update = dataset[1:,4]
#taking the data of confirmed cases, death, recovere and active cases
stat = dataset[1:,7:11].astype(np.int)

#taking the data of confirmed cases from the data
confirmed_cases = stat[:,0]
confirmed_cases = arrangeData(country_names,confirmed_cases)

#sorting in increasing order
tmp = np.sort(confirmed_cases[:,1].astype(np.int))
#sorting in decreasing order
tmp1 = []
for i in range(len(tmp)):
	tmp1.append(tmp[-1*(i+1)])
tmp = tmp1

sorted_data = []
for i in tmp:
	for j in np.where(confirmed_cases[:,1].astype(np.int) == i):
		sorted_data.append(np.array(confirmed_cases[j]))

sorted_data = np.array(sorted_data)
print(sorted_data)