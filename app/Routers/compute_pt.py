from fastapi import APIRouter
import numpy as np
from scipy.signal import find_peaks

router = APIRouter(
    prefix="/compute_pt",
    tags=["compute_pt"]
)

@router.post("/")
def compute_pt(fname: str):
    try:
        result = calculate_pt_inr(fname)
        return result
    except Exception as e:
        return {
            "error": str(e),
            "message": "An error occurred during processing."
        }

def knee_pt(data):
    # Function to find the knee point of a curve
    diff = np.diff(data)
    d_diff = np.diff(diff)
    return np.argmax(d_diff) + 2

def calculate_pt_inr(fname: str):
    fps = 60
    end_video_path = f'stop_time_{fname}.txt'
    start_video_path = f'start_time_{fname}.txt'

    # Read particle motion curve and note length of video
    end_video = np.loadtxt(end_video_path)
    end_video = np.convolve(end_video, np.ones(10), mode='valid') / 10

    # Initialize time array
    sz = end_video.shape
    t = np.linspace(0, (len(end_video) * (fps / 10)) / fps, sz[0])

    # Read start_time file
    begin_video = np.loadtxt(start_video_path)

    # Find knee point of pipette motion curve and process start time
    kp = knee_pt(np.convolve(begin_video, np.ones(10), mode='valid'))
    begin_video = begin_video[:kp]
    pks, locs = find_peaks(begin_video)
    begin_time = t[locs[np.argmax(pks)]] if len(locs) > 0 else 0

    # Calculate end time with offset
    offset = locs[np.argmax(pks)] + (10 * 10) if len(locs) > 0 else 0
    end_video = end_video[offset:]
    end_video = (end_video - np.min(end_video)) / (np.max(end_video) - np.min(end_video))
    f = np.where(end_video < 0.01)[0]
    end_video = end_video[:f[0]] if len(f) > 0 else end_video
    kp = knee_pt(end_video) + offset
    end_time = t[kp]

    # Calculate PT and INR
    pt = (end_time - begin_time) * 10
    pt_normal = 12
    isi = 1.31
    alpha = -0.31
    inr = (pt / pt_normal) ** (isi - alpha)

    # Determine normal ranges and status
    pt_status = "Normal" if 11 <= pt <= 13.5 else "Abnormal Treatment required"
    inr_status = "Normal" if 0.8 <= inr <= 1.1 else "Abnormal Treatment required"

    return {
        "PT": f"{pt:.1f} seconds",
        "INR": f"{inr:.3f}",
        "PT Status": pt_status,
        "INR Status": inr_status
    }
