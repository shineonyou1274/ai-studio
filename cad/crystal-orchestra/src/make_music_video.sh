#!/usr/bin/env bash
# Loop the rendered 40-beat clip under the full song and mux the audio.
# usage: make_music_video.sh LOOP.mp4 SONG.mp3 OUT.mp4
set -euo pipefail
loop="$1"; song="$2"; out="$3"

beat=$(python3 -c "print(60/143.55)")
loop_s=$(python3 -c "print(40*60/143.55)")                    # exact loop length in the music
frames=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$loop")
rate=$(python3 -c "print($frames/$loop_s)")                    # play the loop at exactly 40 beats
song_s=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$song")
fade_out=$(python3 -c "print(max(0, $song_s - 3))")

ffmpeg -v error -y \
  -stream_loop -1 -r "$rate" -i "$loop" -i "$song" \
  -filter_complex "[0:v]fps=30,format=yuv420p,fade=t=in:st=0:d=1.2,fade=t=out:st=${fade_out}:d=3[v];[1:a]afade=t=out:st=${fade_out}:d=3[a]" \
  -map "[v]" -map "[a]" -t "$song_s" \
  -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 256k -movflags +faststart "$out"
echo "wrote $out (${song_s}s, loop ${frames} frames at ${rate} fps = ${loop_s}s, beat ${beat}s)"
