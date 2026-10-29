# ==============================================================================
# Scene:      RandomDieRolls
# Source:     videos/_2023/clt/main.py (lines 137-156)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomDieRolls.py RandomDieRolls -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RandomDieRolls(InteractiveScene):
    def construct(self):
        n_runs = 30
        n_movements_per_run = 30

        faces = VGroup(*(
            DieFace(n, fill_color=BLUE_E, dot_color=WHITE)
            for n in range(1, 7)
        ))

        for x in range(n_runs):
            random_faces = VGroup(*(
                random.choice(faces).copy()
                for x in range(n_movements_per_run)
            ))
            for face in random_faces:
                face.shift(np.random.uniform(-0.1, 0.1, 3))
            self.play(ShowSubmobjectsOneByOne(random_faces, run_time=1))
            self.wait()
            self.remove(random_faces)
