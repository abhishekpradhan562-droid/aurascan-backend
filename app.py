import requests
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

API_KEY = 'AIzaSyCLQpJw5KzKAAXE6vDvCW4OOoC7YB3yTvU'
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers.add("Access-Control-Allow-Origin", "*")
        res.headers.add("Access-Control-Allow-Headers", "*")
        res.headers.add("Access-Control-Allow-Methods", "*")
        return res

    try:
        
        data = request.get_json(silent=True) or {}
        text = data.get('text', 'No text provided')
        action = data.get('action', 'summarize')
        question = data.get('question', 'Explain this')

        
        prompts = {
            'summarize': f"Give me 3 short bullets about this: {text}",
            'explain_words': f"Define 3 hard words from this text in 'Word - Definition' format. No stars. Text: {text}",
            'ask_doubt': f"Context: {text}\nQuestion: {question}\nAnswer in 3-4 lines max."
        }

        
        final_prompt = prompts.get(action, f"Tell me about: {text}")

        
        payload = {"contents": [{"parts": [{"text": final_prompt}]}]}
        r = requests.post(API_URL, json=payload, timeout=15)
        
        
        if r.status_code == 200:
            result = r.json()
            output = result['candidates'][0]['content']['parts'][0]['text']
            
            resp = jsonify({"output": output})
            resp.headers.add("Access-Control-Allow-Origin", "*")
            return resp
        else:
            return jsonify({"output": f"Google Error: {r.status_code}"}), 400

    except Exception as e:
        print(f"CRASH ERROR: {str(e)}") # This shows the real error in your CMD
        return jsonify({"output": f"Internal Error: {str(e)}"}), 500           
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=False)
