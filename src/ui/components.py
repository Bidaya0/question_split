import streamlit as st
from models.state import AppState

def show_question(question, is_review=False):
    st.subheader(f"题目 {st.session_state.current + 1}/{len(st.session_state.questions)}")
    if is_review:
        st.markdown("**错题回放模式**")
    elif st.session_state.continuous_mode:
        st.markdown("**背题模式**")
        show_practice_mode_buttons()
    else:
        st.markdown("**考试模拟模式**")
    st.markdown(f"**{question.question}**")

    user_answer = st.radio(
        "请选择答案：",
        options=list(question.options.keys()),
        format_func=lambda x: f"{x}: {question.options[x]}"
    )

    if st.button("提交答案") and not st.session_state.show_answer:
        handle_answer_submission(question, user_answer)

    if st.session_state.show_answer:
        show_answer_and_explanation(question)

def show_practice_mode_buttons():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("退出背题模式"):
            st.session_state.clear_state()
            st.rerun()
    with col2:
        if len(st.session_state.wrong_questions) > 0 and st.button("进入错题模式"):
            enter_review_mode()

def show_answer_and_explanation(question):
    st.markdown(f"**正确答案：** {question.answer}")
    st.markdown(f"**解析：** {question.explanation}")

    if st.session_state.continuous_mode:
        handle_practice_mode_next()
    else:
        handle_exam_mode_next()

def show_results():
    st.subheader("答题结果")
    wrong_questions = [q.id for q in st.session_state.questions
                      if st.session_state.answers.get(q.id) is False]
    
    st.session_state.wrong_questions = wrong_questions

    st.write(f"总题数: {len(st.session_state.questions)}")
    st.write(f"正确题数: {len(st.session_state.questions) - len(wrong_questions)}")
    st.write(f"错误题数: {len(wrong_questions)}")

    if wrong_questions:
        st.subheader("错题题号")
        st.write(", ".join(map(str, sorted(wrong_questions))))
        
        if not st.session_state.review_mode:
            if st.button("错题回放"):
                enter_review_mode()

    if st.button("重新开始"):
        st.session_state.clear_state()
        st.rerun()

def handle_answer_submission(question, user_answer):
    is_correct = (user_answer == question.answer)
    st.session_state.answers[question.id] = is_correct
    st.session_state.show_answer = True
    if st.session_state.continuous_mode:
        st.session_state.practice_answered_questions.add(question.id)
        if not is_correct:
            st.session_state.wrong_questions.append(question.id)

def handle_practice_mode_next():
    next_question = st.session_state.get_next_practice_question()
    st.session_state.questions = [next_question]
    st.session_state.show_answer = False
    st.session_state.completed = False
    st.rerun()

def handle_exam_mode_next():
    if st.session_state.current < len(st.session_state.questions) - 1:
        if st.button("下一题"):
            st.session_state.current += 1
            st.session_state.show_answer = False
            st.rerun()
    else:
        st.session_state.completed = True
        st.session_state.show_answer = False
        st.rerun()

def enter_review_mode():
    current_wrong_questions = st.session_state.wrong_questions.copy()
    question_bank = st.session_state.question_bank
    current_mode = st.session_state.mode
    st.session_state.clear_state()
    st.session_state.question_bank = question_bank
    st.session_state.mode = current_mode
    st.session_state.review_mode = True
    st.session_state.current = 0
    st.session_state.show_answer = False
    st.session_state.completed = False
    st.session_state.wrong_questions = current_wrong_questions
    st.session_state.questions = question_bank.get_questions_by_ids(current_wrong_questions)
    st.rerun() 