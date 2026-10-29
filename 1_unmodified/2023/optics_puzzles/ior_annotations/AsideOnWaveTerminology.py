# ==============================================================================
# Scene:      AsideOnWaveTerminology
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 428-453)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AsideOnWaveTerminology.py AsideOnWaveTerminology -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AsideOnWaveTerminology(TeacherStudentsScene):
    def construct(self):
        # Test
        title = Text("Wave terminology", font_size=60)
        title.to_corner(UR)
        title.to_edge(UP, buff=0.25)
        title.add(Underline(title))
        title.set_color(YELLOW)
        terms = VGroup(
            Text("Phase"),
            Text("Frequency"),
            Text("Wave number"),
            Text("Amplitude"),
        )
        terms.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        terms.next_to(title, DOWN)
        terms.shift(0.5 * LEFT)

        self.add(title, terms)

        self.play(
            self.teacher.change("raise_right_hand", terms),
            self.change_students("pondering", "tease", "hesitant", look_at=terms),
            LaggedStartMap(FadeIn, terms, shift=0.25 * DOWN, lag_ratio=0.5),
        )
        self.wait(3)
