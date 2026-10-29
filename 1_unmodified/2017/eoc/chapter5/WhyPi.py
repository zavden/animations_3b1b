# ==============================================================================
# Scene:      WhyPi
# Source:     videos/_2017/eoc/chapter5.py (lines 1102-1140)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyPi.py WhyPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyPi(PiCreatureScene):
    def construct(self):
        circle = Circle(radius = 1, color = MAROON_B)
        circle.rotate(np.pi/2)
        circle.to_edge(UP)
        ghost_circle = circle.copy()
        ghost_circle.set_stroke(width = 1)
        diam = Line(circle.get_left(), circle.get_right())
        diam.set_color(YELLOW)
        one = OldTex("1")
        one.next_to(diam, UP)
        circum = diam.copy()
        circum.set_color(circle.get_color())
        circum.scale(np.pi)
        circum.next_to(circle, DOWN, LARGE_BUFF)
        circum.insert_n_curves(circle.get_num_curves()-2)
        circum.make_jagged()
        pi = OldTex("\\pi")
        pi.next_to(circum, UP)
        why = OldTexText("Why?")
        why.next_to(self.pi_creature, UP, MED_LARGE_BUFF)

        self.add(ghost_circle, circle, diam, one)
        self.wait()
        self.play(Transform(circle, circum, run_time = 2))
        self.play(
            Write(pi),
            Write(why),
            self.pi_creature.change_mode, "confused",
        )
        self.wait(3)


    #######

    def create_pi_creature(self):
        self.pi_creature = Randolph()
        self.pi_creature.to_corner(DOWN+LEFT)
        return self.pi_creature
