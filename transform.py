import pandas as pd
import json

fileObject = open("data.json", "r")
jsonContent = fileObject.read()
aList = json.loads(jsonContent)

df = pd.DataFrame(aList['result'])

print(df)