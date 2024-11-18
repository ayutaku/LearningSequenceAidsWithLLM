"""
コースごとの問題一覧から遷移する問題回答画面
"""

import streamlit as st
from operator import itemgetter
from dotenv import load_dotenv
import time

import langchain
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents.base import Document
from langchain.chains.combine_documents.stuff import (
    create_stuff_documents_chain,
)
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from pathlib import Path
from multimetricprog import calculator

class Problem:
    def __init__(self):
        self.main()

    def create_stuff_chain(self, generated_code) -> RunnableSequence:
        json_calculation = calculator.calculate(generated_code)

        base_cyclomatic_complexity = json_calculation["files"]["fp.py"]["cyclomatic_complexity"]
        base_halstead_difficulty = json_calculation["files"]["fp.py"]["halstead_difficulty"]

        # 生成されたコードと複雑度の表示。将来評価する際に利用可能
        # st.write(generated_code)
        # st.write(base_cyclomatic_complexity)
        # st.write(base_halstead_difficulty)

        prompt = ChatPromptTemplate.from_template(

            f"""
            問題文と、初心者が書いたプログラムは以下に示されています。そのプログラムが正解か不正解かを判定し、以下のタスクを行ってください。
            ・正解の場合は正解と表示してください。
            ・不正解の場合は以下の二つのタスクを実行してください。
                1.プログラムの間違いを答えは出さずに指摘してください。
                2.間違いを指摘した後、答えのプログラムのcyclomatic_complexityとhalstead_difficultyのスコアが1/2になるような問題文を出してください。ここで、cyclomatic_complexityおよびhalstead_difficultyは、"https://github.com/priv-kweihmann/multimetric"に示されるmultimetricにより計算されるため、計算方法を参照してください。現在のスコアは、cyclomatic_complexity={base_cyclomatic_complexity},halstead_difficulty={base_halstead_difficulty}です。

            
            """
            # "以下のpython初心者が書いたpythonプログラムであるprogramの間違いを指摘してください。"
            # #"間違いがあった場合はその間違いを練習できる問題を考えて答えと共に教えてください。"
            # "間違いがない場合は「正解です!」と出力してください。"
            # cyclomatic_complexityとは、ソフトウェア品質を測定するソフトウェアコードメトリクスのひとつで、プログラムの複雑度を測定するものです。線形的に独立な経路の数を数値化するもので、例えば、ソースコード内に条件が1つのif文のような決定論理が1つある場合、if文が真の場合とif文が偽の場合があり、線形的に独立したパスは2つとなります。
            #問題文:{quiz}
            "プログラム:{context}"
        )
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        stuff_chain = create_stuff_documents_chain(llm, prompt)
        return stuff_chain

    # def create_gen_ans_chain(self) -> RunnableSequence:
    #     gen_ans_prompt = ChatPromptTemplate.from_template(
    #         "以下のマークダウン形式で示されるプログラミングの問題についてPythonを用いて回答を教えてください。なお、ソースコードのみを答えてください\n"
    #         "#問題 :\n{problem}"
    #     )
    #     gen_basis_chain = ( #正答生成用chain
    #         {"action":itemgetter("problem")}
    #         | gen_ans_prompt
    #         | ChatOpenAI(model_name="gpt-4o", temperature=0)
    #         | StrOutputParser()
    #     )
    #     return gen_basis_chain

    def create_gen_ans_chain(self, problem_sentence) -> RunnableSequence:
        gen_ans_prompt = ChatPromptTemplate.from_template(
            f"以下のマークダウン形式で示されるプログラミングの問題についてPythonを用いて回答を教えてください。なお、ソースコードのみを答えてください\n{problem_sentence}"
            "プログラム:{context}"
        )

        llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        stuff_chain = create_stuff_documents_chain(llm, gen_ans_prompt)

        return stuff_chain

    def main(self):
        load_dotenv(override=True)
        if "stuff_chain" not in st.session_state:  # stuffチェインの初期化
            #正解用のコードを生成
            problem_sentence = self.get_question()
            generated_code = self.create_gen_ans_chain(problem_sentence).invoke({"context": [Document(problem_sentence)]})
            # stuffチェインの初期化
            st.session_state.stuff_chain = self.create_stuff_chain(generated_code)

        if st.button('戻る'):
            st.session_state.page = "selection_problem_home"
            st.experimental_rerun()
        
        page_content = self.get_question() #初回の問題表示
        st.markdown(page_content)

        st.title('コード入力フォーム') #タイトルの設定
        code_input = st.text_area("コードをここに入力してください", height=300) #コード入力エリア
        # コードを表示
        if st.button('Submit'):
            st.write('入力されたコード:')
            st.code(code_input)
            tmp_result = st.session_state.stuff_chain.invoke({"context": [Document(code_input)]})
            if tmp_result == "正解です。": #問題が正解した場合(現時点ではこの方法で判断していますが, より包括的な判断方法が必要だと思われます)
                st.markdown(tmp_result)
                st.session_state.next_problem = None #次に表示するべき問題を初期化する
            else: #問題に不正解であった場合
                st.markdown("## 不正解でした! 次の問題に移行します。\n  (現在は全ての問題が不正解に判定されます)")
                st.session_state.next_problem = tmp_result
                if st.button('OK'):
                    st.rerun()

    def get_question(self):
        if "next_problem" not in st.session_state or st.session_state.next_problem == None: #初回回答時
            course_id = st.session_state.course_id
            question_id = st.session_state.question_id
            parent = Path(__file__).resolve().parent #problem.pyの親ディレクトリの絶対パスを取得
            with open(f"{parent}/DB/course{course_id}/{question_id}.md", mode="r") as f:
                page_content = f.read()
                return page_content
        else: #2回目以降回答時
            return st.session_state.next_problem
        
    def display_code_input(self, count): #回答フォームの表示を行う関数(不正解の限りループさせる)
        st.title('コード入力フォーム') #タイトルの設定
        code_input = st.text_area("コードをここに入力してください", height=300, key=f"text_{count}") #コード入力エリア
        # コードを表示
        if st.button('Submit', key=f"submit_{count}"):
            st.write('入力されたコード:')
            st.code(code_input)
            tmp_result = st.session_state.stuff_chain.invoke({"context": [Document(code_input)]})
            st.markdown(tmp_result)
            return "incorrect"