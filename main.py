from revChatGPT.revChatGPT import Chatbot
import json, cv2
import pytesseract, nltk, re, np, random, os
from flask import Flask, request, jsonify, render_template




def answer(question):
    config = {
            "Authorization": "<Your Bearer Token Here>", # This is optional
            "session_token": "<your token here>" 
    }
    chatbot = Chatbot(config, conversation_id=None)
    chatbot.reset_chat() 
    chatbot.refresh_session() 
    resp = chatbot.get_chat_response(f"{question}") 
    return resp["message"]

tessdata_dir_config = r'--tessdata-dir "#path to tessdata folder"'
pytesseract.pytesseract.tesseract_cmd = r'#path to tesseract.exe'
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get/response', methods=['POST'])
def get_answers():
    file = request.files['file']
    print(file)
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    randomname = str(random.randint(100000, 999999))
    cv2.imwrite(f'questions/{randomname}.png', img)
    image = cv2.imread(f'questions/{randomname}.png')
    questions = pytesseract.image_to_string(image, config=tessdata_dir_config)
    r2 = answer(question=questions)
    os.remove(f'questions/{randomname}.png')
    # seperate the all the data into an array
    answers = []
    for i in r2.split('\n'):
        answers.append(i)
        
    
    return jsonify({'response': answers})


app.run(debug=True)