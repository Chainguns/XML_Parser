import pandas as pd
import base64
import pprint
import json
import re

df = pd.read_xml('juice_shop.xml')

# Create new columns for the decoded request and response
decoded_request = []
for request in df['request']:
    decoded_bytes = base64.b64decode(request)
    decodedStr = str(decoded_bytes, "utf-8")
    decoded_request.append(decodedStr)

df['decoded_request'] = decoded_request

decoded_response = []
for response in df['response']:
    decoded_bytes = base64.b64decode(response)
    decodedStr = str(decoded_bytes, "utf-8")
    decoded_response.append(decodedStr)

df['decoded_response'] = decoded_response

# Clean Data to work with JSON format
df['decoded_request'] = df['decoded_request'].str.replace('\r\n', '\n')
df['decoded_response'] = df['decoded_response'].str.replace('\r\n', '\n')

# Create new dataframe with only the decoded data, and rename the columns
decoded_df = df.filter(['decoded_request', 'decoded_response'])
decoded_df.columns = ['request', 'response']

# Convert to dict
decoded_dict = decoded_df.to_dict(orient="list")

# More formatting... and done!
formatted_data = []
myDict = {'session': []}
myDict["session"].append(decoded_dict)

formatted_data.append(myDict)

#Format again to remove \ character but not \n - currently doesn't work 26.12
with open('test3.json', 'a+') as json_f:
    content = json.dumps(formatted_data)
    new_content = re.sub(pattern=r'\\(?!n)', repl="", string=content)
    pprint.pprint(new_content)
    json.dump(new_content, json_f)
