# ==============================================================================
# Scene:      MentionTheMonster
# Source:     videos/_2020/monster.py (lines 2338-2357)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MentionTheMonster.py MentionTheMonster -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - monster.svg (free replacement) has different point indices for the eyes: _eye_points finds them by geometry
# ==============================================================================

from manim_imports_ext import *

MONSTER_SIZE = 808017424794512875886459904961710757005754368000000000


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


def get_monster_size_label():
    size_label = OldTexText("{:,}".format(MONSTER_SIZE))[0]
    size_parts = VGroup(*[
        size_label[i:i + 12]
        for i in range(0, len(size_label), 12)
    ])
    size_parts.arrange(DOWN, buff=SMALL_BUFF, aligned_edge=LEFT)
    return size_label


class MentionTheMonster(Scene):
    def construct(self):
        monster = get_monster()
        monster.set_height(6)

        self.add(monster)
        self.wait()
        self.play(blink_monster(monster))
        self.wait()

        size_label = get_monster_size_label()
        size_label.match_height(monster)
        size_label.to_edge(RIGHT, buff=LARGE_BUFF)

        self.play(
            ApplyMethod(monster.next_to, size_label, LEFT, LARGE_BUFF, run_time=2),
            ShowIncreasingSubsets(size_label, run_time=6)
        )
        self.play(blink_monster(monster))
        self.wait()
