# -*- coding: utf8 -*-
from django.shortcuts import render, HttpResponse, redirect
import xlrd
import datetime
import requests
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import numpy as np
import scipy
import re

from urllib2 import urlopen as uRequest
from bs4 import BeautifulSoup as soup
import json


counties = { "Alameda":{"xls":"https://www.mlslistings.com/Search/Result/a333bdeb-eedb-482b-8bf5-63f04b649e01/1","gpoi":"point of interest in alameda county","weather":"Alameda County"},
 "Amador":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Amador county","weather":"Amador County"},
"Butte":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Butte county","weather":"butte County"},
u"Calaveras":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Calaveras county","weather":"Calaveras County"},
 "Contra-Costa":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Contra-Costa county","weather":"Contra-Costa County"},
u"Del Norte":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Del Norte county","weather":"Del Norte County"},
 u"El Dorado":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in El Dorado county","weather":"El Dorado County"},
u"Fresno":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Fresno county","weather":"Fresno County"},
u"Glenn":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Glenn county","weather":"Glenn County"},
 "Humboldt":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Humboldt county","weather":"Humboldt County"},
u"Kern":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Kern county","weather":"Kern County"},
 u"Kings":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Kings county","weather":"Kings County"},
u"Lake":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Lake county","weather":"Lake County"},
u"Los Angeles":{"xls":"https://www.mlslistings.com/Search/Result/c1b66683-08e2-4503-91e3-e42e188dab0d/1","gpoi":"point of interest in Los Angeles county","weather":"Los Angeles County"},
 "Madera":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Madera county","weather":"Madera County"},
u"Marin":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Marin county","weather":"Marin County"},
 u"Mariposa":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Mariposa county","weather":"Mariposa County"},
u"Mendocino":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Mendocino county","weather":"Mendocino County"},
u"Merced":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Merced county","weather":"Merced County"},
 "Monterey":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Monterey county","weather":"Monterey County"},
 u"Napa":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Napa county","weather":"Napa County"},
 u"Nevada":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Nevada county","weather":"Nevada County"},
u"Orange":{"xls":"https://www.mlslistings.com/Search/Result/6b30b114-8f3b-40dd-b408-b62052a39d93/1","gpoi":"point of interest in Orange county","weather":"Orange County"},
u"Placer":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Placer county","weather":"Placer County"},
 "Plumas":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Plumas county","weather":"Plumas County"},
u"Riverside":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Riverside county","weather":"Riverside County"},
 u"Sacramento":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Sacramento county","weather":"Sacramento County"},
u"San Benito":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in San Benito county","weather":"San Benito County"},
u"San Bernardino":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in San Bernardino county","weather":"San Bernardino County"},
 "San Diego":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in San Diego county","weather":"San Diego County"},
u"San Francisco":{"xls":"https://www.mlslistings.com/Search/Result/2b1b260f-90f8-49d8-9e57-95b73291f5af/1","gpoi":"point of interest in San Francisco county","weather":"San Francisco County"},
u"San Joaquin":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in San Joaquin county","weather":"San Joaquin County"},
 u"San Luis Obispo":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in San Luis Obispo county","weather":"San Luis Obispo County"},
u"San Mateo":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in San Mateo county","weather":"San Mateo County"},
 "Santa Barbara":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Santa Barbara county","weather":"Santa Barbara County"},
u"Santa Clara":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Santa Clara county","weather":"Santa Clara County"},
 u"Santa Cruz":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Santa Cruz county","weather":"Santa Cruz County"},
u"Shasta":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Shasta county","weather":"Shasta County"},
u"Siskiyou":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Siskiyou county","weather":"Siskiyou County"},
 "Solano":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Solano county","weather":"Solano County"},
u"Sonoma":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Sonoma county","weather":"Sonoma County"},
 u"Stanislaus":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Stanislaus county","weather":"Stanislaus County"},
u"Sutter":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Sutter county","weather":"Sutter County"},
u"Tehama":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Tehama county","weather":"Tehama County"},
 "Tulare":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Tulare county","weather":"Tulare County"},
u"Tuolumne":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Tuolumne county","weather":"Tuolumne County"},
 u"Ventura":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Ventura county","weather":"Ventura County"},
u"Yolo":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Yolo county","weather":"Yolo County"},
u"Yuba":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Yuba county","weather":"Yuba County"},
 "Los Angeles Metropolitan Area":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Los Angeles county","weather":"Los Angeles County"},
u"S.F. Bay Area":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in SF county","weather":"SF County"},
 u"Inland Empire":{"xls":"https://www.mlslistings.com/Search/Result/4433fe0b-95ff-429b-82c0-b4e07319577a/1","gpoi":"point of interest in Ontario county","weather":"Ontario County"}}

api_key = 'AIzaSyDRlMVi72tJvm7-5Gw7HPWmqus9Hx3c0f0'

poi_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

def open_excel(filename):
    '''Will take as input excel filename and returns
    workbook object'''
    workbook = xlrd.open_workbook(filename)
    return workbook

def get_start_row(sheet_name):
    '''function takes in sheetname and returns row number from where valid data starts'''
    start_row = 0
    for index in range(0,sheet_name.nrows):
        if sheet_name.cell(index,0).value=='Mon-Yr':
            start_row=index
            break
    return start_row

def get_list_of_counties():
    print 'This program plots and predicts prices and regression of any county from the following list.'
    list_of_counties   = sheet_name.row_values(start_row)
    list_of_counties.remove('Mon-Yr')
    list_of_counties.remove('CA')
    list_of_counties.remove('')
    return list_of_counties

def get_county_index(sheet_name,county_name):
    '''takes as input sheetname and county name and returns
    column number of the county in the excel sheet'''
    county_index = 0
    list_of_counties = sheet_name.row_values(start_row)
    county_index = list_of_counties.index(county_name)
    return county_index

def get_year_month(workbook,sheet_name,index):
    '''this function converts the date information returned by xlrd into the format Mon-Yr'''
    month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    date = xlrd.xldate_as_tuple(int(sheet_name.cell(index,0).value),workbook.datemode)[0:2]
    year = str(date[0])
    new_date = str(month_list[date[1]-1])+'-' +year
    return new_date

def create_county_price_list(sheet_name,start_row,county_col_index):
    '''this function returns a list of the house prices in the county'''
    county_price_list = []
    for index in range(start_row+1,sheet_name.nrows):
       county_price_list.append(sheet_name.cell(index,county_col_index).value)
    return county_price_list

def get_valid_lists(county_list,year_month_list):
    '''this function removes entries from the county list and corresponding
    entries from year_month list if the price is listed as NA'''
    county_list_valid = []
    year_month_list_valid = []
    for index,value in enumerate(county_list):
       if value != 'NA':
           county_list_valid.append(value)
           year_month_list_valid.append(year_month_list[index])
    return county_list_valid,year_month_list_valid

def plotGraph(county_list,year_month_list,county_name):
    '''this function plots the price and regression graphs for the county specified'''
    id      = [x for x in range(len(year_month_list))]
    x       = np.array(id)
    y       = np.array(county_list)
    p1      = scipy.polyfit(x,y,1)
    x_range = 'Year_Month'
    y_range = 'Price in $'
    title   = 'County: ' + county_name
    fig     = plt.figure()

    plt.scatter(x,y)
    plt.plot(x,scipy.polyval(p1,x))
    plt.xticks(id,year_month_list,rotation=90)
    plt.xlabel(x_range)
    plt.ylabel(y_range)
    plt.title(title)
    plt.legend()
    plt.show()
    plt.savefig('apps/predict_app/static/predict_app/images/figure.png')

def predict_house_price(county_price_list_valid,year_month_list_valid,county_name,month_predict,year_predict):
    '''this function predicts the price of county for specified month and year'''

    id = [x for x in range(len(year_month_list_valid))]
    regr = np.polyfit(id,county_price_list_valid,1)

    m,start_year = year_month_list_valid[0].split('-')
    start_month  = month_dict[m]

    x = (year_predict - int(start_year)) * 12 + month_predict - int(start_month)
    y = regr[0] * x + regr[1] #y = mx + b

    return y

def get_weather(location, request):
    result                      = requests.get(url.format(location)).json()
    weather_data                = {}
    weather_data['temperature'] = result['main']['temp']
    weather_data['description'] = result['weather'][0]['description']
    weather_data['icon']        = result['weather'][0]['icon']
    return weather_data

def get_poi_list(location, poi_request):
    results  = poi_request['results']
    poi_list = []
    for i in range(len(results)):
        if ('photos' in results[i]):
            photos = results[i]['photos'][0]['photo_reference']
        else:
            photos = ''
        poi_list.append({'name':results[i]['name'],'address':results[i]['formatted_address'],
        'rating':results[i]['rating'],'photos':photos})
    return poi_list

def get_listings_list(soup_url):
        #open connection and get page
        uClient   = uRequest(soup_url)
        page_html = uClient.read()
        uClient.close()

        page_soup     = soup(page_html,features='html.parser')
        containers    = page_soup.findAll("div",{"class":"listing-card"} )
        listings_list = []

        for container in containers:
            image                      = container.img["data-src"]
            title_container            = container.find("h5",{"class":"card-title"})
            listing_url                = "https://www.mlslistings.com/"+title_container.find("a")['href']
            listing_address            = title_container.find("a")['title']

            price_and_status_container = container.find("h6",{"class":"listing-price-and-status"})
            listing_price              = container.find("span",{"class":"listing-price"}).text
            listing_status             = container.find("span",{"class":"listing-statusd-block"}).text
            listing_dom                = container.find("span",{"class":"listing-dom-block"}).text
            listing_type               = container.find("div",{"class":"listing-type"}).text
            listing_beds_containers    = container.select("span.listing-beds")
            listing                    = listing_beds_containers[0].find("span",{"class":"info-item-label"}).text

            if(len(listing_beds_containers)==2):
                beds      = listing_beds_containers[1].find("span",{"class":"info-item-value"}).text
                beds_text = listing_beds_containers[1].find("span",{"class":"info-item-label"}).text
            else:
                beds      = ''
                beds_text = ''

            listing_baths_container = container.find("span",{"class":"listing-baths"})

            if(listing_baths_container!=None):
                baths      = listing_baths_container.find("span",{"class":"info-item-value"}).text
                baths_text = listing_baths_container.find("span",{"class":"info-item-label"}).text
            else:
                baths      = ''
                baths_text = ''

            listing_sqft_container = container.find("span",{"class":"listing-sqft"})

            if(listing_sqft_container!=None):
                sqft      = listing_sqft_container.find("span",{"class":"info-item-value"}).text
                sqft_text = listing_sqft_container.find("span",{"class":"info-item-label"}).text
            else:
                sqft      = ''
                sqft_text = ''

            listing_lot_size_container = container.find("span",{"class":"listing-lot-size"})

            if(listing_lot_size_container!=None):
                lot_size      = listing_lot_size_container.find("span",{"class":"info-item-value"}).text
                lot_size_text = listing_lot_size_container.find("span",{"class":"info-item-label"}).text
            else:
                lot_size      = ''
                lot_size_text = ''

            listing_garage_container = container.find("span",{"class":"listing-garage"})

            if(listing_garage_container!=None):
                garage      = listing_garage_container.find("span",{"class":"info-item-value"}).text
                garage_text = listing_garage_container.find("span",{"class":"info-item-label"}).text
            else:
                garage      = ''
                garage_text = ''

            listing_year_built_containers = container.select("span.listing-sqft.last")

            if(len(listing_year_built_containers)==1):
                year_built      = listing_year_built_containers[0].find("span",{"class":"info-item-value"}).text
                year_built_text = listing_year_built_containers[0].find("span",{"class":"info-item-label"}).text
            if(len(listing_year_built_containers)==2):
                year_built      = listing_year_built_containers[1].find("span",{"class":"info-item-value"}).text
                year_built_text = listing_year_built_containers[1].find("span",{"class":"info-item-label"}).text
            else:
                year_built      = ''
                year_built_text = ''

            listings_list.append({'image':image,'listing':listing,'listing_url':listing_url,'listing_address':listing_address,'listing_price':listing_price,'listing_status':listing_status,'listing_dom':listing_dom,'listing_type':listing_type.strip(),'beds':beds,'beds_text':beds_text,'baths':baths,'baths_text':baths_text,'sqft':sqft,'sqft_text':sqft_text,'lot_size':lot_size,'lot_size_text':lot_size_text,'garage':garage,'garage_text':garage_text,'year_built':year_built,'year_built_text':year_built_text})

        return listings_list

list_of_counties = []
month_dict       = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12}
month_list       = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
year_dropdown    = []

url     = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=1c26fde416be84b20c76bec3c521159a'
poi_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

for y in range(datetime.datetime.now().year + 1, (datetime.datetime.now().year + 53)):
    year_dropdown.append(y)

try:
    workbook   = open_excel('/Users/sp/Desktop/Projects/python/medianPricePredictor/Median_Prices_of_Existing_Detached_Homes.xls')
except IOError:
    print 'Cannot open file! No such file or directory!\n'
else:
    sheet_name       = workbook.sheet_by_index(0)
    start_row        = get_start_row(sheet_name)
    list_of_counties = get_list_of_counties()

def index(request):
    request.session['list_of_counties'] = list_of_counties
    request.session['month_dict']       = month_dict
    request.session['month_list']       = month_list
    request.session['year_list']        = year_dropdown
    return render(request, "predict_app/index.html")

def info(request):
    #get weather in the County
    location         = request.session['county']
    weather_location = counties[location]['weather']
    weather_data     = get_weather(weather_location, request)

    #get points of interest in the County
    poi_location = counties[location]['gpoi']
    poi_request  = requests.get(poi_url + 'query=' + poi_location + '&key=' + api_key).json()
    poi_list     = get_poi_list(poi_location, poi_request)

    #get active listings in County
    soup_url      = counties[location]['xls']
    listings_list = get_listings_list(soup_url)

    context = {
        "weather_data": weather_data,
        "poi_list" :poi_list,
        "listings_list" :listings_list
    }
    return render(request, "predict_app/info.html", context)

def create(request):
	if request.method == "POST":
		request.session['month']  = request.POST['month']
        request.session['year']   = request.POST['year']
        request.session['county'] = request.POST['county']
        county_name               = request.POST['county']
        month                     = request.POST['month']
        month_predict             = month_dict[month]
        year_predict              = int(request.POST['year'])

        county_col_index  = get_county_index(sheet_name,county_name)
        year_month_list   = [get_year_month(workbook,sheet_name,index) for index in range(start_row+1,sheet_name.nrows)]
        county_price_list = create_county_price_list(sheet_name,start_row,county_col_index)

        county_price_list_valid,year_month_list_valid = get_valid_lists(county_price_list,year_month_list)

        plotGraph(county_price_list_valid,year_month_list_valid,county_name)

        request.session['price'] = int(predict_house_price(county_price_list_valid,year_month_list_valid,county_name,month_predict,year_predict))

	return redirect("/")
