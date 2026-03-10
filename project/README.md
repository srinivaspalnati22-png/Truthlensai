# TruthLens AI - Fake News Detection Prototype

A high-fidelity hackathon prototype for a fake news and misinformation detection platform. Built with a modern, futuristic startup UI/UX, combining Tailwind CSS, custom glassmorphism, animated data visualizations, and a Python Flask backend.

## 🚀 Features

* **Real-time Authenticity Analysis**: Simulates an advanced NLP model detecting clickbait, bias, and sentiment.
* **Futuristic UI/UX**: Custom canvas particle background, glass-panel components, and gradient animations.
* **Deep Metrics Dashboard**: Interactive Chart.js radar charts and dynamic CSS radial progress indicators.
* **Fully Responsive**: Optimized for desktop and mobile presentations.
* **Zero Database Setup**: Runs purely in-memory, perfect for fast hackathon demonstrations.

## 📁 Project Structure

```text
project/
│
├── backend/
│   └── app.py            # Main Flask Server & Mock AI Logic
│
├── templates/
│   └── index.html        # Main landing page & dashboard UI
│
├── static/
│   ├── css/
│   │   └── style.css     # Glassmorphism & Animations
│   └── js/
│       └── script.js     # Canvas particles, API handling, Chart.js
│
├── requirements.txt      # Python dependencies
└── README.md
```

## 🛠️ How to Run Locally in VS Code

1. **Open the project folder** in VS Code.
2. **Open a new terminal** in VS Code (`Ctrl + ` `).
3. Ensure you are in the `project/` directory:
   ```bash
   cd project
   ```
4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Flask application**:
   ```bash
   python backend/app.py
   ```
6. **Open your browser** and go to:
   ```text
   http://127.0.0.1:5000
   ```
   *(Note: The terminal will output `Running on http://127.0.0.1:5000/`. Ctrl+Click the link to open it).*

## 💡 Hackathon Demo Control Guide
* **To trigger a FAKE result:** Use excessive punctuation/capitalization or very short sentences. (e.g., "SHOCKING ALIEN DISCOVERY!!!")
* **To trigger a LEGITIMATE result:** Use formal keywords like "verified", "according to". (e.g., "According to verified reports, the launch was successful.")
* Both outcomes generate beautiful interactive charts and radar mappings to impress the judges.
