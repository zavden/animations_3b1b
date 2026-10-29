# ==============================================================================
# Scene:      TwoKeyIdeas
# Source:     videos/_2025/laplace/main_supplements.py (lines 28-55)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoKeyIdeas.py TwoKeyIdeas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoKeyIdeas(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"{s}": YELLOW, "{s_n}": YELLOW, "{t}": BLUE}
        title = Text("Key ideas from the last chapter", font_size=72)
        title.to_edge(UP)
        underline = Underline(title, buff=-0.05)

        self.add(title, underline)

        ideas = VGroup(
            TexText(R"1) How to think about $e^{{s}{t}}$", t2c=t2c),
            TexText(R"2) Often, for functions in physics, $\displaystyle f({t}) = \sum_{n=1}^N c_n e^{{s_n} {t}}$", t2c=t2c),
        )
        for idea in ideas:
            idea[:2].scale(1.25, about_edge=RIGHT)
        ideas[0][R"$e^{{s}{t}}$"].scale(1.5, about_edge=DL)
        ideas.arrange(DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        ideas.to_edge(LEFT)

        numbers = VGroup(idea[:2] for idea in ideas)
        words = VGroup(idea[2:] for idea in ideas)

        self.play(LaggedStartMap(FadeIn, numbers, shift=LEFT, lag_ratio=0.5))
        self.wait()
        for word in words:
            self.play(Write(word))
            self.wait()
