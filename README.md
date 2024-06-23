# Push-up Counter using MediaPipe and OpenCV

This project uses MediaPipe to detect poses in a video (e.g., push-ups) and counts the number of correct push-ups performed based on pose analysis.

### Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- MediaPipe (`pip install mediapipe`)

### Usage

1. Clone the repository:
    ```sh
    # Clone the repository
    git clone https://github.com/dqyaa/Pushup-Postur-Analysis-and-Counter/tree/master.git
    cd pushup-counter
    ```

2. Place your video file named `pushup.mp4` in the project directory.

3. Run the `main.py` script:
    ```sh
    # Run the script
    python main.py
    ```

4. The application will display the video with annotated pose landmarks and count the number of push-ups.

### Notes

- Adjust the angle thresholds and other parameters in `pushup_counter.py` as needed for different poses or requirements.
- Press 'q' to quit the application.

