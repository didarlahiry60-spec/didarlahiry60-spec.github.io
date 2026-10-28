import http.server
import socketserver
import os
import json
import mimetypes
import sys

PORT = 3000
DIRECTORY = "/home/didar-lahiry/Antigravity/Target Portfolio 2"

# Ensure all 3D/WASM mime types are properly registered
mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("model/gltf-binary", ".glb")
mimetypes.add_type("image/ktx2", ".ktx2")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/webm", ".webm")

class PortfolioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Handle Spotify / Music API
        if self.path.startswith("/api/now-playing"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "title": "Creative Coding Ambient",
                "artist": "Didar Lahiry Workspace",
                "state": "playing",
                "url": "https://open.spotify.com"
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        # Handle Robot TV AI chat (/api/ask)
        if self.path.startswith("/api/ask"):
            length = int(self.headers.get("content-length", 0))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(body)
                q = payload.get("question", "").lower()
            except:
                q = ""

            answer = "I'm Didar's AI assistant! Didar is an AI Automation Specialist, Web Developer, App Developer, and Reverse Engineer based in Dhaka, Bangladesh. He specializes in AI workflows, LLM integrations, and modern full-stack web and mobile applications. Feel free to connect via the phone on the desk or email him directly at itsdidar60@gmail.com!"

            if any(w in q for w in ["project", "build", "portfolio", "work"]):
                answer = "Didar is currently updating his projects portfolio with cutting-edge autonomous AI workflows and full-stack builds. Stay tuned for new releases!"
            elif any(w in q for w in ["contact", "email", "phone", "hire", "whatsapp"]):
                answer = "You can contact Didar at itsdidar60@gmail.com or via WhatsApp at +880 1631-188500. His full CV is also ready to download on his desk phone!"
            elif any(w in q for w in ["skill", "stack", "tech", "python", "react"]):
                answer = "Didar's core expertise spans AI Tools Integration (LLMs, LangChain, OpenAI APIs), Workflow Automation (Webhooks, n8n, Python pipelines), and Full-Stack Modern Web (React, Node.js, Next.js, FastAPI, Three.js)."

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {"answer": answer}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # Handle Contact Inquiries (/api/contact)
        elif self.path.startswith("/api/contact"):
            length = int(self.headers.get("content-length", 0))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            # Append to messages.json for persistence
            messages_file = os.path.join(DIRECTORY, "messages.json")
            messages = []
            if os.path.exists(messages_file):
                try:
                    with open(messages_file, "r", encoding="utf-8") as f:
                        messages = json.load(f)
                except Exception:
                    messages = []

            from datetime import datetime
            record = {
                "id": len(messages) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": payload.get("name", "Anonymous"),
                "email": payload.get("email", ""),
                "phone": payload.get("phone", "Not provided"),
                "service": payload.get("service", "General Inquiry"),
                "message": payload.get("message", "")
            }
            messages.append(record)

            try:
                with open(messages_file, "w", encoding="utf-8") as f:
                    json.dump(messages, f, indent=2, ensure_ascii=False)
                print(f"📩 New message received from {record['name']} ({record['email']})")
                sys.stdout.flush()
            except Exception as e:
                print(f"Error saving message: {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {"status": "success", "message": "Inquiry recorded successfully"}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with ReusableTCPServer(("", PORT), PortfolioHandler) as httpd:
        print(f"🚀 Didar Portfolio Server running at http://localhost:{PORT}")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
