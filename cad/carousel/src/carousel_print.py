"""Print model: the carousel fused into one solid (STL)."""
from __future__ import annotations

from cadgen import stl

from carousel_parts import carousel


@stl(out="../STL/carousel_print.stl", mesh_tolerance=3e-4)
def carousel_print():
    solids = carousel().solids()
    body = solids[0]
    for s in solids[1:]:
        body = body + s
    body.label = "carousel_print"
    return body


if __name__ == "__main__":
    carousel_print()
