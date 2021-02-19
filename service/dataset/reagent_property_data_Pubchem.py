import json
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

# url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/synonyms/json'

# url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/MolecularFormula,MolecularWeight/JSON'

def recall_json_api(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser',from_encoding= 'utf-8')
    jsonfile = json.loads(str(soup))
    return jsonfile


def get_PropertyTable_data(query):
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/MolecularFormula,MolecularWeight/JSON'%query
    jsonfile = recall_json_api(url)
    properties = jsonfile.get("PropertyTable").get("Properties")[0]
    return properties


def data_processingMB(datalist):
    originaldata = datalist
    seconddata = []
    for i, v in enumerate(originaldata):
        if "C" in v:
            pass
        else:
            seconddata.append(datalist.pop(i))
    return datalist + seconddata


def data_processingD(datalist):
    originaldata = datalist
    seconddata = []
    for i, v in enumerate(originaldata):
        if "g" in v:
            pass
        if "C" in v:
            pass
        else:
            seconddata.append(datalist.pop(i))
    return datalist + seconddata


def get_commonname(cid):
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%d/description/json' %cid
    jsonfile = recall_json_api(url)
    commonname = jsonfile.get("InformationList").get("Information")[0]
    return commonname.pop("Title")


def get_MeltingPoint(cid):
    MP_datalist = []
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%d/JSON?heading=Melting+Point' %cid
    jsonfile = recall_json_api(url)
    Meltingpoint_list = jsonfile.get("Record").get("Section")[0].get("Section")[0].get("Section")[0].get("Information")
    for meltingpoint in Meltingpoint_list:
        if "Value" in meltingpoint.keys():
            try:
                data = meltingpoint.get("Value").get("StringWithMarkup")[0].get("String")
                MP_datalist.append(data)
            except:
                try:
                    data = str(meltingpoint.get("Value").get("Number")[0]) + meltingpoint.get("Value").get("Unit")
                    MP_datalist.append(data)
                except:
                    pass
    return data_processingMB(MP_datalist)


def get_BoilingPoint(cid):
    BP_datalist = []
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%d/JSON?heading=Boiling+Point' %cid
    jsonfile = recall_json_api(url)
    Boilingpoint_list = jsonfile.get("Record").get("Section")[0].get("Section")[0].get("Section")[0].get("Information")
    for boilingpoint in Boilingpoint_list:
        if "Value" in boilingpoint.keys():
            try:
                data = boilingpoint.get("Value").get("StringWithMarkup")[0].get("String")
                BP_datalist.append(data)
            except:
                try:
                    data = str(boilingpoint.get("Value").get("Number")[0]) + boilingpoint.get("Value").get("Unit")
                    BP_datalist.append(data)
                except:
                    pass
    return data_processingMB(BP_datalist)

def get_Density(cid):
    D_datalist = []
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%d/JSON?heading=Density' %cid
    jsonfile = recall_json_api(url)
    Density_list = jsonfile.get("Record").get("Section")[0].get("Section")[0].get("Section")[0].get("Information")
    for density in Density_list:
        if "Value" in density.keys():
            try:
                data = density.get("Value").get("StringWithMarkup")[0].get("String")
                D_datalist.append(data)
            except:
                try:
                    data = str(density.get("Value").get("Number")[0]) + density.get("Value").get("Unit")
                    D_datalist.append(data)
                except:
                    pass 
    return data_processingD(D_datalist)


def get_CAS(cid):
    CAS_datalist = []
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%d/JSON?heading=CAS' %cid
    jsonfile = recall_json_api(url)
    CAS_list = jsonfile.get("Record").get("Section")[0].get("Section")[0].get("Section")[0].get("Information")
    for CAS in CAS_list:
        if "Value" in CAS.keys():
            try:
                data = CAS.get("Value").get("StringWithMarkup")[0].get("String")
                CAS_datalist.append(data)
            except:
                pass 
    return CAS_datalist


dict_properties = get_PropertyTable_data('water')
CID = dict_properties.pop("CID")


file_data = OrderedDict()
colunm_list = ["casNo", "name" , "formula" ,"molecularWeight" , "meltingpoint" , "boilingpoint" ,"density"]
file_data[colunm_list[0]] = get_CAS(CID)[0]
file_data[colunm_list[1]] = get_commonname(CID)
file_data[colunm_list[2]] = dict_properties['MolecularFormula']
file_data[colunm_list[3]] = str(dict_properties['MolecularWeight'])
file_data[colunm_list[4]] = get_MeltingPoint(CID)[0]
file_data[colunm_list[5]] = get_BoilingPoint(CID)[0]
file_data[colunm_list[6]] = get_Density(CID)[0]


file_path = "./Reagent_property_data_pubchem.json"

with open(file_path, 'w', encoding = 'utf-8') as make_file:
    json.dump(file_data, make_file, ensure_ascii=False)
