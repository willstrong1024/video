#!/bin/bash

colours=(red green blue magenta)
subreddits=(entitledparents AmItheAsshole tifu MaliciousCompliance)
index=$((RANDOM%=${#subreddits[@]}))

mkdir -p /tmp/video
cd ~/video

./posts.py ${subreddits[${index}]}
./tts.sh
./images.sh
./videos.sh

for f in /tmp/video/posts/post*/head; do
	title="r/$(cat /tmp/video/posts/name) $(cat ${f})"
	length=$(echo ${title} | wc -c)

	if [ ${length} -le 100 ]; then
		break
	fi
done

convert -background black \
	-size 1280x180 -fill ${colours[${index}]} label:"r/$(cat /tmp/video/posts/name)" \
	-size 1280x540 -fill white caption:"$(cat /tmp/video/posts/post0/head)" \
	-append /tmp/video/youtube/thumbnail.png

./upload.py --file /tmp/video/youtube/video.mp4 --title "${title}" --description "${title}" --category 24
./thumbnail.py --video-id "$(cat /tmp/video/youtube/id)" --file /tmp/video/youtube/thumbnail.png
./like.py --video-id "$(cat /tmp/video/youtube/id)"

rm -rf /tmp/video
