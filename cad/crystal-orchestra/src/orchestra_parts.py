"""Crystal orchestra on a round stage: geometry as a declarative part list.

Millimetres, +Z up, audience (camera) toward -Y. `scene_spec()` is pure
Python: it lists every rendered part as (label, material, build) without
touching the CAD kernel, so the model module can derive its material
assignments and animation from the labels at import time. `build()` makes
a part's geometry, already placed on the stage.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "crystal-piano" / "src"))
import piano_parts as pp  # noqa: E402  (the crystal grand piano from cad/crystal-piano)

from cadgen import build123d as bd  # noqa: E402

STAGE_R = 185.0
STAGE_H = 8.0


# --------------------------------------------------------------------------
# Pure-Python placement (mirrors bd.Pos * bd.Rot(0,0,yaw) * bd.Rot(tilt,0,0))

@dataclass(frozen=True)
class Place:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    yaw: float = 0.0     # about world Z, degrees
    tilt: float = 0.0    # about local X, degrees (applied first)

    def vec(self, v):
        x, y, z = v
        t = math.radians(self.tilt)
        y, z = y * math.cos(t) - z * math.sin(t), y * math.sin(t) + z * math.cos(t)
        a = math.radians(self.yaw)
        x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        return (x, y, z)

    def point(self, p):
        x, y, z = self.vec(p)
        return (x + self.x, y + self.y, z + self.z)

    def apply(self, shape):
        return bd.Pos(self.x, self.y, self.z) * bd.Rot(0, 0, self.yaw) * bd.Rot(self.tilt, 0, 0) * shape


@dataclass
class Part:
    label: str
    material: str
    make: Callable[[], object]   # builds the part in its instrument's local frame
    place: Place = field(default_factory=Place)

    def build(self):
        shape = self.place.apply(self.make())
        shape.label = self.label
        return shape


def _c():
    return (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def _rod(p0, p1, r):
    """Cylinder from point p0 to point p1."""
    v = bd.Vector(*p1) - bd.Vector(*p0)
    return bd.Solid.make_cylinder(r, v.length, bd.Plane(origin=p0, z_dir=v))


# --------------------------------------------------------------------------
# Stage, podium, music stands

def stage_parts() -> list[Part]:
    return [
        Part("stage", "crystal", lambda: bd.Cylinder(STAGE_R, STAGE_H, align=_c())),
        Part("stage_rim_top", "gold",
             lambda: bd.Pos(0, 0, STAGE_H) * bd.Torus(STAGE_R, 1.4)),
        Part("stage_rim_bottom", "gold",
             lambda: bd.Pos(0, 0, 1.4) * bd.Torus(STAGE_R, 1.4)),
    ]


def podium_parts(place: Place) -> list[Part]:
    w, d, h = 46.0, 36.0, 7.0

    def trim():
        bars = [bd.Pos(0, sy * d / 2, h) * bd.Box(w + 2, 1.6, 1.6) for sy in (-1, 1)]
        bars += [bd.Pos(sx * w / 2, 0, h) * bd.Box(1.6, d + 2, 1.6) for sx in (-1, 1)]
        out = bars[0]
        for b in bars[1:]:
            out = out + b
        return out

    return [
        Part("podium", "crystal", lambda: bd.Box(w, d, h, align=_c()), place),
        Part("podium_trim", "gold", trim, place),
    ]


BATON_PIVOT_LOCAL = (0.0, 10.0, 52.0)
BATON_DIR_LOCAL = (0.0, math.cos(math.radians(25)), math.sin(math.radians(25)))


def baton_parts(place: Place) -> list[Part]:
    p0 = BATON_PIVOT_LOCAL
    d = BATON_DIR_LOCAL

    def at(s):
        return tuple(p0[i] + s * d[i] for i in range(3))

    return [
        Part("baton_handle", "ivory", lambda: _rod(at(0), at(6), 1.3), place),
        Part("baton_stick", "gold", lambda: _rod(at(5), at(34), 0.45), place),
    ]


def music_stand_parts(name: str, place: Place) -> list[Part]:
    def frame():
        legs = None
        for k in range(3):
            a = math.radians(120 * k + 90)
            leg = _rod((0, 0, 10), (13 * math.cos(a), 13 * math.sin(a), 0.8), 0.7)
            legs = leg if legs is None else legs + leg
        post = bd.Pos(0, 0, 9) * bd.Cylinder(0.9, 38, align=_c())
        ledge = bd.Pos(0, -1.5, 46.5) * bd.Rot(-25, 0, 0) * bd.Box(28, 2.4, 1.4)
        return legs + post + ledge

    def desk():
        return bd.Pos(0, -0.8, 46.5) * bd.Rot(-25, 0, 0) * bd.Box(28, 1.0, 20, align=_c())

    return [
        Part(f"{name}_frame", "gold", frame, place),
        Part(f"{name}_desk", "crystal", desk, place),
    ]


# --------------------------------------------------------------------------
# Violin family (violin, cello, contrabass)

BODY = [(0.0, 0.0), (0.22, 0.02), (0.30, 0.13), (0.29, 0.29), (0.19, 0.42), (0.17, 0.50),
        (0.19, 0.58), (0.25, 0.70), (0.25, 0.85), (0.16, 0.97)]


@dataclass
class StringSpec:
    name: str
    length: float        # overall length, scroll to bottom of body
    depth: float         # rib depth as a fraction of body length
    lift: float          # endpin / stand height under the body
    bow_z: float         # bow contact height as a fraction of body length
    stand: bool = False  # violins sit on a small gold display stand


def _string_geometry(s: StringSpec):
    L = s.length
    Lb = 0.56 * L
    D = s.depth * Lb
    neck_top = Lb + 0.27 * L
    fb_t = 0.014 * L                      # fingerboard thickness
    y_front = -D / 2
    y_fb = y_front - fb_t                 # fingerboard front face
    y_str = y_fb - 0.006 * L              # string plane
    return L, Lb, D, neck_top, fb_t, y_front, y_fb, y_str


def string_instrument_parts(s: StringSpec, place: Place) -> tuple[list[Part], dict]:
    L, Lb, D, neck_top, fb_t, y_front, y_fb, y_str = _string_geometry(s)
    n = s.name

    def body():
        pts = [(x * Lb, z * Lb) for x, z in BODY] + [(0.0, Lb)] + [(-x * Lb, z * Lb) for x, z in reversed(BODY[1:])]
        with bd.BuildSketch(bd.Plane.XZ) as sk:
            with bd.BuildLine():
                bd.Spline(*pts, periodic=True)
            bd.make_face()
        solid = bd.extrude(sk.sketch, amount=D, dir=(0, 1, 0))
        solid = bd.Pos(0, -D / 2, 0) * solid
        for sx in (-1, 1):
            slot = bd.Pos(sx * 0.15 * Lb, 0, 0.44 * Lb) * bd.Rot(0, sx * 10, 0) * bd.Box(0.022 * Lb, 3 * D, 0.2 * Lb)
            solid = solid - slot
        return solid

    def neck():
        nk = bd.Pos(0, y_front + 0.02 * L, Lb - 1) * bd.Box(0.05 * L, 0.04 * L, neck_top - Lb + 1, align=_c())
        pegbox = bd.Pos(0, y_front + 0.02 * L, neck_top) * bd.Box(0.045 * L, 0.04 * L, 0.07 * L, align=_c())
        scroll = bd.Pos(0, y_front + 0.02 * L, neck_top + 0.085 * L) * bd.Rot(0, 90, 0) * bd.Cylinder(0.03 * L, 0.05 * L)
        return nk + pegbox + scroll

    def pegs():
        out = None
        for k, (sx, dz) in enumerate(((-1, 0.02), (1, 0.035), (-1, 0.05), (1, 0.065))):
            peg = bd.Pos(sx * 0.04 * L, y_front + 0.02 * L, neck_top + dz * L) * bd.Rot(0, 90, 0) * bd.Cylinder(0.008 * L, 0.04 * L)
            out = peg if out is None else out + peg
        return out

    def fingerboard():
        return bd.Pos(0, y_front - fb_t / 2, 0.62 * Lb) * bd.Box(0.06 * L, fb_t, neck_top - 0.62 * Lb, align=_c())

    def tailpiece():
        return bd.Pos(0, y_front - 0.006 * L, 0.05 * Lb) * bd.Box(0.1 * Lb, 0.012 * L, 0.22 * Lb, align=_c())

    def bridge():
        h = abs(y_str - y_front) + 0.004 * L
        return bd.Pos(0, y_front - h / 2, 0.40 * Lb) * bd.Box(0.075 * L, h, 0.012 * L)

    def strings():
        out = None
        r = max(0.0035 * L, 0.2)
        for k in range(4):
            x = (k - 1.5) * 0.013 * L
            st = _rod((x, y_str, 0.26 * Lb), (x, y_str, neck_top), r)
            out = st if out is None else out + st
        return out

    parts = [
        Part(f"{n}_body", "crystal", body, place),
        Part(f"{n}_neck", "crystal", neck, place),
        Part(f"{n}_pegs", "gold", pegs, place),
        Part(f"{n}_fingerboard", "ebony", fingerboard, place),
        Part(f"{n}_tailpiece", "ebony", tailpiece, place),
        Part(f"{n}_bridge", "gold", bridge, place),
        Part(f"{n}_strings", "gold", strings, place),
    ]
    if s.stand:
        def stand():
            rod = bd.Pos(0, 0, -s.lift) * bd.Cylinder(0.012 * L + 0.4, s.lift + 1, align=_c())
            base = bd.Pos(0, 0, -s.lift) * bd.Cylinder(9, 1.6, align=_c())
            cradle = bd.Pos(0, 0, -1.2) * bd.Box(0.36 * Lb, D + 3, 1.6, align=_c())
            return rod + base + cradle
        parts.append(Part(f"{n}_stand", "gold", stand, place))
    else:
        parts.append(Part(f"{n}_endpin", "gold",
                          lambda: bd.Pos(0, 0, -s.lift) * bd.Cylinder(0.01 * L + 0.3, s.lift + 2, align=_c()), place))

    # Bow: across the strings between bridge and fingerboard, rising 12° toward +X
    ang = math.radians(12)
    d = (math.cos(ang), 0.0, math.sin(ang))
    bow_len = 0.6 * L
    zc = s.bow_z * Lb
    yb = y_str - 0.012 * L
    c0 = (0.08 * L * d[0], yb, zc + 0.08 * L * d[2])

    def bow_pt(sv, dy=0.0, dz=0.0):
        return (c0[0] + sv * d[0], c0[1] + dy, c0[2] + sv * d[2] + dz)

    def bow_stick():
        return _rod(bow_pt(-bow_len / 2), bow_pt(bow_len / 2), max(0.008 * L, 0.35))

    def bow_hair():
        return _rod(bow_pt(-bow_len / 2 + 0.06 * L, dz=-0.018 * L), bow_pt(bow_len / 2 - 0.01 * L, dz=-0.018 * L),
                    max(0.005 * L, 0.25))

    def bow_frog():
        cx, cy, cz = bow_pt(-bow_len / 2 + 0.03 * L, dz=-0.01 * L)
        return bd.Pos(cx, cy, cz) * bd.Rot(0, -12, 0) * bd.Box(0.06 * L, 0.02 * L, 0.025 * L)

    bow = [
        Part(f"{n}_bow_stick", "gold", bow_stick, place),
        Part(f"{n}_bow_hair", "hair", bow_hair, place),
        Part(f"{n}_bow_frog", "ebony", bow_frog, place),
    ]
    motion = {"labels": [p.label for p in bow], "dir": place.vec(d), "amp": 0.12 * L}
    return parts + bow, motion


# --------------------------------------------------------------------------
# Harp (profile in the local XZ plane, facing the audience)

def _bezier(p0, p1, p2, p3, n):
    out = []
    for k in range(n + 1):
        t = k / n
        a, b, c, e = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
    return out


HARP_NECK = _bezier((30, 138), (12, 122), (-18, 146), (-42, 122), 20)


def _soundbox_z(x):
    return 10 + (24 - x) * 110 / 64


def _neck_z(x):
    pts = sorted(HARP_NECK)
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


HARP_STRING_X = [20 - 2.7 * k for k in range(21)]


def harp_parts(place: Place) -> tuple[list[Part], list[str]]:
    def base():
        return bd.Pos(12, 0, 0) * bd.Box(54, 24, 8, align=_c())

    def column():
        col = bd.Pos(30, 0, 7) * bd.Cylinder(2.8, 132, align=_c())
        crown = bd.Pos(30, 0, 140) * bd.Sphere(4.0)
        return col + crown

    def soundbox():
        x0, z0, x1, z1 = 24.0, 8.0, -42.0, 124.0
        ux, uz = x1 - x0, z1 - z0
        ln = math.hypot(ux, uz)
        nx, nz = -uz / ln, ux / ln
        w0, w1 = 7.0, 3.5
        poly = [(x0 + nx * w0, z0 + nz * w0), (x1 + nx * w1, z1 + nz * w1),
                (x1 - nx * w1, z1 - nz * w1), (x0 - nx * w0, z0 - nz * w0)]
        face = bd.Plane.XZ * bd.Polygon(*poly, align=None)
        return bd.Pos(0, -7, 0) * bd.extrude(face, amount=14, dir=(0, 1, 0))

    def neck():
        out = None
        for (xa, za), (xb, zb) in zip(HARP_NECK, HARP_NECK[1:]):
            seg = _rod((xa, 0, za), (xb, 0, zb), 2.2) + bd.Pos(xb, 0, zb) * bd.Sphere(2.2)
            out = seg if out is None else out + seg
        return out

    parts = [
        Part("harp_base", "gold", base, place),
        Part("harp_column", "gold", column, place),
        Part("harp_soundbox", "crystal", soundbox, place),
        Part("harp_neck", "gold", neck, place),
    ]
    strings = []
    for k, x in enumerate(HARP_STRING_X):
        z0 = _soundbox_z(x) + 2.0
        z1 = _neck_z(x) - 1.6
        label = f"harp_string{k + 1}"
        parts.append(Part(label, "gold", (lambda x=x, z0=z0, z1=z1: _rod((x, 0, z0), (x, 0, z1), 0.35)), place))
        strings.append(label)
    return parts, strings


# --------------------------------------------------------------------------
# Timpani

def timpano_parts(name: str, R: float, place: Place) -> tuple[list[Part], dict]:
    H = 44.0

    def kettle():
        bowl = bd.Pos(0, 0, H) * bd.Sphere(R)
        cut = bd.Pos(0, 0, H) * bd.Box(3 * R, 3 * R, 2 * R, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        return bowl - cut

    def frame():
        rim = bd.Pos(0, 0, H) * bd.Torus(R, 1.4)
        ring = bd.Pos(0, 0, 1.0) * bd.Torus(R * 0.75, 1.0)
        legs = None
        for k in range(3):
            a = math.radians(120 * k + 30)
            top = (0.82 * R * math.cos(a), 0.82 * R * math.sin(a), H - 0.45 * R)
            foot = (0.75 * R * math.cos(a), 0.75 * R * math.sin(a), 0.0)
            leg = _rod(foot, top, 1.2)
            legs = leg if legs is None else legs + leg
        return rim + ring + legs

    def head():
        return bd.Pos(0, 0, H - 0.3) * bd.Cylinder(R - 0.6, 0.6, align=_c())

    ball = (0.0, -0.3 * R, H + 3.2)
    ang = math.radians(35)
    hdir = (0.0, math.cos(ang), math.sin(ang))
    handle = tuple(ball[i] + 30 * hdir[i] for i in range(3))

    def mallet_stick():
        return _rod(ball, handle, 0.7)

    def mallet_ball():
        return bd.Pos(*ball) * bd.Sphere(2.6)

    parts = [
        Part(f"{name}_kettle", "crystal", kettle, place),
        Part(f"{name}_frame", "gold", frame, place),
        Part(f"{name}_head", "head", head, place),
        Part(f"{name}_mallet_stick", "gold", mallet_stick, place),
        Part(f"{name}_mallet_ball", "ivory", mallet_ball, place),
    ]
    motion = {"labels": [f"{name}_mallet_stick", f"{name}_mallet_ball"],
              "pivot": place.point(handle), "axis": place.vec((1, 0, 0))}
    return parts, motion


# --------------------------------------------------------------------------
# Grand piano (geometry from cad/crystal-piano, restyled with gold accents)

PIANO = Place(-67.0, 75.0, STAGE_H, yaw=-90)


def _white_key_x():
    kb_half = 52 * pp.WHITE_W / 2
    return [-kb_half + (w + 0.5) * pp.WHITE_W for w in range(52)]


def _black_key_x():
    kb_half = 52 * pp.WHITE_W / 2
    out, w = [], 0
    for i in range(88):
        if pp._key_is_black(i):
            out.append(-kb_half + w * pp.WHITE_W)
        else:
            w += 1
    return out


def piano_parts() -> tuple[list[Part], list[str], list[str]]:
    place = PIANO
    parts = [
        Part("piano_case", "crystal", lambda: pp.case_body() - pp._seat_cut(), place),
        Part("piano_lid", "crystal", pp.lid, place),
        Part("piano_music_desk", "crystal", pp.music_desk, place),
        Part("piano_prop_stick", "gold", pp.prop_stick, place),
        Part("piano_hinge", "gold",
             lambda: _rod((-pp.HALF_W + 0.4, pp.LID_FRONT_Y + 2, pp.RIM_TOP + 0.2), (-pp.HALF_W + 0.4, 132, pp.RIM_TOP + 0.2), 0.9),
             place),
    ]

    def piano_strings():
        out = None
        z = pp.RIM_TOP - pp.POCKET_DEPTH + 0.8
        for k in range(12):
            x = -48 + k * 7
            y_end = 140 - (x + 48) * 74 / 78
            st = _rod((x, 14, z), (x, y_end, z), 0.45)
            out = st if out is None else out + st
        return out

    parts.append(Part("piano_strings", "gold", piano_strings, place))

    for k, (x, y) in enumerate(((-46.0, 6.0), (46.0, 6.0), (-34.0, 132.0))):
        parts.append(Part(f"piano_leg{k + 1}", "crystal",
                          (lambda x=x, y=y: bd.Pos(x, y, pp.LEG_FOOT_H) * bd.Cone(
                              pp.LEG_R_BOTTOM, pp.LEG_R_TOP, pp.CASE_BOTTOM + 1 - pp.LEG_FOOT_H, align=_c())),
                          place))
        parts.append(Part(f"piano_foot{k + 1}", "gold",
                          (lambda x=x, y=y: bd.Pos(x, y, 0) * bd.Cylinder(pp.LEG_R_BOTTOM + 0.8, pp.LEG_FOOT_H + 0.5, align=_c())),
                          place))

    def lyre():
        y = 12.0
        box = bd.Pos(0, y, 6.0) * bd.Box(20, 7, 4)
        posts = [bd.Pos(sx * 6, y, 7.5) * bd.Cylinder(1.2, pp.CASE_BOTTOM + 1 - 7.5, align=_c()) for sx in (-1, 1)]
        return box + posts[0] + posts[1]

    def pedals():
        out = None
        for px in (-4.5, 0, 4.5):
            pd = bd.Pos(px, 12 - 6.5, 5.0) * bd.Box(2.2, 6.0, 1.8)
            out = pd if out is None else out + pd
        return out + bd.Pos(0, 15, 0) * bd.Cylinder(1.0, 6.0, align=_c())

    parts += [Part("piano_lyre", "crystal", lyre, place), Part("piano_pedals", "gold", pedals, place)]

    white, black = [], []
    for k, x in enumerate(_white_key_x()):
        label = f"piano_wkey{k + 1}"
        parts.append(Part(label, "ivory", (lambda x=x: bd.Pos(x, -pp.WHITE_L / 2, pp.KEYBED_TOP + pp.WHITE_H / 2)
                                           * bd.Box(pp.WHITE_W - pp.KEY_GAP, pp.WHITE_L, pp.WHITE_H)), place))
        white.append(label)
    for k, x in enumerate(_black_key_x()):
        label = f"piano_bkey{k + 1}"
        parts.append(Part(label, "ebony", (lambda x=x: bd.Pos(x, -pp.BLACK_L / 2, pp.KEYBED_TOP + pp.WHITE_H + pp.BLACK_H / 2)
                                           * bd.Box(pp.BLACK_W, pp.BLACK_L, pp.BLACK_H)), place))
        black.append(label)
    return parts, white, black


# --------------------------------------------------------------------------
# The whole scene

VIOLIN = StringSpec("violin1", 70, 0.13, 40, 0.62, stand=True)
VIOLIN2 = StringSpec("violin2", 70, 0.13, 34, 0.62, stand=True)
CELLO = StringSpec("cello", 100, 0.20, 14, 0.58)
BASS = StringSpec("bass", 145, 0.21, 16, 0.58)


def _upright(s: StringSpec, x, y, yaw, tilt):
    return Place(x, y, STAGE_H + s.lift * math.cos(math.radians(tilt)), yaw=yaw, tilt=tilt)


def scene_spec() -> dict:
    parts = stage_parts()
    piano, white_keys, black_keys = piano_parts()
    parts += piano
    harp_place = Place(128, -5, STAGE_H, yaw=8)
    harp, harp_strings = harp_parts(harp_place)
    parts += harp

    bows = []
    for spec, x, y, yaw, tilt in ((VIOLIN, -118, -55, 18, -8), (VIOLIN2, -68, -92, 10, -8),
                                  (CELLO, 50, -98, -12, -14), (BASS, 105, -72, -20, -12)):
        p, motion = string_instrument_parts(spec, _upright(spec, x, y, yaw, tilt))
        parts += p
        bows.append(motion)

    mallets = []
    for name, R, x, y in (("timpano1", 26.0, -138, 42), ("timpano2", 22.0, -112, 108)):
        p, motion = timpano_parts(name, R, Place(x, y, STAGE_H, yaw=20))
        parts += p
        mallets.append(motion)

    for name, x, y, yaw in (("stand1", -95, -18, 200), ("stand2", 80, -40, 160), ("stand3", 10, 5, 180)):
        parts += music_stand_parts(name, Place(x, y, STAGE_H, yaw=yaw))

    podium = Place(0, -142, STAGE_H)
    parts += podium_parts(podium)
    parts += music_stand_parts("score_stand", Place(0, -116, STAGE_H + 7, yaw=180))
    baton_place = Place(0, -142, STAGE_H + 7)
    parts += baton_parts(baton_place)

    labels = [p.label for p in parts]
    assert len(labels) == len(set(labels)), "duplicate part labels"
    return {
        "parts": parts,
        "white_keys": white_keys,
        "black_keys": black_keys,
        "harp_strings": harp_strings,
        "harp_dir": harp_place.vec((0, 1, 0)),   # across the string plane
        "bows": bows,
        "mallets": mallets,
        "baton": {"labels": ["baton_handle", "baton_stick"],
                  "pivot": baton_place.point(BATON_PIVOT_LOCAL),
                  "axis_lift": baton_place.vec((1, 0, 0)),
                  "axis_sweep": (0.0, 0.0, 1.0)},
    }
