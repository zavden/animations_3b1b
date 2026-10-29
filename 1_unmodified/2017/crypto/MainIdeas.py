# ==============================================================================
# Scene:      MainIdeas
# Source:     videos/_2017/crypto.py (lines 4467-4499)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MainIdeas.py MainIdeas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MainIdeas(Scene):
    def construct(self):
        title = OldTexText("Main ideas")
        title.scale(1.5)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_X_RADIUS)
        h_line.next_to(title, DOWN)
        VGroup(title, h_line).to_corner(UP+LEFT)

        ideas = VGroup(*[
            OldTexText("$\\cdot$ " + words)
            for words in [
                "Digital signatures",
                "The ledger is the currency",
                "Decentralize",
                "Proof of work",
                "Block chain",
            ]
        ])
        colors = BLUE, WHITE, RED, GREEN, YELLOW
        for idea, color in zip(ideas, colors):
            idea.set_color(color)
        ideas.arrange(
            DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        ideas.next_to(h_line, DOWN)

        self.add(title, h_line)
        for idea in ideas:
            self.play(LaggedStartMap(FadeIn, idea))
        self.wait()
