"""Geometry for a cute mini carousel music box (80 mm diameter).

Millimetres, +Z up, spin axis on Z. The carousel is two groups:
`base` (plinth and winding key, fixed) and `rotor` (platform, poles,
animals and the striped roof, which turn together).
"""
from __future__ import annotations

import math

from cadgen import build123d as bd
from cadgen import srgb

MINT = "#A8E6CF"
PINK = "#FFB7C5"
LEMON = "#FFF1A8"
LAVENDER = "#CDB4F6"
PASTELS = [MINT, PINK, LEMON, LAVENDER]
COCOA = "#5A4650"      # eyes and noses

RADIUS = 40.0          # overall radius (80 mm diameter)
PLINTH_H = 8.0
STEP_R = 36.0
STEP_H = 3.0
PLATFORM_R = 34.0
PLATFORM_H = 3.0
POLE_RING = 27.0       # radius of the six poles and animals
POLE_R = 1.6
CENTER_POLE_R = 4.0
BAND_BOTTOM = 50.0     # underside of the roof band
BAND_H = 4.0
ROOF_H = 22.0
ROOF_STRIPES = 12
FINIAL_R = 3.0
ANIMAL_Z = 27.0        # body centre height; neighbours sit 3 mm up/down

PLATFORM_TOP = PLINTH_H + STEP_H + PLATFORM_H
ROOF_BOTTOM = BAND_BOTTOM + BAND_H


def _centered_base():
    return (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def _paint(shape, label: str, color: str):
    shape.label = label
    shape.color = srgb(color)
    return shape


def base() -> bd.Compound:
    plinth = bd.Cylinder(RADIUS, PLINTH_H, align=_centered_base())
    step = bd.Pos(0, 0, PLINTH_H) * bd.Cylinder(STEP_R, STEP_H, align=_centered_base())
    # Winding key on the side of the plinth: shaft plus a two-lobed handle
    shaft = bd.Pos(RADIUS - 1, 0, PLINTH_H / 2) * bd.Rot(0, 90, 0) * bd.Cylinder(1.5, 5, align=_centered_base())
    lobes = [bd.Pos(RADIUS + 3.5, 0, PLINTH_H / 2 + dz) * bd.Rot(0, 90, 0) * bd.Cylinder(1.8, 2, align=_centered_base())
             for dz in (-2.0, 2.0)]
    handle = lobes[0] + lobes[1] + bd.Pos(RADIUS + 4.5, 0, PLINTH_H / 2) * bd.Box(2, 2.4, 4.0)
    return bd.Compound(children=[
        _paint(plinth, "plinth", MINT),
        _paint(step, "plinth_step", LEMON),
        _paint(shaft, "key_shaft", LAVENDER),
        _paint(handle, "key_handle", LAVENDER),
    ], label="base")


def _animal(kind: str, i: int, color: str) -> bd.Compound:
    """A blocky bear or bunny facing +X, body centred on the origin."""
    parts = []
    body = bd.Box(10, 6.5, 6.5)
    head = bd.Pos(6.5, 0, 4.5) * bd.Box(6.5, 6.5, 6.5)
    parts += [_paint(body, f"{kind}{i}_body", color), _paint(head, f"{kind}{i}_head", color)]
    if kind == "bear":
        for k, y in enumerate((-2.4, 2.4)):
            ear = bd.Pos(6.0, y, 7.2) * bd.Cylinder(1.4, 2.4, align=_centered_base())
            parts.append(_paint(ear, f"{kind}{i}_ear{k + 1}", color))
        snout = bd.Pos(10.2, 0, 3.6) * bd.Box(1.4, 3.0, 2.4)
        parts.append(_paint(snout, f"{kind}{i}_snout", "#FFF6EA"))
    else:
        for k, y in enumerate((-1.6, 1.6)):
            splay = 12 if y > 0 else -12   # ears lean outward and turn slightly
            ear = bd.Pos(5.6, y, 7.0) * bd.Rot(-splay, 0, splay * 0.7) * bd.Box(1.6, 1.5, 7.4, align=_centered_base())
            parts.append(_paint(ear, f"{kind}{i}_ear{k + 1}", color))
        tail = bd.Pos(-5.4, 0, 1.0) * bd.Rot(0, 90, 0) * bd.Sphere(1.6)  # poles along X, clear of the body seam
        parts.append(_paint(tail, f"{kind}{i}_tail", "#FFFFFF"))
    for k, y in enumerate((-1.6, 1.6)):
        eye = bd.Pos(9.85, y, 5.6) * bd.Box(0.6, 0.9, 0.9)
        parts.append(_paint(eye, f"{kind}{i}_eye{k + 1}", COCOA))
    nose = bd.Pos(10.95 if kind == "bear" else 9.85, 0, 4.2) * bd.Box(0.6, 1.0, 0.8)
    parts.append(_paint(nose, f"{kind}{i}_nose", COCOA))
    return bd.Compound(children=parts, label=f"{kind}{i}")


def rotor() -> bd.Compound:
    children = []
    platform = bd.Pos(0, 0, PLINTH_H + STEP_H) * bd.Cylinder(PLATFORM_R, PLATFORM_H, align=_centered_base())
    children.append(_paint(platform, "platform", PINK))
    center = bd.Pos(0, 0, PLATFORM_TOP - 0.5) * bd.Cylinder(CENTER_POLE_R, BAND_BOTTOM - PLATFORM_TOP + 1, align=_centered_base())
    children.append(_paint(center, "center_pole", LAVENDER))

    for i in range(6):
        a = math.radians(60 * i + 30)
        x, y = POLE_RING * math.cos(a), POLE_RING * math.sin(a)
        pole = bd.Pos(x, y, PLATFORM_TOP - 0.5) * bd.Cylinder(POLE_R, BAND_BOTTOM - PLATFORM_TOP + 1, align=_centered_base())
        children.append(_paint(pole, f"pole{i + 1}", PASTELS[(i + 2) % 4]))

        kind = "bear" if i % 2 == 0 else "bunny"
        z = ANIMAL_Z + (3 if i % 2 == 0 else -3)
        # Face along the direction of travel (counter-clockwise from above)
        heading = 60 * i + 30 + 90
        animal = bd.Pos(x, y, z) * bd.Rot(0, 0, heading) * _animal(kind, i + 1, PASTELS[i % 4])
        animal.label = f"{kind}{i + 1}"
        children.append(animal)

    band = bd.Pos(0, 0, BAND_BOTTOM) * bd.Cylinder(RADIUS, BAND_H, align=_centered_base())
    children.append(_paint(band, "roof_band", LAVENDER))
    for k in range(12):
        a = math.radians(30 * k + 15)
        bead = (bd.Pos(RADIUS * math.cos(a), RADIUS * math.sin(a), BAND_BOTTOM + BAND_H / 2)
                * bd.Rot(0, 0, math.degrees(a)) * bd.Rot(0, 90, 0) * bd.Sphere(1.4))  # poles radial
        children.append(_paint(bead, f"bead{k + 1}", LEMON))

    cone = bd.Pos(0, 0, ROOF_BOTTOM) * bd.Cone(RADIUS, 0.0, ROOF_H, align=_centered_base())
    span = 360 / ROOF_STRIPES
    stripe_colors = [PINK, MINT, LEMON, LAVENDER]
    for k in range(ROOF_STRIPES):
        a0, a1 = math.radians(span * k), math.radians(span * (k + 1))
        far = 2 * RADIUS
        wedge = bd.extrude(
            bd.Polygon((0, 0), (far * math.cos(a0), far * math.sin(a0)),
                       (far * math.cos(a1), far * math.sin(a1)), align=None),
            amount=200, dir=(0, 0, 1),
        )
        children.append(_paint(cone & wedge, f"roof_stripe{k + 1}", stripe_colors[k % 4]))
    finial = bd.Pos(0, 0, ROOF_BOTTOM + ROOF_H) * bd.Sphere(FINIAL_R)
    children.append(_paint(finial, "finial", PINK))
    return bd.Compound(children=children, label="rotor")


def carousel() -> bd.Compound:
    return bd.Compound(children=[base(), rotor()], label="carousel")


def animal_part_names(kind: str) -> list[str]:
    extra = ["snout"] if kind == "bear" else ["tail"]
    return ["body", "head", "ear1", "ear2"] + extra + ["eye1", "eye2", "nose"]


def animal_labels() -> dict[str, list[str]]:
    """Rendered-part labels of each animal, keyed by animal (no geometry built)."""
    out = {}
    for i in range(6):
        kind = "bear" if i % 2 == 0 else "bunny"
        name = f"{kind}{i + 1}"
        out[name] = [f"{name}_{p}" for p in animal_part_names(kind)]
    return out


def rotor_labels() -> list[str]:
    """Rendered-part labels of every rotor part, in build order (no geometry built)."""
    labels = ["platform", "center_pole"]
    animals = list(animal_labels().values())
    for i in range(6):
        labels += [f"pole{i + 1}"] + animals[i]
    labels += ["roof_band"] + [f"bead{k + 1}" for k in range(12)]
    labels += [f"roof_stripe{k + 1}" for k in range(ROOF_STRIPES)] + ["finial"]
    return labels


def leaf_labels(shape) -> list[str]:
    """Labels of every rendered part under a built group (for checks)."""
    out = []
    for child in shape.children:
        if child.children:
            out += leaf_labels(child)
        else:
            out.append(child.label)
    return out
