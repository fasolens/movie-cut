# movie-cut

## Overview

Simple tool to cut movie/animation/TV shows from longer recordings.

Cut is based on opening frame and closing frame. 
Opening frame - frame from opening of animation. The frame is the same in all episodes.
Closing frame - frame from closing of animation. The frame is the same in all episodes.

## Instalation of tools

Download boost

```text
./bootstrap.sh
./b2
sudo ./b2 install
```

With these commands boost will be compiled and installed under `/usr/local/lib/`

Download PythonMagick from
https://www.imagemagick.org/download/python/

```text
./configure
make
sudo make install
```

PythonMagick is python2 only.

Possibly can use: https://packages.debian.org/stretch/python3-pythonmagick
