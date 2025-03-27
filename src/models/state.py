import streamlit as st
from models.question import QuestionBank
import random

class AppState:
    def __init__(self):
        self.initialize_state()

    def initialize_state(self):
        # 初始化题库
        if 'question_bank' not in st.session_state:
            st.session_state.question_bank = QuestionBank()

        # 初始化其他状态
        if 'current' not in st.session_state:
            st.session_state.current = 0
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
        if 'completed' not in st.session_state:
            st.session_state.completed = False
        if 'wrong_questions' not in st.session_state:
            st.session_state.wrong_questions = []
        if 'review_mode' not in st.session_state:
            st.session_state.review_mode = False
        if 'mode' not in st.session_state:
            st.session_state.mode = None
        if 'continuous_mode' not in st.session_state:
            st.session_state.continuous_mode = False
        if 'practice_answered_questions' not in st.session_state:
            st.session_state.practice_answered_questions = set()
        if 'questions' not in st.session_state:
            st.session_state.questions = []

    def clear_state(self):
        # 保存必要的状态
        question_bank = st.session_state.question_bank
        st.session_state.clear()
        st.session_state.question_bank = question_bank

    def initialize_exam_mode(self):
        question_bank = st.session_state.question_bank
        num_questions = min(100, len(question_bank.questions))
        st.session_state.questions = question_bank.get_random_questions(num_questions)
        st.session_state.continuous_mode = False
        st.session_state.mode = "考试模拟模式"
        st.session_state.current = 0
        st.session_state.show_answer = False
        st.session_state.completed = False
        st.session_state.review_mode = False
        st.session_state.answers = {}

    def initialize_practice_mode(self):
        question_bank = st.session_state.question_bank
        st.session_state.practice_answered_questions = set()
        st.session_state.questions = [random.choice(question_bank.questions)]
        st.session_state.continuous_mode = True
        st.session_state.completed = False
        st.session_state.show_answer = False
        st.session_state.current = 0
        st.session_state.mode = "背题模式"
        st.session_state.review_mode = False
        st.session_state.answers = {}

    def get_next_practice_question(self):
        question_bank = st.session_state.question_bank
        all_question_ids = {q.id for q in question_bank.questions}
        remaining_ids = all_question_ids - st.session_state.practice_answered_questions
        
        if not remaining_ids:
            st.session_state.practice_answered_questions = set()
            remaining_ids = all_question_ids
        
        next_id = random.choice(list(remaining_ids))
        return question_bank.get_question_by_id(next_id) 