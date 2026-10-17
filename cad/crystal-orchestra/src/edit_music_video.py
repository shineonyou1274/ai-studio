"""Cut the rendered camera shots to the song's beat grid and add the music.

usage: python3 edit_music_video.py SHOTS_DIR SONG.mp3 OUT.mp4 [--work DIR]

Shot k of a pass covers beats 10k..10k+10 of the 40-beat loop. Pass A plays
on even repeats of the loop and pass B on odd ones, so the camera changes
every 10 beats (about 4.2 s) and never repeats back to back. Each shot gets a
slow digital push-in or pull-out. A title fades in over the opening shot.
"""
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

BEAT = 60 / 143.55
FIRST_BEAT = 0.163
LOOP_BEATS, SHOT_BEATS = 40, 10
FPS = 30
W, H = 1080, 1350
TITLE_FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SUB_FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Light.otf"

ap = argparse.ArgumentParser()
ap.add_argument("shots"); ap.add_argument("song"); ap.add_argument("out")
ap.add_argument("--work", default=None)
ap.add_argument("--passes", nargs="*", help="use only these passes (e.g. A for a preview)")
args = ap.parse_args()
shots_dir = Path(args.shots)
work = Path(args.work or shots_dir / "edit"); shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
plan = json.load(open(Path(__file__).with_name("shots.json")))
if args.passes:
    plan["passes"] = {k: v for k, v in plan["passes"].items() if k in args.passes}


def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)


# 1. push-in / pull-out on each shot, written out as JPEG frames
frames = {}
for pname, shots in plan["passes"].items():
    for k, shot in enumerate(shots):
        src = shots_dir / f"{shot['name']}.mp4"
        n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                                "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(src)],
                               capture_output=True, text=True, check=True).stdout.strip())
        z = shot.get("zoom", 1.0)
        z0, z1 = (1.0, z) if z >= 1 else (1 / z, 1.0)
        zexpr = f"{z0}+({z1}-{z0})*on/{max(n - 1, 1)}"
        d = work / shot["name"]; d.mkdir()
        ff("-i", str(src), "-vf",
           f"scale={2*W}:{2*H}:flags=lanczos,zoompan=z='{zexpr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
           f":s={W}x{H}:fps={FPS}", "-q:v", "2", str(d / "%04d.jpg"))
        frames[(pname, k)] = sorted(d.glob("*.jpg"))
        print(f"{shot['name']}: {n} frames, zoom {z0:.3f}->{z1:.3f}", flush=True)

# 2. pick a frame for every output frame of the song
song_s = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                               args.song], capture_output=True, text=True, check=True).stdout)
total = int(math.floor(song_s * FPS))
seq = work / "seq"; seq.mkdir()
passes = list(plan["passes"])
for i in range(total):
    u = (i / FPS - FIRST_BEAT) / BEAT
    r = math.floor(u / LOOP_BEATS)
    q = u - r * LOOP_BEATS
    k = min(int(q // SHOT_BEATS), 3)
    pname = passes[r % len(passes)] if r >= 0 else passes[0]
    shot_frames = frames[(pname, k)]
    f = min(len(shot_frames) - 1, max(0, round((q - k * SHOT_BEATS) * BEAT * FPS)))
    (seq / f"{i:05d}.jpg").symlink_to(shot_frames[f].resolve())

# 3. encode with the song, fades and an opening title
fade_out = max(0.0, song_s - 3)
title = (f"drawtext=fontfile={TITLE_FONT}:text='Cozy Winter Night':fontsize=86:fontcolor=0xF3D58A:"
         f"x=(w-text_w)/2:y=h*0.11:alpha='if(lt(t,0.8),0,if(lt(t,2),(t-0.8)/1.2,if(lt(t,4.4),1,if(lt(t,5.6),(5.6-t)/1.2,0))))',"
         f"drawtext=fontfile={SUB_FONT}:text='a crystal orchestra':fontsize=40:fontcolor=0xE3F1FF:"
         f"x=(w-text_w)/2:y=h*0.11+108:alpha='if(lt(t,1.3),0,if(lt(t,2.5),(t-1.3)/1.2,if(lt(t,4.4),0.85,if(lt(t,5.6),0.85*(5.6-t)/1.2,0))))'")
ff("-framerate", str(FPS), "-i", str(seq / "%05d.jpg"), "-i", args.song,
   "-filter_complex", f"[0:v]{title},format=yuv420p,fade=t=in:st=0:d=1.2,fade=t=out:st={fade_out}:d=3[v];"
                      f"[1:a]afade=t=out:st={fade_out}:d=3[a]",
   "-map", "[v]", "-map", "[a]", "-t", str(song_s),
   "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", args.out)
print(f"wrote {args.out}: {total} frames, {song_s:.2f}s")
