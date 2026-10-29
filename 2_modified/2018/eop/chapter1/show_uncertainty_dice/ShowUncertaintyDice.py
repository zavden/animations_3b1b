# ==============================================================================
# Scene:      ShowUncertaintyDice
# Source:     videos/_2018/eop/chapter1/show_uncertainty_dice.py (lines 4-33)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/dice.py
#
# Run from this folder:
#     manimgl ShowUncertaintyDice.py ShowUncertaintyDice -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - removed self.ensure_valid_file() (GL SVGMobject has no such method; it resolves file_name itself)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/dice.py -----

class DieFace(SVGMobject):
    
    def __init__(self, value, **kwargs):

        self.value = value
        self.file_name = "Dice-" + str(value)
        # CHANGE: ensure_valid_file() does not exist in GL (SVGMobject finds the file by name)
        SVGMobject.__init__(self, file_name = self.file_name)


class RowOfDice(VGroup):
    CONFIG = {
        "values" : list(range(1,7)),
        "direction": RIGHT,
    }

    def init_points(self):
        for value in self.values:
            new_die = DieFace(value)
            new_die.submobjects[0].set_fill(opacity = 0)
            new_die.submobjects[0].set_stroke(width = 7)
            new_die.next_to(self, self.direction)
            self.add(new_die)
        self.move_to(ORIGIN)



# ----- From _2018/eop/chapter1/show_uncertainty_dice.py -----

class ShowUncertaintyDice(Scene):

    def throw_a_die(self, run_time = 0.3):

        eye = np.random.randint(1,7)
        face = self.row_of_dice.submobjects[eye - 1]

        self.play(
            ApplyMethod(face.submobjects[0].set_fill, {"opacity": 1},
                rate_func = there_and_back,
                run_time = run_time,
            ),
        )

    def construct(self):

        self.row_of_dice = RowOfDice(direction = DOWN).scale(0.5)
        self.add(self.row_of_dice)

        for i in range(5):
            self.throw_a_die()
            self.wait(1)

        for i in range(10):
            self.throw_a_die()
            self.wait(0.3)

        for i in range(100):
            self.throw_a_die(0.05)
            self.wait(0.0)
