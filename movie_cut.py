#!/usr/bin/python3

import subprocess
import os
import shutil
import movie

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
# d = subprocess.run(['ls', '-l', VIDEO_DIR], stdout=subprocess.PIPE)
# print(d.stdout.decode('utf-8'))
# print(video_files)


def clear_dir(*args) -> str:
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

    cmd.append('tmp/%06d.png')
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


def analyse_frames_opening(path, STARTING_FRAME, BEGIN_FRAME):
    STARTING_FRAME = os.path.join(path, STARTING_FRAME)
    BEGIN_FRAME = os.path.join(path, BEGIN_FRAME)
    result_files = os.listdir('tmp')
    result_files.sort()
    res_files = result_files[7000:]
    if os.path.exists('open_frame'):
        os.remove('open_frame')
    FOUND = False
    FOUND_NO = 0
    found_frames = []
    for fn in res_files:
        file_to_compare = os.path.join('tmp', fn)
        cmp = compare_images(STARTING_FRAME, file_to_compare)
        # print(cmp[0], file_to_compare)
        if float(cmp[0]) < 1000:
            FOUND = True
            FOUND_NO = FOUND_NO + 1
            print("OPENING FRAME", cmp[0])
            with open('open_frame', 'a') as f:
                f.write("{0} {1}\n".format(cmp[0], cmp[1]))
            found_frames.append(cmp)
        else:
            if FOUND and FOUND_NO > 1:
                break
    starting_frame = min(zip(found_frames))[0][1]
    starting_frame = (get_frame_number(starting_frame))
    res_files = result_files[:starting_frame]
    res_files.reverse()
    FOUND = False
    FOUND_NO = 0
    frms = 0
    for fn in res_files:
        file_to_compare = os.path.join('tmp', fn)
        cmp = compare_images(BEGIN_FRAME, file_to_compare)
        # print(cmp[0], file_to_compare)
        if float(cmp[0]) < 4000:
            FOUND = True
            FOUND_NO = FOUND_NO + 1
            print("REVERSE BEGIN FRAME: ", cmp[0])
            with open('open_frame', 'a') as f:
                f.write("{0} {1}\n".format(cmp[0], cmp[1]))
            found_frames.append(cmp)
        else:
            if frms > 100 or FOUND and FOUND_NO > 1:
                break
        frms = frms + 1
    begin_frame = min(zip(found_frames))[0][1]
    print('BEGIN FRAME: ', begin_frame)
    begin_frame = get_frame_number(begin_frame)+1
    return begin_frame/float(mov.frame_ratio)


def get_frame_number(filename):
    fn = filename.split(os.sep)[-1]
    fn = fn.split('.')[0]
    num = int(fn)
    return num


def analyse_frames_closing(path, CLOSING_FRAME, BEGIN_FRAME=None):
    CLOSING_FRAME = os.path.join(path, CLOSING_FRAME)
    if BEGIN_FRAME is not None:
        BEGIN_FRAME = os.path.join(path, BEGIN_FRAME)
    result_files = os.listdir('tmp')
    result_files.sort()
    result_files.reverse()
    res_files = result_files[10000:]
    if os.path.exists('close_frame'):
        os.remove('close_frame')
    FOUND = False
    FOUND_NO = 0
    found_frames = []
    for fn in res_files:
        file_to_compare = os.path.join('tmp', fn)
        cmp = compare_images(CLOSING_FRAME, file_to_compare)
        # print(cmp[0], file_to_compare)
        if float(cmp[0]) < 1000:
            FOUND = True
            FOUND_NO = FOUND_NO + 1
            print("CLOSING FRAME: ", cmp[0])
            with open('open_frame', 'a') as f:
                f.write("{0} {1}\n".format(cmp[0], cmp[1]))
            found_frames.append(cmp)
        else:
            if FOUND and FOUND_NO > 1:
                break
    closing_frame = min(zip(found_frames))[0][1]
    closing_frame = (get_frame_number(closing_frame))
    print(closing_frame)

    if BEGIN_FRAME is not None:
        res_files = result_files[:closing_frame]
        res_files.reverse()
        FOUND = False
        FOUND_NO = 0
        frms = 0
        for fn in res_files:
            file_to_compare = os.path.join('tmp', fn)
            cmp = compare_images(BEGIN_FRAME, file_to_compare)
            # print(cmp[0], file_to_compare)
            if float(cmp[0]) < 4000:
                FOUND = True
                FOUND_NO = FOUND_NO + 1
                print("### ", cmp[0])
                with open('open_frame', 'a') as f:
                    f.write("{0} {1}\n".format(cmp[0], cmp[1]))
                found_frames.append(cmp)
            else:
                if frms > 100 or FOUND and FOUND_NO > 1:
                    break
            frms = frms + 1
        begin_frame = min(zip(found_frames))[0][1]
        print('###', begin_frame)
        begin_frame = get_frame_number(begin_frame)+1

    return closing_frame/float(mov.frame_ratio)


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
    if os.path.isfile(fn):
        VIDEO_TO_EDIT = os.path.join(VIDEO_DIR, fn)
        mov = movie.Movie(VIDEO_TO_EDIT)
        print(mov.filename)
        clear_dir('tmp')
        extract_frames(mov.path)
        seek_time = analyse_frames_opening(os.path.join('/',
                                            'home',
                                            'fasolens',
                                            'Videos',
                                            'dinopociag',
                                            'opening'),
                               '00408.png',
                               '00382.png')
        print('SEEK_TIME = ', seek_time)
        duration_time = analyse_frames_closing(os.path.join('/',
                                                            'home',
                                                            'fasolens',
                                                            'Videos',
                                                            'dinopociag',
                                                            'closing'),
                                               '00229.png')
        duration_time = duration_time-seek_time
        print('DURATION_TIME = ', duration_time)
        cut_movie(mov.path,
                  seek=seek_time,
                  time=duration_time,
                  output="{0}.mp4".format(mov.filename))


# # # # with open('open_frame', 'r') as f:
# # # #     lines = f.readlines()
# # # #
# # # # frm = dict()
# # # # for line in lines:
# #
# # # #     l = line.split(" ")
# # # #     frm[l[-1].strip()] = l[0].strip()
# # # #
# # # # # maximum = max(frm, key=frm.get())
# # # # # print(maximum, frm[maximum])
# # # #
# # # # minimum = min(frm, key=frm.get)
# # # # print(minimum, frm[minimum])
# # # #
# # # # frame_number = minimum.rstrip(".png")
# # # # frame_number = int(frame_number)-26
# # # # offset = frame_number/25
# # # # print(offset)

#
# # subprocess.run(['ffmpeg',
# #                 '-ss', '05:{0}'.format(offset),
# #                 '-i', VIDEO_TO_EDIT,
# #                 '-c:v', 'copy',
# #                 '-c:a', 'copy',
# #                 'out.mp4'])
# # shutil.move('out.mp4', 'out.ts')
#
# # # # if os.path.exists('tmp'):
# # # #     shutil.rmtree('tmp')
# # # # os.mkdir('tmp')
# # # #
# # # # subprocess.run(['ffmpeg', '-ss', '25:00', '-i', 'out.ts', '-t', '02:30', 'tmp/%06d.png'])
# # # #
# # # # res_files = os.listdir('tmp')
# # # # res_files.sort()
# # # # if os.path.exists('close_frame'):
# # # #     os.remove('close_frame')
# # # # for fn in res_files:
# # # #     file_to_compare = os.path.join('tmp', fn)
# # # #     with open('close_frame', 'a') as f:
# # # #         print(file_to_compare)
# # # #         d = subprocess.run(['compare',
# # # #                             '-metric',
# # # #                             'MAE',
# # # #                             '/home/fasolens/Videos/dinopociag/closing/00229.png',
# # # #                             '/home/fasolens/work/movie-cut/tmp/{0}'.format(fn),
# # # #                             'null:',
# # # #                             '2>&1'],
# # # #                            stdout=subprocess.PIPE,
# # # #                            stderr=subprocess.PIPE)
# # # #         f.write("{0} {1}\n".format(d.stderr.decode('utf-8'), fn))
# # # #
# # # # with open('close_frame', 'r') as f:
# # # #     lines = f.readlines()
# # # #
# # # # frm_c = dict()
# # # # for line in lines:
# # # #     l = line.split(" ")
# # # #     frm_c[l[-1].strip()] = l[0].strip()
# # # #
# # # # minimum = min(frm_c, key=frm_c.get)
# # # # print(minimum, frm_c[minimum])
# # # #
# # # # frame_number = minimum.rstrip(".png")
# # # # frame_number = int(frame_number)
# # # # offset = frame_number/25
# # # # print(offset)
# # # # # minutes = int(offset/60)
# # # # # secs = offset-minutes*60
# # # # off = 25*60+offset
# # # # print("{0:.2f}".format(off))
# # # # # mm = 25+minutes
# # # # # print('{0}:{1:.2f}'.format(mm, float(secs)))
# # # # subprocess.run(['ffmpeg',
# # # #                 '-i', 'out.ts',
# # # #                 '-c:v', 'copy',
# # # #                 '-c:a', 'copy',
# # # #                 # '-t', '{0:.2f}'.format(off),
# # # #                 '-t', '1500.00',
# # # #                 'final.mp4'])
# # # #
# # # # shutil.move('final.mp4', 'final.ts')
# # # en = 1897.36 - 313.44
# # # subprocess.run(['ffmpeg',
# # #                 '-ss', '313.44',
# # #                 '-i', VIDEO_TO_EDIT,
# # #                 '-c:v', 'copy',
# # #                 '-c:a', 'copy',
# # #                 '-t', str(en),
# # #                 'final.mp4'])
# # # shutil.move('final.mp4', 'final.ts')
