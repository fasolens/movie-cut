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
import movie

class Editor:
    def __init__(self, video: movie.Movie,
                 opening_movie,
                 opening,
                 closing_movie,
                 closing):
        self.opening_movie = opening_movie
        self.opening = opening
        self.closing_movie = closing_movie
        self.closing = closing