import sys
import numpy as np
import cv2
import os
import time
from scipy.signal import find_peaks
from knee_pt import knee_pt
from start_time import circlecropbw

# Function to compute the knee point of a curve
def compute_knee_point(data):
    diff = np.diff(data)
    d_diff = np.diff(diff)
    return np.argmax(d_diff) + 2

# Function to extract frames from the video
def extract(fname):
	if not os.path.exists(fname):
		os.mkdir(fname)
		vidcap = cv2.VideoCapture('./'+fname+'.mp4')
		success,image = vidcap.read()
		count = 0
		while success:
			cv2.imwrite("./"+fname+"/frame%d.jpg" % count, image)
			success,image = vidcap.read()
			print (fname,count)
			count += 1
t=time.time()
extract('video')

# Function to compute start time
def compute_start_time(fname, fps, y, x, r1, r2):
    n = int(fps * 10)
    met = []
    for start in np.arange(0, n+1, fps/10):
        img1 = cv2.imread(f'{fname}/frame{int(start)}.jpg')
        sz = img1.shape[:2]
        if sz[0] == 1080:
            img1 = np.rot90(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), 3)
        img1 = circlecropbw(img1, y, x, r1, 1)
        img1 = img1[y-r2:y+r2, x-r2:x+r2]

        img2 = cv2.imread(f'{fname}/frame{int(start+fps/10)}.jpg')
        sz = img2.shape[:2]
        if sz[0] == 1080:
            img2 = np.rot90(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), 3)
        img2 = circlecropbw(img2, y, x, r1, 1)
        img2 = img2[y-r2:y+r2, x-r2:x+r2]

        cc = np.abs(img1.astype(np.int32) - img2.astype(np.int32))
        met.append(np.sum(cc))
        print(f'{(start/n)*100}% complete')

    np.savetxt(f'start_time_{fname}.txt', met)

# Function to compute stop time
def compute_stop_time(fname, fps, y, x, r1, r2):
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

        diff = cv2.absdiff(img1.astype(np.int32), img2.astype(np.int32))
        met_val = np.sum(diff)
        met.append(met_val)
        print(f'{(start / n) * 100}% complete')

    np.savetxt(f'stop_time_{fname}.txt', met)

# Function to calculate PT and INR
def calculate_pt_and_inr(fname, fps):
    #begin_video = np.loadtxt('start_time_' + fname + '.txt')
    #begin_video = np.convolve(begin_video, np.ones(10), mode='valid') / 10

    end_video = np.loadtxt('stop_time_' + fname + '.txt')
    end_video = np.convolve(end_video, np.ones(10), mode='valid') / 10

    sz = end_video.shape
    t = np.linspace(0, (len(end_video) * (fps / 10)) / fps, sz[0])

    kp = knee_pt(np.convolve(begin_video, np.ones(10), mode='valid'))

    begin_video = begin_video[:kp]
    xstart = np.linspace(0, (len(begin_video) * (fps / 10)) / fps, len(begin_video))

    pks, locs = find_peaks(begin_video)
    if len(locs) > 0:
        startp = np.argmax(pks)
        startloc = locs[startp]
        begin_time = t[startloc]
    else:
        begin_time = 0

    offset = startloc + (10 * 10) if len(locs) > 0 else 0
    end_video = end_video[offset:]

    end_video = (end_video - np.min(end_video)) / (np.max(end_video) - np.min(end_video))
    f = np.where(end_video < 0.01)[0]
    end_video = end_video[:f[0]]

    kp = knee_pt(end_video) + offset
    end_time = t[kp]

    pt = (end_time - begin_time) * 10
    pt_normal = 12
    isi = 1.31
    alpha = -0.31
    inr = (pt / pt_normal) ** (isi - alpha)

    normal_pt_range = (11, 13.5)
    normal_inr_range = (0.8, 1.1)

    if normal_pt_range[0] <= pt <= normal_pt_range[1]:
        pt_status = "Normal"
    else:
        pt_status = "Abnormal Treatment required"

    if normal_inr_range[0] <= inr <= normal_inr_range[1]:
        inr_status = "Normal"
    else:
        inr_status = "Abnormal Treatment required"

    print('PT: {:.1f} seconds ({})'.format(pt, pt_status))
    print('INR: {:.3f} ({})'.format(inr, inr_status))

if __name__ == "__main__":
    fname = 'video'
    fps = 60
    y, x = 920, 500
    r1, r2 = 200, 350

    extract(fname)
    compute_start_time(fname, fps, y, x, r1, r2)
    compute_stop_time(fname, fps, y, x, r1, r2)
    calculate_pt_and_inr(fname, fps)
