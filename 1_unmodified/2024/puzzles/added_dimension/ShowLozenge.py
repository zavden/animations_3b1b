# ==============================================================================
# Scene:      ShowLozenge
# Source:     videos/_2024/puzzles/added_dimension.py (lines 13-96)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowLozenge.py ShowLozenge -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_lozenge(side_length=1):
    verts = [math.sqrt(3) * LEFT, UP, math.sqrt(3) * RIGHT, DOWN]
    result = Polygon(*verts)
    result.scale(side_length / get_norm(verts[0] - verts[1]))
    return result


class ShowLozenge(InteractiveScene):
    def construct(self):
        # Add Lozenge
        lozenge = get_lozenge()
        lozenge.scale(4)
        lozenge.set_stroke(TEAL)

        arc1 = Arc(-30 * DEGREES, 60 * DEGREES, arc_center=lozenge.get_left(), radius=0.75)
        arc2 = Arc(-150 * DEGREES, 120 * DEGREES, arc_center=lozenge.get_top(), radius=0.5)

        VGroup(lozenge, arc1, arc2).stretch(0.95, 0)  # Remove

        # arc1_label = Tex(R"60^\circ")
        arc1_label = Tex(R"70.5^\circ")
        arc1_label.next_to(arc1, RIGHT, MED_SMALL_BUFF)
        # arc2_label = Tex(R"120^\circ")
        arc2_label = Tex(R"109.5^\circ")
        arc2_label.next_to(arc2, DOWN, MED_SMALL_BUFF)
        angle_labels = VGroup(
            arc1, arc1_label,
            arc2, arc2_label,
        )
        angle_labels.set_z_index(1)

        self.play(
            ShowCreation(lozenge, time_span=(1, 2.5)),
            VShowPassingFlash(lozenge.copy().insert_n_curves(20).set_stroke(width=5), time_width=2),
            run_time=3
        )
        self.play(
            Write(arc1_label),
            ShowCreation(arc1),
        )
        self.play(
            Write(arc2_label),
            ShowCreation(arc2),
        )
        self.add(angle_labels)
        self.wait()

        # Tile the plane
        verts = lozenge.get_anchors()[:4]
        v1 = verts[1] - verts[0]
        v2 = verts[-1] - verts[0]
        row = VGroup(lozenge.copy().shift(x * v1) for x in range(-10, 11))
        rows = VGroup(row.copy().shift(y * v2) for y in range(-10, 11))
        tiles = VGroup(*rows.family_members_with_points())
        tiles.sort(lambda p: get_norm(p))

        for mob in row, rows:
            mob.set_fill(GREY, 1)
            mob.set_stroke(WHITE, 2)
            mob.shift(-tiles[0].get_center())

        n_center_tiles = 501

        self.play(
            self.frame.animate.set_height(40),
            lozenge.animate.set_fill(GREY, 1),
            LaggedStart(
                (TransformFromCopy(lozenge, tile, path_arc=30 * DEGREES) for tile in row),
                lag_ratio=1.0 / len(row),
                time_span=(1, 3),
            ),
            run_time=4
        )
        self.play(
            LaggedStart(
                (TransformFromCopy(row, row2, path_arc=30 * DEGREES) for row2 in rows),
                lag_ratio=1.0 / len(rows),
                run_time=3,
            ),
        )
        self.clear()
        self.add(rows, angle_labels)

        # Squish it
        self.play(FadeOut(angle_labels))
        rows.save_state()
        self.play(rows.animate.stretch(2, 0), run_time=2)
        self.wait()
        self.play(Restore(rows), run_time=2)
        self.play(Write(angle_labels))
        self.wait()
