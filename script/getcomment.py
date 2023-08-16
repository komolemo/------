import requests
import json
import datetime

URL = 'https://www.googleapis.com/youtube/v3/'
# ここにAPI KEYを入力
API_KEY = 'AIzaSyA_-0Nh2cknRWqaPvZcgs4d83zSeTDtsFY'
# ここにVideo IDを入力
# VIDEO_ID = 'C1G8aJY-RVs'

# テキスト保存用のファイル名の用意
dt_now = datetime.datetime.now()
filename = dt_now.strftime('%Y_%m_%d_%H%M')

# 一つの動画の全コメントを取得
def getComments(id):
    # コメント取得に関するパラメータの設定
    params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': id,
    'order': 'relevance',
    'textFormat': 'plaintext',
    'maxResults': 100,
    }
    # 全コメントデータの取得
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()
    commentDataList = resource['items']

    commentList = []
    for data in commentDataList:
        commentList += [getOneComment(data)]
    # 確認用
    print(commentList)
    return commentList

# 一つのコメントデータからテキストデータ（投稿されたコメント）を抽出
def getOneComment(data):
    return data['snippet']['topLevelComment']['snippet']['textDisplay']

#動画IDの取得
with open("../研究用アプリ/input/youtubeVideoIDs.txt","r", encoding='UTF-8') as f:
    idList = f.read().split("\n")

# コメント自体の保存
with open(f"./commentList_{filename}.txt", 'w') as f:
    f.truncate(0)

# 取得した動画IDの全動画のコメントの取得
allcommentLists = []
for id in idList:
    with open(f"./commentList_{filename}.txt", 'a', encoding='utf-8') as f:
        print("\n#\n#\n# ================================================================\n#\n#\n", file=f)
    # 全コメントの取得
    commentList = getComments(id)
    # コメント自体の保存
    with open(f"./commentList_{filename}.txt", 'a', encoding='utf-8') as f:
        print(commentList, file=f)
    allcommentLists += [commentList]

# 確認用
print(allcommentLists)

#JSONファイルに保存
with open('../研究用アプリ/data/tempCommentList.json', 'w') as f:
    json.dump(allcommentLists, f, indent=2)