from pymongo import MongoClient

client = MongoClient("mongodb+srv://next:nextproject@cluster0.myrfh.mongodb.net/ChemDatabase?retryWrites=true&w=majority")
djongo_test = client['djongo_test']
reagentPropertyData = djongo_test['api_reagentpropertydata']
materialSafetyData = djongo_test['api_materialsafetydata']

new_ReagentData = []
new_SafetyData = []

# json 파일을 읽어 new_ReagentData, new_SafetyData에 append

reagentPropertyData.insert_many(new_ReagentData)
materialSafetyData.insert_many(new_SafetyData)
