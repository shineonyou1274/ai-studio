"""Print model: the same crystal piano fused into one closed solid (STL)."""
from __future__ import annotations

from cadgen import stl

from piano_parts import parts


@stl(out="../STL/crystal_piano_print.stl", mesh_tolerance=3e-4)
def crystal_piano_print():
    shapes = list(parts().values())
    body = shapes[0]
    for s in shapes[1:]:
        body = body + s
    body.label = "crystal_piano_print"
    return body


if __name__ == "__main__":
    crystal_piano_print()
