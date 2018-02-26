import os
from movie import Movie
from editor import Editor


class MovieCutter:
    def __init__(self, path):
        self.path = path
        self.video_files = []
        self.opening_movie = None
        self.opening = None
        self.closing_movie = None
        self.closing = None

    def run(self):
        self.get_files_to_edit()

        # filter out directories
        self.video_files = [fn for fn in self.video_files if os.path.isfile(os.path.join(self.path, fn))]
        for fn in self.video_files:
            video = Movie(os.path.join(self.path, fn))
            if not video.status:
                continue
            Editor(video,
                   self.opening_movie,
                   self.opening,
                   self.closing_movie,
                   self.closing).run()

    def get_files_to_edit(self):
        self.video_files = os.listdir(self.path)
        self.video_files.sort()
        opening_files = os.listdir(os.path.join(self.path, 'opening'))
        opening_files.sort()
        if len(opening_files) == 1:
            self.opening = os.path.join(self.path, 'opening', opening_files[0])
        elif len(opening_files) == 2:
            self.opening = os.path.join(self.path, 'opening', opening_files[0])
            self.opening_movie = os.path.join(self.path, 'opening', opening_files[1])
        else:
            # TODO throw error
            pass
        closing_files = os.listdir(os.path.join(self.path, 'closing'))
        closing_files.sort()
        if len(closing_files) == 1:
            self.closing = os.path.join(self.path, 'closing', closing_files[0])
        elif len(closing_files) == 2:
            self.closing = os.path.join(self.path, 'closing', closing_files[1])
            self.closing_movie = os.path.join(self.path, 'closing', closing_files[0])
        else:
            # TODO throw error
            pass


if __name__ == '__main__':
    MovieCutter('test').run()
