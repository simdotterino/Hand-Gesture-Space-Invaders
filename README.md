# CMPT310 Space Invaders

**Created by:** Simran Vig, Junghun Byun, Ines Machinho Rodrigues  
**Course:** CMPT 310, Simon Fraser University  

## Description
A hand-gesture-controlled version of Space Invaders using a KNN model trained on an organic dataset. Players can move the spaceship and fire using hand gestures detected through a webcam. For detailed instructions, see the [how-to-guide] (https://github.com/simdotterino/Hand-Gesture-Space-Invaders/blob/main/how-to-guide.pdf).

## Language & Version
- Python 3.10 or earlier (required for MediaPipe compatibility)

## Libraries
- MediaPipe Hands  
- Scikit-learn  
- Pygame  
- NumPy  
- OpenCV (cv2)

## Hardware Requirements
- Webcam  
- Mouse or trackpad

## Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/simdotterino/Hand-Gesture-Space-Invaders
   cd Hand-Gesture-Space-Invaders

2. Set up a Python 3.10 virtual environment
   python3.10 -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Mac/Linux
   source venv/bin/activate

3. Install required libraries
   python3.10 -m pip install mediapipe scikit-learn pygame numpy opencv-python

4. Run the game
   python3.10 game_logic/game_interface.py

To see the metrics of our knn model, run game_assets/main.py. Notably, our model has an overall average accuracy of approximately 93%. 

