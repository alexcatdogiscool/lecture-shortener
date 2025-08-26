import os
import soundfile as sf
import numpy as np
import time
import sys

"""
script.py output_fps auto_cutoff input_filename
"""

if len(sys.argv) != 4:
    print("ERROR. invalid arguments.\nCorrect usage:\nscript.py output_fps(number) auto_cutoff(True/False) input_filename")
    exit()


start_time = time.time()
FPS = int(sys.argv[1])
CUTOFF_VOLUME = 0
CUTOFF_PERCENT_BELOW = 0.20
FILENAME = sys.argv[3]
frame_dir = "frames"
pair_dir = "pairs"
os.makedirs(frame_dir, exist_ok=True)
os.makedirs(pair_dir, exist_ok=True)

print(f"Starting processing of video {FILENAME}\n")

### ask for cutoff volume ##
print("getting cutoff volume")
os.system(f"ffmpeg -i {FILENAME} -y full_audio.wav")
print(os.system("ls -laR"))
data, s = sf.read("full_audio.wav")
rms = np.sqrt(np.mean(data**2))
print(f"the rms of the audio is: {rms}")
if sys.argv[2].lower() == "true":
    CUTOFF_VOLUME = rms - (rms*CUTOFF_PERCENT_BELOW)
    print(f"Cutoff volume automatically set to {CUTOFF_VOLUME}.\n")
else:
    CUTOFF_VOLUME = float(input("enter the cutoff volume.\nFrames with a lower volume than this will be cut: "))


###  reduce video fps to desired number ###
print("reducing the framerate")
os.system(f"ffmpeg -i {FILENAME} -r {FPS} -ac 1 -loglevel quiet -y frame_adjusted.mp4")


### save individual frame images and audio clip pairs into files ###

#delete contents of frame directory

print("extracting frames")

if os.path.exists(frame_dir):
    for item in os.listdir(frame_dir):
        item_path = os.path.join(frame_dir, item)
        os.remove(item_path)

os.system(f"ffmpeg -y -i frame_adjusted.mp4 -loglevel quiet -qscale:v 2 {frame_dir}/frame_%05d.png")#get all frame pngs
os.system(f"ffmpeg -y -i frame_adjusted.mp4 -loglevel quiet -ac 1 full_audio.wav")#get the audio


print("measuring volume")

num_frames = int(os.listdir(frame_dir)[-1].split("_")[1].split(".")[0])
keep_frames = []

data, sr = sf.read("full_audio.wav")
samples_per_frame = sr // FPS

for i in range(num_frames-1):
    out_path = os.path.join(frame_dir, f"audio_{i:05d}.wav")
    start = i*samples_per_frame
    end = start + samples_per_frame
    clip = data[start:end]
    rms = np.sqrt(np.mean(clip**2))
    if rms > CUTOFF_VOLUME:
        keep_frames.append(i)
        sf.write(out_path, clip, sr)

### merge all the marked frames ###

print("merge the frames")
ff = open("fconcat.txt", 'w')
af = open("aconcat.txt", 'w')

for i in keep_frames:
    ff.write(f"file '{frame_dir}/frame_{i+1:05d}.png'\nduration {1/FPS}\n")
    af.write(f"file '{frame_dir}/audio_{i:05d}.wav'\n")

ff.close()
af.close()

os.system(f"ffmpeg -f concat -safe 0 -i fconcat.txt -vsync vfr -pix_fmt yuv420p -loglevel quiet -y foutput.mp4")
os.system(f"ffmpeg -f concat -safe 0 -i aconcat.txt -c copy -loglevel quiet -y aoutput.wav")

os.system(f"ffmpeg -i foutput.mp4 -i aoutput.wav -loglevel quiet -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -y {FILENAME.split('.')[0]}_shortened.mp4")

### cleaning up ###

print("cleaning up")
os.remove("foutput.mp4")
os.remove("aoutput.wav")
os.remove("frame_adjusted.mp4")
os.remove("full_audio.wav")
os.remove("aconcat.txt")
os.remove("fconcat.txt")
if os.path.exists(frame_dir):
    for item in os.listdir(frame_dir):
        item_path = os.path.join(frame_dir, item)
        os.remove(item_path)
os.rmdir("frames")
if os.path.exists(pair_dir):
    for item in os.listdir(pair_dir):
        item_path = os.path.join(pair_dir, item)
        os.remove(item_path)
os.rmdir("pairs")
print("done deleting")
print("DONE!")
end_time = time.time()
print(f"processing of video {FILENAME} finished in {end_time - start_time} seconds.\n")