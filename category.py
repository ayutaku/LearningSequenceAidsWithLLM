"""
アクセスすると初めに表示されるトップページを構成するファイル
"""

import streamlit as st
from selection_problem import SelectionProblem
class Category:
    def __init__(self):
        # 初期ページの設定
        if 'page' not in st.session_state:
            st.session_state.page = 'main'

        self.show_page()

    # メインページ
    def main_page(self):

        st.title('プログラミング入門 - 1')
        st.write('プログラミングの基礎的な操作を自分が利用したい言語を選択して演習を解きながら学んでいきます。')
        st.markdown('## コース内容')

        courses = [
            {"course_id":1, "course_name": "構造化プログラムI", "content": "制御構造や文を組み合わせる構造化プログラミングの基礎を身につけます。"},
            {"course_id":2, "course_name": "配列", "content": "データの列を1つの変数として管理する配列を習得します。"},
            {"course_id":3, "course_name": "構造化プログラムII", "content": "繰り返し処理や配列を組み合わせることで、構造化プログラミングの理解を深めます。"},
        ]

        # 表の作成
        for course in courses:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{course['course_name']}** :")
                st.markdown(f"> {course['content']}")
            with col2:
                if st.button("次へ", key=course['course_name']):
                    st.session_state.page = 'selection_problem_home'
                    st.session_state.course_id = course['course_id']
                    st.experimental_rerun()

    def show_course(self):
        selection_problem = SelectionProblem()

    def show_page(self):
        # ページの表示
        if st.session_state.page == 'main':
            self.main_page()
        else:
            self.show_course()