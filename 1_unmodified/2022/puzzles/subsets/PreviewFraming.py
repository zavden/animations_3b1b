# ==============================================================================
# Scene:      PreviewFraming
# Source:     videos/_2022/puzzles/subsets.py (lines 209-287)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewFraming.py PreviewFraming -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewFraming(TeacherStudentsScene):
    def construct(self):
        # Setup
        morty = self.teacher
        ss = self.students

        # top_text = Text("Question about whole numbers")
        # tt0 = top_text
        # tt1 = VMobject()
        top_text = Text("Today's puzzle (explained in a moment)")
        tt0 = top_text.select_part("Today's puzzle")
        tt1 = top_text.select_part("(explained in a moment)")

        top_text.to_edge(UP, buff=MED_SMALL_BUFF)
        tt1.set_fill(GREY_B)
        tt0.save_state()
        tt0.set_x(0)
        top_rect = Rectangle(
            width=0.75 * FRAME_WIDTH,
            height=0.125 * FRAME_WIDTH,
        )
        top_rect.set_fill(BLACK, 1)
        top_rect.set_stroke(WHITE, 1)
        top_rect.next_to(top_text, DOWN)

        self.play(
            # FadeInFromPoint(top_rect, morty.get_corner(UR)),
            DrawBorderThenFill(top_rect),
            morty.change("raise_right_hand", top_rect),
            self.change_students(
                "erm", "thinking", "pondering",
                look_at=top_rect,
            ),
            Write(tt0)
        )
        self.wait(2)
        self.play(
            tt0.animate.restore(),
            FadeIn(tt1, lag_ratio=0.1),
            self.change_students(
                "pondering", "hesitant", "sassy",
                look_at=top_rect,
            ),
        )
        self.wait(4)

        # Spoiler
        spoiler_rect = ScreenRectangle()
        spoiler_rect.set_fill(BLACK, 1)
        spoiler_rect.set_stroke(WHITE, 1)
        spoiler_rect.set_height(4.5)
        spoiler_rect.to_corner(DL)
        spoiler_rect.align_to(top_rect, LEFT)
        spoiler_word = Text("Spoiler", color=RED, font_size=60)
        # spoiler_word = Text("Complex solution", color=BLUE)
        spoiler_word.next_to(spoiler_rect, RIGHT, buff=MED_LARGE_BUFF, aligned_edge=UP)
        spoiler_word.shift(SMALL_BUFF * DOWN)

        for pi in ss:
            pi.generate_target()
            pi.target.shift(2 * DOWN)
            pi.target.change("horrified", UP)
            pi.target.set_opacity(0)

        self.play(
            FadeIn(spoiler_rect, DOWN),
            LaggedStartMap(MoveToTarget, ss, run_time=1.5),
            morty.change("tease", ORIGIN),
            Write(spoiler_word),
        )
        self.play(Blink(morty))
        self.wait(3)
        self.play(morty.change("surprised", spoiler_rect))
        self.play(Blink(morty))
        self.wait(2)
        self.play(morty.change("hesitant", spoiler_rect))
        self.wait()
        self.play(Blink(morty))
        self.wait(3)
