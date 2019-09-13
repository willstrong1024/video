#!/bin/bash

n=$(find /tmp/video/posts/post* -maxdepth 0 | wc -l)
t=0

mkdir /tmp/video/videos
mkdir /tmp/video/youtube

i=0
while [ ${i} -lt ${n} ]; do
	sox "/tmp/video/audio/head${i}.wav" "/tmp/video/audio/body${i}.wav" "/tmp/video/audio/post${i}.wav"
	i=$((i + 1))
done

i=0
while [ ${i} -lt ${n} ] && [ ${t} -lt 600 ]; do
	ffmpeg -loop 1 -i "/tmp/video/images/post${i}.png" -filter_complex "color=black:s=1920x1080[bg];[bg][0]overlay=y='-floor(t*h/ $(soxi -D "/tmp/video/audio/post${i}.wav")/H)*H':x=(W-w)/2" -i "/tmp/video/audio/post${i}.wav" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 128k -shortest -pix_fmt yuv420p "/tmp/video/videos/post${i}.mp4"
	echo "file 'post${i}.mp4'" >> /tmp/video/videos/list

	length=$(printf %.0f $(ffprobe -i "/tmp/video/videos/post${i}.mp4" -show_entries format=duration -v quiet -of csv="p=0"))
	t=$((t + length))

	i=$((i + 1))
done

ffmpeg -f concat -i /tmp/video/videos/list -c copy /tmp/video/youtube/video.mp4
