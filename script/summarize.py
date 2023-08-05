# import os
# import openai

# # APIキーの設定
# openai.api_key = os.environ["OPENAI_API_KEY"]

# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": "大谷翔平について教えて"},
#     ],
# )
# print(response.choices[0]["message"]["content"].strip())

import os
os.environ["OPENAI_API_KEY"] = "OpenAIのAPIコード"

import json

from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain import LLMChain

import datetime
 
# 言語モデルとしてOpenAIのモデルを指定
llm = OpenAI(model_name="gpt-3.5-turbo", max_tokens=1024)
 
# プロンプトのテンプレートを作成
typologizeTemplate = "次の文章群を内容によって分類し、分類ごとにその内容を述べよ {original_sentences}" #次の配列について、内容によって分類し、内容ごとにその概略を述べよ
 
# プロンプトのテンプレート内にある要約前のテキストを変数として設定pip show pipenv
typologizePrompt = PromptTemplate(
    input_variables=["original_sentences"],
    template=typologizeTemplate,
)

# プロンプトを実行させるチェーンを設定
typologize = LLMChain(llm=llm, prompt=typologizePrompt,verbose=True)
 
# チェーンの実行および結果の表示
with open('../研究用アプリ/data/tempCommentList.json') as f:
    textArrayList = json.load(f)

answerList = []
i = 0

dt_now = datetime.datetime.now()
filename = dt_now.strftime('%Y_%m_%d_%H%M')
print(filename)

with open(f"./answer_{filename}.txt", 'w') as f:
    f.truncate(0)

for textArray in textArrayList:
    if not i == 6 and not i == 7:
        # print(textArray)
        answer = typologize(textArray)['text']
        # answerList += [answer]
        with open(f"./answer_{filename}.txt", 'a', encoding='utf-8') as f:
            print(answer, file=f)
        print(answer)
    i += 1
    if i > len(textArrayList) - 1:
        break

# print(answerList)

# print(str(answer['text']))
# with open('answer.txt', "w", encoding='utf-8', newline='\n') as f:
#     f.write(str(answer['text']))