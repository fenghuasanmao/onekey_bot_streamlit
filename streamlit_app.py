import streamlit as st
import requests


def get_response(user_input: str) -> str:
    SERVER_URL = 'http://142.171.63.201:5100/api/get_answer'
    data = {
        'question': user_input
    }
    try:
        # 发送 POST 请求到服务器
        # 请注意调整 timeout 参数以适应你的实际情况，
        # 这里为示例设置为 5 秒等待服务器响应
        response = requests.post(SERVER_URL, json=data, timeout=15)

        # 检查响应的状态码是否为 200（OK）
        if response.status_code == 200:
            # 解析返回的 JSON 数据
            answer_data = response.json()
            # 获取 'answer' 对应的值
            answer = answer_data.get('answer', 'No answer provided by server.')
        else:
            # 请求没有成功，返回错误状态码
            answer = f'Server error, status code={response.status_code}.'

    except requests.exceptions.RequestException as e:
        # 请求发生错误，例如连接问题
        answer = str(e)

    # 返回获取的答案或错误信息
    return answer


# 设置页面的标题
st.title('OneKey Bot测试页面')

# 创建一个文本输入框，用户可以在这里输入他们的问题
user_question = st.text_input('请输入你的问题')

# 创建一个按钮，当被点击时会处理问题
if st.button('提交'):
    # 当用户没有输入问题时给出提示
    if not user_question:
        st.write('请输入一个问题。')
    else:
        # 调用后台函数来获取问题的答案
        answer = get_response(user_question)
        # 在页面上显示答案
        st.write('回答:', answer)
