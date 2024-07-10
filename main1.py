#Final Code

import cv2
import numpy as np
import os
import glob
import csv
from natsort import natsorted
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import time

def update_csv_status(csv_path, seatnum, status, class_name):
    rows = []
    fieldnames = ['seat_number', 'seat_coordinates']

    # Read the existing CSV file
    with open(csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames.extend(reader.fieldnames[2:])  # Keep existing columns

        for row in reader:
            if row['seat_number'] == seatnum:
                row[class_name] = status
                row[f'{class_name}_date_time'] = datetime.now().strftime("%d-%m-%Y %H:%M")
            rows.append(row)

    # Add new fields if they don't exist
    if class_name not in fieldnames:
        fieldnames.append(class_name)
        fieldnames.append(f'{class_name}_date_time')

    # Write back the updated data to the CSV file
    with open(csv_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def process_image(image_path, csv_path):
    class_name = os.path.basename(image_path).split('.')[0]
    result_folder = class_name

    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    rois = []
    with open(csv_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        for row in reader:
            coordinates = eval(row['seat_coordinates'])
            rois.append((row['seat_number'], coordinates))

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Resize the image to 1661 x 750 as done during ROI definition
    image_resized = cv2.resize(image, (1661, 750))

    for seatnum, (y1, y2, x1, x2) in rois:
        cropped_image = image_resized[y1:y2, x1:x2]
        outfile = os.path.join(result_folder, seatnum + ".jpg")
        cv2.imwrite(outfile, cropped_image)

    model = YOLO("yolov8x.pt")

    image_files = natsorted(glob.glob(os.path.join(result_folder, "*.jpg")))

    imgs = [cv2.imread(file) for file in image_files]
    if not imgs or any(img is None for img in imgs):
        raise ValueError("No valid images found to process.")

    results = model.predict(imgs, save=True, save_txt=True, project=result_folder, name='results', exist_ok=True)

    for i, r in enumerate(results):
        im_bgr = r.plot()
        im_rgb = Image.fromarray(im_bgr[..., ::-1])
        result_filename = f"results{i}.jpg"
        result_path = os.path.join(result_folder, result_filename)
        r.save(filename=result_path)

        seatnum = os.path.basename(image_files[i]).split('.')[0]
        status = 'Absent'
        for detection in r.boxes.data:
            if detection[-1] == 0:
                status = 'Present'
                break
        update_csv_status(csv_path, seatnum, status, class_name)

def capture_and_process(rtsp_url, csv_path, snapshot_folder, img_counter):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return img_counter

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: Could not read frame from video stream")
        return img_counter

    # Resize the frame to 1661 x 750 as done during ROI definition
    frame_resized = cv2.resize(frame, (1661, 750))

    img_name = os.path.join(snapshot_folder, f"snapshot_{img_counter}.jpg")
    cv2.imwrite(img_name, frame_resized)
    print(f"{img_name} written!")
    try:
        process_image(img_name, csv_path)
    except Exception as e:
        print(f"Error processing image {img_name}: {e}")

    img_counter += 1
    return img_counter

def main():
    rtsp_url = "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1"
    csv_path = "test.csv"
    snapshot_folder = "snapshots"

    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    img_counter = 0
    num_snapshots = 2  # Number of snapshots to capture

    while img_counter < num_snapshots:
        img_counter = capture_and_process(rtsp_url, csv_path, snapshot_folder, img_counter)
        time.sleep(120)  # Wait for 300 seconds (5 minutes) before capturing the next snapshot

if __name__ == "__main__":
    main()
