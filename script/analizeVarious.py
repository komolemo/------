import json
from collections import Counter
import MeCab

with open('../研究用アプリ/tempCommentList.json') as f:
    textArray = json.load(f)

# import MeCab
# from collections import Counter

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
        if word_type in ["名詞"]:
            word_list.append(node.surface)
        node=node.next
    # word_chain=' '.join(word_list)

    print(word_list)
    return word_list

def extract_most_common_nouns(documents, num_words=10):
    # すべての文章を連結して一つの大きな文章にする
    combined_text = " ".join(documents)
    
    # 形態素解析して名詞の単語に分割する
    nouns = tokenize_text(combined_text)
    
    # 単語の出現回数をカウントする
    word_counts = Counter(nouns)
    
    # 出現回数の多い順に上位 num_words 個の単語を抽出
    most_common_nouns = word_counts.most_common(num_words)
    
    return most_common_nouns

# テスト用の文章群
documents = textArray
# [
#     "これはサンプル文章です。",
#     "これは別のサンプル文章です。",
#     "文章群を使って単語の出現回数を抽出します。サンプル文章には重複する単語が含まれています。"
# ]

# 最も出現回数の多い名詞を10個抽出
most_common_nouns = extract_most_common_nouns(documents, num_words=10)

# 結果を表示
for noun, count in most_common_nouns:
    print(f"{noun}: {count}回")
