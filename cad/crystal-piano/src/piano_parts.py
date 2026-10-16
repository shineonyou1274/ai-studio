"""Geometry for a desk-ornament crystal grand piano (about 1:13 scale).

Millimetres, +Z up, keyboard at the front (-Y), bass side at -X.
The lid is hinged on the straight bass-side rim and propped open.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd

# Case (top view outline) and heights
HALF_W = 56.0          # case half-width
CASE_BOTTOM = 48.0     # underside of the case
RIM_TOP = 76.0         # top of the rim
RIM_WALL = 2.5         # rim wall around the open soundboard pocket
POCKET_DEPTH = 4.0     # soundboard pocket depth below the rim top

# Keyboard: 88 keys, A0..C8
WHITE_W = 1.8          # white key pitch (52 whites = 93.6 mm)
WHITE_L = 13.0         # exposed white key length
KEY_GAP = 0.3          # groove between white keys
KEYBED_TOP = 53.0      # top of the key slip / keybed
WHITE_H = 2.5          # white key height above the keybed
BLACK_W = 1.0
BLACK_L = 7.5
BLACK_H = 1.5          # black key height above the white keys
CHEEK_TOP = 60.0       # top of the keyboard end blocks

# Lid
LID_T = 1.5
LID_FRONT_Y = 12.0     # lid starts behind the music desk
LID_ANGLE = 22.0       # opening angle (deg)
LID_SINK = 0.6         # lid sits this far into the rim so the hinge is a solid joint

# Legs and pedal lyre
LEG_R_TOP = 4.0
LEG_R_BOTTOM = 3.0
LEG_FOOT_H = 4.0       # caster block height
PROP_R = 1.0

OUTLINE_SPLINE = [
    (HALF_W, 28), (50, 48), (36, 66), (22, 84), (12, 104),
    (4, 124), (-8, 141), (-26, 150), (-44, 149), (-HALF_W, 136),
]


def _outline_face(front_y: float = 0.0) -> bd.Face:
    with bd.BuildSketch() as sk:
        with bd.BuildLine():
            bd.Spline(*OUTLINE_SPLINE, tangents=[(0, 1), (0, -1)])
            bd.Polyline((-HALF_W, 136), (-HALF_W, 0), (HALF_W, 0), (HALF_W, 28))
        bd.make_face()
    face = sk.sketch.faces()[0]
    if front_y > 0:
        keep = bd.Pos(0, front_y + 100, 0) * bd.Rectangle(300, 200)
        face = (face & keep).faces()[0]
    return face


def case_body() -> bd.Solid:
    outline = _outline_face()
    case = bd.extrude(bd.Pos(0, 0, CASE_BOTTOM) * outline, amount=RIM_TOP - CASE_BOTTOM)
    inner = bd.offset(outline, -RIM_WALL)
    pocket = bd.extrude(bd.Pos(0, 0, RIM_TOP - POCKET_DEPTH) * inner, amount=POCKET_DEPTH + 1)
    case = case - pocket

    # Key slip under the keys and the two cheek blocks either side
    kb_half = 52 * WHITE_W / 2
    keybed = bd.Pos(0, -WHITE_L / 2 - 1, (CASE_BOTTOM + KEYBED_TOP) / 2) * bd.Box(
        2 * HALF_W, WHITE_L + 2, KEYBED_TOP - CASE_BOTTOM
    )
    cheek_w = HALF_W - kb_half
    cheeks = [
        bd.Pos(sx * (kb_half + cheek_w / 2), -WHITE_L / 2 - 1, (CASE_BOTTOM + CHEEK_TOP) / 2)
        * bd.Box(cheek_w, WHITE_L + 2, CHEEK_TOP - CASE_BOTTOM)
        for sx in (-1, 1)
    ]
    return case + keybed + cheeks[0] + cheeks[1]


def _key_is_black(i: int) -> bool:
    return (9 + i) % 12 in (1, 3, 6, 8, 10)   # key 0 is A0


def white_keys() -> bd.Solid:
    kb_half = 52 * WHITE_W / 2
    keys = []
    w = 0
    for i in range(88):
        if _key_is_black(i):
            continue
        x = -kb_half + (w + 0.5) * WHITE_W
        keys.append(bd.Pos(x, -WHITE_L / 2, KEYBED_TOP + WHITE_H / 2)
                    * bd.Box(WHITE_W - KEY_GAP, WHITE_L, WHITE_H))
        w += 1
    assert w == 52
    # A thin web under the grooves keeps the keyboard one printable piece
    web = bd.Pos(0, -WHITE_L / 2, KEYBED_TOP + 0.5) * bd.Box(2 * kb_half, WHITE_L, 1.0)
    return web + keys


def black_keys() -> list[bd.Solid]:
    kb_half = 52 * WHITE_W / 2
    keys = []
    w = 0
    for i in range(88):
        if _key_is_black(i):
            x = -kb_half + w * WHITE_W   # on the boundary after the previous white key
            keys.append(bd.Pos(x, -BLACK_L / 2, KEYBED_TOP + WHITE_H + BLACK_H / 2 - 0.2)
                        * bd.Box(BLACK_W, BLACK_L, BLACK_H + 0.4))
        else:
            w += 1
    assert len(keys) == 36
    return keys


def music_desk() -> bd.Solid:
    panel = bd.Box(64, 1.2, 18, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    panel = bd.Rot(-14, 0, 0) * panel           # leans back toward the tail
    return bd.Pos(0, 8, RIM_TOP - 1.0) * panel


def lid() -> bd.Solid:
    face = _outline_face(LID_FRONT_Y)
    slab = bd.extrude(bd.Pos(0, 0, RIM_TOP - LID_SINK) * face, amount=LID_T)
    hinge = bd.Axis((-HALF_W, 0, RIM_TOP), (0, 1, 0))
    return slab.rotate(hinge, -LID_ANGLE)


def lid_underside_z(x: float) -> float:
    a = math.radians(LID_ANGLE)
    return RIM_TOP + (x + HALF_W) * math.tan(a) - LID_SINK / math.cos(a)


def hinges() -> list[bd.Solid]:
    return [bd.Pos(-HALF_W + 1.5, y, RIM_TOP + 1.0) * bd.Box(3, 6, 2.6) for y in (35, 80, 125)]


def prop_stick() -> bd.Solid:
    x, y = 30.0, 62.0
    z0 = RIM_TOP - 1.0
    z1 = lid_underside_z(x) + 0.8
    return bd.Pos(x, y, z0) * bd.Cylinder(PROP_R, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def legs() -> list[bd.Solid]:
    out = []
    for x, y in ((-46.0, 6.0), (46.0, 6.0), (-34.0, 132.0)):
        leg = bd.Pos(x, y, LEG_FOOT_H) * bd.Cone(
            LEG_R_BOTTOM, LEG_R_TOP, CASE_BOTTOM + 1 - LEG_FOOT_H,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        foot = bd.Pos(x, y, 0) * bd.Cylinder(
            LEG_R_BOTTOM + 0.6, LEG_FOOT_H + 0.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        out.append(leg + foot)
    return out


def lyre() -> bd.Solid:
    y = 12.0
    box = bd.Pos(0, y, 6.0) * bd.Box(20, 7, 4)
    posts = [bd.Pos(sx * 6, y, 7.5) * bd.Cylinder(1.2, CASE_BOTTOM + 1 - 7.5,
                                                   align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
             for sx in (-1, 1)]
    pedals = [bd.Pos(px, y - 3.5 - 3.0, 5.0) * bd.Box(1.4, 6.0, 1.0) for px in (-4.5, 0, 4.5)]
    # back prop rod from the pedal box down to the floor (as on a real lyre)
    rod = bd.Pos(0, y + 3.0, 0) * bd.Cylinder(1.0, 6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return box + posts[0] + posts[1] + pedals[0] + pedals[1] + pedals[2] + rod


def parts() -> dict[str, bd.Shape]:
    """Every part, labelled, unfused (for display)."""
    return {
        "case": case_body() + hinges()[0] + hinges()[1] + hinges()[2],
        "music_desk": music_desk(),
        "lid": lid(),
        "prop_stick": prop_stick(),
        "white_keys": white_keys(),
        "black_keys": bd.Compound(black_keys()),
        "legs": bd.Compound(legs()),
        "lyre": lyre(),
    }
