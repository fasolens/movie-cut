# Commands

## avconv

sudo apt-get install libav-tools

avconv -i my_awesome_video.mp4 -r 30 -f image2 %04d.png
-i - video
-r / frame-rate - number of frames by second
-f - output as image

avconv -i my_awesome_video.mp4 -r 30 -ss 00:02:02 -t 00:00:03 -f image2 %04d.png
-ss - start stream time -> offset
-t - duration of capturing

## ffmpeg

ffmpeg -ss 05:00 -i <input> -t 05:00 filename%05d.png

## cvlc

vlc "pathtovideo" --video-filter=scene --vout=dummy --start-time=300 --stop-time=600 --scene-ratio=250 --scene-path=”pathtosaveimages” vlc://quit
cvlc "dinopociąg-03.14-78-264-60q.mp4" --video-filter=scene --vout=dummy --stop-time=60 --scene-ratio=1 --scene-path=5 vlc://quit
cvlc "dinopociąg-03.14-78-264-60q.mp4" --video-filter=scene --vout=dummy --stop-time=60 --scene-ratio=1 --scene-path=5 vlc://quit

## mplayer

mplayer -ao null -vo png input_file
mplayer -nosound -vo png:z=9 input_file

## tools

### imagemagick

#### Delegates to install

http://www.imagemagick.org/download/delegates/
http://www.imagemagick.org/download/delegates/jpegsrc.v9b.tar.gz

convert image1 image2 -compose Difference -composite \
            -colorspace gray -verbose  info: |\
       sed -n '/statistics:/,/^  [^ ]/ p'

convert image1 image2 -compose Difference -composite \
           -colorspace gray -format '%[fx:mean*100]' info:

convert image1 image2 -compose Difference -composite \
           -colorspace gray -format '%[mean]' info:

compare -metric MAE image1 image2 null: 2>&1


for a in {0..9}; do for b in {0..9}; do for c in {0..9}; do for d in {0..9}; do for e in {0..9}; do echo "2/$a$b$c$d$e.png"; compare -metric MAE 1/00275.png "2/$a$b$c$d$e.png" null: 2>&1; echo ""; done; done; done; done; done;

-ss PARAMETER BEFORE -i PARAMETER
ffmpeg  -i TV_RECORDING.ts -ss 05:01 -t 01:00 1/%05d.png

CUT
ffmpeg -ss 16.00 -i dinopociąg-03.09-66-264-60q.mp4 -t 15.00 -c:v copy -c:a copy out.mp4


