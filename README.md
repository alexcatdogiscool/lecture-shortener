# lecture-shortener

this program is intended to be used to cut out dead air in lectures so the time can be reduced and you can watch them faster.
it will work with any video though.

# Usage
in the directory, run "python poc.py desired_fps(number) auto_cutoff(boolean) path_to_video"

the desired fps value sets the output FPS. if the video is just a lecturer reading slides you can set this to something low like 5 or so.
lower frame rates will process videos faster.

the auto_cutoff parameter sets weather to let the program automatically find the volume at which to remove frames.
be default, it is set to 20% below the RMS average of the entire videos audio, meaning any frame below that volume will be cut.

## processing
on my PC, a 1 hour lecture set with an FPS of 5 takes around 3 minutes to process.
processing time is linear to video leangth
results will vary based off of your computers cpu and the amount of dead air in the video

# results
For my lectures, i can reliably cut off 40% of the length, meaning, 50 minutes -> 30 minutes.