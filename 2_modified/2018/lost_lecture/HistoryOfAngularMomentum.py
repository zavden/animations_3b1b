# ==============================================================================
# Scene:      HistoryOfAngularMomentum
# Source:     videos/_2018/lost_lecture.py (lines 2700-2743)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HistoryOfAngularMomentum.py HistoryOfAngularMomentum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the text and the ImageMobject added to it must live in a Group: VMobject.set_fill/set_opacity (FadeInFromDown) fails on an ImageMobject inside a VMobject family
#   - same: outer container is a Group because it holds an ImageMobject
#   - index_of_submobject_to_align indexes the TARGET too (arrow[0] was Cairo's tip, GL's Arrow has no submobjects): align the moved mobject's first part with submobject_to_align instead
# ==============================================================================

from manim_imports_ext import *

class HistoryOfAngularMomentum(TeacherStudentsScene):
    CONFIG = {
        "camera_config": {"fill_opacity": 1}
    }

    def construct(self):
        am = VGroup(OldTexText("Angular momentum"))
        # CHANGE: the text and the ImageMobject added to it must live in a Group: VMobject.set_fill/set_opacity (FadeInFromDown) fails on an ImageMobject inside a VMobject family
        k2l = Group(OldTexText("Kepler's 2nd law"))
        arrow = Arrow(ORIGIN, RIGHT)

        # CHANGE: same: outer container is a Group because it holds an ImageMobject
        group = Group(am, arrow, k2l)
        group.arrange(RIGHT)
        group.next_to(self.hold_up_spot, UL)

        k2l_image = ImageMobject("Kepler2ndLaw")
        k2l_image.match_width(k2l)
        k2l_image.next_to(k2l, UP)
        k2l.add(k2l_image)

        angular_momentum_formula = OldTex(
            "R", "\\times", "m", "\\vec{\\textbf{v}}_\\perp",
        )
        angular_momentum_formula.set_color_by_tex_to_color_map({
            "R": PINK,
            "v": YELLOW,
        })
        angular_momentum_formula.next_to(am, UP)
        am.add(angular_momentum_formula)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeInFromDown(group),
            self.change_students(*3 * ["pondering"])
        )
        self.wait()
        self.play(
            # CHANGE: index_of_submobject_to_align indexes the TARGET too (arrow[0] was Cairo's tip, GL's Arrow has no submobjects): align the moved mobject's first part with submobject_to_align instead
            am.next_to, arrow, RIGHT,
            {"submobject_to_align": am[0]},
            k2l.next_to, arrow, LEFT,
            {"submobject_to_align": k2l[0]},
            path_arc=90 * DEGREES,
            run_time=2
        )
        self.wait(3)
