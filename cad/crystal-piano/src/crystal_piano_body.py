"""Print model: the piano body without its lid, fused into one solid (STL).

Print upright on the feet. The lid is a separate print
(crystal_piano_lid.py) that glues onto the angled seat and prop-stick pin.
"""
from __future__ import annotations

from cadgen import stl

from piano_parts import parts


@stl(out="../STL/crystal_piano_body.stl", mesh_tolerance=3e-4)
def crystal_piano_body():
    shapes = [s for label, s in parts().items() if label != "lid"]
    body = shapes[0]
    for s in shapes[1:]:
        body = body + s
    body.label = "crystal_piano_body"
    return body


if __name__ == "__main__":
    crystal_piano_body()
