# ==============================================================================
# Scene:      ShowDiskScaling
# Source:     videos/_2017/fractal_dimension.py (lines 1577-1683)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDiskScaling.py ShowDiskScaling -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def break_up(mobject, factor = 1.3):
    mobject.scale(factor)
    for submob in mobject:
        submob.scale(1./factor)
    return mobject


class Britain(SVGMobject):
    CONFIG = {
        "file_name" : "Britain.svg",
        "stroke_width" : 0,
        "fill_color" : BLUE_D,
        "fill_opacity" : 1,
        "height" : 5,
        "mark_paths_closed" : True,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_points(self[0].get_points())
        self.submobjects = []
        self.set_height(self.height)
        self.center()


class ShowDiskScaling(Scene):
    def construct(self):
        self.show_non_self_similar_shapes()
        self.isolate_disk()
        self.scale_disk()
        self.write_mass_scaling_factor()
        self.try_fitting_small_disks()

    def show_non_self_similar_shapes(self):
        title = OldTexText(
            "Most shapes are not self-similar"
        )
        title.to_edge(UP)
        self.add(title)

        hexagon = RegularPolygon(n = 6)
        disk = Circle()
        blob = VMobject().set_points_smoothly([
            RIGHT, RIGHT+UP, ORIGIN, RIGHT+DOWN, LEFT, UP, RIGHT
        ])
        britain = Britain()
        shapes = VGroup(hexagon, blob, disk, britain)
        for shape in shapes:
            shape.set_width(1.5)
            shape.set_stroke(width = 0)
            shape.set_fill(opacity = 1)
        shapes.set_color_by_gradient(BLUE_B, BLUE_E)
        shapes.arrange(RIGHT, buff = LARGE_BUFF)
        shapes.next_to(title, DOWN)
        for shape in shapes:
            self.play(FadeIn(shape))
        self.wait(2)

        self.disk = disk
        self.to_fade = VGroup(
            title, hexagon, blob, britain
        )

    def isolate_disk(self):
        disk = self.disk
        self.play(
            FadeOut(self.to_fade),
            disk.set_width, 2,
            disk.next_to, ORIGIN, LEFT, 2,
            disk.set_fill, BLUE_D, 0.7
        )

        radius = Line(
            disk.get_center(), disk.get_right(),
            color = YELLOW
        )
        one = OldTex("1").next_to(radius, DOWN, SMALL_BUFF)

        self.play(ShowCreation(radius))
        self.play(Write(one))
        self.wait()

        self.disk.add(radius, one)

    def scale_disk(self):
        scaled_disk = self.disk.copy()
        scaled_disk.generate_target()
        scaled_disk.target.scale(2)
        scaled_disk.target.next_to(ORIGIN, RIGHT)

        one = scaled_disk.target[-1]
        two = OldTex("2")
        two.move_to(one, UP)
        scaled_disk.target.submobjects[-1] = two

        self.play(MoveToTarget(scaled_disk))
        self.wait()

        self.scaled_disk = scaled_disk

    def write_mass_scaling_factor(self):
        mass_scaling = OldTexText(
            "Mass scaling factor: $2^2 = 4$"
        )
        mass_scaling.next_to(self.scaled_disk, UP)
        mass_scaling.to_edge(UP)
        self.play(Write(mass_scaling))
        self.wait()

    def try_fitting_small_disks(self):
        disk = self.disk.copy()
        disk.submobjects = []
        disk.set_fill(opacity = 0.5)
        foursome = VGroup(*[
            disk.copy().next_to(ORIGIN, vect, buff = 0)
            for vect in compass_directions(start_vect = UP+RIGHT)
        ])
        foursome.move_to(self.scaled_disk)

        self.play(Transform(disk, foursome))
        self.remove(*self.get_mobjects_from_last_animation())
        self.add(foursome)
        self.wait()
        self.play(ApplyFunction(
            lambda m : break_up(m, 0.2),
            foursome,
            rate_func = there_and_back,
            run_time = 4,
        ))
        self.wait()
        self.play(FadeOut(foursome))
        self.wait()
