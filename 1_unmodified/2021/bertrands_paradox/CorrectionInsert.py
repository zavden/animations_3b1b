# ==============================================================================
# Scene:      CorrectionInsert
# Source:     videos/_2021/bertrands_paradox.py (lines 953-1095)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CorrectionInsert.py CorrectionInsert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CorrectionInsert(Scene):
    def construct(self):
        # Words
        title = OldTexText("Looking for an unambiguous ``uniform'' distribution?")
        title.to_edge(UP, buff=0.25)
        kw = dict(
            # font_size=36,
            # color=GREY_A,
            t2c={"compact": YELLOW, "transitively": BLUE},
            t2s={"compact": ITALIC},
        )
        conditions = VGroup(
            Text("1) Find a symmetry which acts transitively", **kw),
            Text("2) The space must be compact", **kw),
        )
        conditions.arrange(DOWN, aligned_edge=LEFT)
        conditions.next_to(title, DOWN, MED_LARGE_BUFF)

        conditions.to_edge(UP)

        # Add shapes
        radius = 1.5

        interval = UnitInterval(width=4)
        interval.add_numbers([0, 0.5, 1.0], num_decimal_places=1)

        circle = Circle(radius=radius)
        circle.set_stroke(GREY_B, 2)

        sphere = Sphere(radius=radius)
        sphere.set_color(BLUE_D, 1)
        sphere.set_opacity(0.5)
        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(width=0.5)
        mesh_shadow = mesh.copy().set_stroke(opacity=0.35)
        sphere_group = Group(mesh_shadow, sphere, mesh)
        sphere_group.rotate(80 * DEGREES, LEFT)
        sphere_group.rotate(2.5 * DEGREES, OUT)
        sphere.set_sort_to_camera()

        shapes = Group(interval, circle, sphere_group)
        shapes.arrange(RIGHT, buff=LARGE_BUFF)
        shapes.set_y(-1)

        # Dots
        interval_dots = DotCloud([interval.pfp(random.random()) for n in range(100)])
        circle_dots = DotCloud([circle.pfp(random.random()) for n in range(100)])
        sphere_dots = DotCloud([
            sphere.pfp(math.acos(random.random()) / PI)
            for n in range(300)
        ])

        all_dots = Group(interval_dots, circle_dots, sphere_dots)
        for dots in all_dots:
            dots.set_glow_factor(5)
            dots.set_radius(0.1)
            dots.set_color(YELLOW)
            dots.add_updater(lambda m: m)
        sphere_dots.set_opacity(np.random.choice([1, 0.2], sphere_dots.get_num_points()))
        circle_dots.set_radius(0.15)

        # Animations
        self.add(conditions[0])
        self.add(shapes)
        self.add(*dots)

        self.play(*(ShowCreation(dots, rate_func=linear, run_time=15) for dots in all_dots))
        self.wait(4)
        self.play(Write(conditions[1][:2]))
        self.wait(2)
        self.play(Write(conditions[1][2:]))
        self.wait()

        # Compact
        rects = Rectangle(height=4.75, width=6).get_grid(1, 2, buff=0.5)
        rects.set_stroke(GREY, 1)
        rects.to_edge(DOWN)

        rect_titles = VGroup(Text("Compact"), Text("Not compact"))
        for rt, r, color in zip(rect_titles, rects, [YELLOW, RED]):
            rt.scale(0.7)
            rt.next_to(r, UP, buff=SMALL_BUFF)
            rt.set_color(color)

        compact_spaces = Group(
            Group(interval, interval_dots),
            Group(circle, circle_dots),
            Group(*sphere_group, sphere_dots)
        )
        compact_spaces.generate_target()
        compact_spaces.target.arrange(DOWN)
        compact_spaces.target.set_height(0.9 * rects[0].get_height())
        compact_spaces.target.move_to(rects[0])

        movers = []
        for cs, cst in zip(compact_spaces, compact_spaces.target):
            for m, mt in zip(cs, cst):
                m.generate_target()
                m.target.replace(mt)
                movers.append(m)

        self.play(
            *map(MoveToTarget, movers),
            *map(ShowCreation, rects),
            *map(FadeIn, rect_titles),
        )
        self.wait()

        # Non-compact
        reals = NumberLine((-5, 5), include_tip=True)
        reals.ticks.remove(reals.ticks[0])
        reals.add(reals.copy().flip())
        reals.add_numbers(font_size=20)
        reals.set_width(0.9 * rects[1].get_width())
        reals.next_to(rects[1].get_top(), DOWN, buff=LARGE_BUFF)
        reals_label = Text("Real number line", font_size=30)
        reals_label.next_to(reals, UP, SMALL_BUFF)

        plane = Square(4)
        plane.set_stroke(width=0)
        plane.set_fill(GREY_D, 1)
        plane.set_gloss(0.5)
        plane.set_reflectiveness(0.4)
        arrows = VGroup(*(
            Arrow(v, 2 * v, stroke_width=2)
            for v in compass_directions(8)
        ))
        group = VGroup(plane, arrows)
        group.rotate(80 * DEGREES, LEFT)
        group.set_width(4.5)
        group.next_to(reals, DOWN, buff=1.5)
        group.shift(0.25 * LEFT)

        self.play(
            ShowCreation(reals),
            FadeIn(reals_label),
        )
        self.wait()
        self.play(
            GrowFromCenter(plane),
            *map(ShowCreation, arrows),
        )
        self.wait(3)
