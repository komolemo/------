import itertools
import collections
import json
import MeCab
import pandas as pd

#stopwordsの指定
with open("../研究用アプリ/data/stopWordJp.txt","r", encoding='UTF-8') as f:
    stopwords1 = f.read().split("\n")
    # print(stopwords1)

stopwords2 = ["の","よう","/",".", "=","-","utm","_","&","._...","2022","cp","し","さ","せ","て","する","なる","いる","い","ん","やる","/?"]
stopwords = list(set(stopwords1+stopwords2))
# print(stopwords)

def tokenize_textArray(textArray):
    tokenizedTextArray = []
    for v in textArray:
        text = tokenize_text(v)
        tokenizedTextArray += [text]
    # print(tokenizedTextArray)
    return tokenizedTextArray

def tokenize_text(text):
    # MeCabで形態素解析を行い、名詞のみを取得する
    tagger = MeCab.Tagger('-Owakati -d "C:/Program Files (x86)/MeCab/dic/ipadic" -u "C:/Program Files (x86)/MeCab/dic/NEologd.dic"')
    tagger.parse('')
    node = tagger.parseToNode(text)

    #取り出す品詞を決めている.今回は名詞
    word_list=[]
    while node:
        word_type = node.feature.split(',')[0]
        #名詞の他にも動詞や形容詞なども追加できる
        if word_type in ["名詞"] or word_type in ["固有名詞"]: # or word_type in ["動詞"]
            word_list.append(node.surface)
        node=node.next
    # word_chain=' '.join(word_list)

    # stopwordsの除去
    word_list = [t for t in word_list if t  not in stopwords]
    # print(word_list)
    return word_list

# def CoOccurrence(textArray):
#     sentences = tokenize_textArray(textArray)

#     sentences_combs = [list(itertools.combinations(sentence,2)) for sentence in sentences]

#     words_combs = [[tuple(sorted(words)) for words in sentence] for sentence in sentences_combs]
#     target_combs = []
#     for words_comb in words_combs:
#         target_combs.extend(words_comb)
    
#     ct = collections.Counter(target_combs)

#     df = pd.DataFrame([{"1番目" : i[0][0], "2番目": i[0][1], "count":i[1]} for i in ct.most_common()])
#     return df.head(50)

def CoOccurrenceM(text):
    # sentences = tokenize_textArray(text)
    sentences = tokenize_text(text)
    # print(sentences)

    # sentences_combs = [list(itertools.combinations(sentence,2)) for sentence in sentences]
    sentences_combs = list(itertools.combinations(sentences,2))

    # words_combs = [[tuple(sorted(words)) for words in sentence] for sentence in sentences_combs]
    words_combs = tuple(sorted(sentences_combs)) 
    # print(words_combs)
    
    # target_combs = []
    # for words_comb in words_combs:
    #     target_combs.extend(words_comb)
    
    # ct = collections.Counter(target_combs)
    ct = collections.Counter(words_combs)
    frequencyNum = min(len(ct), 5)
    if frequencyNum > 0:
        v, c = zip(*ct.most_common(frequencyNum))
        # print(list(v))
        return v

def CoOccurrenceAll(textArray):
    combList = []
    for text in textArray:
        # print(text)
        if not CoOccurrenceM(text) == None:
            combList += CoOccurrenceM(text)
    print(combList)
    ct = collections.Counter(combList)
    df = pd.DataFrame([{"1番目" : i[0][0], "2番目": i[0][1], "count":i[1]} for i in ct.most_common()])
    # print(df.head(50))
    return df.head(50)

#入力
with open('../研究用アプリ/data/tempCommentList.json') as f:
    TextArrayList = json.load(f)

dfArray = []

for TextArray in TextArrayList:
    # print(TextArray)
    dfArray += [CoOccurrenceAll(TextArray)]

# すべての文章を連結して一つの大きな文章にする
combined_textArray = sum(TextArrayList, [])
print(len(list(combined_textArray)))
dfArray += [CoOccurrenceAll(combined_textArray)]

# print(combined_textArray)

# ================================================================
# 
# 共起ネットワーク図の作成
# 
# ================================================================

from pyvis.network import Network
import pandas as pd

def kyoki_word_network(df):
    got_net = Network(height="1000px", width="95%", bgcolor="#FFFFFF", font_color="black", notebook=True)

    got_net.force_atlas_2based()
    got_data = df[:150]

    sources = got_data['1番目']#count
    targets = got_data['2番目']#first
    weights = got_data['count']#second

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    for node in got_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    got_net.show_buttons(filter_=['physics'])
    return got_net

dfNo = 1
for df in dfArray:
    got_net = kyoki_word_network(df)
    got_net.show(f"../研究用アプリ/output/kyoki_{dfNo}.html")
    dfNo += 1