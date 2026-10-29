# ==============================================================================
# Scene:      GuessSteadyState
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1112-1179)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GuessSteadyState.py GuessSteadyState -w -m --fps 15
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


class GuessSteadyState(InteractiveScene):
    def construct(self):
        # Show prompt
        prompt = VGroup(
            Text("Guess that: "),
            Tex(R"""
                \vec{\textbf{x}}(t) =
                A \cos(\omega_l t)
            """, t2c=EQUATION_T2C)
        )
        prompt.arrange(RIGHT, buff=0.5)
        prompt.to_edge(UP)
        A_part = prompt[1]["A"]
        A_part.set_color(GREY_B)
        freq = prompt[1][R"\omega_l"]

        A_arrow = Vector(0.3 * UP, stroke_width=2).next_to(A_part, DOWN, buff=0.1)
        freq_arrow = Vector(0.3 * UP, stroke_width=2).next_to(freq, DOWN, buff=0.1)
        freq_arrow.set_color(TEAL)

        A_word = Text("Solve for\nthis", font_size=24)
        A_word.next_to(A_arrow, DOWN, buff=0.1)
        freq_word = Text("Light frequency", font_size=24)
        freq_word.next_to(freq_arrow, DOWN, buff=0.1)
        freq_word.shift(0.5 * RIGHT)
        freq_word.set_color(TEAL)
        A_word.align_to(freq_word, UP)

        rect = FullScreenRectangle()
        rect.set_fill(BLACK, 1)
        rect.set_height(2, about_edge=UP, stretch=True)

        self.add(rect)
        self.add(prompt)
        self.play(
            GrowArrow(A_arrow),
            FadeIn(A_word),
        )
        self.play(
            GrowArrow(freq_arrow),
            FadeIn(freq_word),
        )
        self.wait()

        # Answer
        amp_tex = R"\frac{q \vec{\textbf{E}}_0}{m\left(\omega_r^2-\omega_l^2\right)}"
        solution = Tex(
            fR"\vec{{\textbf{{x}}}}(t) = {amp_tex} \cos(\omega_l t)",
            t2c=EQUATION_T2C
        )
        solution.move_to(np.array([3.85, 0.65, 0.0]))

        self.play(
            rect.animate.set_height(FRAME_HEIGHT, about_edge=UP, stretch=True).set_anim_args(run_time=2),
            FadeOut(VGroup(
                prompt[0],
                A_arrow, A_word,
                freq_arrow, freq_word
            )),
            TransformMatchingTex(
                prompt[1], solution,
                matched_pairs=[
                    (prompt[1][R"\vec{\textbf{x}}(t)"], solution[R"\vec{\textbf{x}}(t)"]),
                    (A_part, solution[amp_tex])
                ]
            ),
        )
        self.wait()
