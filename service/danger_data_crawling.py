import json
import requests 
from bs4 import BeautifulSoup
import pandas as pd

file_path = "./sample/danger_sample.json"

response = requests.get('https://icis.me.go.kr/chmCls/chmClsView.do?hlhsn_sn=%d' %1)
soup = BeautifulSoup(response.content, 'html.parser')
        
table = soup.find('table', { 'class': 'view_table' })

table_index_list = []

table_tr_list = []

def find_list_num(label):
    for i in table_tr_list:
        if label in i.text:
            return table_tr_list.index(i)

def data_table_processing(start_label,end_label):
    for tr in table.find_all("tr"):
        table_tr_list.append(tr)

    return table_tr_list[find_list_num(start_label):find_list_num(end_label)]

def index_processing(index):
    processed_indexes = index.split('·')
    processed_indexes = [line.rstrip() for line in processed_indexes]
    return processed_indexes

def row_data_processing(table_row_name,processed_table):
    try:
        for tr in processed_table :
            if table_row_name in tr.text:
                index = tr.find("td").text
                indexes = index_processing(index)
                processed_index = "\n".join(indexes[1:])
            else :
                pass
        return processed_index
    except:
        return "자료없음"


# processed_data_table_1 = data_table_processing('관리정보','물리화학적 특성 정보')
# processed_data_table_2 = data_table_processing('물리화학적 성질','물질 제조 방법')
# processed_data_table_3 = data_table_processing('NFPA 위험성 코드','화재 및 폭발 위험 특성')
# processed_data_table_4 = data_table_processing('화재 및 폭발 위험 특성','응급 의학 정보')
# processed_data_table_5 = data_table_processing('응급 의학 정보','독성정보')
# processed_data_table_6 = data_table_processing('화학사고대응','해양 대응 정보')

first_row_list = ['CAS 번호']
second_row_list = ['상태','색상','냄새','맛']
third_row_list = ['건강위험성','화재위험성','반응위험성','특수위험성']
fifth_row_list = ['반응성','부식성','피해야 할 조건','일반 증상','흡입','피부','안구','경구','기타']
sixth_row_list = ['흡입','피부','안구','경구','기타']
seventh_row_list = ['누출방제요령','화재진압요령','취급 및 저장 방법','취급시 주의사항','폐기시 주의사항']


def data_collecting(table_row_name_list,start_label,end_label):
    collected_data_list = []
    processed_data_table = data_table_processing(start_label,end_label)
    for row_name in table_row_name_list :
        data = row_data_processing(row_name,processed_data_table)
        collected_data_list.append(data)
    return collected_data_list

collected_data_list_1 = data_collecting(first_row_list,'관리정보','물리화학적 특성 정보')
collected_data_list_2 = data_collecting(second_row_list,'물리화학적 성질','물질 제조 방법')



collected_data_list_3_4 = data_collecting(third_row_list,'NFPA 위험성 코드','화재 및 폭발 위험 특성')

collected_data_list_3 = []
collected_data_list_4 = []
for i in collected_data_list_3_4 :
    if any(int_type.isdigit() for int_type in i):
        collected_data_list_3.append(i[0])
        collected_data_list_4.append(i[2:])
    else :
        collected_data_list_3.append('자료없음')
        collected_data_list_4.append(i)

collected_data_list_3
collected_data_list_4




collected_data_list_5 = data_collecting(fifth_row_list,'화재 및 폭발 위험 특성','응급 의학 정보')
collected_data_list_6 = data_collecting(sixth_row_list,'응급 의학 정보','독성정보')
collected_data_list_7 = data_collecting(seventh_row_list,'화학사고대응','해양 대응 정보')

row_data = collected_data_list_1 + collected_data_list_2 + collected_data_list_3 + collected_data_list_4 + collected_data_list_5 + collected_data_list_6 + collected_data_list_7

print(len(row_data))



# print(row_data_processing("화재 및 폭발 가능성",processed_data_table))




    
#def table_index_append():

danger_table = pd.DataFrame(columns=['cas_no','물리화학적 성질:상태','물리화학적 성질:색상','물리화학적 성질:냄새','물리화학적 성질:맛','NFPA 위험성 코드:건강위험성 percent','NFPA 위험성 코드:화재위험성 percent','NFPA 위험성 코드:반응위험성 percent','NFPA 위험성 코드:특수위험성 percent','NFPA 위험성 코드:건강위험성','NFPA 위험성 코드:화재위험성','NFPA 위험성 코드:반응위험성',
'NFPA 위험성 코드:특수위험성','안전/반응 위험 특성:반응성(안전성, 산화성)','안전/반응 위험 특성:부식성','안전/반응 위험 특성:피해야 할 조건','인체 유해성:일반 증상','인체 유해성:흡입','인체 유해성:피부','인체 유해성:안구','인체 유해성:경구','인체 유해성:기타',
'응급 조치 요령:흡입','응급 조치 요령:피부','응급 조치 요령:안구','응급 조치 요령:경구','응급 조치 요령:기타','사고 대응 정보:누출방제요령','사고 대응 정보:화재진압요령','취급 주의 정보:취급 및 저장 방법','취급 주의 정보:취급시 주의사항','취급 주의 정보:폐기시 주의사항'])

list_check = ['cas_no','물리화학적 성질:상태','물리화학적 성질:색상','물리화학적 성질:냄새','물리화학적 성질:맛','NFPA 위험성 코드:건강위험성 percent','NFPA 위험성 코드:화재위험성 percent','NFPA 위험성 코드:반응위험성 percent','NFPA 위험성 코드:특수위험성 percent','NFPA 위험성 코드:건강위험성','NFPA 위험성 코드:화재위험성','NFPA 위험성 코드:반응위험성',
'NFPA 위험성 코드:특수위험성','안전/반응 위험 특성:반응성(안전성, 산화성)','안전/반응 위험 특성:부식성','안전/반응 위험 특성:피해야 할 조건','인체 유해성:일반 증상','인체 유해성:흡입','인체 유해성:피부','인체 유해성:안구','인체 유해성:경구','인체 유해성:기타',
'응급 조치 요령:흡입','응급 조치 요령:피부','응급 조치 요령:안구','응급 조치 요령:경구','응급 조치 요령:기타','사고 대응 정보:누출방제요령','사고 대응 정보:화재진압요령','취급 주의 정보:취급 및 저장 방법','취급 주의 정보:취급시 주의사항','취급 주의 정보:폐기시 주의사항']

danger_table.loc[0] = row_data

danger_table = danger_table.to_json(file_path, orient='records',force_ascii=False)

# with open(file_path, 'w',encoding='utf-8') as outfile:
#     json.dump(danger_table, outfile, ensure_ascii=False)