from pymediainfo import MediaInfo
import os

class Movie:
    def __init__(self, path_to_file):
        self.path = path_to_file
        self.filename = path_to_file.split(os.sep)[-1]
        self.media = MediaInfo.parse(self.path)
        self.video = self.get_video()
        self.frame_ratio = self.get_frame_ratio()
        self.duration = self.get_duration()  # in secs

    def get_video(self):
        tracks = self.media.tracks
        video_track = [track for track in tracks if track.track_type == 'Video']
        if len(video_track) == 1:
            video_track = video_track[0]
        return video_track

    def get_frame_ratio(self):
        return self.video.frame_rate

    def get_duration(self):
        return self.video.duration/1000


if __name__ == '__main__':
    m = Movie('/home/fasolens/Videos/wędrówki_z_dinozaurami_2013.mp4')
    print(m.frame_ratio)
