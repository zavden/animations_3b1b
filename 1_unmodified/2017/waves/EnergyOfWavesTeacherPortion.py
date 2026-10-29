# ==============================================================================
# Scene:      EnergyOfWavesTeacherPortion
# Source:     videos/_2017/waves.py (lines 2334-2414)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EnergyOfWavesTeacherPortion.py EnergyOfWavesTeacherPortion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class EnergyOfWavesTeacherPortion(TeacherStudentsScene):
    def construct(self):
        self.show_energy_equation()
        self.show_both_ways_of_thinking_about_it()

    def show_energy_equation(self):
        dot = Dot(self.teacher.get_top() + 2*(UP+LEFT))
        dot.fade(1)
        self.dot = dot

        energy = OldTex(
            "\\frac{\\text{Energy}}{\\text{Volume}}",
            "=", 
            "\\epsilon_0", "A", "^2"
        )
        energy.set_color_by_tex("A", GREEN)
        energy.to_corner(UP+LEFT)

        component_energy = OldTex(
            "=", "\\epsilon_0", "A_x", "^2", 
            "+", "\\epsilon_0", "A_y", "^2", 
        )
        for i in 2, 6:
            component_energy[i][0].set_color(GREEN)
            component_energy[i+1].set_color(GREEN)
        component_energy.next_to(energy[1], DOWN, MED_LARGE_BUFF, LEFT)

        self.play(
            Animation(dot),
            self.teacher.change, "raise_right_hand", dot,
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = dot
        )
        self.wait(2)
        self.play(Write(energy))
        self.play(self.teacher.change, "happy")
        self.wait(3)
        self.play(
            ReplacementTransform(
                VGroup(*energy[-4:]).copy(),
                VGroup(*component_energy[:4])
            ),
            ReplacementTransform(
                VGroup(*energy[-4:]).copy(),
                VGroup(*component_energy[4:])
            )
        )
        self.play_student_changes(*["happy"]*3, look_at = energy)
        self.wait()

    def show_both_ways_of_thinking_about_it(self):
        s1, s2 = self.get_students()[:2]
        b1, b2 = [
            ThoughtBubble(direction = v).scale(0.5)
            for v in (LEFT, RIGHT)
        ]
        b1.pin_to(s1)
        b2.pin_to(s2)

        b1.write("Add \\\\ components")
        b2.write("Pythagorean \\\\ theorem")

        for b, s in (b1, s1), (b2, s2):
            self.play(
                ShowCreation(b),
                Write(b.content, run_time = 2),
                s.change, "thinking"
            )
            self.wait(2)
        self.play_student_changes(
            *["plain"]*3,
            look_at = self.dot,
            added_anims = [
                self.teacher.change, "raise_right_hand", self.dot
            ]

        )
        self.play(self.teacher.look_at, self.dot)
        self.wait(5)
