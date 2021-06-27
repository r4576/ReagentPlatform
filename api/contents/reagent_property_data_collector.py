import json
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re


class Table:
    def __init__(self,url,table_class ) :
        self._url = url
        self._table_class = table_class

    def get_table_list(self):
        return self.__make_table_list()


    def __make_table_list(self):
        response = requests.get(self._url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find_all('table', { 'class': self._table_class })


class Crawling_link_table(Table):
    def get_url_list(self,table_list):
        return self.__make_wikiurl_list(table_list)

    
    def __make_wikiurl_list(self,table_list):
        url_list = []
        for i in range(0,len(table_list)):
            for url in table_list[i].find_all("a"):
                if '/wiki/' in url.get('href'):
                    url_list.append(url.get('href'))
                else :
                    pass
        return url_list


class Crawling_data_table(Table):
    def get_table(self) :
        return self.get_table_list()[0]


    def get_data(self,property_name):
        text = self.__find_data(property_name)
        if type(text) == str:
            return text.strip()
        else :
            pass
    

    def get_Name(self):
        all_name_list = []
        all_name_list.append(self.__recall_main_name())
        try :
            all_name_list = all_name_list + self.__recall_other_name()
            return all_name_list
        except :
            return all_name_list

    
    def __text_processing(self,text):
        if '[' in text :
            return re.sub(re.compile(r'\[.*?\]'),'',text)
        else :
            return text

    def __find_data(self,property_name):  
        table = self.get_table()
        for tr in table.find_all('tr'):
            tr_contents = tr.find("a", {'title': property_name})
            if tr_contents != None :
                contents = list(tr.children)[-1].text
                return self.__text_processing(contents)
            else :
                pass
        

    def get_CAS_no(self):
        table = self.get_table()
        CAS_no = table.find("a",{ "class" : "external text" }).text
        CAS_no = self.__text_processing(CAS_no)
        return CAS_no.strip()


    def __recall_main_name(self):
        table = self.get_table()
        reagent_name = table.find('caption').text
        reagent_name = self.__text_processing(reagent_name)
        return reagent_name.strip()
    

    def __recall_other_name(self):
        table = self.get_table()
        for td in table.find_all('tr'):
            try:
                if "Other names" in td.text :
                    text = str(list(td.children)[-1]).split('br')
                    text = text[1:]
                    name_list = []
                    for i in text :
                        index = re.search('>(.+?)<', i).group(1)
                        name_list.append(index)
                    return name_list

                else :
                    pass
            
            except:
                pass


Crawling_wiki_link_table = Crawling_link_table('https://en.wikipedia.org/wiki/Glossary_of_chemical_formulae','wikitable') 
Crawling_table_list = Crawling_wiki_link_table.get_table_list()
Crawling_table_url_list = Crawling_wiki_link_table.get_url_list(Crawling_table_list)


filedata_list = []

# toyset = [0,5,29,50,1600]

try:
    # for i in toyset:
    for i in range(len(Crawling_table_url_list)):
        Crawling_url = 'https://en.wikipedia.org%s' %Crawling_table_url_list[i]

        Crawling_wiki_data_table = Crawling_data_table(Crawling_url, 'infobox bordered')
        # Crawling_wiki_data_table = Crawling_data_table('https://en.wikipedia.org/wiki/Gold(III)_iodide','infobox bordered')

        # print(Crawling_wiki_data_table.get_CAS_no())
        # print(Crawling_wiki_data_table.get_data('Density'))
        # print(Crawling_wiki_data_table.get_data('Melting point'))
        # print(Crawling_wiki_data_table.get_data('Boiling point'))
        # print(Crawling_wiki_data_table.get_data('Chemical formula'))
        # print(Crawling_wiki_data_table.get_Name())

        file_data = OrderedDict()
        colunm_list = ["casNo", "name" , "formula" ,"molecularWeight" , "meltingpoint" , "boilingpoint" ,"density"]


        file_data[colunm_list[0]] = Crawling_wiki_data_table.get_CAS_no()
        file_data[colunm_list[1]] = Crawling_wiki_data_table.get_Name()
        file_data[colunm_list[2]] = Crawling_wiki_data_table.get_data('Chemical formula')
        file_data[colunm_list[3]] = Crawling_wiki_data_table.get_data('Molar mass')
        file_data[colunm_list[4]] = Crawling_wiki_data_table.get_data('Melting point')
        file_data[colunm_list[5]] = Crawling_wiki_data_table.get_data('Boiling point')
        file_data[colunm_list[6]] = Crawling_wiki_data_table.get_data('Density')

        filedata_list.append(file_data)
        # filedata_list.append(json.dumps(file_data, ensure_ascii=False))

        if i % 50 == 0:
            print("[",i,"/",1600, "]")
except:
    pass


file_path = "./data/Reagent_property_data.json"

with open(file_path, 'w', encoding = 'utf-8') as make_file:
    json.dump(filedata_list, make_file, ensure_ascii=False)
