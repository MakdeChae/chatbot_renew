# -*- coding: utf-8 -*-
import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
# from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

VALID_USERNAME = os.getenv("ADMIN_ID")
VALID_PASSWORD = os.getenv("ADMIN_PW")

googlekey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=googlekey)

# mykey = os.getenv("OPENAI_API_KEY")
# def get_chatgpt_response(filtered_msg):

#     client = OpenAI(api_key=mykey)  # Replace with your actual API key

#     messages = [
#         {"role": "system", "content": "대화하듯 말해, 내가 물어보는것 중에 모르면 구글 검색해줘"},
#         {"role": "user", "content": filtered_msg}
#     ]

#     try:
#         chat_completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             max_tokens=500
#         )

#         return chat_completion.choices[0].message.content

#     except Exception as e:
#         return filtered_msg
# @app.route('/get_kakao_response_old', methods=['POST'])
# def get_response_old():
#     data = request.get_json()
#     if not data:
#         return jsonify({'response': '유효하지 않은 요청입니다.'})

#     room = data.get('room', 'Unknown')
#     msg = data.get('msg', 'No message provided')
#     sender = data.get('sender', 'Unknown sender')
#     is_group_chat = data.get('isGroupChat', False)
#     replier = data.get('replier', 'Unknown replier')
#     image_db = data.get('imageDB', 'No image data')
#     package_name = data.get('packageName', 'Unknown package')

#     if "@딥챗봇" in msg:
#         filtered_msg = msg.replace("@딥챗봇", "").strip()
#         filtered_msg = filtered_msg.replace("[나를 멘션]", "").strip()
#         chatgpt_response = get_chatgpt_response(filtered_msg)

#         response_message = chatgpt_response
#         return jsonify({'response': response_message})

#     response_message = ""
#     return jsonify({'response': response_message})

def get_gemini_response(user_id, filtered_msg):
    """Google Gemini API를 사용하여 응답을 생성하는 함수"""
    try:
        generation_config = {
            "temperature": 0.9,          # 응답의 창의성 (높을수록 창의적, 낮을수록 보수적)
            "top_p": 1,                  # Nucleus Sampling (1이면 무제한)
            "top_k": 1,                  # 상위 K개의 후보만 고려 (1이면 가장 확률 높은 토큰 선택)
            "max_output_tokens": 2048,    # 최대 응답 길이 (최대 1024 토큰)
            }
            
        model = genai.GenerativeModel("gemini-1.5-flash",generation_config=generation_config)

        response = model.generate_content(filtered_msg)
        
        if response and hasattr(response, "text"):
            response_message = response.text
        else:
            response_message = "현재 Gemini 이용 불가합니다."

        return response_message

    except Exception as e:
        return f"Gemini API 오류 발생: {str(e)}"
    
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session['user'] = username
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/get_kakao_response', methods=['POST'])
def get_response():
    """Handles incoming chatbot messages and forwards them to Gemini API."""
    data = request.get_json()
    # print(data)
    if not data:
        return jsonify({'response': '유효하지 않은 요청입니다.'})

    user_id = data.get('sender', 'Unknown sender')
    msg = data.get('msg', 'No message provided')

    if "@딥챗봇" in msg:
        filtered_msg = msg.replace("@딥챗봇", "").strip()
        filtered_msg = filtered_msg.replace("[나를 멘션]", "").strip()
        gemini_response = get_gemini_response(user_id, filtered_msg)
        return jsonify({'response': gemini_response})

    return jsonify({'response': ''})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
