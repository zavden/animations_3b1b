# ==============================================================================
# Scene:      WhatWeNeedToUnderstand
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 118-161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatWeNeedToUnderstand.py WhatWeNeedToUnderstand -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatWeNeedToUnderstand(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        # React
        self.play(
            self.change_students("pondering", "maybe", "confused", look_at=self.screen),
            morty.change("tease")
        )
        self.wait(3)
        self.play(
            self.change_students("erm", "sassy", "maybe", look_at=self.screen)
        )
        self.wait(3)

        # Core concepts
        concepts = VGroup(
            Text("Polarization"),
            Text("Scattering"),
            Text("The index of refraction"),
        )
        concepts.arrange(DOWN, aligned_edge=LEFT)
        concepts.next_to(self.hold_up_spot, UP)

        for i in range(3):
            concepts[i].align_to(concepts, DOWN)
            self.play(
                FadeIn(concepts[i], 0.5 * UP),
                concepts[:i].animate.shift(UP),
                morty.change("raise_right_hand", concepts),
                *(pi.animate.look_at(concepts) for pi in stds),
            )
            self.wait()
        self.wait()

        # Start with an overview
        self.play(
            morty.says("To begin:\nAn overview"),
            FadeOut(concepts, UP),
            self.change_students("tease", "happy", "well", look_at=morty.eyes)
        )
        self.look_at(self.screen)
        self.wait(3)
