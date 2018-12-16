from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, SoupStrainer
import re
import pandas as pd
import numpy as np
import os

url='http://qcode.us/codes/riovista/view.php?version=beta&view=mobile&topic=0'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(120)

urls_level_1 = []
urls_level_1_new = []
urls_level_2 = []
urls_level_2_new = []
urls_level_3 = []
urls_level_3_new = []
urls_level_3_filtered = []
urls_level_4 = []
urls_level_4_new = []
urls_level_5 = []
urls_level_5_new = []
final_list = []

columns = ['Source', 'Source Date', 'Section', 'Code', 'Topic', 'Subject', 'Language', 'Notes', 'URL', 'True1', 'True2', 'N']
Data = pd.DataFrame(columns=columns)

url = "http://qcode.us/codes/riovista/view.php?view=mobile"
driver.get(url)
elems = driver.find_elements_by_xpath("//*[@href]")
for elem in elems:
    link = elem.get_attribute("href")
    urls_level_1.append(link)
    
z = 0
while z < len(urls_level_1):
    if 'php?topic' in urls_level_1[z]:
        urls_level_1_new.append(urls_level_1[z])
    z += 1
urls_level_1_new = urls_level_1_new[2:]
urls_level_1_new = list(sorted(set(urls_level_1_new)))

################# THIS BLOCK GETS A LIST OF URLS
a = 0
level = 1
titles = 1
while a < len(urls_level_1_new):
    print(level)
    driver.get(urls_level_1_new[a])
    elems = driver.find_elements_by_xpath("//*[@href]")
    for elem in elems:
        link = elem.get_attribute("href")
        urls_level_2.append(link)
    b = 0
    while b < len(urls_level_2):
        if (urls_level_1_new[a][36:] + '-') in urls_level_2[b]:
            urls_level_2_new.append(urls_level_2[b])
        b+=1
    print(urls_level_2_new)
    urls_level_2_new = list(sorted(set(urls_level_2_new)))
    print(urls_level_2_new)
    print('Length of 2: ' + str(len(urls_level_2_new)))
    if(len(urls_level_2_new) != 0):
        c = 0
        while c < len(urls_level_2_new):
            driver.get(urls_level_2_new[c])
            elems = driver.find_elements_by_xpath("//*[@href]")
            for elem in elems:
                link = elem.get_attribute("href")
                urls_level_3.append(link)
            d = 0
            while d < len(urls_level_3):
                j=0
                while j < len(urls_level_2_new):
                    if (((urls_level_2_new[j][(len(urls_level_2_new[j]) - 16):]) + '-') in urls_level_3[d]):
                        urls_level_3_new.append(urls_level_3[d])
                    j+=1
                print(urls_level_3_new)
                urls_level_3_new = list(sorted(set(urls_level_3_new)))
                print(urls_level_3_new)
                d+=1
            print('Length of 3: ' + str(len(urls_level_3_new)))
            if(len(urls_level_3_new) != 0):
                e = 0
                while e < len(urls_level_3_new):
                    driver.get(urls_level_3_new[e])
                    elems = driver.find_elements_by_xpath("//*[@href]")
                    for elem in elems:
                        link = elem.get_attribute('href')
                        urls_level_4.append(link)
                    f = 0
                    while f < len(urls_level_4):
                        p = 0
                        while p < len(urls_level_3_new):
                            if (urls_level_3_new[p][(len(urls_level_3_new[p]) - 25):] + ('-' or '_')) in urls_level_4[f]:
                                urls_level_4_new.append(urls_level_4[f])
                            p+=1
                        print(urls_level_4_new)
                        urls_level_4_new = list(sorted(set(urls_level_4_new)))
                        print(urls_level_4_new)
                        f+=1
                    print('Length of 4: ' + str(len(urls_level_4_new)))
                    if(len(urls_level_4_new) != 0):
                        h = 0
                        while h < len(urls_level_4_new):
                            driver.get(urls_level_4_new[h])
                            elems = driver.find_elements_by_xpath("//*[@href]")
                            for elem in elems:
                                link = elem.get_attribute('href')
                                urls_level_5.append(link)
                            l = 0
                            while l < len(urls_level_5):
                                r = 0
                                while r < len(urls_level_4_new):
                                    if(urls_level_4_new[r][(len(urls_level_4_new[r]) - 25):] + ('-' or '_')) in urls_level_5[l]:
                                        urls_level_5_new.aappend(urls_level_5[l])
                                    r+=1
                                print(urls_level_5_new)
                                urls_level_5_new = list(set(urls_level_5_new))
                                print(urls_level_5_new)
                                l+=1
                            print('Length of 5: ' + str(len(urls_level_5_new)))
                            if(len(urls_level_5 != 0)):
                                print('Needs higher level: ' + str(level))
                            else:
                                m = 0
                                while m < len(urls_level_4_new):
                                    final_list.append(urls_level_4_new[m])
                                    m+=1
                                print(urls_level_4_new)
                                urls_level_4 = []
                                urls_level_4_new = []
                            h+=1
                    else:
                        n = 0
                        while n < len(urls_level_3_new):
                            final_list.append(urls_level_3_new[n])
                            n+=1
                    urls_level_3 = []
                    urls_level_3_new = []
                    e+=1
            else:
                g = 0
                while g < len(urls_level_2_new):
                    final_list.append(urls_level_2_new[g])
                    g+=1
            urls_level_2 = []
            urls_level_2_new = []
            c+=1
    else:
        o = 0
        while o < len(urls_level_1_new):
            final_list.append(urls_level_1_new[o])
            o+=1
    urls_level_2 = []
    urls_level_2_new = []
    level+=1
    a+=1

######################### THIS BLOCK CLEANS THE LIST OF URLS
final = set(final_list)
set1 = set(urls_level_1_new)
c = final.difference(set1)
total_list = list(c)
total_list_new = []
i = 0
while i < len(total_list):
    total_list_new.append(total_list[i][:40] + 'version=beta&view=mobile&' + total_list[i][40:])
    i+=1

################### THIS BLOCK PULLS DATA FROM THE URLS
i = 0
while i < len(total_list_new):
    url=total_list_new[i]
    driver.get(url)
    driver.implicitly_wait(120)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    language = []
    headers = []
    for p in soup.findAll("div", {"class": "content"}):
        language.append(p.text)
    totalText = ' '.join(language)
    for a in soup.findAll("div", {"class": "ancestor"}):
        headers.append(a.text)
    for row in soup.findAll("div", {"class": "currentTopic"}):
        codeCombined = row.text
    code = codeCombined.split()[0]
    codeCombined1 = codeCombined.split(' ')
    del codeCombined1[0:9]
    subject = ' '.join(codeCombined1)
    localURL = url
    date = 2004
    Data = Data.append({'Source': headers[0], 'Source Date': date, 'Code': code, 'Topic': headers[1], 'Subject': subject, 'Language': totalText, 'Notes': ' ', 'URL': localURL, 'True1': 'True', 'True2': 'True', 'N': '/N'}, ignore_index=True)
    i+=1

##################################### THIS BLOCK CLEANS THE DATA
i = 0
while i < 142:
    Data['Language'][i] = Data['Language'][i].split('\n\n\n\n')[1]
    i+=1
Language1 = Data['Language']
i = 0
while i < len(Language1):
    Language1[i] = Language1[i].split('\n\xa0\xa0\xa0\xa0')
    del Language1[i][0]
    Language1[i] = '\\'.join(Language1[i])
    i = i+1
Code1 = Data['Code']
Section1 = Data['Section']
i = 0
while i < len(Code1):
    Code1[i] = Code1[i].split('.')
    Section1[i] = Code1[i][0]
    del Code1[i][0]
    Code1[i] = '.'.join(Code1[i])
    i = i + 1
Section1 = Section1.astype(int)
Data['Language'] = Language1
Data['Code'] = Code1
Data['Section'] = Section1

######################## DROP NAN VALUES
Data = Data.replace('', np.nan, regex=True)
Data = Data.dropna()

Data.to_csv("Rio_Vista_1_normal.csv")
Data.to_csv("Rio_Vista_1.csv", sep="|")