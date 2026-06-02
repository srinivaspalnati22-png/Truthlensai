# TruthLens AI - Fake News Detection Platform

A high-fidelity prototype for a fake news and misinformation detection platform. Built with a modern, futuristic startup UI/UX, combining Tailwind CSS, custom glassmorphism, animated data visualizations, and advanced NLP-inspired analysis.

**Live Demo:** Runs on Flask backend with real-time authenticity analysis and interactive dashboards.

---

## 🚀 Features

- **Real-time Authenticity Analysis**: Simulates advanced NLP models detecting clickbait, bias, and sentiment
- **Futuristic UI/UX**: Custom canvas particle background, glass-panel components, and gradient animations
- **Deep Metrics Dashboard**: Interactive Chart.js radar charts and dynamic CSS radial progress indicators
- **Fully Responsive**: Optimized for desktop and mobile presentations
- **Zero Database Setup**: Runs purely in-memory, perfect for fast demonstrations
- **Comprehensive Scoring System**: Multi-dimensional analysis with credibility, bias, sentiment, and clickbait detection

---

## 📁 Project Structure

```
project/
│
├── backend/
│   └── app.py                    # Main Flask Server & Mock AI Logic
│
├── templates/
│   └── index.html                # Main landing page & dashboard UI
│
├── static/
│   ├── css/
│   │   └── style.css             # Glassmorphism & Animations
│   └── js/
│       └── script.js             # Canvas particles, API handling, Chart.js
│
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Local Development

1. **Clone the repository** (or navigate to it):
   ```bash
   git clone https://github.com/srinivaspalnati22-png/Truthlensai.git
   cd Truthlensai
   ```

2. **Navigate to the project directory**:
   ```bash
   cd project
   ```

3. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application**:
   ```bash
   python backend/app.py
   ```

6. **Open in browser**:
   ```
   http://127.0.0.1:5000
   ```
   *(The terminal will output the running URL. Ctrl+Click to open it directly)*

---

## 💡 How to Use - Demo Guide

### Testing the Fake News Detection

**To trigger a FAKE result:**
- Use excessive punctuation/capitalization
- Use very short, sensational sentences
- Example: `"SHOCKING ALIEN DISCOVERY!!!"`

**To trigger a LEGITIMATE result:**
- Use formal, verified keywords
- Use complete sentences with sources
- Example: `"According to verified reports, the launch was successful."`

### Analysis Metrics

The dashboard displays:
- **Credibility Score**: Overall trustworthiness (0-100)
- **Bias Detection**: Political or ideological leaning
- **Sentiment Analysis**: Emotional tone and manipulation indicators
- **Clickbait Probability**: Sensationalism detection
- **Authenticity Radar**: Multi-dimensional analysis chart

---

## 🎨 Technology Stack

### Frontend
- **HTML5**: Semantic structure
- **Tailwind CSS**: Utility-first styling with glassmorphism effects
- **Vanilla JavaScript**: Canvas particles, Chart.js integration
- **Chart.js**: Interactive radar and statistical visualizations

### Backend
- **Flask**: Lightweight Python web framework
- **Python 3**: Server-side logic and mock NLP analysis

### Styling & Effects
- **Custom CSS Animations**: Gradient shifts, particle effects, transitions
- **Canvas API**: Real-time animated particle background
- **Responsive Design**: Mobile-first approach

---

## 📊 API Endpoints

### POST `/analyze`
Analyzes a given text for authenticity and misinformation.

**Request:**
```json
{
  "text": "Your news text here"
}
```

**Response:**
```json
{
  "credibility_score": 75,
  "bias_level": "moderate",
  "sentiment": "neutral",
  "clickbait_probability": 0.15,
  "verdict": "LEGITIMATE",
  "metrics": {
    "authenticity": 78,
    "bias": 45,
    "sentiment": 50,
    "clickbait": 15
  }
}
```

---

## 🎯 Use Cases

- **Journalism & Media**: Quick-check tool for reporters
- **Social Media**: Browser extension or widget integration
- **Educational**: Teaching AI/NLP concepts with visual feedback
- **Hackathon Demos**: Impressive prototype for competitions
- **User Research**: Testing misinformation detection concepts

---

## 🔮 Future Enhancements

- [ ] Real ML model integration (spaCy, Hugging Face Transformers)
- [ ] Database support for historical analysis
- [ ] Browser extension version
- [ ] Multi-language support
- [ ] Source credibility rating system
- [ ] Fact-checking API integration
- [ ] User authentication & saved analyses
- [ ] Advanced NLP models for semantic analysis

---

## 📝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Srinivas Palnati**  
GitHub: [@srinivaspalnati22-png](https://github.com/srinivaspalnati22-png)

---

## 🤝 Support

If you encounter any issues or have suggestions:
- Open an [issue](https://github.com/srinivaspalnati22-png/Truthlensai/issues)
- Check existing documentation
- Review Flask and Tailwind CSS documentation

---

## ⭐ Acknowledgments

- Flask community for the excellent web framework
- Tailwind CSS for modern utility-first styling
- Chart.js for interactive data visualization
- All contributors and users who've supported this project

---

**Made with ❤️ for fighting misinformation and building a more informed world.**
