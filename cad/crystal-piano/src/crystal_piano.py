"""Display model: transparent crystal grand piano with glass finishes (GLB)."""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, srgb, step

from piano_parts import parts

CRYSTAL = {"name": "Clear crystal", "baseColor": "#EAF6FF", "roughness": 0.03,
           "metalness": 0.0, "clearcoat": 1.0, "clearcoatRoughness": 0.02, "opacity": 0.32}
SMOKE = {"name": "Smoke crystal", "baseColor": "#3A4656", "roughness": 0.05,
         "metalness": 0.0, "clearcoat": 1.0, "clearcoatRoughness": 0.02, "opacity": 0.7}


@step(out="../STEP/crystal_piano.step", materials={
    "definitions": {"crystal": CRYSTAL, "smoke": SMOKE},
    "assignments": [
        {"targets": ["#case", "#music_desk", "#lid", "#prop_stick", "#white_keys", "#legs", "#lyre"],
         "material": "crystal"},
        {"targets": ["#black_keys"], "material": "smoke"},
    ],
})
@glb(out="../GLB/crystal_piano.glb")
def crystal_piano():
    children = []
    for label, shape in parts().items():
        smoke = label == "black_keys"
        color = srgb("#3A4656") if smoke else srgb("#EAF6FF")  # opacity comes from the material
        if label in ("black_keys", "legs"):
            leaves = []
            for k, solid in enumerate(shape.solids()):
                solid.label = f"{label}_{k + 1}"
                solid.color = color
                leaves.append(solid)
            node = bd.Compound(children=leaves)
        else:
            node = shape
            node.color = color
        node.label = label
        children.append(node)
    piano = bd.Compound(children=children)
    piano.label = "crystal_piano"
    return piano


if __name__ == "__main__":
    crystal_piano()
