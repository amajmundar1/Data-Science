from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, SoupStrainer
import re
import pandas as pd
import numpy as np
import os

url='https://codes.iccsafe.org/content/IMC2012?site_type=public'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(120)

############################ Gets the list of urls where data will be found #################################
links = []
elems = driver.find_elements_by_xpath("//*[@href]")
for elem in elems:
    link = elem.get_attribute("href")
    links.append(link)
links = [ x for x in links if "chapter" in x ]
Data = {}

############################ Iterates through list of URLs ########################################
j = 0
while j < len(links):
    Section = []
    Title = []
    Language = []
    Headers = []
########################## Gets information from webpage based on how the webpage arrenges the data ######################
    driver.get(links[j])
    soup = BeautifulSoup(driver.page_source, 'lxml');
    for element in soup.findAll("p", class_=True):
        if len(element["class"]) == 1:
            if ("left_ind" in element["class"][0]):
                Language.append((" |CHILD| ") + element.text)
            elif ("ICCBULLET" in element["class"][0]):
                Language.append((" |CHILD| ") + element.text)
            else:
                Language.append((" |PARENT| ") + element.text)
        else:
            if ("left_ind" in element["class"][0]) or ("left_ind" in element["class"][1]):
                Language.append((" |CHILD| ") + element.text)
            elif ("ICCBULLET" in element["class"][0]) or ("ICCBULLET" in element["class"][1]):
                Language.append((" |CHILD| ") + element.text)
            else:
                Language.append((" |PARENT| ") + element.text)
####################### Cleans Data into individual columns ################################
    del Language[0:13]
    del Language[-33:]
    Language = ''.join(Language)
    Language = Language.split('|PARENT|')
    del Language[0]
    Language = [w.replace('|CHILD|', '\\') for w in Language]
    for element in Language:
        Headers.append(element.split('. ')[0])
    for element in Headers:
        temp = element.split('] ')
        if len(temp) > 1:
            temp = temp[1:]
            Title.append('] '.join(temp))
        else:
            Title.append(''.join(temp))
        del temp
    
    temp = []
    for element in Title:
        if element[0] == " ":
            temp.append(element[1:])
        else:
            temp.append(element)
    Title = temp
    del temp
    
    i = 0
    while i < len(Title):
        temp = Title[i].split('.')
        if temp[0].isdigit():
            temp2 = temp[0] + '.' + (temp[1].split(' '))[0]
            Section.append(temp2)
            del temp2
            del temp[0]
            Title[i] = '.'.join(temp)
            del temp
            i = i + 1
        else:
            Section.append("202")
            i = i + 1
    
    i = 0
    while i < len(Title):
        if(Title[i] == Language[i]):
            del Title[i]
            del Language[i]
            del Section[i]
            i = 0
        else:
            i = i + 1
    
    temp = []
    for element in Title:
        temp1 = element.split(' ')
        del temp1[0]
        temp.append(' '.join(temp1))
        del temp1
    Title = temp
    del temp
    
    i = 0
    while i < len(Title):
        if Title[i] == "":
            del Title[i]
            del Section[i]
            del Language[i]
            i = 0
        else:
            i = i + 1
    
    temp = []
    i = 0
    while i < len(Language):
        if Title[i]:
            temp1 = Language[i].split(Title[i])
            del temp1[0]
            temp.append(Title[i].join(temp1))
            del temp1
        i = i + 1
    Language = temp
    del temp
    
    i = 0
    while i < len(Language):
        if Language[i]:
            i = i + 1
        else:
            del Language[i]
            del Section[i]
            del Title[i]
            i = 0
########################### Add data to Dataframe, each webpage has its own ##############################
    Data["Part{0}".format(j)] = pd.DataFrame({'Source': "2012 International Fire Codes", 'Last Updated': "April 2014", 'Section': Section, 'Title': Title, 'Language': Language, 'URLs': links[j], 'True1': 'True', 'True2': 'True', 'N': '/N'})
    j = j + 1

########################### Combine All Dataframes into one Dataframe ##############################
frames = []
j = 0
while j < len(links):
    frames.append(Data["Part{0}".format(j)])
    j = j + 1
CompleteData = pd.concat(frames, ignore_index = True)

############################## Rearrange the columns ############################################
CompleteData = CompleteData[['Source', 'Last Updated', 'Section', 'Title', 'Language', 'URLs', 'True1', 'True2', 'N']]

############################# Export to CSV ###################################################
CompleteData.to_csv("International_Mechanical_Codes_norm.csv")
CompleteData.to_csv("International_Mechanical_Codes_pipe_del.csv", sep='|')
