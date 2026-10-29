# ==============================================================================
# Scene:      SnapshotOfACar
# Source:     videos/_2017/eoc/chapter2.py (lines 635-674)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SnapshotOfACar.py SnapshotOfACar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SnapshotOfACar(Scene):
    def construct(self):
        car = Car()
        car.scale(1.5)
        car.move_to(3*LEFT+DOWN)
        flash_box = Rectangle(
            width = FRAME_WIDTH,
            height = FRAME_HEIGHT,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 1,
        )
        speed_lines = VGroup(*[
            Line(point, point+0.5*LEFT)
            for point in [
                0.5*UP+0.25*RIGHT,
                ORIGIN, 
                0.5*DOWN+0.25*RIGHT
            ]
        ])
        question = OldTexText("""
            How fast is
            this car going?
        """)

        self.play(MoveCar(
            car, RIGHT+DOWN, 
            run_time = 2,
            rate_func = rush_into
        ))
        car.get_tires().set_color(GREY)
        speed_lines.next_to(car, LEFT)
        self.add(speed_lines)
        self.play(
            flash_box.set_fill, None, 0,
            rate_func = rush_from
        )
        question.next_to(car, UP, buff = LARGE_BUFF)
        self.play(Write(question, run_time = 2))
        self.wait(2)
