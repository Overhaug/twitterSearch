# Simply to count instances of ... in data file

import Search
import json

result = 0

with open("data/json_data.json", "r", encoding="utf-8") as read_file:
    x = json.load(read_file)
    for k in x['tweets']:
        if 'tweet' in k:
            result += 1
    print(result)
