import json

#open token.json file from the same directory
def get_token():
    with open('Utils/Token/token.json') as f:
        data = json.load(f)
        return data['token']
