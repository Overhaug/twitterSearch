import json

with open('data/json_data.json', 'r', encoding='utf-8') as file:
    jsonFile = json.load(file)

    l = []
    for i in jsonFile['tweets']:
        l.append(i)

    with open('data/js_d.json', 'w', encoding='utf-8') as write:
        json.dump(l, write, ensure_ascii=False, indent=2)

    # Open file, encoding for utf-8
    src = open("data/js_d.json", "r", encoding="utf-8")
    firstLine = "var tweets = "
    oLine = src.readlines()
    # Prepend string on first line
    oLine.insert(0, firstLine)
    src.close()

    # Open file in write mode
    src = open("data/js_d.json", "w", encoding="utf-8")
    src.writelines(oLine)
    src.close()


