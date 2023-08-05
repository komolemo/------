# JSONファイルをテキストファイルに変換する
import json
with open('./tempCommentList.json') as f:
    textToReserve = json.load(f)

    # print(str(answer['text']))
with open('./tempCommentList.txt', "w", encoding='utf-8', newline='\n') as f:
    f.write(str(textToReserve))