# ==============================================================================
# Scene:      DefineConvexity
# Source:     videos/_2021/shadows.py (lines 4592-4753)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineConvexity.py DefineConvexity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineConvexity(Scene):
    def construct(self):
        # Shape
        definition = "A set is convex if the line connecting any\n"\
                     "two points within it is contained in the set"
        set_color = BLUE
        line_color = GREEN
        title = Text(
            definition,
            t2c={
                "convex": set_color,
                "line connecting any\ntwo points": line_color,
            },
            t2s={"convex": ITALIC},
        )
        title.to_edge(UP)
        title.set_opacity(0.2)

        shape = Square(4.5)
        shape.set_fill(set_color, 0.25)
        shape.set_stroke(set_color, 2)
        shape.next_to(title, DOWN, LARGE_BUFF)

        self.add(title)
        self.play(
            title.get_part_by_text("A set is convex").animate.set_opacity(1),
            Write(shape)
        )
        self.wait()

        # Show two points
        line = Line(shape.pfp(0.1), shape.pfp(0.5))
        line.scale(0.7)
        line.set_stroke(line_color, 2)
        dots = DotCloud(line.get_start_and_end())
        dots.set_color(line_color)
        dots.make_3d(0.5)
        dots.save_state()
        dots.set_radius(0)
        dots.set_opacity(0)

        self.play(
            title[definition.index("if"):definition.index("is", 16)].animate.set_opacity(1),
            Restore(dots),
        )
        self.play(ShowCreation(line))
        self.wait()
        self.play(
            title[definition.index("is", 16):].animate.set_opacity(1),
        )

        # Alternate places
        dots.add_updater(lambda m: m.set_points(line.get_start_and_end()))

        def show_sample_lines(n=5):
            for x in range(5):
                self.play(
                    line.animate.put_start_and_end_on(
                        shape.pfp(random.random()),
                        shape.pfp(random.random()),
                    ).scale(random.random(), about_point=shape.get_center())
                )
                self.wait(0.5)

        show_sample_lines()

        # Letter π
        def tex_to_shape(tex):
            result = OldTex(tex).family_members_with_points()[0]
            result.match_style(shape)
            result.match_height(shape)
            result.move_to(shape)
            result_points = result.get_points().copy()
            index = np.argmax([np.dot(p, UR) for p in result_points])
            index = 3 * (index // 3)
            result.set_points([*result_points[index:], *result_points[:index]])
            return result

        pi = tex_to_shape("\\pi")
        letter_c = tex_to_shape("\\textbf{C}")
        letter_c.insert_n_curves(50)

        line.generate_target()
        line.target.put_start_and_end_on(*(
            pi.get_boundary_point(v) for v in (DL, DR)
        ))
        line.target.scale(0.9)
        not_convex_label = Text("Not convex!", color=RED)
        not_convex_label.next_to(pi, LEFT)

        shape.insert_n_curves(100)
        self.play(
            Transform(shape, pi, path_arc=PI / 2),
            MoveToTarget(line),
            run_time=2,
        )
        self.play(
            FadeIn(not_convex_label, scale=2)
        )
        self.wait()
        shape.insert_n_curves(80)
        self.play(
            Transform(shape, letter_c),
            line.animate.put_start_and_end_on(*(
                letter_c.pfp(a) for a in (0, 0.5)
            )),
            run_time=2,
        )
        self.play(UpdateFromAlphaFunc(
            line,
            lambda l, a: l.put_start_and_end_on(
                letter_c.pfp(0.4 * a), l.get_end()
            ),
            run_time=6,
        ))
        self.wait()

        # Polygon
        convex_label = OldTexText("Convex \\ding{51}")
        convex_label.set_color(YELLOW)
        convex_label.move_to(not_convex_label)
        polygon = RegularPolygon(7)
        polygon.match_height(shape)
        polygon.move_to(shape)
        polygon.match_style(shape)

        self.remove(not_convex_label)
        self.play(
            FadeTransform(shape, polygon),
            line.animate.put_start_and_end_on(
                polygon.get_vertices()[1],
                polygon.get_vertices()[-1],
            ),
            TransformMatchingShapes(not_convex_label.copy(), convex_label),
            run_time=2
        )
        self.wait()

        polygon.generate_target()
        new_tip = 2 * line.get_center() - polygon.get_start()
        polygon.target.set_points_as_corners([
            new_tip, *polygon.get_vertices()[1:], new_tip
        ])
        self.play(
            MoveToTarget(polygon),
            TransformMatchingShapes(convex_label, not_convex_label),
        )
        self.wait()

        # Show light beam
        beam = DashedLine(ORIGIN, FRAME_WIDTH * RIGHT)
        beam.set_stroke(YELLOW, 1)
        beam.next_to(line, DOWN, MED_SMALL_BUFF)
        flash_line = Line(beam.get_start(), beam.get_end())
        flash_line.set_stroke(YELLOW, 5)
        flash_line.insert_n_curves(100)
        self.play(
            ShowCreation(beam),
            VShowPassingFlash(flash_line),
            run_time=1,
        )
        self.wait()
