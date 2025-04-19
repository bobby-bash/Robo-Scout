# import cv2

# def find_available_cameras(max_index=10):
#     available_cameras = []
#     for index in range(max_index):
#         cap = cv2.VideoCapture(index)
#         if cap.isOpened():
#             available_cameras.append(index)
#             cap.release()
#     return available_cameras

# cameras = find_available_cameras()
# print("Available Camera Indices:", cameras)

# import cv2

# # List available camera indices
# index = 0
# available_cameras = []

# while True:
#     cap = cv2.VideoCapture(index, cv2.CAP_ANY)  # Use CAP_ANY to try all backends
#     if not cap.isOpened():
#         break
#     available_cameras.append(index)
#     cap.release()
#     index += 1  # Check the next index

# print("Available Camera Indices:", available_cameras)

import cv2

# Change the index if the camera is not opening (try 0, 1, 2, etc.)
camera_index = 0  
cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # CAP_DSHOW for DirectShow on Windows

if not cap.isOpened():
    print("Error: Could not open the Logitech CP20 camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Logitech CP20 Camera", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
