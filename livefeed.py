# import cv2
# import time

# # Define the RTSP URL
# rtsp_url = "rtsp://dd:Lbsnaa123@10.10.116.67"

# # Create a VideoCapture object to capture video from the RTSP stream
# cap = cv2.VideoCapture(rtsp_url)

# # Check if the video capture is opened successfully
# if not cap.isOpened():
#     print("Error: Could not open video stream")
#     exit()

# # Main loop to capture and display the video stream
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Could not read frame from video stream")
#         break

#     # Resize the frame to 1200 x 720 (if needed)
#     frame_resized = cv2.resize(frame, (1661, 750))

#     # Display the resulting frame
#     cv2.imshow('Video Stream', frame_resized)

#     # Exit the loop when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the VideoCapture object and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()
import cv2
import os

# # Define the RTSP URL front
# rtsp_url = "rtsp://dd:Lbsnaa123@10.10.116.67"

# Define the RTSP URL dome
rtsp_url = "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1"

# Create a VideoCapture object to capture video from the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the video capture is opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Create the "roi_snap" directory if it doesn't exist
snapshot_folder = "roi_snap"
if not os.path.exists(snapshot_folder):
    os.makedirs(snapshot_folder)
    print(f"Created directory: {snapshot_folder}")

# Initialize a counter for the snapshot file names
img_counter = 0

# Main loop to capture and display the video stream
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from video stream")
        break

    # Resize the frame to 1661 x 750 (as specified)
    frame_resized = cv2.resize(frame, (1661, 750))

    # Display the resulting frame
    cv2.imshow('Video Stream',frame_resized)

    # Ask the user whether to save a snapshot or quit
    user_input = input("Enter 'y' to save a snapshot or 'q' to quit: ").strip().lower()
    if user_input == 'q':
        # Exit the loop when 'q' is pressed
        break
    elif user_input == 'y':
        # Save a snapshot
        img_name = os.path.join(snapshot_folder, f"snapshot_dome{img_counter}.jpg")
        try:
            cv2.imwrite(img_name, frame_resized)
            print(f"Snapshot saved: {img_name}")
            img_counter += 1
        except Exception as e:
            print(f"Failed to save snapshot: {e}")

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
