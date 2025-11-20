# ♟️ Chess AI with Deep Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Welcome to my **Chess AI** project! This isn't just another chess engine; it's a neural network-based AI that learns to play by studying human games. 🧠✨

Built with **PyTorch** for the brain and **Flask** for the beautiful web interface, this project lets you challenge an AI that can be as easy as a toddler or (eventually) as tough as a Grandmaster.

---

## 🚀 Features

*   **🤖 Deep Learning AI**: Uses a Convolutional Neural Network (CNN) trained on millions of positions.
*   **🎚️ Multiple Difficulties**:
    *   **Easy**: For casual play (or boosting your ego).
    *   **Medium**: A decent challenge.
    *   **Hard**: Sweaty palms territory.
    *   **Extreme**: Good luck.
*   **🖥️ Modern Web Interface**:
    *   Sleek dark mode UI.
    *   **Move History**: See every move and click to rewind time! ⏳
    *   **Flip Board**: Want to play Black? Just flip it! The AI automatically takes over White. 🔄
*   **☁️ Kaggle Training Ready**: Includes a standalone script (`for_kaggle.py`) to train your own models on the cloud for free!

---

## 🛠️ Installation

Getting started is super easy. You'll need Python installed.

1.  **Clone the repo** (or download the files):
    ```bash
    git clone https://github.com/yourusername/chess-ai.git
    cd chess-ai
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🎮 How to Play

1.  **Start the server**:
    ```bash
    python app.py
    ```
2.  Open your browser and go to:
    `http://127.0.0.1:5000`

3.  **Pick a difficulty** and start moving pieces!

> **Note**: By default, the project comes with a basic `chess_model.pth`. To unlock the true power of Medium/Hard/Extreme modes, you need to train the models (see below).

---

## 🧠 Training Your Own AI

Want to make the AI smarter? You can train it yourself!

### Option A: Train Locally (Slow 🐢)
Run the training script on your machine:
```bash
python train.py
```

### Option B: Train on Kaggle (Fast 🐇)
I've prepared a special script for cloud training.
1.  Go to [Kaggle](https://www.kaggle.com/).
2.  Create a New Notebook.
3.  Copy the content of `for_kaggle.py` into the notebook.
4.  Upload a PGN dataset (search for "Chess Games" on Kaggle).
5.  Run the notebook!
6.  Download the generated `.pth` files (`model_medium.pth`, etc.) and put them in your project folder.

---

## 🏗️ Tech Stack

*   **Backend**: Python, Flask
*   **AI/ML**: PyTorch, NumPy
*   **Chess Logic**: `python-chess`
*   **Frontend**: HTML5, CSS3, jQuery, Chessboard.js, Chess.js

---

## 🤝 Contributing

Feel free to fork this project, submit PRs, or open issues if you find bugs (or if the AI plays an illegal move... it happens to the best of us).

Happy Coding & Checkmating! ♔♕
