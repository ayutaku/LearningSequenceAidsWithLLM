import streamlit as st
import streamlit as st
from dotenv import load_dotenv

import langchain
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents.base import Document
from langchain.chains.combine_documents.stuff import (
    create_stuff_documents_chain,
)
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables.base import RunnableSequence

def create_stuff_chain() -> RunnableSequence:
    prompt = ChatPromptTemplate.from_template(
        "以下のpython初心者が書いたpythonプログラムであるprogramの間違いを指摘してください。"
        #"間違いがあった場合はその間違いを練習できる問題を考えて答えと共に教えてください。"
        "間違いがない場合は「正解です!」と出力してください。"
        "program:{context}"
    )
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    stuff_chain = create_stuff_documents_chain(llm, prompt)
    return stuff_chain


load_dotenv(override=True)
if "stuff_chain" not in st.session_state:  # stuffチェインの初期化
    st.session_state.stuff_chain = create_stuff_chain()
#問題の設定
st.title('問題')
st.write('与えられた長方形の面積と周囲長を計算するプログラムを作成してください')
st.header('入力')
st.write('長方形の横の長さaと縦の長さbは、単一のスペースで区切られた行に指定されます。')
st.subheader('Sample Input 1')
st.write('3 5')
st.header('出力')
st.write('長方形の面積と周囲の長さをスペース区切りで出力してください')
st.subheader('Sample Output 1')
st.write('15 16')
st.header('制約')
st.write('1 ≤ a, b ≤ 100')




# タイトルの設定
st.title('コード入力フォーム')


# コード入力エリア
code_input = st.text_area("コードをここに入力してください", height=300)

# コードを表示
if st.button('Submit'):
    st.write('入力されたコード:')
    st.code(code_input)
    tmp_result = st.session_state.stuff_chain.invoke({"context": [Document(code_input)]})
    st.markdown(tmp_result)