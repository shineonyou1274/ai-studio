"""Desk phone stand: 60° backrest, charging-cable hole, prints support-free.

Print orientation: as modelled, base flat on the bed (+Z up).
Side profile lies in the YZ plane (front at Y=0, back at +Y) and is
extruded across X. Every downward-facing surface is >= 50° from
horizontal, so no supports are needed for FDM.
"""
import math

from cadgen import build123d as bd
from cadgen import step, stl

WIDTH = 80.0            # across X
ANGLE = 60.0            # backrest angle from horizontal (deg)
LEDGE_Z = 20.0          # height of the phone ledge (groove floor)
BASE_T = 4.0            # base plate thickness
LIP_T = 4.0             # front lip thickness
LIP_H = 10.0            # lip height above the ledge
GROOVE = 14.0           # groove depth for phone + case
BACK_T = 5.0            # backrest slab thickness
BACK_L = 85.0           # backrest length along the incline
STRUT_T = 5.0           # rear vertical strut thickness
CABLE_W = 14.0          # cable hole / tunnel width (X)
CABLE_HOLE_D = 10.0     # cable hole depth (Y) in the groove floor
TUNNEL_H = 6.0          # tunnel straight-wall height
ROOF_ANGLE = 50.0       # tunnel roof slope from horizontal (>45° = no supports)


def _prism(face):
    """Extrude a (y, z) profile face across the full width."""
    return bd.extrude(bd.Plane.YZ.offset(-WIDTH / 2) * face, amount=WIDTH, dir=(1, 0, 0))


def stand_body():
    a = math.radians(ANGLE)
    d = (math.cos(a), math.sin(a))        # up the incline
    n = (math.sin(a), -math.cos(a))       # slab normal, toward the back
    y0 = LIP_T + GROOVE                   # backrest front face meets the ledge here

    f0 = (y0, LEDGE_Z)
    f1 = (y0 + BACK_L * d[0], LEDGE_Z + BACK_L * d[1])
    r1 = (f1[0] + BACK_T * n[0], f1[1] + BACK_T * n[1])
    rear_y0 = y0 + BACK_T / math.sin(a)   # backrest rear face at z = LEDGE_Z

    def underside_z(y):
        return LEDGE_Z + (y - rear_y0) * math.tan(a)

    strut_y1 = r1[0] - 4.0
    strut_y0 = strut_y1 - STRUT_T

    # One side profile (base, front block, lip, backrest, strut) with the
    # triangular void as a hole, so each side of the part is a single face.
    outer = bd.Polygon(
        (0, 0), (strut_y1, 0), (strut_y1, underside_z(strut_y1)), r1, f1, f0,
        (LIP_T, LEDGE_Z), (LIP_T, LEDGE_Z + LIP_H), (0, LEDGE_Z + LIP_H),
        align=None,
    )
    void = bd.Polygon(
        (rear_y0, BASE_T), (strut_y0, BASE_T), (strut_y0, underside_z(strut_y0)),
        (rear_y0, LEDGE_Z),
        align=None,
    )
    body = _prism(outer - void)

    # Cable path: vertical hole in the groove floor down to the desk, then a
    # pointed-roof tunnel running out the back under the stand.
    hole_y0 = LIP_T + 2.0
    hole = bd.Pos(0, hole_y0 + CABLE_HOLE_D / 2, LEDGE_Z / 2) * bd.Box(
        CABLE_W, CABLE_HOLE_D, LEDGE_Z + 2
    )
    half = CABLE_W / 2
    peak = TUNNEL_H + half * math.tan(math.radians(ROOF_ANGLE))
    tunnel_end = strut_y1 + 1.0
    tunnel_face = bd.Plane.XZ.offset(-tunnel_end) * bd.Polygon(
        (-half, -1), (half, -1), (half, TUNNEL_H), (0, peak), (-half, TUNNEL_H), align=None
    )
    tunnel = bd.extrude(tunnel_face, amount=tunnel_end - hole_y0, dir=(0, -1, 0))

    body = body - hole - tunnel
    return body


@step(out="../STEP/phone_stand.step")
@stl(out="../STL/phone_stand.stl", mesh_tolerance=1e-3)
def phone_stand():
    body = stand_body()
    body.label = "phone_stand"
    return body


if __name__ == "__main__":
    phone_stand()
