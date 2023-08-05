# JSONファイルをテキストファイルに変換する
# import json
# import csv
# with open('./tempCommentList.json') as f:
#     textToReserve = json.load(f)

import json
import csv

def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # ヘッダーを記述する場合は以下の行を追加
        # writer.writerow(["Column1", "Column2", ...])
        
        for item in data:
            writer.writerow([item])

# JSONファイルとCSVファイルのパスを指定して変換を実行
json_file_path = './tempCommentList.json'
csv_file_path = './tempCommentList.csv'
json_to_csv(json_file_path, csv_file_path)