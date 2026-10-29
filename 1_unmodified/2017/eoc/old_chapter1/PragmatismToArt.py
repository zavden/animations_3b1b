# ==============================================================================
# Scene:      PragmatismToArt
# Source:     videos/_2017/eoc/old_chapter1.py (lines 481-539)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PragmatismToArt.py PragmatismToArt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PragmatismToArt(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)
        morty.shift(LEFT)
        pragmatism = OldTexText("Pragmatism")
        art = OldTexText("Art")
        pragmatism.move_to(morty.get_corner(UP+LEFT), aligned_edge = DOWN)
        art.move_to(morty.get_corner(UP+RIGHT), aligned_edge = DOWN)
        art.shift(0.2*(LEFT+UP))

        circle1 = Circle(
            radius = 2,
            fill_opacity = 1,
            fill_color = BLUE_E,            
            stroke_width = 0,
        )
        circle2 = Circle(
            radius = 2,
            stroke_color = YELLOW
        )
        arrow = DoubleArrow(LEFT, RIGHT, color = WHITE)
        circle_group = VGroup(circle1, arrow, circle2)
        circle_group.arrange()
        circle_group.to_corner(UP+LEFT)
        circle2.save_state()
        circle2.move_to(circle1)
        q_marks = OldTexText("???").next_to(arrow, UP)


        self.play(
            morty.change_mode, "raise_right_hand",
            morty.look_at, pragmatism,
            Write(pragmatism, run_time = 1),
        )
        self.play(Blink(morty))
        self.play(
            morty.change_mode, "raise_left_hand",
            morty.look_at, art,
            Transform(
                VectorizedPoint(morty.get_corner(UP+RIGHT)),
                art
            ),
            pragmatism.fade, 0.7,
            pragmatism.rotate, np.pi/4,
            pragmatism.shift, DOWN+LEFT
        )
        self.play(Blink(morty))
        self.play(
            GrowFromCenter(circle1),
            morty.look_at, circle1
        )
        self.play(ShowCreation(circle2))
        self.play(
            ShowCreation(arrow),
            Write(q_marks),
            circle2.restore
        )
        self.play(Blink(morty))
