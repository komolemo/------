import requests
import json
import datetime

URL = 'https://www.googleapis.com/youtube/v3/'
# ここにAPI KEYを入力
API_KEY = 'YouTube Data API v3のAPIキー'
# ここにVideo IDを入力
# VIDEO_ID = 'C1G8aJY-RVs'

commentList = []
commentListArray = []
dt_now = datetime.datetime.now()
filename = dt_now.strftime('%Y_%m_%d_%H%M')

def print_video_comment(no, video_id, next_page_token):
  global commentList

  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'order': 'relevance',
    'textFormat': 'plaintext',
    'maxResults': 100,
  }
  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'commentThreads', params=params)
  resource = response.json()

  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
    # 返信数
    reply_cnt = comment_info['snippet']['totalReplyCount']
    # ユーザー名
    user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
    # Id
    parentId = comment_info['snippet']['topLevelComment']['id']

    commentDataTxt = '{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name, reply_cnt)
    # print(commentDataTxt)
    # テキストファイルにコメントを格納
    with open(f"./commentList_{filename}.txt", 'a', encoding='utf-8') as f:
      print(commentDataTxt, file=f)
    # JSONファイルに格納するように加工
    commentList += [text.replace('\r', '\n').replace('\n', ' ')]
    if reply_cnt > 0:
      cno = 1
      print_video_reply(no, cno, video_id, None, parentId)
    no = no + 1

  if 'nextPageToken' in resource:
    print_video_comment(no, video_id, resource["nextPageToken"])

def print_video_reply(no, cno, video_id, next_page_token, id):
    global commentList
  
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plaintext',
        'maxResults': 50,
        'parentId': id,
    }

    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'comments', params=params)
    resource = response.json()

    for comment_info in resource['items']:
        # コメント
        text = comment_info['snippet']['textDisplay']
        # グッド数
        like_cnt = comment_info['snippet']['likeCount']
        # ユーザー名
        user_name = comment_info['snippet']['authorDisplayName']

    commentDataTxt = '{:0=4}-{:0=3}\t{}\t{}\t{}'.format(no, cno, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name)
    # print(commentDataTxt)
    # テキストファイルにコメントを格納
    with open(f"./commentList_{filename}.txt", 'a', encoding='utf-8') as f:
      print(commentDataTxt, file=f)
    # JSONファイルに格納するように加工
    commentList += [text.replace('\r', '\n').replace('\n', ' ')]
    cno = cno + 1

    if 'nextPageToken' in resource:
        print_video_reply(no, cno, video_id, resource["nextPageToken"], id)

#URLの取得
with open("../研究用アプリ/input/youtubeVideoIDs.txt","r", encoding='UTF-8') as f:
    idList = f.read().split("\n")

with open(f"./commentList_{filename}.txt", 'w') as f:
    f.truncate(0)

for videoId in idList:
  # コメントを全取得する
  # テキストファイルにコメントを格納
  with open(f"./commentList_{filename}.txt", 'a', encoding='utf-8') as f:
    print("\n#\n#\n# ================================================================\n#\n#\n", file=f)
  commentList = []
  no = 1
  print_video_comment(no, videoId, None)
  commentListArray += [commentList]

# print(commentListArray)
# print(len(commentListArray))

#JSONファイルに保存
with open('../研究用アプリ/data/tempCommentList.json', 'w') as f:
    json.dump(commentListArray, f, indent=2)

# with open('../研究用アプリ/data/tempCommentList.txt', 'w') as f:
#     f.write(commentListArray)