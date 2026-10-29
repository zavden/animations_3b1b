# ==============================================================================
# Scene:      RandyIsSickOrNot
# Source:     videos/_2018/eop/chapter1/show_uncertainty_disease.py (lines 6-56)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/sick_pi_creature.py
#
# Run from this folder:
#     manimgl RandyIsSickOrNot.py RandyIsSickOrNot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/eop_constants.py -----

SICKLY_GREEN = "#9BBD37"



# ----- From _2018/eop/reusables/sick_pi_creature.py -----

class SicklyPiCreature(PiCreature):
    CONFIG = {
        "sick_color": SICKLY_GREEN
    }

    def get_slightly_sick(self):

        self.save_state()
        self.set_color(self.sick_color)

    def get_sick(self):

        self.get_slightly_sick()
        self.change_mode("sick")

    def get_better(self):
        self.restore()



# ----- From _2018/eop/chapter1/show_uncertainty_disease.py -----

class RandyIsSickOrNot(Scene):


    def construct(self):
        title = OldTexText("1 in 200")
        title.to_edge(UP)

        
        randy = SicklyPiCreature()
        randy.set_height(3)
        randy.move_to(2*LEFT)
        randy.change_mode("plain")
        randy.set_color(BLUE)
        randy.save_state()

        self.add(randy)

        p_sick = OldTex("p(","\\text{sick}",") = 0.5\%").scale(1.7)
        p_sick.set_color_by_tex("sick", SICKLY_GREEN)
        p_sick.next_to(randy, UP, buff = LARGE_BUFF)
        self.add(p_sick)
        self.wait()
        
        self.play(
            ApplyMethod(randy.get_slightly_sick, rate_func = there_and_back)
        )
        self.play(Blink(randy))
        self.wait(2)

        self.play(
            ApplyMethod(randy.get_sick)
        )

        self.play(Blink(randy))
        self.wait()

        self.play(randy.get_better)

        self.play(
            ApplyMethod(randy.get_slightly_sick, rate_func = there_and_back)
        )
        self.play(Blink(randy))
        self.wait(0.5)

        self.play(
            ApplyMethod(randy.get_sick)
        )
        
        self.play(Blink(randy))
        self.play(randy.get_better)
        self.wait(3)
