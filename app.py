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

# 确保 question_bank 在会话开始时就被初始化
if 'question_bank' not in st.session_state:
    st.session_state.question_bank = load_questions()

def initialize_session():
    # 确保所有状态都已初始化
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

def initialize_exam_mode():
    question_bank = st.session_state.question_bank
    num_questions = min(100, len(question_bank))
    st.session_state.questions = random.sample(question_bank, num_questions)
    st.session_state.continuous_mode = False
    st.session_state.mode = "考试模拟模式"
    st.session_state.current = 0
    st.session_state.show_answer = False
    st.session_state.completed = False
    st.session_state.review_mode = False
    st.session_state.answers = {}

def initialize_practice_mode():
    # 初始化背题模式的状态
    st.session_state.practice_answered_questions = set()  # 记录已答过的题目ID
    st.session_state.questions = [random.choice(st.session_state.question_bank)]
    st.session_state.continuous_mode = True
    st.session_state.completed = False
    st.session_state.show_answer = False
    st.session_state.current = 0
    st.session_state.mode = "背题模式"
    st.session_state.review_mode = False
    st.session_state.answers = {}

def get_next_practice_question():
    # 获取下一道未答过的题目
    all_question_ids = {q["id"] for q in st.session_state.question_bank}
    remaining_ids = all_question_ids - st.session_state.practice_answered_questions
    
    if not remaining_ids:
        # 如果所有题目都答过了，重置已答题目集合
        st.session_state.practice_answered_questions = set()
        remaining_ids = all_question_ids
    
    # 随机选择一道未答过的题目
    next_id = random.choice(list(remaining_ids))
    return next(q for q in st.session_state.question_bank if q["id"] == next_id)

def show_results():
    st.subheader("答题结果")
    wrong_questions = [q["id"] for q in st.session_state.questions
                      if st.session_state.answers.get(q["id"]) is False]
    
    st.session_state.wrong_questions = wrong_questions

    st.write(f"总题数: {len(st.session_state.questions)}")
    st.write(f"正确题数: {len(st.session_state.questions) - len(wrong_questions)}")
    st.write(f"错误题数: {len(wrong_questions)}")

    if wrong_questions:
        st.subheader("错题题号")
        st.write(", ".join(map(str, sorted(wrong_questions))))
        
        if not st.session_state.review_mode:
            # 考试模拟模式结束后，显示错题回放按钮
            if st.button("错题回放"):
                # 保存当前的错题列表和question_bank
                current_wrong_questions = wrong_questions.copy()
                question_bank = st.session_state.question_bank
                current_mode = st.session_state.mode
                # 重置所有状态
                st.session_state.clear()
                # 恢复必要的状态
                st.session_state.question_bank = question_bank
                st.session_state.mode = current_mode
                # 重新设置错题回放模式的状态
                st.session_state.review_mode = True
                st.session_state.current = 0
                st.session_state.show_answer = False
                st.session_state.completed = False
                st.session_state.wrong_questions = current_wrong_questions
                # 设置错题列表
                st.session_state.questions = [q for q in st.session_state.question_bank 
                                           if q["id"] in current_wrong_questions]
                st.rerun()

    # 显示重新开始按钮
    if st.button("重新开始"):
        # 保存question_bank
        question_bank = st.session_state.question_bank
        st.session_state.clear()
        st.session_state.question_bank = question_bank
        st.rerun()

def show_question(question, is_review=False):
    st.subheader(f"题目 {st.session_state.current + 1}/{len(st.session_state.questions)}")
    if is_review:
        st.markdown("**错题回放模式**")
    elif st.session_state.continuous_mode:
        st.markdown("**背题模式**")
        # 添加退出和错题模式按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("退出背题模式"):
                # 保存question_bank
                question_bank = st.session_state.question_bank
                st.session_state.clear()
                st.session_state.question_bank = question_bank
                st.rerun()
        with col2:
            if len(st.session_state.wrong_questions) > 0 and st.button("进入错题模式"):
                # 保存当前的错题列表和question_bank
                current_wrong_questions = st.session_state.wrong_questions.copy()
                question_bank = st.session_state.question_bank
                current_mode = st.session_state.mode
                # 重置所有状态
                st.session_state.clear()
                # 恢复必要的状态
                st.session_state.question_bank = question_bank
                st.session_state.mode = current_mode
                # 重新设置错题回放模式的状态
                st.session_state.review_mode = True
                st.session_state.current = 0
                st.session_state.show_answer = False
                st.session_state.completed = False
                st.session_state.wrong_questions = current_wrong_questions
                # 设置错题列表
                st.session_state.questions = [q for q in st.session_state.question_bank 
                                           if q["id"] in current_wrong_questions]
                st.rerun()
    else:
        st.markdown("**考试模拟模式**")
    st.markdown(f"**{question['question']}**")

    user_answer = st.radio(
        "请选择答案：",
        options=list(question["options"].keys()),
        format_func=lambda x: f"{x}: {question['options'][x]}"
    )

    if st.button("提交答案") and not st.session_state.show_answer:
        is_correct = (user_answer == question["answer"])
        st.session_state.answers[question["id"]] = is_correct
        st.session_state.show_answer = True
        # 在背题模式下记录已答题目和错题
        if st.session_state.continuous_mode:
            st.session_state.practice_answered_questions.add(question["id"])
            if not is_correct:
                st.session_state.wrong_questions.append(question["id"])

    if st.session_state.show_answer:
        st.markdown(f"**正确答案：** {question['answer']}")
        st.markdown(f"**解析：** {question['explanation']}")

        if st.session_state.continuous_mode:
            # 背题模式：获取下一道题目
            next_question = get_next_practice_question()
            st.session_state.questions = [next_question]
            st.session_state.show_answer = False
            st.session_state.completed = False  # 确保背题模式下不会结束
            st.rerun()
        else:
            # 考试模拟模式或错题回放模式：显示下一题按钮
            if st.session_state.current < len(st.session_state.questions) - 1:
                if st.button("下一题"):
                    st.session_state.current += 1
                    st.session_state.show_answer = False
                    st.rerun()
            else:
                # 错题回放模式或考试模拟模式结束，显示结果
                st.session_state.completed = True
                st.session_state.show_answer = False  # 重置显示答案状态
                st.rerun()

def main():
    st.title("在线答题系统")
    
    # 确保所有状态都已初始化
    initialize_session()
    
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
                initialize_exam_mode()
            else:
                initialize_practice_mode()
            st.rerun()
        return

    # 确保有题目可答
    if not st.session_state.questions:
        if st.session_state.mode == "考试模拟模式":
            initialize_exam_mode()
        else:
            initialize_practice_mode()
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
