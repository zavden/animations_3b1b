# ==============================================================================
# Scene:      RunCarFactory
# Source:     videos/_2020/beta/beta1.py (lines 1946-2009)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RunCarFactory.py RunCarFactory -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The placeholder "factory" SVG has only 211 points (the original >318): the trick of covering with black squares (point indices) is omitted
#   - the Car in custom/drawings.py (the repo's version) no longer has the driver `randy`; hiding it is omitted
# ==============================================================================

from manim_imports_ext import *

class RunCarFactory(Scene):
    def construct(self):
        # Factory
        factory = SVGMobject(file_name="factory")
        factory.set_fill(GREY_D)
        factory.set_stroke(width=0)
        factory.flip()
        factory.set_height(6)
        factory.to_edge(LEFT)

        self.add(factory)

        # Dumb hack
        points = factory[0].get_points()
        # CHANGE: the placeholder "factory" SVG has only 211 points (the original had more than 318) and the trick of covering with black squares does not apply; it is omitted
        for line in []:
            square = Square()
            square.set_fill(BLACK, 1)
            square.set_stroke(width=0)
            square.replace(line)
            factory.add(square)

        rect = Rectangle()
        rect.match_style(factory)
        rect.set_height(1.1)
        rect.set_width(6.75, stretch=True)
        rect.move_to(factory, DL)

        # Get cars
        car = Car(color=interpolate_color(BLUE_E, GREY_C, 0.5))
        car.set_height(0.9)
        for tire in car.get_tires():
            tire.set_fill(GREY_C)
            tire.set_stroke(BLACK)
        # CHANGE: the Car in custom/drawings.py (the repo's version) no longer has the driver `randy`; hiding it is omitted
        pass
        car.move_to(rect.get_corner(DR))

        cars = VGroup()
        n_cars = 20
        for x in range(n_cars):
            cars.add(car.copy())

        for car in cars[4], cars[6]:
            scratch = VMobject()
            scratch.start_new_path(UP)
            scratch.add_line_to(0.25 * DL)
            scratch.add_line_to(0.25 * UR)
            scratch.add_line_to(DOWN)
            scratch.set_stroke([RED_A, RED_C], [0.1, 2, 2, 0.1])
            scratch.set_height(0.25)
            scratch.move_to(car)
            scratch.shift(0.1 * DOWN)
            car.add(scratch)

        self.add(cars, rect)
        self.play(LaggedStartMap(
            MoveCar, cars,
            lambda m: (m, m.get_corner(DR) + 10 * RIGHT),
            lag_ratio=0.3,
            rate_func=linear,
            run_time=1.5 * n_cars,
        ))
        self.remove(cars)
