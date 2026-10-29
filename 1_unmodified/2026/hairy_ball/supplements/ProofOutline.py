# ==============================================================================
# Scene:      ProofOutline
# Source:     videos/_2026/hairy_ball/supplements.py (lines 267-326)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProofOutline.py ProofOutline -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProofOutline(InteractiveScene):
    def construct(self):
        # Add outline
        title = Text("Proof by Contradiction", font_size=72)
        title.to_edge(UP)
        background = FullScreenRectangle()

        frames = Square().replicate(2)
        frames.set_height(4.5)
        frames.arrange(RIGHT, buff=3.5)
        frames.next_to(title, DOWN, buff=1.5)
        frames.set_fill(BLACK, 1)
        frames.set_stroke(WHITE, 2)

        implies = Tex(R"\Longrightarrow", font_size=120)
        implies.move_to(frames)

        impossibility = Text("Impossibility", font_size=90)
        impossibility.next_to(implies, RIGHT, MED_LARGE_BUFF)
        impossibility.set_color(RED)

        assumption = Text("Assume there exists a non-zero\ncontinuous vector field", font_size=30)
        assumption.set_color(BLUE)
        assumption.next_to(frames[0], UP)

        self.add(background)
        self.play(Write(title), run_time=2)
        self.wait()
        self.play(
            FadeIn(frames[0]),
            # FadeIn(assumption, lag_ratio=0.01)
        )
        self.wait()
        implies.save_state()
        implies.stretch(0, 0, about_edge=LEFT)
        self.play(Restore(implies))
        self.play(FadeIn(impossibility, lag_ratio=0.1))
        self.wait()
        self.play(
            DrawBorderThenFill(frames[1]),
            impossibility.animate.scale(0.5).next_to(frames[1], UP)
        )
        self.wait()
        self.play(FadeOut(impossibility))

        # Next part
        words = VGroup(Text("Assume the impossible"), Text("Find a contradiction"))
        brace = Brace(frames[0], RIGHT)
        question = Text("What do we\nshow here?", font_size=72)
        question.next_to(brace, RIGHT)

        self.play(
            FadeOut(implies),
            FadeOut(frames[1]),
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(question, lag_ratio=0.1),
        )
        self.wait()
