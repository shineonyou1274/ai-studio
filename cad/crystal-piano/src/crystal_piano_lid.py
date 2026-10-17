"""Print model: the piano lid, flat on the bed with its pin hole facing up (STL)."""
from __future__ import annotations

from cadgen import stl

from piano_parts import lid_print


@stl(out="../STL/crystal_piano_lid.stl", mesh_tolerance=3e-4)
def crystal_piano_lid():
    lid = lid_print()
    lid.label = "crystal_piano_lid"
    return lid


if __name__ == "__main__":
    crystal_piano_lid()
