# ==============================================================================
# Scene:      LongDiffusion
# Source:     videos/_2018/turbulence.py (lines 669-672)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LongDiffusion.py LongDiffusion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Diffusion(VMobject):
    CONFIG = {
        "height": 1.5,
        "n_dots": 1000,
        "colors": [RED, BLUE]
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.add_dots()
        self.add_invisible_circles()

    def add_dots(self):
        dots = VGroup(*[Dot() for x in range(self.n_dots)])
        dots.arrange_in_grid(buff=SMALL_BUFF)
        dots.center()
        dots.set_height(self.height)
        dots.sort(lambda p: p[0])
        dots[:len(dots) // 2].set_color(self.colors[0])
        dots[len(dots) // 2:].set_color(self.colors[1])
        dots.set_fill(opacity=0.8)
        self.dots = dots
        self.add(dots)

    def add_invisible_circles(self):
        circles = VGroup()
        for dot in self.dots:
            point = dot.get_center()
            radius = get_norm(point)
            circle = Circle(radius=radius)
            circle.rotate(angle_of_vector(point))
            circle.fade(1)
            circles.add(circle)
            self.add_updater_to_dot(dot, circle)
        self.add(circles)

    def add_updater_to_dot(self, dot, circle):
        dot.total_time = 0
        radius = get_norm(dot.get_center())
        freq = 0.1 + 0.05 * random.random() + 0.05 / radius

        def update(dot, dt):
            dot.total_time += dt
            prop = (freq * dot.total_time) % 1
            dot.move_to(circle.point_from_proportion(prop))

        dot.add_updater(update)


class LongDiffusion(Scene):
    def construct(self):
        self.add(Diffusion())
        self.wait(30)
