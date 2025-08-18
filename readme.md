# Creepy Message Detector (PyQt6 + OCR)

A desktop app to **detect creepy or harassing messages** in text or screenshots.  
Built with **PyQt6** for the GUI and **Tesseract OCR** for extracting text from images.  
Designed to be **lightweight, explainable, and offline** (no cloud/ML dependency).

---

## ✨ Features

- **Input options**
  - Paste or type text
  - Upload a screenshot → OCR → analyze
- **Scoring system** with transparent phrase matches (e.g., `ask_send_pic`, `explicit_terms`)
- **Filter levels**
  - **Easy** (strict, ≥ 0.55)
  - **Medium** (lenient, ≥ 0.30)
- **Categories covered**
  - Requests for pics/nudes  
  - Sexual/explicit vocabulary  
  - Coercion & persistence (“don’t ignore me”)  
  - Flirt openers  
  - Harassment (slurs, insults, threats, doxxing, stalking)  
- **Conversation tracking** – recent scores are accumulated in `AppState`  
- **Runs fully offline** once Tesseract is installed  

---

## 📦 Requirements

- **Python 3.11+**
- **Tesseract OCR** (for screenshots, optional if you only analyze text)  
  - Windows typical paths:  
    - `C:\Users\<you>\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`  
    - `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Python packages:
  - `PyQt6`
  - `pytesseract`
  - `Pillow`

---

## 🚀 Setup (Windows PowerShell)

```powershell
# clone
git clone https://github.com/<you>/nlp_creepdetector.git
cd nlp_creepdetector

# create and activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# install dependencies
pip install -U pip
pip install PyQt6 pytesseract Pillow

# run
python main.py
