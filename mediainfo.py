import subprocess


class MediaInfo:
    def __init__(self, path):
        subp = subprocess.run(['mediainfo', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(subp.stdout.decode('utf-8'))


if __name__ == '__main__':
    mi = Mediainfo('/home/fasolens/Videos/wędrówki_z_dinozaurami_2013.mp4')
