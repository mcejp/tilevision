# Relevant spec: https://www.w3.org/TR/SVG2/paths.html

import math


FMT = "%.3f"


def circle(x, y, r):
    # wow... https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs
    return (f"M {x + r} {y} a {r} {r} 0 0 0 {-2*r} 0 " +
            f"a {r} {r} 0 0 0 {2*r} 0")


def grid(w, h, offset_x, offset_y):
    return (" ".join(hline(offset_x, w + offset_x, y + offset_y) for y in range(h + 1)) + " " +
            " ".join(vline(x + offset_x, offset_y, h + offset_y) for x in range(w + 1)))


def hline(x1, x2, y):
    return f"M {FMT % x1} {FMT % y} h {FMT % (x2 - x1)}"


def line(x1, y1, x2, y2):
    return f"M {x1} {y1} L {x2} {y2}"


def line_polar(x, y, radius, angle):
    dx = radius * math.cos(angle)
    dy = radius * math.sin(angle)
    return f"M {x} {y} l {dx:.2f} {dy:.2f}"


def marching_squares_binary_fill(map):
    def rotate(points, times):
        if times % 4 == 0:
            return points
        elif times % 4 == 1:
            return [(1 - y, x) for x, y in points]
        elif times % 4 == 2:
            return [(1 - x, 1 - y) for x, y in points]
        elif times % 4 == 3:
            return [(y, 1 - x) for x, y in points]

    # FIXME: should be an array for faster access, but must implement corner cases (0101 and 1010) first
    PATTERNS = {}

    # empty and full
    PATTERNS[0b0000] = []
    PATTERNS[0b1111] = [(0, 0), (1, 0), (1, 1), (0, 1)]

    # bottom, right, top, left
    for i, pat in enumerate([0b0011, 0b0110, 0b1100, 0b1001]):
        PATTERNS[pat] = rotate([(0, 0), (1, 0), (1, 0.5), (0, 0.5)], i)

    # corners: BL, BR, TR, TL
    for i, pat in enumerate([0b0001, 0b0010, 0b0100, 0b1000]):
        PATTERNS[pat] = rotate([(0, 0), (0.5, 0), (0, 0.5)], i)

    # negative corners: BL, BR, TR, BL
    for i, pat in enumerate([0b1110, 0b1101, 0b1011, 0b0111]):
        PATTERNS[pat] = rotate([(0, 0.5), (0.5, 0), (1, 0), (1, 1), (0, 1)], i)

    parts = []

    for y in range(len(map) - 1):
        for x in range(len(map[y]) - 1):
            botleft = map[y, x]
            botright = map[y, x + 1]
            topright = map[y + 1, x + 1]
            topleft = map[y + 1, x]

            pattern = (topleft<<3) | (topright<<2) | (botright<<1) | botleft
            shape = PATTERNS[pattern]

            if not shape:
                continue

            parts.append(polyline([(x + xx, y + yy) for xx, yy in shape]))

    return " ".join(parts)


def polyline(points: list[tuple[float, float]]):
    assert len(points) >= 2

    str_points = [f"{x:.3f} {y:.3f}" for x, y in points]

    """
    TODO:
    A command letter may be eliminated if an identical command letter would otherwise precede it;
    for instance, the following contains an unnecessary second "L" command:
    M 100 200 L 200 100 L -100 -200
    It may be expressed more compactly as:
    M 100 200 L 200 100 -100 -200
    """

    return f"M " + " L ".join(str_points)


def rectangle_centered(x, y, w, h):
    return f"M {x - w / 2:.3f} {y - h / 2:.3f} h {w:.3f} v {h:.3f} h {-w:.3f} z"


def star(degree: int, r1, r2, x=0, y=0, rotation=math.pi / 2):
    assert degree >= 3

    pts = []

    for i in range(degree):
        angle = rotation + i * (2 * math.pi / degree)
        # pts.append(f"{x + r1 * math.cos(angle):.2f} {y + r1 * math.sin(angle):.2f}")
        pts.append((x + r1 * math.cos(angle), y + r1 * math.sin(angle)))

        angle = rotation + (i + 0.5) * (2 * math.pi / degree)
        # pts.append(f"{x + r2 * math.cos(angle):.2f} {y + r2 * math.sin(angle):.2f}")
        pts.append((x + r2 * math.cos(angle), y + r2 * math.sin(angle)))

    return polyline(pts)


def triangle(x, y, radius, rotation=math.pi / 2):
    pts = []

    for a in [0, 2/3, 4/3]:
        angle = rotation + math.pi * a
        pts.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))

    return polyline(pts)


def vline(x, y1, y2):
    return f"M {FMT % x} {FMT % y1} v {FMT % (y2 - y1)}"
