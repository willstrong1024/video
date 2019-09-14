#!/bin/bash

mkdir -p /tmp/video/images

i=0
for post in /tmp/video/posts/post*; do
	capture-website --element="#t3_$(cat ${post}/id)" --height=10000 "$(cat ${post}/url)" "/tmp/video/images/post${i}.png"
	i=$((i + 1))
done
