# ==============================================================================
# Scene:      ShowSomeOrthonormalTransformations
# Source:     videos/_2018/cramer.py (lines 1247-1260)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSomeOrthonormalTransformations.py ShowSomeOrthonormalTransformations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSomeOrthonormalTransformations(LinearTransformationScene):
    CONFIG = {
        "random_seed": 1,
        "n_angles": 7,
    }

    def construct(self):
        for x in range(self.n_angles):
            angle = TAU * np.random.random() - TAU / 2
            matrix = rotation_matrix(angle, OUT)[:2, :2]
            if x in [2, 4]:
                matrix[:, 1] *= -1
            self.apply_matrix(matrix, run_time=1)
            self.wait()
