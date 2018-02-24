#!/usr/bin/python3

import subprocess
import os
import shutil
import movie
import argparse


# parser = argparse.ArgumentParser(description="Cut movie based on samples of frames.\n"
#                                              "Opening frame - unique frame from the every beginning"
#                                              "of the movie\n"
#                                              "Closing frame - unique frame from the ending of the movie")
# parser.add_argument('videosDir', metavar='V', type=str,
#                     help="Directory where videos to precess are placed")
# # parser.add_argument()
# args = parser.parse_args()
# exit(0)
# TODO make it argument
VIDEO_DIR = "/home/fasolens/Videos/dinopociag"
OPENING_DIR = os.path.join(VIDEO_DIR, 'opening')
CLOSING_DIR = os.path.join(VIDEO_DIR, 'closing')

video_files = os.listdir(VIDEO_DIR)
video_files.sort()
opening_files = os.listdir(OPENING_DIR)
opening_files.sort()
closing_files = os.listdir(CLOSING_DIR)
closing_files.sort()


def clear_dir(*args):
    """
    Clear existing directory from all files and subdirectories.
    If directory it not exist, it is created.

    :rtype: str
    :param args: path to directory as a list of directories separated by comma.
    :return: path to cleared/created directory
    """
    dir_to_clear = os.path.join(*args)
    if os.path.exists(dir_to_clear):
        shutil.rmtree(dir_to_clear)
    os.makedirs(dir_to_clear)
    return dir_to_clear


# TODO check if tool is installed
def extract_frames(video, seek=None, time=None):
    cmd = []
    tool = 'ffmpeg'

    cmd.append(tool)
    if seek is not None:
        cmd.append('-ss')
        cmd.append(seek)

    cmd.append('-i')
    cmd.append(video)

    if time is not None:
        cmd.append('-t')
        cmd.append(time)

    cmd.append('tmp/%06d.jpg')
    # cmd.append('tmp/%06d.png')
    subprocess.run(cmd)


def compare_images(sample_img, img):
    d = subprocess.run(['compare',
                        '-metric',
                        'MAE',
                        sample_img,
                        # '/home/fasolens/work/movie-cut/tmp/{0}'.format(img),
                        img,
                        'null:',
                        '2>&1'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    res = d.stderr.decode('utf-8')
    res = res.split(" ")
    return res[0], img


def get_frame_number(filename):
    fn = filename.split(os.sep)[-1]
    fn = fn.split('.')[0]
    num = int(fn)
    return num


def find_best_frame(frames, frame_step, sample, compare_num, found_frames_number, open_close):
# set variables for loop
    FOUND = False
    FOUND_NO = 0
    found_frames = []
    counter = 0

    for fn in frames[::frame_step]:
        counter = counter + 1
        # if counter % 100 == 1:
            # print(counter, fn)
        file_to_compare = os.path.join('tmp', fn)
        cmp = compare_images(sample, file_to_compare)
        print(cmp[0], file_to_compare)
        with open('open_frame', 'a') as f:
            f.write("{0} {1}\n".format(cmp[0], cmp[1]))
        if float(cmp[0]) < compare_num:
            FOUND = True
            FOUND_NO = FOUND_NO + 1
            print("{} FRAME".format(open_close), cmp[0])
            found_frames.append(cmp)
        else:
            if FOUND:
                if FOUND_NO >= found_frames_number:
                    break
    return min(zip(found_frames))[0][1]


def analyse_frames_opening(path, STARTING_FRAME, BEGIN_FRAME, offset_frame, frame_step, compare_num):
    frame_step = int(frame_step)
    STARTING_FRAME = os.path.join(path, STARTING_FRAME)
    BEGIN_FRAME = os.path.join(path, BEGIN_FRAME)
    result_files = os.listdir('tmp')
    result_files.sort()
    res_files = result_files[offset_frame:]

    # remove log file if exists
    if os.path.exists('open_frame'):
        os.remove('open_frame')

    starting_frame = find_best_frame(res_files, frame_step, STARTING_FRAME, compare_num, 2, "OPENING")
    starting_frame = get_frame_number(starting_frame)

    # precise starting frame
    offset_frame = starting_frame-5*frame_step
    res_files = result_files[offset_frame:]
    starting_frame = find_best_frame(res_files, 1, STARTING_FRAME, compare_num, 2, "OPENING")

    print('BEGIN FRAME: ', starting_frame)
    begin_frame = get_frame_number(starting_frame)+1
    return begin_frame/float(mov.frame_ratio)


def analyse_frames_closing(path, CLOSING_FRAME, offset_frame, frame_step, compare_num):
    frame_step = int(frame_step)
    CLOSING_FRAME = os.path.join(path, CLOSING_FRAME)
    # CLOSE_FRAME = os.path.join(path, CLOSE_FRAME)
    result_files = os.listdir('tmp')
    result_files.sort()
    result_files.reverse()
    res_files = result_files[offset_frame:]

    # remove file if exists
    if os.path.exists('close_frame'):
        os.remove('close_frame')

    closing_frame = find_best_frame(res_files, frame_step, CLOSING_FRAME, compare_num, 1, "CLOSING")
    closing_frame = get_frame_number(closing_frame)

    # precise closing frame
    offset_frame = closing_frame+5*frame_step
    res_files = result_files[len(result_files)-offset_frame:]
    closing_frame = find_best_frame(res_files, 1, CLOSING_FRAME, compare_num, 2, "CLOSING")

    print('CLOSING FRAME: ', closing_frame)
    close_frame = get_frame_number(closing_frame)+1
    return close_frame/float(mov.frame_ratio)


# TODO check if tool is installed
def cut_movie(video, seek=None, time=None, output=None):
    cmd = []
    tool = 'ffmpeg'

    cmd.append(tool)
    if seek is not None:
        cmd.append('-ss')
        cmd.append(str(seek))

    cmd.append('-i')
    cmd.append(video)

    cmd.append('-c:v')
    cmd.append('copy')

    cmd.append('-c:a')
    cmd.append('copy')

    if time is not None:
        cmd.append('-t')
        cmd.append(str(time))

    if output is None:
        cmd.append('out.mp4')
    else:
        cmd.append(output)
    print(cmd)
    subprocess.run(cmd)


for fn in video_files:
    if os.path.isfile(os.path.join(VIDEO_DIR, fn)):
        VIDEO_TO_EDIT = os.path.join(VIDEO_DIR, fn)
        mov = movie.Movie(VIDEO_TO_EDIT)
        print(mov.filename)
        # clear_dir('tmp')
        print('EXTRACT FRAMES')
        # extract_frames(mov.path)
        print('SEARCHING OPENING')
        seek_time = analyse_frames_opening(os.path.join('/',
                                                        'home',
                                                        'fasolens',
                                                        'Videos',
                                                        'dinopociag',
                                                        'opening'),
                                           '00408.png',
                                           '00382.png',
                                           36000,
                                           float(mov.frame_ratio),
                                           7500)
        print('SEEK_TIME = ', seek_time)
        print('SEARCHING CLOSING')
        duration_time = analyse_frames_closing(os.path.join('/',
                                                            'home',
                                                            'fasolens',
                                                            'Videos',
                                                            'dinopociag',
                                                            'closing'),
                                               '00229.png',
                                               11000, float(mov.frame_ratio),
                                               7500)
        duration_time = duration_time-seek_time
        print('DURATION_TIME = ', duration_time)
        print('CUTTING')
        cut_movie(mov.path,
                  seek=seek_time,
                  time=duration_time,
                  output="{0}.mp4".format(mov.filename))

