# ==============================================================================
# Scene:      TopicRolidex
# Source:     videos/_2022/puzzles/subsets.py (lines 4416-4449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TopicRolidex.py TopicRolidex -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TopicRolidex(InteractiveScene):
    def construct(self):
        words = VGroup(
            Text("Algebra"),
            Text("Number theory"),
            Text("Analysis"),
            Text("Topology"),
            Text("Geometry"),
            Text("Combinatorics"),
            Text("Group theory"),
        )
        words.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)
        words.arrange(DOWN, aligned_edge=LEFT)
        words.next_to(ORIGIN, DR)
        words.shift(UP)

        def update_words(ws):
            for word in ws:
                word.set_opacity(1.0 - clip(1.25 * abs(word.get_y()), 0, 1))

        words.add_updater(update_words)

        lhs = Text("Example in ")
        lhs.center()
        words.next_to(lhs, RIGHT, submobject_to_align=words[0])
        self.add(lhs)

        self.add(words)
        self.play(
            words.animate.shift(-words[-2].get_y() * UP),
            UpdateFromFunc(words, update_words),
            run_time=4
        )
        self.wait()
