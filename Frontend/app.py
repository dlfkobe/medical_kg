from flask import Flask, request, jsonify
# 假设这是你的ChatBotGraph类的实例化
from chatbot_graph import ChatBotGraph

app = Flask(__name__)
app.static_folder = 'static'  # 默认静态文件夹名称
handler = ChatBotGraph()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    question = data['question']
    answer = handler.chat_main(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 在本地网络的0.0.0.0地址上运行