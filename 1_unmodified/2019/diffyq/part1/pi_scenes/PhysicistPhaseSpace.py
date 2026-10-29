# ==============================================================================
# Scene:      PhysicistPhaseSpace
# Source:     videos/_2019/diffyq/part1/pi_scenes.py (lines 233-282)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhysicistPhaseSpace.py PhysicistPhaseSpace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhysicistPhaseSpace(PiCreatureScene):
    def construct(self):
        physy = self.pi_creature
        name = OldTexText("Physicist")
        name.scale(1.5)
        name.to_corner(DL, buff=MED_SMALL_BUFF)
        physy.next_to(name, UP, SMALL_BUFF)
        VGroup(name, physy).shift_onto_screen()

        axes = Axes(
            x_min=-1,
            x_max=10,
            y_min=-1,
            y_max=7,
        )
        axes.set_height(6)
        axes.next_to(physy, RIGHT)
        axes.to_edge(UP)
        axes.set_stroke(width=1)
        x_label = OldTexText("Position")
        x_label.next_to(axes.x_axis.get_right(), UP)
        y_label = OldTexText("Momentum")
        y_label.next_to(axes.y_axis.get_top(), RIGHT)

        title = OldTexText("Phase space")
        title.scale(1.5)
        title.set_color(YELLOW)
        title.move_to(axes)

        self.add(name, physy)

        self.play(
            physy.change, "angry",
            Write(axes),
            FadeInFromDown(title)
        )
        self.wait(2)
        self.play(
            GrowFromPoint(x_label, physy.get_corner(UR)),
            physy.change, "raise_right_hand",
            axes.x_axis.get_right()
        )
        self.play(
            GrowFromPoint(y_label, physy.get_corner(UR)),
            physy.look_at, axes.y_axis.get_top(),
        )
        self.wait(3)

    def create_pi_creature(self):
        return PiCreature(color=GREY).to_corner(DL)
