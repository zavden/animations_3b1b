# ==============================================================================
# Scene:      DigitsOfPi
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 919-982)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DigitsOfPi.py DigitsOfPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DigitsOfPi(InteractiveScene):
    def construct(self):
        # Test
        pi_text = Path(Path(__file__).parent, "digits_of_pi.txt").read_text()
        pi_text_lines = pi_text.split("\n")
        one_line_pi = Tex(R"\pi = " + pi_text_lines[0])
        one_line_pi[0].scale(1.5)
        self.play(FadeIn(one_line_pi, lag_ratio=0.25, run_time=5))
        self.wait()

        # Second half
        index = 25
        nines = Tex(R"\dots999999999999999999999 \dots")
        nines.next_to(one_line_pi[:index], RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)

        prefix_brace = Brace(VGroup(one_line_pi[2:index], nines[:3]), UP, MED_SMALL_BUFF)
        prefix_label = prefix_brace.get_text("First n digits")
        nines_brace = Brace(nines[3:], UP, MED_SMALL_BUFF)
        nines_label = nines_brace.get_text("Next n digits")

        self.play(
            FadeOut(one_line_pi[index:]),
            FadeIn(nines, lag_ratio=0.25, run_time=3),
        )
        self.wait()
        self.play(LaggedStart(
            GrowFromCenter(prefix_brace),
            Write(prefix_label),
            GrowFromCenter(nines_brace),
            Write(nines_label),
            lag_ratio=0.25
        ))
        self.wait()

        # Show full pi
        frame = self.frame
        pi_tex = pi_text[2:].replace("\n", R"\\&")
        full_pi = Tex(R"\pi = 3.&" + pi_tex)
        full_pi.to_edge(UP)
        dots = Tex(R"\vdots", font_size=72)
        dots.next_to(full_pi, DOWN)
        digits_per_line = len(pi_text_lines[-1].strip())
        big_nines = Text("\n".join([
            "9" * digits_per_line
            for line in pi_text_lines
        ]))
        big_nines.match_width(full_pi[-digits_per_line:])
        big_nines.next_to(dots, DOWN)
        big_nines.align_to(full_pi, RIGHT)
        big_nines.set_color(RED)

        self.play(
            ReplacementTransform(one_line_pi[:index], full_pi[:index]),
            FadeIn(full_pi[index:], lag_ratio=1e-3, time_span=(0.5, 3)),
            FadeOut(VGroup(prefix_brace, prefix_label, nines_brace, nines_label, nines)),
            FadeIn(dots, time_span=(2, 3))
        )
        self.wait()
        self.play(
            frame.animate.scale(1.8, about_edge=UP),
            FadeIn(big_nines, lag_ratio=1e-2),
            run_time=6
        )
        self.wait()
