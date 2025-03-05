# MathGestures - Mathematical Problem Solving with Hand Gestures

MathGestures is an innovative application that allows you to solve mathematical problems using hand gestures. It detects your hand movements using OpenCV and MediaPipe technologies and solves your mathematical problems using Google's Gemini AI model.

## 🌟 Features

- ✍️ Write mathematical problems with hand gestures
- 🤖 Real-time hand gesture detection
- 🧮 Automatic mathematical problem solving
- 🎯 User-friendly interface
- 📱 Web-based usage with Streamlit

## 🛠️ Requirements

```
python 3.8 or higher
opencv-python==4.8.1.78
cvzone==1.6.1
mediapipe==0.10.21
numpy==1.26.4
google-generativeai
Pillow
streamlit
```

## 🚀 Installation

1. Clone the project:
```bash
git clone https://github.com/username/MathGestures.git
cd MathGestures
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# For Windows:
.venv\Scripts\activate
# For Linux/Mac:
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Start the application:
```bash
streamlit run main.py
```

## 📝 Usage

1. When you start the application, your webcam feed will appear on the screen.
2. Raise your index finger to activate writing mode.
3. Write your mathematical problem in the air.
4. Raise your thumb to erase what you've written.
5. Raise all fingers (except pinky) to see the solution.

## 🎮 Hand Gesture Controls

- ✌️ Index finger: Writing mode
- 👍 Thumb: Erasing mode
- ✋ Four fingers (except pinky): Show solution

## ⚠️ Important Notes

- Use in a well-lit environment
- Show your hand clearly to the camera
- Write large and legible
- Keep only one hand in front of the camera

## 🤝 Contributing

1. Fork this project
2. Create a new branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Added new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## 👥 Authors

- [Eren] - *Initial Developer*

## 🙏 Acknowledgments

- OpenCV team
- MediaPipe team
- Google Gemini AI team
- Streamlit team

## 📞 Contact

For questions: [erenterzi@protonmail.com]

---
⭐️ Don't forget to give a star if you like this project! 
