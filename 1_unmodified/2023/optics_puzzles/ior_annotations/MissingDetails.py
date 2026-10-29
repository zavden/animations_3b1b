# ==============================================================================
# Scene:      MissingDetails
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1347-1370)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MissingDetails.py MissingDetails -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MissingDetails(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Details I skipped:", font_size=72)
        title.to_edge(UP)
        title.add(Underline(title))
        title.set_color(BLUE)

        details = BulletedList(
            "There will be many resonant frequencies",
            "Our force law should include a damping term",
            "Why the wave produced by a plane of charges is a \\\\" + \
            "quarter-cycle out of phase with the incoming light",
            "Everything related to the magnetic field",
            "Whether accounting for quantum effects makes a difference",
        )
        details.next_to(title, DOWN, buff=0.5)
        details.set_fill(border_width=0)

        self.add(title)
        self.play(LaggedStartMap(FadeIn, details, shift=0.5 * DOWN, lag_ratio=0.35, run_time=3))
        self.wait()
        self.play(details.animate.fade_all_but(1))
        self.wait()
