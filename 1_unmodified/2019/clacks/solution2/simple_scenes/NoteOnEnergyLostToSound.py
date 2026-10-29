# ==============================================================================
# Scene:      NoteOnEnergyLostToSound
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 74-82)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoteOnEnergyLostToSound.py NoteOnEnergyLostToSound -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoteOnEnergyLostToSound(Scene):
    def construct(self):
        self.add(OldTexText(
            "Yeah yeah, the clack sound\\\\"
            "would require energy, but\\\\"
            "don't let accuracy get in the\\\\"
            "way of delight!",
            alignment="",
        ))
