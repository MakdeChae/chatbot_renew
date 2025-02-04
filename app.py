# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

googlekey = os.getenv("GOOGLE_API_KEY")
mykey = os.getenv("OPENAI_API_KEY")

genai.configure(api_key=googlekey)

# Store conversation history for each user
# conversation_history = {}

def get_chatgpt_response(filtered_msg):
    # Initialize the OpenAI client
    client = OpenAI(api_key=mykey)  # Replace with your actual API key

    # Create messages list with system and user prompts
    messages = [
        {"role": "system", "content": "대화하듯 말해, 내가 물어보는것 중에 모르면 구글 검색해줘"},
        {"role": "user", "content": filtered_msg}
    ]

    try:
        # Generate response from ChatGPT
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500
        )

        # Return only the text of the response
        return chat_completion.choices[0].message.content

    except Exception as e:
        # Handle any exceptions (like network issues) by returning a custom message
        return filtered_msg


def get_gemini_response(user_id, filtered_msg):
    """Google Gemini API를 사용하여 응답을 생성하는 함수"""
    try:
        # 유저의 대화 기록이 없으면 초기화
        # if user_id not in conversation_history:
        #     conversation_history[user_id] = [
        #         {"role": "system", "content": "대화하듯 말해, 내가 물어보는것 중에 모르면 구글 검색해줘"}
        #     ]

        # 유저의 메시지를 대화 기록에 추가
        # conversation_history[user_id].append({"role": "user", "content": filtered_msg})

        # 대화 내용을 하나의 문자열로 변환
        # conversation_text = "\n".join([msg["content"] for msg in conversation_history[user_id]])

        generation_config = {
            "temperature": 0.9,          # 응답의 창의성 (높을수록 창의적, 낮을수록 보수적)
            "top_p": 1,                  # Nucleus Sampling (1이면 무제한)
            "top_k": 1,                  # 상위 K개의 후보만 고려 (1이면 가장 확률 높은 토큰 선택)
            "max_output_tokens": 2048,    # 최대 응답 길이 (최대 1024 토큰)
            }
            
        model = genai.GenerativeModel("gemini-1.5-flash",generation_config=generation_config)
        # ✅ 응답 생성 (generate_content 사용)
        response = model.generate_content(filtered_msg)

        # ✅ 응답을 JSON 직렬화가 가능한 문자열로 변환
        if response and hasattr(response, "text"):
            response_message = response.text
        else:
            response_message = "현재 Gemini 이용 불가합니다."

        # # Gemini의 응답을 대화 기록에 저장
        # conversation_history[user_id].append({"role": "assistant", "content": response_message})

        return response_message

    except Exception as e:
        return f"Gemini API 오류 발생: {str(e)}"
    

@app.route('/')
def index():
    # uploads 폴더에 저장된 파일 목록을 가져와 렌더링
    return render_template('index.html')

@app.route('/get_kakao_response_old', methods=['POST'])
def get_response_old():
    # 클라이언트에서 보내온 데이터 가져오기
    data = request.get_json()
    if not data:
        return jsonify({'response': '유효하지 않은 요청입니다.'})

    # Extract parameters
    room = data.get('room', 'Unknown')
    msg = data.get('msg', 'No message provided')
    sender = data.get('sender', 'Unknown sender')
    is_group_chat = data.get('isGroupChat', False)
    replier = data.get('replier', 'Unknown replier')
    image_db = data.get('imageDB', 'No image data')
    package_name = data.get('packageName', 'Unknown package')

    # Get ChatGPT response using the filtered message
    if "@딥챗봇" in msg:
        filtered_msg = msg.replace("@딥챗봇", "").strip()
        filtered_msg = filtered_msg.replace("[나를 멘션]", "").strip()
        chatgpt_response = get_chatgpt_response(filtered_msg)

        # Use the response correctly
        response_message = chatgpt_response
        return jsonify({'response': response_message})

    # If no valid message, return an empty response
    response_message = ""
    return jsonify({'response': response_message})



@app.route('/get_kakao_response', methods=['POST'])
def get_response():
    """Handles incoming chatbot messages and forwards them to Gemini API."""
    data = request.get_json()
    # print(data)
    if not data:
        return jsonify({'response': '유효하지 않은 요청입니다.'})

    user_id = data.get('sender', 'Unknown sender')
    msg = data.get('msg', 'No message provided')

    # Check if the bot is mentioned in the message
    if "@딥챗봇" in msg:
        filtered_msg = msg.replace("@딥챗봇", "").strip()
        filtered_msg = filtered_msg.replace("[나를 멘션]", "").strip()
        gemini_response = get_gemini_response(user_id, filtered_msg)
        return jsonify({'response': gemini_response})

    return jsonify({'response': ''})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
