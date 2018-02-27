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
import subprocess
import os


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
        self.video = video

    def compare_images(self, sample_img: str, current_img: str) -> (int, str):
        """Compare two images and return tuple of a comparison vector and path to second image

        :param sample_img: path to first image
        :type sample_img: str
        :param current_img: path to second image
        :type current_img: str
        :return: (vector of comparison, path to current_imt)
        :rtype: (int, str)
        """
        d = subprocess.run(['compare',
                            '-metric',
                            'MAE',
                            sample_img,
                            current_img,
                            'null:',
                            '2>&1'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        res = d.stderr.decode('utf-8')
        res = res.split(" ")
        return res[0], current_img

    def get_frame_number_from_filename(self, fn: str) -> int:
        """Converts filename to number of frame

        :param fn: path to file
        :type fn: str
        :return: frame number
        :rtype: int
        """
        fn = fn.split(os.sep)[-1]
        fn = fn.split('.')[0]
        num = int(fn)
        return num

    def find_frame(self,
                   frames,  # list of frames
                   sample_frame,  # path
                   opening_offset=0,  # int
                   closing_offset=0,
                   frame_step=1,  # int
                   compare_number=7500):  # float
        FOUND = False
        found_frames = []

        for fn in frames[::frame_step]:
            file_to_compare = os.path.join('tmp', fn)
            compare_result = self.compare_images(sample_frame, file_to_compare)
            if float(compare_result[0]) < compare_number:
                FOUND = True

    def find_opening_frame(self,
                           frames,
                           opening_offset):
        self.find_frame(frames,
                        self.opening,
                        opening_offset=opening_offset)

    def find_opening_movie_frame(self,
                                 frames):
        self.find_frame(frames,
                        self.opening_movie)

    def find_opening(self,
                     frames,
                     opening_offset):
        # if self.opening_movie:
        #     self.find_opening_movie_frame(frames)
        self.find_opening_frame(frames,
                                opening_offset)

    def find_closing_frame(self,
                           frames,
                           closing_offset):
        self.find_frame(frames,
                        self.closing,
                        closing_offset=closing_offset)

    def find_closing_movie_frame(self,
                                 frames):
        self.find_frame(frames,
                        self.closing_movie)

    def find_closing(self,
                     frames,
                     closing_offset):
        if self.closing_movie:
            self.find_closing_movie_frame(frames)
        self.find_closing_frame(frames,
                                closing_offset)

    def cut(self):
        pass

    def run(self,
            opening_offset=None,
            closing_offset=None):
        frames = os.listdir('tmp')
        frames.sort()
        self.find_opening(frames,
                          opening_offset)
        self.find_closing(frames,
                          closing_offset)
        self.cut()
