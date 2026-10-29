# ==============================================================================
# Scene:      DisectDrivenEq
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 932-1011)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DisectDrivenEq.py DisectDrivenEq -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

EQUATION_T2C = {
    R"\vec{\textbf{x}}(t)": RED,
    R"\vec{\textbf{F}}(t)": YELLOW,
    R"\vec{\textbf{a}}(t)": YELLOW,
    R"\frac{d^2 \vec{\textbf{x}}}{dt^2}(t) ": YELLOW,
    R"\vec{\textbf{E}}_0": BLUE,
    R"\omega_r": PINK,
    R"\omega_l": TEAL,
}


class DisectDrivenEq(InteractiveScene):
    def construct(self):
        # Setup
        driven_eq = Tex(
            R"""
                \vec{\textbf{F}}(t) = - k \vec{\textbf{x}}(t)
                + \vec{\textbf{E}}_0 q \cos(\omega_l t)
            """,
            t2c=EQUATION_T2C
        )
        driven_eq.to_corner(UR, buff=0.6)

        lhs = driven_eq[R"\vec{\textbf{F}}(t) = - k \vec{\textbf{x}}(t)"]
        parts = VGroup(*(
            driven_eq[tex]
            for tex in [
                R"\vec{\textbf{E}}_0 q \cos(\omega_l t)",
                R"\omega_l",
                R"\vec{\textbf{E}}_0",
                R"q",
            ]
        ))
        light_part, omega_l, E0, q = parts
        words = VGroup(
            Text("Force from a\nlight wave"),
            Text("Angular frequency\nof the light (color)"),
            Text("Strength of\nthe wave"),
            Text("Charge of the\nelectron"),
        )
        words[0].scale(0.75)
        words[1:].scale(0.75)
        for part, word in zip(parts, words):
            word.next_to(part, DOWN, buff=0.35)
            word.shift_onto_screen()
            word.match_color(part[0][0])
        words[0].set_color(WHITE)

        rect = SurroundingRectangle(light_part)
        rect.set_stroke(TEAL, 2)

        # for expr in driven_eq, words[0]:
        #     bg = BackgroundRectangle(expr, buff=MED_SMALL_BUFF)
        #     bg.set_fill(BLACK, 1)
        #     self.add(bg)

        words[0].set_backstroke(BLACK, 8)

        # Animations
        self.play(FadeIn(lhs, UP))
        self.wait()
        self.play(
            Write(driven_eq["+"]),
            FadeIn(light_part, lag_ratio=0.1),
        )
        self.play(
            ShowCreation(rect),
            Write(words[0]),
        )
        self.wait()

        self.play(
            rect.animate.surround(omega_l),
            FadeTransform(*words[0:2]),
        )
        self.wait()
        self.play(
            rect.animate.surround(E0),
            FadeTransform(*words[1:3]),
        )
        self.wait()
        self.play(
            rect.animate.surround(q),
            FadeTransform(*words[2:4]),
        )
        self.wait()
        self.play(
            rect.animate.surround(light_part),
            FadeTransform(words[3], words[0]),
        )
        self.wait()
