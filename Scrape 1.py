from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, SoupStrainer
import re
import pandas as pd
import numpy as np
import os

url='http://library.amlegal.com/nxt/gateway.dll/Illinois/tinley/villageoftinleyparkillinoiscodeofordinan?f=templates$fn=default.htm$3.0$vid=amlegal:tinleypark_il'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(120)

link_appends = ['titleigeneralprovisions',
'titleiiiadministration',
'titlevpublicworks',
'titleviitrafficcode',
'titleixgeneralregulations',
'titlexibusinessregulations',
'titlexiiigeneraloffenses',
'titlexvlandusage'];
base_link = 'http://library.amlegal.com/nxt/gateway.dll/Illinois/tinley/';
level_1_urls = [];
level_2_urls = [];
level_3_urls = [];
level_4_urls = [];
final_list = [];
check_list = [];
columns = ['Source', 'Last Update', 'Chapter', 'Code', 'Topic', 'Subject', 'Language', 'URL', 'True1', 'True2', 'N'];
Data = pd.DataFrame(columns = columns);
i = 0;
while i < len(link_appends):
    level_1_urls.append(base_link + link_appends[i]);
    i = i + 1;
i = 0;
while i < len(level_1_urls):
    driver.get(level_1_urls[i])
    driver.implicitly_wait(120)
    links = []
    elems = driver.find_elements_by_xpath("//*[@href]")
    for elem in elems:
        link = elem.get_attribute("href")
        links.append(link)
    level_2_urls = [s for s in links if "jumplink" in s];
    level_2_urls = list(set(level_2_urls) ^ set(level_1_urls));
    level_2_urls = [item for item in level_2_urls if item not in level_1_urls]
    k = 0
    while k < len(level_2_urls):
        if(len(level_2_urls[k][-7:].split('.')) == 1):
            final_list.append(level_2_urls[k])
        else:
            del level_2_urls[k]
        k = k + 1;
    j = 0;
    while j < len(level_2_urls):
        driver.get(level_2_urls[j])
        driver.implicitly_wait(120)
        links = []
        elems = driver.find_elements_by_xpath("//*[@href]")
        for elem in elems:
            link = elem.get_attribute("href")
            links.append(link)
        level_3_urls = [s for s in links if "jumplink" in s];
        level_3_urls = list(set(level_3_urls) ^ set(level_2_urls));
        level_3_urls = [item for item in level_3_urls if item not in level_2_urls]
        temp = []
        for u in level_3_urls:
            if (len(u.split('.')) == 1):
                temp.append(u)
                final_list.append(u)
        level_3_urls = temp
        temp = []
        k = 0
        while k < len(level_3_urls):
            print('Level 3')
            print(level_3_urls[k])
            driver.get(level_3_urls[k])
            driver.implicitly_wait(120)
            links = []
            elems = driver.find_elements_by_xpath("//*[@href]")
            for elem in elems:
                link = elem.get_attribute("href")
                links.append(link)
            level_4_urls = [s for s in links if "jumplink" in s];
            level_4_urls = list(set(level_4_urls) ^ set(check_list));
            level_4_urls = [item for item in level_4_urls if item not in level_3_urls]
            if len(level_4_urls) != 1:
                l = 0
                while l < len(level_4_urls):
                    if(len(level_4_urls[l][-7:].split('.')) == 1):
                        final_list.append(level_4_urls[l])
                    else:
                        del level_4_urls[l]
                    l = l + 1;
                check_list = level_4_urls;
            level_4_urls = []
            k = k + 1;
        level_3_urls = []
        j = j + 1;
    level_2_urls = []
    i = i + 1;
i = 0
while i < len(final_list):
    driver.get(final_list[i])
    driver.implicitly_wait(120)
    soup = BeautifulSoup(driver.page_source, 'lxml');
    strSoup = str(soup);
    Sections = [];
    Section_number = [];
    Section_descr = [];
    code = [];
    title_number = []
    source = 'Tinley Park'
    year = 2018;
    newSoup = [];
    for a in soup.findAll("div", {"class": "Chapter"}):
        topic = a.text;
    for a in soup.findAll("div", {"class": "Section"}):
        Sections.append(a.text);
    j = 0;
    while j < len(Sections):
        temp = Sections[j].split('§');
        temp = temp[-1].split('\xa0');
        if (len(temp) == 1):
            Section_descr.append(''.join(temp));
        else:
            Section_number.append(''.join(temp[-2]));
            Section_descr.append(''.join(temp[-1]));
        j = j + 1;
    j = 0;
    while j < len(Section_number):
        temp = Section_number[j].split('.');
        title_number.append(temp[0]);
        code.append(str(temp[0]) + '.' + str(temp[1]));
        del temp
        j = j + 1;
    splitSoup = strSoup.split('<div class="Section"');
    del splitSoup[0];
    j = 0;
    while j < len(splitSoup):
        splitSoup[j] = splitSoup[j][1:];
        newSoup.append(BeautifulSoup(splitSoup[j], "html.parser"));
        j = j + 1;
    textSoup = [];
    j = 0
    while j < len(newSoup):
        temp = newSoup[j].text.split('\xa0\xa0\xa0');
        del temp[0];
        textSoup.append('\\'.join(temp));
        del temp
        j = j + 1;
    temp = textSoup[-1].split('Disclaimer:');
    del temp[-1]
    temp = ''.join(temp)
    textSoup[-1] = temp
    del temp
    if (len(Section_number) == len(Section_descr) and len(Section_number) == len(textSoup)):
        j = 0;
        while j < len(Section_number):
            Data = Data.append({'Source': source, 'Last Update': year, 'Chapter':title_number[j], 'Code': code[j], 'Topic': topic, 'Subject': Section_descr[j], 'Language': textSoup[j], 'URL': final_list[i], 'True1': 'True', 'True2': 'True', 'N': '/N'}, ignore_index=True)
            j = j + 1;
    i = i + 1;
Data.to_csv("Tineley_Park_1_normal.csv")
Data.to_csv("Tineley_Park_1.csv", sep="|")