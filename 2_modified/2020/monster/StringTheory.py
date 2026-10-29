# ==============================================================================
# Scene:      StringTheory
# Source:     videos/_2020/monster.py (lines 4482-4523)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl StringTheory.py StringTheory -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - monster.svg (free replacement) has different point indices for the eyes: _eye_points finds them by geometry
# ==============================================================================

from manim_imports_ext import *

def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


def _eye_points(mob):
    # CHANGE: monster.svg is a free replacement and its eyes are not at points 498:528 / 582:612; they are found as the two small subpaths at the top
    pts = mob.get_points()
    ends = mob.get_subpath_end_indices_from_points(pts)
    starts = [0, *(ends[:-1] + 2)]
    cy = mob.get_center()[1]
    eyes = [
        pts[a:b + 1] for a, b in zip(starts, ends)
        if np.ptp(pts[a:b + 1, 0]) < 0.1 * mob.get_width() and pts[a:b + 1, 1].mean() > cy
    ]
    eyes.sort(key=lambda p: p[:, 0].mean())
    return eyes[:2]


def blink_monster(monster):
    monster.generate_target()
    left_eye_points, right_eye_points = _eye_points(monster.target[0])
    for points in left_eye_points, right_eye_points:
        points[:, 1] = points[0, 1]
    return MoveToTarget(monster, rate_func=squish_rate_func(there_and_back, 0.4, 0.6))


class StringTheory(Scene):
    def construct(self):
        monster = get_monster()
        monster.set_height(4)
        arrow = OldTex("\\leftrightarrow").scale(2)

        n = 10
        points = compass_directions(n)
        freqs = np.random.random(n) + 0.3

        string = VMobject()
        string.set_stroke([BLUE, TEAL, BLUE, TEAL, BLUE, TEAL, BLUE], 4)

        def update_string(string, points=points, freqs=freqs, sc=self):
            for point, freq in zip(points, freqs):
                point[:] = normalize(point) * (1 + 0.2 * np.sin(TAU * freq * sc.time))
            string.set_points_smoothly([*points, points[0]])

        string.add_updater(update_string)

        arrow.next_to(string, LEFT, LARGE_BUFF)
        monster.next_to(arrow, LEFT, LARGE_BUFF)
        # self.camera.frame.move_to(arrow)
        self.camera.frame.scale(0.5)

        st_name = OldTexText("String theory")
        st_name.scale(1.5)
        st_name.next_to(string, UP, LARGE_BUFF)

        sg_name = OldTexText("Sporadic groups")
        sg_name.scale(1.5)
        sg_name.next_to(monster, DOWN)

        self.add(monster)
        self.add(arrow)
        self.add(string)
        self.wait(2)
        self.play(Write(sg_name))
        self.play(Write(st_name))
        for x in range(4):
            self.play(blink_monster(monster))
            self.wait(5)
