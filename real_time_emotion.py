import cv2
from deepface import DeepFace
import csv
import datetime

def main():
    # Create CSV with titles time_seconds and dominant_emotion
    with open("emotion_log.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_seconds", "dominant_emotion"])

    # Track time while recording
    cap = cv2.VideoCapture(0)
    previous_second = None 
    start_time = None  

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            analysis = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False
            )

            if isinstance(analysis, list) and len(analysis) > 0:
                first_face = analysis[0]
                dominant_emotion = first_face.get("dominant_emotion", None)

                if dominant_emotion:
                    # Get the current time in seconds since midnight, storing time in seconds since midnight allows for easier plotting, interpolation, and trend detection.
                    now = datetime.datetime.now()
                    time_seconds = now.hour * 3600 + now.minute * 60 + now.second

                    # Set the start time on the first recorded emotion
                    if start_time is None:
                        start_time = time_seconds

                    # Normalize time (subtract the start time)
                    normalized_time = time_seconds - start_time

                    # Only log the first detected emotion per second
                    if time_seconds != previous_second:
                        with open("emotion_log.csv", mode="a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([normalized_time, dominant_emotion])

                        previous_second = time_seconds  # Update last logged second

                    # Display the detected emotion on the webcam feed
                    cv2.putText(
                        frame,
                        dominant_emotion,
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 255, 0),
                        2
                    )

        except Exception as e:
            print("DeepFace error:", e)

        cv2.imshow("Webcam Feed (Press 'spacebar' to Quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
