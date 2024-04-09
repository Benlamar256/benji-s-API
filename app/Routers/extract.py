from fastapi import APIRouter, UploadFile, File
import cv2
import os
import time

router = APIRouter()

async def extract_frames(video_path: str, output_folder: str):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    # Extract frames from the video
    while success:
        # Save frame as JPEG file
        cv2.imwrite(f"{output_folder}/frame{count}.jpg", image)
        success, image = vidcap.read()
        print(f"Extracted frame {count}")
        count += 1

@router.post("/extract")
async def extract_video_frames(video_file: UploadFile = File(...)):
    # Save the uploaded video file to the 'uploads' directory
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    video_path = f"{upload_folder}/{video_file.filename}"
    with open(video_path, "wb") as buffer:
        buffer.write(video_file.file.read())

    output_folder = f"video"
    
    # Extract frames from the video
    await extract_frames(video_path, output_folder)
    Extraction_time= f"{int(time.time())}"

    return {"message": "Frames extracted successfully", "Extraction_time":Extraction_time, "output_folder": output_folder}
   