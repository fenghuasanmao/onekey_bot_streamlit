import streamlit as st
import requests
from datetime import datetime

# CSS 样式
st.markdown(
    """
    <style>
    .title-font {
        font-size: 24px !important;
    }
    .stTextInput > div > div > input {
        width: 100% !important;
    }
    .content-font {
        font-size: 14px;
    }
    .submit-button-container {
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_response(user_input: str) -> str:
    SERVER_URL = 'http://142.171.63.201:5100/api/get_answer'
    data = {
        'question': user_input
    }
    try:
        response = requests.post(SERVER_URL, json=data, timeout=15)
        if response.status_code == 200:
            answer_data = response.json()
            answer = answer_data.get('answer', 'No answer provided by server.')
        else:
            answer = f'Server error, status code={response.status_code}.'
    except requests.exceptions.RequestException as e:
        answer = str(e)
    return answer

# 设置页面的标题，使用缩小后的字体大小
st.markdown('<h1 class="title-font">OneKey Bot测试页面</h1>', unsafe_allow_html=True)

# 初始化 session_state 中的问题列表和答案列表
if 'qa_pairs' not in st.session_state:
    st.session_state.qa_pairs = []

# 创建输入框
user_question = st.text_input('请输入你的问题', '')

# 创建提交按钮
submit_button = st.button('提交', key='submit_btn')

# 检查提交按钮是否被点击
if submit_button:
    if not user_question:
        st.write('请输入一个问题。')
    else:
        answer = get_response(user_question)
        qa_pair = {
            'question': user_question,
            'answer': answer,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        st.session_state.qa_pairs.append(qa_pair)
        # 清空输入框内容
        user_question = ""
        st.experimental_rerun()

# 提交按钮下方增加分割线
st.markdown('<div class="submit-button-container"></div>', unsafe_allow_html=True)
st.markdown('---')

# 显示所有问题和答案，按时间倒序显示
num_questions = len(st.session_state.qa_pairs)
for i, qa in enumerate(reversed(st.session_state.qa_pairs)):
    st.write(f"<div class='content-font'><b>时间 {qa['timestamp']}:</b><br/><b>问题 {num_questions - i}:</b> {qa['question']}<br/><b>回答 {num_questions - i}:</b> {qa['answer']}</div>", unsafe_allow_html=True)
    st.write("---")  # 分隔符
