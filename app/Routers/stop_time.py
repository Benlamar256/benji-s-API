import numpy as np
import cv2
import os
from fastapi import APIRouter

router = APIRouter()

def circlecropbw(img, cx, cy, cr, invert):
    img2 = np.uint8(np.dstack([img, img, img]))
    out, _ = circlecrop(img2, cx, cy, cr, invert)
    out = out[:, :, 0]
    return out
def circlecrop(img, cx, cy, cr, invert):
    rows, columns, _ = img.shape
    rgbImage2 = np.zeros((rows, columns, 3), dtype=np.uint8)

    ci = [cx, cy, cr]
    xx, yy = np.meshgrid(np.arange(1, columns + 1) - ci[0], np.arange(1, rows + 1) - ci[1])  # Adjusted dimensions
    mask = (xx ** 2 + yy ** 2) < ci[2] ** 2
    if invert == 1:
        mask = ~mask

    redChannel1 = img[:, :, 0]
    greenChannel1 = img[:, :, 1]
    blueChannel1 = img[:, :, 2]
    redChannel2 = rgbImage2[:, :, 0]
    greenChannel2 = rgbImage2[:, :, 1]
    blueChannel2 = rgbImage2[:, :, 2]

    redChannel2[mask] = redChannel1[mask]
    greenChannel2[mask] = greenChannel1[mask]
    blueChannel2[mask] = blueChannel1[mask]

    out = np.stack([redChannel2, greenChannel2, blueChannel2], axis=2)
    return out, mask


def process_video_frames(fname, fps=60):
    fps = 60
    fname = 'video'
    y, x = 920, 500
    r1, r2 = 200, 350
    n = len(os.listdir(fname)) - 3
    n = (n // fps) * fps - (fps / 10)
    met = []
    
    for start in np.arange(0, n + 1, fps / 10):
        img1 = cv2.imread(f'{fname}/frame{int(start)}.jpg')
        sz = img1.shape[:2]
        if sz[0] == 1080:
            img1 = np.rot90(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), 3)
        img1 = circlecropbw(img1, y, x, r1, 0)
        img1 = img1[y - r2:y + r2, x - r2:x + r2]

        img2 = cv2.imread(f'{fname}/frame{int(start + fps / 10)}.jpg')
        sz = img2.shape[:2]
        if sz[0] == 1080: 
            img2 = np.rot90(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), 3)
        img2 = circlecropbw(img2, y, x, r1, 0)
        img2 = img2[y - r2:y + r2, x - r2:x + r2]

        print("img1 shape:", img1.shape)

        diff = cv2.absdiff(img1.astype(np.int32), img2.astype(np.int32))
        met_val = np.sum(diff)
        met.append(met_val)
        print(f'{(start / n) * 100}% complete')
    
    np.savetxt(f'stop_time_{fname}.txt', met)
    return f'{(start/n)*100}% complete'

@router.post("/stop_time")
def stop_time(fname: str):
    response = process_video_frames(fname)
    return {"message": response}
