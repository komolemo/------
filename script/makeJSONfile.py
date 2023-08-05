import json

# def outputJSON():
#     d = {
#     'A': {'X': 1, 'Y': 1.0, 'Z': 'abc'},
#     'B': [True, False, None, float('nan'), float('inf')]
#     }
#     with open('./test.json', 'w') as f:
#         json.dump(d, f, indent=2)

# outputJSON()

with open('./tempCommentList.json') as f:
    d = json.load(f)

print(d)