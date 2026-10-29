# ==============================================================================
# Scene:      FrameIntuitionVsExamples
# Source:     videos/_2026/hairy_ball/supplements.py (lines 697-738)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FrameIntuitionVsExamples.py FrameIntuitionVsExamples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FrameIntuitionVsExamples(InteractiveScene):
    def construct(self):
        titles = VGroup(
            Text("Intuitive idea"),
            Text("Counterexample"),
            Text("Clever proof"),
        )
        for x, title in zip([-1, 1, 1], titles):
            title.scale(1.5)
            title.move_to(x * FRAME_WIDTH * RIGHT / 4)
            title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.to_edge(UP, buff=1.5)
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        VGroup(h_line, v_line).set_stroke(WHITE, 2)

        ideas = VGroup(
            Text("Turning a sphere\ninside-out must crease it"),
            Text("All closed loops\nhave inscribed rectangles"),
        )
        for idea in ideas:
            idea.next_to(h_line, DOWN)
            idea.set_color(GREY_A)
            idea.shift(FRAME_WIDTH * LEFT / 4)

        self.add(v_line, h_line)
        self.add(titles[0])
        self.wait()

        # Test
        self.play(FadeIn(ideas[0]))
        self.play(
            FadeIn(titles[1], lag_ratio=0.1)
        )
        self.wait()
        self.play(
            FadeOut(ideas[0]),
            FadeIn(ideas[1]),
            FadeOut(titles[1], lag_ratio=0.1),
            FadeIn(titles[2], lag_ratio=0.1),
        )
        self.wait()
