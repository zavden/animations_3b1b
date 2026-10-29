# ==============================================================================
# Scene:      SeparateIntoTwoQuestions
# Source:     videos/_2019/spirals.py (lines 1391-1432)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeparateIntoTwoQuestions.py SeparateIntoTwoQuestions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SeparateIntoTwoQuestions(Scene):
    def construct(self):
        top_q = OldTexText("Why do", " primes", " cause", " spirals", "?")
        top_q.scale(2)
        top_q.to_edge(UP)

        q1 = OldTexText("Where do the\\\\", "spirals", " come from?")
        q2 = OldTexText("What happens when\\\\", "filtering to", " primes", "?")
        for q in q1, q2:
            q.scale(1.3)
            q.next_to(top_q, DOWN, LARGE_BUFF)
        q1.to_edge(LEFT)
        q1.set_color(YELLOW)
        q2.to_edge(RIGHT)
        q2.set_color(TEAL)

        v_line = DashedLine(
            top_q.get_bottom() + MED_SMALL_BUFF * DOWN,
            FRAME_HEIGHT * DOWN / 2,
        )

        self.add(top_q)
        self.wait()

        for q, text in [(q1, "spirals"), (q2, "primes")]:
            self.play(
                top_q.get_part_by_tex(text).set_color, q.get_color(),
                TransformFromCopy(
                    top_q.get_part_by_tex(text),
                    q.get_part_by_tex(text),
                ),
                LaggedStartMap(
                    FadeIn,
                    filter(
                        lambda m: m is not q.get_part_by_tex(text),
                        q,
                    )
                ),
            )
        self.wait()
        self.play(ShowCreation(v_line))
        self.wait()
