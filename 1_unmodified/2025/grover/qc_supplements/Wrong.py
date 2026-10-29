# ==============================================================================
# Scene:      Wrong
# Source:     videos/_2025/grover/qc_supplements.py (lines 279-301)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Wrong.py Wrong -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Wrong(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer()
        morty.to_corner(DR)
        # morty.body.insert_n_curves(10000)
        self.play(morty.says("Wrong!", mode="surprised"))
        self.play(Blink(morty))
        self.wait()

        old_bubble = morty.bubble
        new_bubble = morty.get_bubble(Text("Also wrong!"), bubble_type=SpeechBubble)
        self.play(
            TransformMatchingStrings(
                old_bubble.content,
                new_bubble.content,
                key_map={"Wrong": "wrong"},
                run_time=1
            ),
            Transform(old_bubble[0], new_bubble[0]),
            morty.change("tease")
        )
        self.wait()
