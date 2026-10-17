"""Mini carousel music box: pastel parts, spin joint and an 8 s turn clip (STEP + GLB)."""
from __future__ import annotations

import json

import cadgen
from cadgen import glb, step

from carousel_parts import animal_labels, carousel, rotor_labels

TURN_SECONDS = 8.0
BOB_MM = 2.0           # animals ride up and down on their poles

KINEMATICS = {
    "mates": [
        cadgen.revolute("spin", parent="#base", child="#rotor",
                        origin=(0, 0, 0), direction=(0, 0, 1), limits=(-180, 180)),
    ],
    "poses": {"rest": {"spin": 0}, "quarter": {"spin": 90}},
}

ANIMATION = r"""
const ROTOR = %s;
const ANIMALS = %s;
const T = %s;
const BOB = %s;

export const clips = {
  spin: {
    label: "Turn once (8 s)",
    duration: T,
    loop: true,
    update(t, m) {
      const angle = 360 * t / T;
      Object.values(ANIMALS).forEach((parts, i) => {
        const dz = BOB * Math.sin(2 * Math.PI * (3 * t / T) + i * Math.PI / 3);
        parts.forEach((p) => m.get(p).translate([0, 0, dz]));
      });
      ROTOR.forEach((p) => m.get(p).rotate([0, 0, 1], angle, [0, 0, 0]));
    },
  },
};
""" % (json.dumps(rotor_labels()), json.dumps(animal_labels()), TURN_SECONDS, BOB_MM)

MATERIALS = {
    "definitions": {
        "pastel": {"name": "Glossy pastel plastic", "roughness": 0.35, "metalness": 0.0,
                   "clearcoat": 0.6, "clearcoatRoughness": 0.15},
    },
    "assignments": [{"targets": ["#carousel"], "material": "pastel"}],
}


@step(out="../STEP/carousel.step", kinematics=KINEMATICS, animation=ANIMATION, materials=MATERIALS)
@glb(out="../GLB/carousel.glb")
def carousel_model():
    return carousel()


if __name__ == "__main__":
    carousel_model()
