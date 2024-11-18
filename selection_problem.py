"""
トップページから遷移するコース内の問題選択画面
"""

import streamlit as st
from problem import Problem
import time

class SelectionProblem:
    # 問題のデータ
    course1_problems = [
        {"id": 1, "name": "Print a Rectangle"},
        {"id": 2, "name": "Print a Frame"},
        {"id": 3, "name": "Print a Chessboard"},
        {"id": 4, "name": "Structured Programming"}
    ]
    course2_problems = [
        {"id": 1, "name": "Reversing Numbers"},
        {"id": 2, "name": "Finding Missing Cards"},
        {"id": 3, "name": "Official House"},
        {"id": 4, "name": "Matrix Vector Multiplication"}
    ]
    course3_problems = [
        {"id": 1, "name": "Grading"},
        {"id": 2, "name": "How many ways?"},
        {"id": 3, "name": "Spreadsheet"},
        {"id": 4, "name": "Matrix Multiplication"}
    ]

    def __init__(self):
        # セッション状態を初期化
        if 'page' not in st.session_state:
            st.session_state.page = 'selection_problem_home'
        if st.session_state.course_id == 1:
            self.problems = self.course1_problems
        elif st.session_state.course_id == 2:
            self.problems = self.course2_problems
        elif st.session_state.course_id == 3:
            self.problems = self.course3_problems
        else:
            st.markdown("# エラーが発生しました!!")
            st.markdown("5秒後にトップページへ遷移します")
            time.sleep(5)
            st.session_state.page = "main"
            st.experimental_rerun()
        self.show_page()

    def show_home(self):
        if st.button('戻る'):
            st.session_state.page = "main"
            st.experimental_rerun()
        
        st.title("問題リスト")
        # 表の作成
        for problem in self.problems:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**Q{problem['id']}: {problem['name']}**")
            with col2:
                if st.button("解く", key=problem['id']):
                    st.session_state.page = 'question'
                    st.session_state.question_id = problem['id']
                    st.experimental_rerun()

    def show_question(self):
        problem = Problem()

    def show_page(self):
        if st.session_state.page == 'selection_problem_home':
            self.show_home()
        elif st.session_state.page == 'question':
            self.show_question()