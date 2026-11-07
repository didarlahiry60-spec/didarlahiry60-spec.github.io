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

            ql = q.lower().strip()
            banglish_words = r'\b(kibhabe|kivabe|jogajog|jogayog|kemon|acho|aso|asen|asos|obostha|khobor|bari|koi|kothay|thake|thako|porashona|porashuna|pore|shob|ashe|bolte|chai|krbo|korbo|parba|paro|ache|tumi|apni|amar|or|tar|sthe|shathe|sathe|kotha|barta|mama|valo|bhalo|dekhi|shonao|akto|ektu|bolen|bolo|kontuct|contruct|dite|nibo|neo|taka|dam|koto|boyos|janan|bolben|korso|banalso|ase|koro|koris|korche|sahajjo|shartho|cha|coffee|biye|khabar|tomar|tor|apnar|ke|ki|konta|kare|kiser|somporke)\b'
            import re
            is_bn = bool(re.search(r'[\u0980-\u09FF]', q)) or bool(re.search(banglish_words, ql, re.I))

            if re.search(r'(contact|contruct|kontact|kontuct|connect|reach|hire|email|mail|phone|whatsapp|number|call|message|msg|meeting|যোগাযোগ|ইমেইল|ফোন|হোয়াটসঅ্যাপ|হোয়াটসঅ্যাপ|নাম্বার|নম্বর|কথা\s*বল|মেসেজ|হায়ার|হায়ার|কাজ\s*দিতে|কাজ\s*করাতে|jogajog|jogayog|kotha\s*bol|sthe\s*contruct|sathe\s*contruct|or\s*sthe|tar\s*sathe|hire\s*k|kaj\s*dite|pabo|call\s*dibo|mail\s*krbo)', ql):
                answer = "দিদারের সাথে সরাসরি যোগাযোগ করার মাধ্যমসমূহ:\n📧 ইমেইল: didarlahiry2.0@gmail.com\n💬 হোয়াটসঅ্যাপ: +880 1631-188500 (https://wa.me/8801631188500)\n📱 এছাড়াও ডেস্কে রাখা স্মার্টফোনে ক্লিক করে সরাসরি মেসেজ পাঠাতে পারেন অথবা সিভি (CV) ডাউনলোড করতে পারেন!" if is_bn else "You can connect with Didar directly via:\n📧 Email: didarlahiry2.0@gmail.com\n💬 WhatsApp: +880 1631-188500 (https://wa.me/8801631188500)\n📱 Or tap the phone on the desk to send a direct message or download his CV!"
            elif re.search(r'(location|address|where|live|living|city|country|কোথায়\s*থাকো|বাসা|বাড়ি|কোথাকার|দেশ|ঢাকা|kothay\s*thak|bari\s*k|basha\s*k|desh\s*k|dhaka)', ql):
                answer = "দিদার ঢাকা, বাংলাদেশে (Dhaka, Bangladesh) থাকেন। তিনি দেশি ও আন্তর্জাতিক ক্লায়েন্ট এবং টিমদের সাথে রিমোটলি কাজ করেন।" if is_bn else "Didar lives in Dhaka, Bangladesh. He works remotely with clients and tech teams worldwide."
            elif re.search(r'(kishan|krishan|কৃষাণ|কৃষান|chash|krishi|কৃষি|dam\s*market|weather|আবহাওয়া|কৃষক)', ql):
                answer = "🌾 কৃষাণ (Kishan AI Platform):\nবাংলাদেশের কৃষকদের জন্য জাতীয় এগ্রো-ইন্টেলিজেন্স সিস্টেম।\n• DAM (কৃষি বিপণন অধিদপ্তর) থেকে প্রতিদিনের পাইকারি ও খুচরা বাজারদর ট্র্যাক করে।\n• Open-Meteo দিয়ে ৭ দিনের হাইপার-লোকাল আবহাওয়ার পূর্বাভাস ও ফসলের পরামর্শ দেয়।\n• সম্পূর্ণ বাংলায় টেক্সট-টু-স্পিচ (TTS) ভয়েস ফিচার ও অফলাইন ক্যাশিং।\n• স্ট্যাক: Flutter, Dart, Python FastAPI, Gemini API, SQLite।\n\nমনিটরের Kishan ট্যাবে ক্লিক করে লাইভ ডিটেইলস দেখুন!" if is_bn else "🌾 Kishan (কৃষাণ) AI Platform:\nNational agricultural intelligence for farmers across Bangladesh.\n• Tracks live DAM wholesale vs retail produce market rates with trend indicators.\n• Hyper-local 7-day crop advisory and weather forecasts via Open-Meteo.\n• Bengali Text-to-Speech (TTS) voice accessibility and offline SQLite cache.\n• Stack: Flutter, Dart, Python FastAPI, Gemini API, SQLite.\n\nCheck the monitor's Kishan tab to explore!"
            elif re.search(r'(letter|লেটার|envelope|খাম|stationery|চিঠি)', ql):
                answer = "✉️ Letter Portfolio Experience:\nএকটি ফিজিক্যাল এনভেলপ ও লেটার ডেস্ক মেটাফোর ওয়েব অ্যাপ্লিকেশন।\n• বাস্তব চিঠির খাম খোলার অভিজ্ঞতা এবং ইন্টারেক্টিভ প্রজেক্ট ফোল্ডার।\n• মাউসের নড়াচড়া অনুযায়ী 3D টিল্ট পারসপেক্টিভ ও Framer Motion স্প্রিং ফিজিক্স।\n• স্ট্যাক: Next.js App Router, TypeScript, Tailwind CSS, Framer Motion।\n\nমনিটরে ক্লিক করে অথবা https://didarlahiry60-spec.github.io/letter-portfolio/ লিংকে সরাসরি দেখে আসতে পারেন!" if is_bn else "✉️ Letter Portfolio Experience:\nA tactile stationary & envelope desk web experience.\n• Physical envelopes that unfold smoothly with interactive project letters.\n• Dynamic 3D tilt perspective and Framer Motion spring physics.\n• Stack: Next.js App Router, TypeScript, Tailwind CSS, Framer Motion.\n\nClick the Letter Portfolio tab on the monitor or visit https://didarlahiry60-spec.github.io/letter-portfolio/!"
            elif re.search(r'(sales|টেলিগ্রাম|সেলস|telegram|ads\s*fashion|bot|বট|দোকান|বিক্রি|কাস্টমার)', ql) and not re.search(r'(fb|facebook|ফেসবুক)', ql):
                answer = "🛍️ E-Commerce AI Sales Agent (ADS Fashion Bot):\n২৪/৭ সক্রিয় টেলিগ্রাম সেলস রিপ্রেজেন্টেটিভ ও কাস্টমার সাপোর্ট বট।\n• ক্রেতাদের সাথে স্বাভাবিক বাংলায় কথা বলে ফ্যাশন সাইজ, ফেব্রিক ও স্টক পরামর্শ দেয়।\n• Google Gemini AI দ্বারা প্রাসঙ্গিক প্রোডাক্ট রেকমেন্ড করে ও স্বয়ংক্রিয়ভাবে অর্ডার কনফার্ম করে।\n• স্ট্যাক: Python, Google Gemini API, python-telegram-bot, SQLite, AsyncIO।\n\nমনিটরে AI Sales Agent ট্যাবে এর বিস্তারিত ডেমো আছে!" if is_bn else "🛍️ E-Commerce AI Sales Agent:\n24/7 intelligent Telegram sales representative and customer support agent.\n• Natural conversational sales negotiations in Bengali and English.\n• Multi-turn context-aware recommendations via Gemini AI and automated SQLite checkout.\n• Stack: Python, Google Gemini API, python-telegram-bot, SQLite, AsyncIO."
            elif re.search(r'(facebook|ফেসবুক|fb\s*auto|fb\s*automation|সোশ্যাল\s*মিডিয়া|social\s*media|অটোমেশন)', ql):
                answer = "📱 Facebook 24/7 AI Automation System:\nক্লাউড-রেডি সোশ্যাল মিডিয়া অটোমেশন অটোপাইলট।\n• দিনে ৩ বার (সকাল ১০:০০, দুপুর ২:৩০, রাত ৮:৩০) প্রযুক্তি বিষয়ক AI পোস্ট পাবলিশ করে।\n• Python Pillow দিয়ে ব্র্যান্ডেড গ্রাফিক ব্যানার ইমেজ স্বয়ংক্রিয়ভাবে জেনারেট করে।\n• কমেন্টের তাৎক্ষণিক বাংলা রিপ্লাই এবং মেসেঞ্জারে ২৪/৭ কাস্টমার সাপোর্ট দেয়।\n• স্ট্যাক: Python, Facebook Graph API, Gemini API, Pillow, Flask, APScheduler।" if is_bn else "📱 Facebook 24/7 AI Automation System:\nCloud-ready social media autopilot system.\n• Curates and publishes tech posts 3x daily (10:00 AM, 2:30 PM, 8:30 PM BST).\n• Generates branded graphic banners automatically using Python Pillow.\n• Instant real-time Bengali comment replies and 24/7 Messenger chatbot.\n• Stack: Python, Facebook Graph API, Gemini API, Pillow, APScheduler, Flask."
            elif re.search(r'(project|প্রজেক্ট|portfolio|পোর্টফোলিও|কাজ|বিল্ড|build|ki\s*ki\s*kaj|kaj\s*ki|ki\s*project)', ql):
                answer = "দিদারের ৪টি প্রধান ফিচার্ড প্রজেক্ট মনিটরে সাজানো আছে:\n1. 🌾 কৃষাণ (Kishan AI) — জাতীয় কৃষি আবহাওয়া ও বাজারদর প্ল্যাটফর্ম\n2. ✉️ Letter Portfolio — 3D ইন্টারেক্টিভ এনভেলপ ওয়েব এক্সপেরিয়েন্স\n3. 🛍️ AI Sales Agent — 24/7 টেলিগ্রাম কাস্টমার সাপোর্ট ও সেলস বট\n4. 📱 FB Automation — ফেসবুক AI কন্টেন্ট ও মেসেঞ্জার অটোপাইলট\n\nমনিটরের যেকোনো প্রজেক্ট বাটনে ক্লিক করে কোড ও ডেমো দেখতে পারেন!" if is_bn else "Didar has 4 featured production-grade projects on the monitor:\n1. 🌾 Kishan AI Platform — National agricultural telemetry & Bengali voice assistant\n2. ✉️ Letter Portfolio — Interactive envelope & stationery 3D web experience\n3. 🛍️ AI Sales Agent — 24/7 autonomous Telegram sales representative with Gemini AI\n4. 📱 FB Automation — Facebook 24/7 dynamic banner & AI auto-reply system\n\nClick any project tab on the monitor to see the full showcase!"
            elif re.search(r'(who|identity|about\s*didar|tell\s*me\s*about|তুমি\s*কে|কে\s*তুমি|দিদার\s*কে|নাম\s*কি|পরিচয়|tumi\s*ke|apni\s*ke|didar\s*ke|didar\s*k|parichoy|somporke|kar\s*portfolio)', ql):
                answer = "আমি দিদার লাহিড়ীর এআই রোবট অ্যাসিস্ট্যান্ট! আর দিদার লাহিড়ী হলেন ঢাকা, বাংলাদেশের একজন AI অটোমেশন স্পেশালিস্ট, ফুল-স্ট্যাক ওয়েব ও অ্যাপ ডেভেলপার এবং রিভার্স ইঞ্জিনিয়ার।\nতিনি জটিল AI অটোমেশন, অটোনোমাস এজেন্ট, আধুনিক 3D ওয়েব এবং সিকিউর সিস্টেমস তৈরি করেন। ডেস্কে তাকিয়ে তার কাজের পুরো পরিবেশ দেখতে পারেন!" if is_bn else "I'm Didar Lahiry's 24/7 AI assistant! Didar is an AI Automation Specialist, Full-Stack Web & App Developer, and Reverse Engineer based in Dhaka, Bangladesh. He builds intelligent multi-agent systems, cross-platform apps, and interactive 3D web experiences."
            elif re.search(r'(skill|স্কিল|দক্ষতা|স্ট্যাক|stack|tech|টেক|কী\s*কী\s*পারো|কী\s*পারো|পারো|python|flutter|react|three\.?js|ai\s*agent|fastapi|node|javascript|typescript|ki\s*ki\s*paro|ki\s*paro|ki\s*jano)', ql):
                answer = "দিদারের প্রধান টেকনিক্যাল দক্ষতাসমূহ:\n• AI & Agents: Autonomous AI Agents, Google Gemini API, LangChain, Multi-Agent Orchestration, Phoenix 3.0।\n• Web Development: JavaScript/TypeScript, React, Next.js, Astro, Three.js (3D WebGL), Node.js, Tailwind CSS।\n• App Development: Flutter, Dart, Python (FastAPI/Flask), SQLite, Offline-first sync।\n• Reverse Engineering (REA): Frida, GDB, Rizin/Cutter, Ghidra, Android APK/DEX অ্যানালাইসিস।" if is_bn else "Didar's core technical expertise spans:\n• AI & Automation: Autonomous AI Agents, Google Gemini API, Multi-Agent Orchestration, LangChain, Voice Orchestrator.\n• Full-Stack & 3D Web: JavaScript/TypeScript, React, Next.js, Astro, Three.js/WebGL, Node.js, Tailwind CSS.\n• Mobile & App Dev: Flutter, Dart, Python (FastAPI/Flask), SQLite, REST/GraphQL.\n• Reverse Engineering (REA): Binary analysis, Frida, GDB, Rizin/Cutter, Ghidra, Android APK reverse engineering."
            elif re.search(r'(education|পড়াশোনা|পড়াশুনা|লেখাপড়া|college|কলেজ|school|স্কুল|hsc|ssc|এইচএসসি|এসএসসি|ভার্সিটি|university|রেজাল্ট|gpa|porashona|porashuna|kothay\s*pore)', ql):
                answer = "দিদারের শিক্ষাগত যোগ্যতা:\n🎓 HSC: সরকারি শ্রীনগর কলেজ (Govt. Sreenagar College) · ব্যাচ ২০২৪ · GPA 4.58 (বিজ্ঞান বিভাগ - ম্যাথ, ফিজিক্স ও আইসিটি)\n🎓 SSC: কাজী পাগলা এ.টি. ইনস্টিটিউশন · ব্যাচ ২০২২ · GPA 4.89 (বিজ্ঞান বিভাগ)\n\nবোর্ডের পিনবোর্ডে এডুকেশন সেকশনে এর পূর্ণ বিবরণ রয়েছে!" if is_bn else "Didar's educational credentials:\n🎓 Higher Secondary (HSC): Govt. Sreenagar College · Batch 2024 · GPA 4.58 (Science: Math, Physics & ICT)\n🎓 Secondary (SSC): Kazir Pagla A.T. Institution · Batch 2022 · GPA 4.89 (Science)\n\nCheck the Education tab on the pinboard for more details!"
            elif re.search(r'(experience|অভিজ্ঞতা|কোথায়\s*কাজ|কাজ\s*করেছো|চাকরি|job|career|koto\s*diner\s*experience)', ql):
                answer = "দিদার ২০২৬ থেকে প্রফেশনাল হিসেবে কাজ করছেন:\n• AI Automation Specialist: অটোনোমাস মাল্টি-টার্ন এজেন্ট ও ভয়েস কন্ট্রোলড পাইপলাইন তৈরি।\n• Web & App Developer: হাই-পারফরম্যান্স 3D ওয়েবজিএল এক্সপেরিয়েন্স এবং ক্রস-প্ল্যাটফর্ম মোবাইল অ্যাপস।\n• Reverse Engineer: বাইনারি অ্যানালাইসিস, সিকিউরিটি ফরেনসিক্স ও এপিআই রিভার্স ইঞ্জিনিয়ারিং।" if is_bn else "Didar works across 4 professional core specializations:\n• AI Automation Specialist (2026-Present): Multi-agent architectures & autonomous LLM workflows.\n• Web & App Developer (2026-Present): High performance 3D Three.js experiences & cross-platform Flutter apps.\n• Reverse Engineer (2026-Present): Binary analysis, Frida instrumentation, and protocol inspection."
            elif re.search(r'(cost|price|pricing|charge|budget|rate|fee|দাম|টাকা|খরচ|বাজেট|কত\s*টাকা|koto\s*taka|dam\s*koto|budget\s*koto)', ql):
                answer = "দিদার যেকোনো ক্লায়েন্ট প্রজেক্টের কাজের পরিধি ও ফিচারের ওপর ভিত্তি করে ক্লায়েন্ট-বান্ধব ও বাস্তবসম্মত বাজেট নির্ধারণ করেন। আপনার প্রজেক্ট আইডিয়া ও বাজেট নিয়ে সরাসরি আলোচনা করতে ইমেইলে (didarlahiry2.0@gmail.com) অথবা হোয়াটসঅ্যাপে (+880 1631-188500) নক দিন!" if is_bn else "Didar offers fair, flexible pricing based on the scope and requirements of your project. To get a quote, reach out directly via email at didarlahiry2.0@gmail.com or on WhatsApp at +880 1631-188500!"
            elif re.search(r'(kemon|কেমন|hi|hello|হ্যালো|সালাম|salam|hey|halo|হেই|ki\s*obostha|ki\s*khobor|kire\s*mama)', ql):
                answer = "হ্যালো! আমি দারুণ আছি! আমি দিদার লাহিড়ীর এআই রোবট। দিদারের প্রজেক্ট, স্কিল, পড়াশোনা, অভিজ্ঞতা বা যোগাযোগ নিয়ে যেকোনো প্রশ্ন আমাকে করতে পারেন। আপনি কেমন আছেন?" if is_bn else "Hey there! I'm doing great! I'm Didar's AI assistant. Ask me anything about Didar's projects, tech stack, experience, or how to get in touch. How can I help you today?"
            elif re.search(r'(cv|resume|রেজুমে|জীবনবৃত্তান্ত)', ql):
                answer = "দিদারের সম্পূর্ণ রেজুমে ডাউনলোড করতে ডেস্কে রাখা ফোনে যান অথবা সরাসরি এই লিঙ্ক থেকে নামিয়ে নিতে পারেন: /DIDAR-LAHIRY%20(Resume).pdf" if is_bn else "You can download Didar's full resume directly via: /DIDAR-LAHIRY%20(Resume).pdf or check the phone on the desk!"
            else:
                answer = "আমি দিদার লাহিড়ীর এআই রোবট অ্যাসিস্ট্যান্ট! আমি দিদারের সাথে যোগাযোগ (ইমেইল/হোয়াটসঅ্যাপ), ৪টি প্রধান প্রজেক্ট (কৃষাণ, লেটার পোর্টফোলিও, সেলস বট, ফেসবুক অটোমেশন), স্কিল, পড়াশোনা বা কাজের বিষয়ে যেকোনো তথ্য দিতে পারি। আপনার কী জানতে চান বলুন!" if is_bn else "I'm Didar's AI assistant! I can answer anything about Didar's contact info, 4 featured projects (Kishan, Letter Portfolio, AI Sales Bot, Facebook Automation), technical skills, or background. What would you like to explore?"

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
