# ==============================================================================
# Scene:      ProsConsOfContext
# Source:     videos/_2021/some1_winners.py (lines 309-362)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProsConsOfContext.py ProsConsOfContext -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProsConsOfContext(Scene):
    def construct(self):
        title = Text("Framing as a contest", font_size=60)
        title.to_edge(UP)

        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(title, DOWN)
        v_line = Line(h_line.get_center(), FRAME_HEIGHT * DOWN / 2)

        pro_label = Text("Pros", font_size=60)
        pro_label.set_color(GREEN)
        pro_label.next_to(h_line, DOWN)
        pro_label.set_x(-FRAME_WIDTH / 4)
        con_label = Text("Cons", font_size=60)
        con_label.set_color(RED)
        con_label.next_to(h_line, DOWN)
        con_label.set_x(FRAME_WIDTH / 4)

        self.play(
            LaggedStart(
                ShowCreation(h_line),
                ShowCreation(v_line),
                lag_ratio=0.5,
            ),
            LaggedStart(
                FadeIn(title, 0.25 * UP),
                FadeIn(pro_label),
                FadeIn(con_label),
                lag_ratio=0.5,
            )
        )
        self.wait()

        pros = VGroup(
            Text("Clear deadline"),
            Text("Extra push for quality"),
        )
        pros.set_color(GREEN_A)
        pros.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        pros.next_to(pro_label, DOWN, LARGE_BUFF)

        con = Text("Suggests that\nsuccess = winning")
        con.set_color(RED_B)
        con.match_x(con_label)
        con.align_to(pros[0], UP)

        for words in (*pros, con):
            dot = Dot()
            dot.next_to(words[0], LEFT)
            words.add_to_back(dot)
            self.play(Write(words, run_time=2))
            self.wait()

        self.embed()
