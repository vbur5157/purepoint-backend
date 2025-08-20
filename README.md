
# PurePoint Backend Server (Anansi API)

This is the backend for PurePoint Cleaning & Restoration's intelligent assistant, Anansi. It handles chat communication with OpenAI GPT and supports integration into your site or app.

## 🌐 Endpoint
- `POST /chat`: Accepts JSON `{"message": "Your question"}` and returns `{"reply": "Anansi's response"}`

## 🚀 Setup Instructions

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Create a `.env` file and add your API key:
```
OPENAI_API_KEY=your-api-key-here
```

3. Run the server:
```
python purepoint_backend_server.py
```

4. Deploy using:
- **Render.com** (auto-detects Flask via `Procfile`)
- **Netlify functions** (for frontend proxies)
