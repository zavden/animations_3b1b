# ==============================================================================
# Scene:      RungsUpToGalaxies
# Source:     videos/_2025/cosmic_distance/part2.py (lines 1369-1393)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RungsUpToGalaxies.py RungsUpToGalaxies -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RungsUpToGalaxies(InteractiveScene):
    def construct(self):
        # Test
        rungs = VGroup(
            Text("Distance to the sun"),
            Text("Stellar parallax"),
            Text("Main sequence fitting"),
            Text("Cepheid periods"),
            Text("Red shift"),
        )
        rungs.arrange(UP, buff=LARGE_BUFF, aligned_edge=LEFT)
        rungs.to_edge(LEFT)

        self.add(rungs)
        for n in [0, 1, 2, 4, 3, 4]:
            rungs.target = rungs.generate_target()
            for k, rung in enumerate(rungs.target):
                if n == k:
                    height, opacity = (0.5, 1)
                else:
                    height, opacity = (0.3, 0.35)
                rung.set_height(height, about_edge=LEFT)
                rung.set_opacity(opacity)
            self.play(MoveToTarget(rungs))
            self.wait()
