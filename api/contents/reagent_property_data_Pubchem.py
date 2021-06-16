import json
from typing import final
import requests
from bs4 import BeautifulSoup


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
    datanumber_list = []
    seconddata = []
    for i, v in enumerate(datalist):
        if "C" in v:
            if '(' in v:
                datanumber_list.append(i)
            else:
                pass
        else:
            datanumber_list.append(i)
    for i in reversed(datanumber_list) :
        seconddata.append(datalist.pop(i))
    return datalist + seconddata


def data_processingD(datalist):
    datanumber_list = []
    seconddata = []
    for i, v in enumerate(datalist):
        if "g" in v:
            if '(' in v:
                datanumber_list.append(i)
            else:
                pass
        else:
            datanumber_list.append(i)
    for i in reversed(datanumber_list) :
        seconddata.append(datalist.pop(i))
    return datalist + seconddata


def get_commonname(cid):
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%d/description/json' %cid
    jsonfile = recall_json_api(url)
    commonname = jsonfile.get("InformationList").get("Information")[0]
    return commonname.pop("Title")


def get_MeltingPoint(cid):
    try:    
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
        return data_processingMB(MP_datalist)[0]
    except:
        return None


def get_BoilingPoint(cid):
    try:
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
        return data_processingMB(BP_datalist)[0]
    except:
        return None

def get_Density(cid):
    try:
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
        return data_processingD(D_datalist)[0]
    except:
        return None


def get_CAS(cid):
    try:
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
        return CAS_datalist[0]
    except:
        return None


def get_Table_data(name):
    try :
        dict_properties = get_PropertyTable_data(name)
        CID = dict_properties.pop("CID")

        file_data = {}
        colunm_list = ["casNo", "formula" ,"molecularWeight" , "meltingpoint" , "boilingpoint" ,"density"]
        file_data[colunm_list[0]] = get_CAS(CID)
        file_data[colunm_list[1]] = dict_properties['MolecularFormula']
        file_data[colunm_list[2]] = str(dict_properties['MolecularWeight'])
        file_data[colunm_list[3]] = get_MeltingPoint(CID)
        file_data[colunm_list[4]] = get_BoilingPoint(CID)
        file_data[colunm_list[5]] = get_Density(CID)
    except:
        file_data = None
    finally:
        return file_data


def get_query(name):
    try:
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/synonyms/json' %name
        jsonfile = recall_json_api(url)

        dict_properties = get_PropertyTable_data(name)
        CID = dict_properties.pop("CID")

        query_dict = {}
        colunm_list = ["casNo", "name", "synonyms"]
        query_dict[colunm_list[0]] = get_CAS(CID)
        query_dict[colunm_list[1]] = get_commonname(CID)
        query_dict[colunm_list[2]] = jsonfile.get("InformationList").get("Information")[0].get("Synonym")
    except:
        query_dict = None
    finally:
        return query_dict


if __name__ == "__main__":
    print(get_query("Water"))
    # print(get_Table_data("water"))
    # print(get_Table_data("wat"))
