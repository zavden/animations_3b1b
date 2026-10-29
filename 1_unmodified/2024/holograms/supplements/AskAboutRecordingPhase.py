# ==============================================================================
# Scene:      AskAboutRecordingPhase
# Source:     videos/_2024/holograms/supplements.py (lines 436-474)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutRecordingPhase.py AskAboutRecordingPhase -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutRecordingPhase(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer()
        morty.to_corner(DR)
        randy = Randolph(height=2.5)
        randy.next_to(morty, LEFT, buff=1.5, aligned_edge=DOWN)
        for pi in [morty, randy]:
            pi.body.insert_n_curves(100)

        self.add(morty, randy)
        self.play(
            morty.says(
                Text("""
                    How could you
                    detect this phase
                    difference?
                """),
                look_at=randy.eyes,
            ),
            randy.change("pondering", morty.eyes)
        )
        self.play(Blink(randy))
        self.play(
            randy.animate.look_at(3 * UL),
            morty.change("tease", 3 * UL),
        )
        self.play(randy.change("erm", 3 * UL))
        self.play(Blink(morty))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("confused", 3 * UL))
        self.play(morty.change("pondering", 3 * UL))
        self.play(Blink(randy))
        self.wait(3)
        self.play(randy.change("thinking", 3 * LEFT))
        self.play(Blink(randy))
        self.play(Blink(morty))
        self.wait(2)
