"""Render every camera shot in shots.json as a 10-beat video segment of the 'play' clip.

usage: python3 render_shots.py OUT_DIR [--parallel N] [--only NAME ...]
Run from cad/crystal-orchestra. Each pass covers the 40-beat loop in four shots;
shot k starts on beat 10k of the song grid.
"""
import argparse
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BEAT = 60 / 143.55
FIRST_BEAT = 0.163
SHOT_BEATS = 10
CADGEN = ["uvx", "--no-config", "--managed-python", "--python", "3.13", "--from", "cadgen==0.7.21", "cadgen"]

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--parallel", type=int, default=3)
ap.add_argument("--only", nargs="*")
args = ap.parse_args()
out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
shots = json.load(open(Path(__file__).with_name("shots.json")))

jobs = []
for pass_shots in shots["passes"].values():
    for k, shot in enumerate(pass_shots):
        if args.only and shot["name"] not in args.only:
            continue
        job = {
            "input": "STEP/crystal_orchestra.step",
            "display": {"mode": "render", "background": {"color": "#10141F"},
                        "floor": {"finish": "glossy", "color": "#10141F"},
                        "lighting": {"quality": "final", "exposure": 0.4},
                        "camera": {"projection": "perspective", "focalLength": shots["focal"]}},
            "animation": {"clip": "play"},
            "video": {"fps": 30, "quality": "high", "start": FIRST_BEAT + k * SHOT_BEATS * BEAT,
                      "seconds": SHOT_BEATS * BEAT},
            "outputs": [{"path": str(out / f"{shot['name']}.mp4"), "width": 1080, "height": 1350,
                         "camera": {"position": shot["position"], "target": shot["target"], "up": [0, 0, 1]}}],
        }
        path = out / f"{shot['name']}.job.json"
        path.write_text(json.dumps(job, indent=1))
        jobs.append((shot["name"], path))


def run(item):
    name, path = item
    r = subprocess.run(CADGEN + ["step", "snapshot", "--job", str(path)], capture_output=True, text=True,
                       env={**os.environ, "CADGEN_TELEMETRY": "0"})
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:]
    return f"{name}: exit {r.returncode} {tail}"


with ThreadPoolExecutor(args.parallel) as pool:
    for line in pool.map(run, jobs):
        print(line, flush=True)
