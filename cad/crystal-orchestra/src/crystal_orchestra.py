"""Crystal orchestra: glass-and-gold instruments on a round stage, with a
40-beat clip timed to "Cozy Winter Night" (143.55 BPM, first beat 0.163 s).
"""
from __future__ import annotations

import json

from cadgen import build123d as bd
from cadgen import glb, srgb, step

from orchestra_parts import piano_events, scene_spec

BEAT = 60 / 143.55        # seconds per beat (librosa beat tracking of the song)
FIRST_BEAT = 0.163        # seconds into the song
LOOP_BEATS = 40           # 10 bars; the clip loops seamlessly

MATERIALS = {
    "crystal": {"name": "Crystal", "baseColor": "#E3F1FF", "roughness": 0.04, "metalness": 0.0,
                "clearcoat": 1.0, "clearcoatRoughness": 0.03, "opacity": 0.3},
    "gold": {"name": "Gold", "baseColor": "#E6B54A", "roughness": 0.22, "metalness": 1.0,
             "clearcoat": 0.3, "clearcoatRoughness": 0.1},
    "ivory": {"name": "Ivory", "baseColor": "#F8F5EE", "roughness": 0.35, "metalness": 0.0,
              "clearcoat": 0.4, "clearcoatRoughness": 0.2},
    "ebony": {"name": "Ebony", "baseColor": "#15171C", "roughness": 0.25, "metalness": 0.0,
              "clearcoat": 0.8, "clearcoatRoughness": 0.1},
    "head": {"name": "Drum head", "baseColor": "#F2EDE3", "roughness": 0.5, "metalness": 0.0,
             "opacity": 0.85},
    "hair": {"name": "Bow hair", "baseColor": "#F3EFE6", "roughness": 0.6, "metalness": 0.0},
}

SPEC = scene_spec()


def _assignments():
    by_material = {}
    for p in SPEC["parts"]:
        by_material.setdefault(p.material, []).append("#" + p.label)
    return [{"targets": labels, "material": m} for m, labels in by_material.items()]


def _piano_events():
    return [[b, [SPEC["white_keys"][i] for i in keys]] for b, keys in piano_events()]


DATA = {
    "beat": BEAT, "first": FIRST_BEAT, "loopBeats": LOOP_BEATS,
    "all": [p.label for p in SPEC["parts"]],
    "keys": _piano_events(),
    "harp": SPEC["harp_strings"],
    "harpDir": SPEC["harp_dir"],
    "bows": SPEC["bows"],
    "mallets": SPEC["mallets"],
    "baton": SPEC["baton"],
    "notes": SPEC["notes"],
}

ANIMATION = r"""
const D = %s;
const TAU = 2 * Math.PI;
const L = D.loopBeats * D.beat;

function wrap(x, n) { return ((x %% n) + n) %% n; }

export const clips = {
  play: {
    label: "Orchestra loop (40 beats)",
    duration: L,
    loop: true,
    update(t, m) {
      const u = (t - D.first) / D.beat;            // beats since the song's first beat

      // piano keys: press quickly, release softly
      const dip = {};
      for (const [b, keys] of D.keys) {
        const s = wrap(u - b, D.loopBeats);
        if (s < 1.8) {
          const env = s < 0.1 ? s / 0.1 : Math.exp(-(s - 0.1) * 2.2);
          for (const k of keys) dip[k] = Math.max(dip[k] || 0, env);
        }
      }
      for (const k in dip) m.get(k).translate([0, 0, -0.7 * dip[k]]);

      // harp strings shimmer after a soft pluck
      D.harp.forEach((label, i) => {
        const s = wrap(u - ((i * 7) %% D.loopBeats) * 0.5, D.loopBeats / 2);
        const a = 0.6 * Math.exp(-s * 1.4) * Math.sin(TAU * 2 * s);
        m.get(label).translate(D.harpDir.map((c) => c * a));
      });

      // bows: smooth strokes (violins 4 beats, cello and bass 8 beats)
      D.bows.forEach((bow, i) => {
        const period = i < 2 ? 4 : 8;
        const s = bow.amp * Math.sin(TAU * u / period + i * 0.9);
        const v = bow.dir.map((c) => c * s);
        bow.labels.forEach((p) => m.get(p).translate(v));
      });

      // timpani mallets: a soft bounce on alternate half-time downbeats
      D.mallets.forEach((mallet, i) => {
        const hit = i * 4;
        const d = Math.abs(wrap(u - hit + 4, 8) - 4);  // beats to the nearest hit
        const lift = 16 * (1 - Math.exp(-Math.pow(d / 1.1, 2)));
        mallet.labels.forEach((p) => m.get(p).rotate(mallet.axis, -lift, mallet.pivot));
      });

      // baton: down-up on each half-time beat, a slow sweep across each bar
      const bt = D.baton;
      const lift = 10 * Math.sin(TAU * u / 2);
      const sweep = 14 * Math.sin(TAU * u / 8);
      bt.labels.forEach((p) => {
        m.get(p).rotate(bt.axis_lift, lift, bt.pivot);
        m.get(p).rotate(bt.axis_sweep, sweep, bt.pivot);
      });

      // notes rise from whatever just played, turning as they fade
      for (const n of D.notes) {
        let best = null;
        for (const tr of n.tr) {
          const s = wrap(u - tr.b, D.loopBeats);
          if (s < n.life && (best === null || s < best.s)) best = { s, off: tr.off };
        }
        const h = m.get(n.label);
        if (best === null) { h.visible(false); continue; }
        const p = best.s / n.life;
        const fade = Math.min(1, p / 0.15) * (p > 0.55 ? (1 - p) / 0.45 : 1);
        h.opacity(0.95 * fade);
        h.rotate([0, 0, 1], 35 * Math.sin(TAU * p + n.spin0), n.rest);   // a gentle wobble, mostly facing front
        const sway = 6 * Math.sin(Math.PI * p + n.spin0);
        h.translate([best.off[0] + sway, best.off[1], best.off[2] + 42 * p]);
      }

      // the whole stage turns gently to and fro, once per loop
      const yaw = 12 * Math.sin(TAU * t / L);
      for (const p of D.all) m.get(p).rotate([0, 0, 1], yaw, [0, 0, 0]);
    },
  },
};
""" % json.dumps(DATA)


@step(out="../STEP/crystal_orchestra.step", animation=ANIMATION,
      materials={"definitions": MATERIALS, "assignments": _assignments()})
@glb(out="../GLB/crystal_orchestra.glb")
def crystal_orchestra():
    leaves = []
    for p in SPEC["parts"]:
        shape = p.build()
        if not isinstance(shape, bd.Solid):
            solids = shape.solids()
            shape = solids[0] if len(solids) == 1 else bd.Compound(solids)
            shape.label = p.label
        shape.color = srgb(MATERIALS[p.material]["baseColor"])
        leaves.append(shape)
    return bd.Compound(children=leaves, label="orchestra")


if __name__ == "__main__":
    crystal_orchestra()
