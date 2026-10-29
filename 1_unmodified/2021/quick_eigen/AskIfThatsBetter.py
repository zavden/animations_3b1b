# ==============================================================================
# Scene:      AskIfThatsBetter
# Source:     videos/_2021/quick_eigen.py (lines 1316-1338)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskIfThatsBetter.py AskIfThatsBetter -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskIfThatsBetter(Scene):
    def construct(self):
        randy = Randolph(height=2)
        randy.to_edge(DOWN)
        randy.change("pondering", UL)

        self.add(BackgroundRectangle(randy, fill_opacity=1), randy)
        self.play(
            PiCreatureSays(
                randy, "Is that better?", target_mode="sassy",
                bubble_config={"direction": LEFT, "width": 4, "height": 2},
                look_at=UL
            )
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            RemovePiCreatureBubble(randy, target_mode="thinking")
        )
        self.wait(2)
        self.play(randy.change("pondering", UL))
        self.play(Blink(randy))
        self.wait()
