"""1. Search for frame from th beginning of the movie. Skipping by 1 second (frame rate)
2. If found one frame in limit
    2.1. Back 100 frames back (or to the beginning) and search with more precise every 1 frame.
    2.2. All found frames add to list and get the best match

New algorithm
Get list of files to analyse.
Extract frames from movie.
if frames_number = 0
    Get number of frames -> current_frame_number
if current_frame_number <> frames_number/+/-/(10% -
Get two frames for opening
    One frame is from movie, the next one is just before movie
and two for closing
    One frame is from movie, the next one is just after movie


"""
import os

class Movie_cutter:
    def __init__(self, path):
        self.path = path
        self.video_files = []
        self.opening_files = []
        self.closing_files = []

    def run(self):
        files_to_edit = self.get_files_to_edit()
        for fn in files_to_edit:
            self.edit(fn)

    def get_files_to_edit(self):
        self.video_files = os.listdir(self.path)
        self.video_files.sort()
        self.opening_files = os.listdir(os.path.join(self.path, 'opening'))
        self.opening_files.sort()
        self.closing_files = os.listdir(os.path.join(self.path, 'closing'))
        self.closing_files.sort()

