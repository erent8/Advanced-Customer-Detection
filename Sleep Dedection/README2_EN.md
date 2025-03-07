# Eye Blink Detector - Drowsiness Detection System

## About the Project
This project is a computer vision application that detects driver drowsiness in real-time. The system continuously monitors the driver's eyes and detects drowsy driving conditions by analyzing eye closure duration.

## Features
- 🎥 Real-time video analysis
- 👁️ Eye blink detection
- ⏱️ Eye closure duration measurement
- 🚨 Audio alert system
- 📊 Eye Aspect Ratio (EAR) visualization

## Technical Details
The system uses the following technologies:
- **Python**: Main programming language
- **OpenCV**: Image processing and video capture
- **dlib**: Face and facial landmark detection
- **scipy**: Euclidean distance calculations
- **pygame**: Audio alert system

### Eye Aspect Ratio (EAR) Calculation
EAR is calculated using the following formula:
```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```
Where:
- p1-p6: 6 reference points around the eye
- ||.||: Euclidean distance between two points

## Installation

### System Requirements
- Python 3.7 or higher
- Webcam
- Windows/Linux/MacOS operating system

### Step-by-Step Installation
1. **Python Installation**
   ```bash
   # Download and install Python (python.org)
   # Don't forget to add to PATH
   ```

2. **Creating Virtual Environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # For Windows
   source .venv/bin/activate # For Linux/MacOS
   ```

3. **Installing Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Downloading Face Landmark File**
   - Download shape_predictor_68_face_landmarks.dat file
   - Copy it to the project folder

## User Guide

### Starting the Program
```bash
python drowsiness_detection.py
```

### Controls
- **q**: Exit program
- Webcam feed will be displayed while the program is running
- Eye Aspect Ratio (EAR) is shown at the top of the screen
- Audio and visual alerts are triggered when drowsy driving is detected

### Parameter Adjustment
Important parameters in the program:
- `EAR_THRESHOLD`: EAR value threshold for considering eyes closed (default: 0.25)
- `CONSECUTIVE_FRAMES`: Number of consecutive frames needed for alert (default: 20)

These values can be adjusted in the `drowsiness_detection.py` file.

## Testing
Test scenarios are included to verify system functionality:
```bash
python -m unittest test_drowsiness_detection.py -v
```

Tests check the following:
- Accuracy of EAR calculation
- Correct detection of eye points
- Distinction between open/closed eye states
- Error handling

## Safety Warnings
- This system is a driving safety aid and should not be relied upon solely
- System performance may be affected by lighting conditions
- Wearing glasses may affect detection accuracy

## Troubleshooting
1. **Camera Access Error**
   - Check camera connection
   - Ensure no other application is using the camera

2. **dlib Installation Error**
   - Make sure Visual Studio Build Tools is installed
   - Verify correct CMake installation

3. **Low Performance**
   - Ensure your computer meets system requirements
   - Close unnecessary background applications

## Contributing
1. Fork this repository
2. Create a new branch
3. Commit your changes
4. Push your branch
5. Create a Pull Request

## Contact
You can open an Issue for questions and suggestions.

## License
This project was developed as open source.
