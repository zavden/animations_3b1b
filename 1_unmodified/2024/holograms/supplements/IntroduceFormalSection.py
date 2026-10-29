# ==============================================================================
# Scene:      IntroduceFormalSection
# Source:     videos/_2024/holograms/supplements.py (lines 1343-1410)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceFormalSection.py IntroduceFormalSection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceFormalSection(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(LaggedStart(
            stds[0].change("sassy", morty.eyes),
            stds[1].says("Okay but really, why\ndoes it work?", look_at=morty.eyes),
            stds[2].change("angry", look_at=morty.eyes),
            morty.change("guilty"),
        ))
        self.wait(2)
        self.play(LaggedStart(
            morty.change("tease"),
            stds[0].change("well"),
            stds[1].debubble(),
            stds[2].change("hesitant"),
            lag_ratio=0.5
        ))
        self.wait(2)

        # Show complex plane
        plane = ComplexPlane((-3, 3), (-3, 3))
        plane.faded_lines.set_stroke(BLUE_E, 1, 0.5)
        plane.axes.set_stroke(width=1)
        plane.background_lines.set_stroke(width=1)
        plane.set_width(3)
        plane.next_to(self.hold_up_spot, UP)

        a, b = (2, 1.5)
        z = complex(a, b)
        z_dot = GlowDot(plane.n2p(0), color=WHITE)
        z_dot.set_z_index(1)
        h_line = Line(plane.n2p(0), plane.n2p(a))
        v_line = Line(plane.n2p(a), plane.n2p(z))
        h_line.set_stroke(YELLOW, 3)
        v_line.set_stroke(RED, 3)
        a_label = Tex(R"a", font_size=24)
        a_label.match_color(h_line)
        a_label.next_to(h_line, DOWN, buff=0.1)
        b_label = Tex(R"bi", font_size=24)
        b_label.match_color(v_line)
        b_label.next_to(v_line, RIGHT, buff=0.1)
        z_label = Tex(R"a + bi", font_size=24)
        z_label.next_to(v_line.get_end(), UR, SMALL_BUFF)
        VGroup(a_label, b_label, z_label).set_backstroke(BLACK, 3)

        self.play(
            morty.change("raise_right_hand", plane),
            self.change_students(*3 * ["pondering"], look_at=plane),
            FadeIn(plane, UP),
        )
        self.play(
            ShowCreation(h_line),
            FadeIn(a_label, 0.5 * RIGHT),
            z_dot.animate.move_to(plane.n2p(a)),
        )
        self.play(
            ShowCreation(v_line),
            FadeIn(b_label, 0.5 * UP),
            z_dot.animate.move_to(plane.n2p(z)),
        )
        self.play(
            TransformMatchingShapes(VGroup(a_label, b_label).copy(), z_label)
        )
        self.play(self.change_students("erm", "thinking", "well", look_at=plane))
        self.wait(2)
