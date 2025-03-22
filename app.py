import streamlit as st
import random
import json

# 从JSON文件加载题目
def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        raw_questions = json.load(f)

    # 转换数据格式
    formatted_questions = []
    for q in raw_questions:
        formatted = {
            "id": q["id"],
            "question": q["stem"],
            "answer": q["answer"],
            "explanation": q["explanation"] if q["explanation"] else "暂无解析",
            "options": {opt["option"]: opt["content"] for opt in q["options"]}
        }
        formatted_questions.append(formatted)
    return formatted_questions

def initialize_session():
    if 'questions' not in st.session_state:
        question_bank = load_questions()
        num_questions = min(100, len(question_bank))
        st.session_state.questions = random.sample(question_bank, num_questions)
        st.session_state.current = 0
        st.session_state.answers = {}
        st.session_state.show_answer = False
        st.session_state.completed = False

def show_results():
    st.subheader("答题结果")
    wrong_questions = [q["id"] for q in st.session_state.questions
                      if st.session_state.answers.get(q["id"]) is False]

    st.write(f"总题数: {len(st.session_state.questions)}")
    st.write(f"正确题数: {len(st.session_state.questions) - len(wrong_questions)}")
    st.write(f"错误题数: {len(wrong_questions)}")

    if wrong_questions:
        st.subheader("错题题号")
        st.write(", ".join(map(str, sorted(wrong_questions))))

    if st.button("重新开始"):
        st.session_state.clear()
        st.rerun()

def main():
    st.title("在线答题系统")
    initialize_session()

    if st.session_state.completed:
        show_results()
        return

    question = st.session_state.questions[st.session_state.current]
    progress = st.progress((st.session_state.current + 1) / len(st.session_state.questions))

    # 显示题目
    st.subheader(f"题目 {st.session_state.current + 1}/{len(st.session_state.questions)}")
    st.markdown(f"**{question['question']}**")

    # 显示选项
    user_answer = st.radio(
        "请选择答案：",
        options=list(question["options"].keys()),
        format_func=lambda x: f"{x}: {question['options'][x]}"
    )

    # 提交答案
    if st.button("提交答案") and not st.session_state.show_answer:
        st.session_state.answers[question["id"]] = (user_answer == question["answer"])
        st.session_state.show_answer = True

    # 显示答案解析
    if st.session_state.show_answer:
        st.markdown(f"**正确答案：** {question['answer']}")
        st.markdown(f"**解析：** {question['explanation']}")

        # 下一题按钮
        if st.session_state.current < len(st.session_state.questions) - 1:
            if st.button("下一题"):
                st.session_state.current += 1
                st.session_state.show_answer = False
                st.rerun()
        else:
            st.session_state.completed = True
            st.rerun()

if __name__ == "__main__":
    main()
