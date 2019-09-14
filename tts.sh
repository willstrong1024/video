#!/bin/bash

dltts() {
	if [ ${#} -ne 1 ]; then
		echo "${0}: dltts: wrong number of arguments"
		exit 1
	fi

	curl -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
		-H "Content-Type: application/json; charset=utf-8" \
		--data "{
			'input':{
				'text':'${1}'
			},
			'voice':{
				'languageCode':'en-gb',
				'name':'en-GB-Wavenet-D',
			},
			'audioConfig':{
				'audioEncoding':'LINEAR16',
			}
		}" "https://texttospeech.googleapis.com/v1/text:synthesize"
}

tts() {
	if [ ${#} -ne 1 ]; then
		echo "${0}: tts: wrong number of arguments"
		exit 1
	fi

	i=0
	for f in $1; do
		input=$(sed "s/'/\\\'/g" "${f}" | sed 's/"/\\\"/g' | sed "s/*//g" | sed 's/\!\{0,1\}\[[^]]*\]([^)]*)//g' | \tr '\n' ' ')
		IFS=$'\n' tmp=$(echo ${input} | fold -s -w5000)

		j=0
		for string in ${tmp[@]}; do
			dltts "${string}" | jq -r ".audioContent" | base64 -d > "/tmp/video/audio/tmp${j}.wav"
			j=$((j + 1))
		done

		sox /tmp/video/audio/tmp*.wav "/tmp/video/audio/$(basename ${f})${i}.wav"
		rm -f /tmp/video/audio/tmp*.wav

		i=$((i + 1))
	done
}

mkdir /tmp/video/audio

tts "/tmp/video/posts/*/body"
tts "/tmp/video/posts/*/head"
