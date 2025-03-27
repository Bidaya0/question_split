import streamlit as st
from models.state import AppState
from ui.components import show_question, show_results

def main():
    st.title("在线答题系统")
    
    # 初始化应用状态
    app_state = AppState()
    
    # 选择学习模式
    if st.session_state.mode is None or (st.session_state.completed and not st.session_state.review_mode):
        st.subheader("请选择学习模式")
        mode = st.radio(
            "选择模式：",
            ["考试模拟模式", "背题模式"],
            help="考试模拟模式：随机抽取100道题进行模拟考试\n背题模式：持续随机抽取题目进行练习"
        )
        if st.button("开始学习"):
            st.session_state.mode = mode
            if mode == "考试模拟模式":
                st.session_state.initialize_exam_mode()
            else:
                st.session_state.initialize_practice_mode()
            st.rerun()
        return

    # 确保有题目可答
    if not st.session_state.questions:
        if st.session_state.mode == "考试模拟模式":
            st.session_state.initialize_exam_mode()
        else:
            st.session_state.initialize_practice_mode()
        st.rerun()

    # 在考试模拟模式或错题回放模式结束时显示结果
    if st.session_state.completed:
        show_results()
        return

    question = st.session_state.questions[st.session_state.current]
    
    # 只在考试模拟模式下显示进度条
    if st.session_state.mode == "考试模拟模式":
        progress = st.progress((st.session_state.current + 1) / len(st.session_state.questions))

    show_question(question, st.session_state.review_mode)

if __name__ == "__main__":
    main() 