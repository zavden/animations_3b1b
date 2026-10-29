# ==============================================================================
# Scene:      NoteToPatrons
# Source:     videos/_2022/puzzles/subsets.py (lines 4687-4708)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoteToPatrons.py NoteToPatrons -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoteToPatrons(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        title = Text("(Note for patrons)", font_size=60)
        title.to_edge(UP)

        self.play(
            morty.change("raise_right_hand"),
            FadeInFromPoint(title, morty.get_corner(UL)),
        )
        modes = ["happy", "tease", "shruggie", "gracious"]
        for x in range(70):
            if random.random() < 0.3:
                self.play(Blink(morty))
            elif random.random() < 0.1:
                self.play(morty.change(
                    random.choice(modes),
                    title,
                ))
            else:
                self.wait()
