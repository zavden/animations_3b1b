# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2018/wallis.py (lines 169-194)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(Scene):
    def construct(self):
        topics = VGroup(
            OldTexText("The setup"),
            OldTexText("Circle geometry with complex polynomials"),
            OldTexText("Proof of the Wallis product"),
            OldTexText("Formalities not discussed"),
            OldTexText(
                "Generalizing this proof to get \\\\ the product formula for sine"),
        )
        for topic in topics:
            dot = Dot(color=BLUE)
            dot.next_to(topic, LEFT)
            topic.add(dot)
        topics.arrange(
            DOWN, aligned_edge=LEFT, buff=LARGE_BUFF
        )
        self.add(topics)
        self.wait()
        for i in range(len(topics)):
            self.play(
                topics[i + 1:].set_fill, {"opacity": 0.25},
                topics[:i].set_fill, {"opacity": 0.25},
                topics[i].set_fill, {"opacity": 1},
            )
            self.wait(2)
