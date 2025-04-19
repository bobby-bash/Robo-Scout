import cv2

# Replace `0` with the correct index if needed
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot access the camera")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()
