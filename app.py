# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os
from urllib.parse import unquote
import openai
from dotenv import load_dotenv

PORT = 8000
sessions = {}  # IP-based simple session store

# ---- Dummy LLM function (replace with real OpenAI call later) ----
# def dummy_llm_answer(question):
#     return f"[LLM Response to]: {question}"
import openai
import os
load_dotenv()
# Use your OpenAI API key from environment
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def real_llm_answer(question):
    try:
        print("🔮 Calling OpenAI LLM...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error from OpenAI]: {str(e)}"

class MyHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_file(self, filepath, content_type="text/html"):
        if not os.path.exists(filepath):
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def get_session_id(self):
        ip = self.client_address[0]
        ua = self.headers.get("User-Agent", "")
        return f"{ip}-{ua}"

    def do_GET(self):
        path = unquote(self.path)
        if path == "/" or path == "/index.html":
            self._send_file("static/index.html")
        elif path == "/about.html":
            self._send_file("static/about.html")
        elif path == "/history":
            sid = self.get_session_id()
            self._send_json({"history": sessions.get(sid, [])})
        elif path.startswith("/static/"):
            ext = path.split(".")[-1]
            types = {"css": "text/css", "js": "application/javascript", "html": "text/html"}
            self._send_file(path.lstrip("/"), types.get(ext, "text/plain"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/ask":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            print("🔍 Received POST body:", body.decode("utf-8"))  # ADD THIS
            try:
                data = json.loads(body.decode("utf-8"))
                question = data.get("question", "").strip()
                if not question:
                    raise ValueError("No question provided.")
                answer = real_llm_answer(question)  # USE THE CORRECT FUNCTION HERE
                sid = self.get_session_id()
                sessions.setdefault(sid, []).append({"question": question, "answer": answer})
                self._send_json({"answer": answer})
            except Exception as e:
                print("❌ Error:", str(e))
                self._send_json({"error": str(e)}, 400)
        else:
            self.send_error(404, "POST route not found")



if __name__ == '__main__':
    print(f"🚀 Running on http://localhost:{PORT}")
    with HTTPServer(("", PORT), MyHandler) as server:
        server.serve_forever()

