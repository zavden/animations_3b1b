# ==============================================================================
# Scene:      LightUpNodes
# Source:     videos/_2017/mug.py (lines 1024-1240)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LightUpNodes.py LightUpNodes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UtilitiesPuzzleScene(Scene):
    CONFIG = {
        "object_height" : 0.75,
        "h_distance" : 2,
        "v_distance" : 2,
        "line_width" : 4,
    }
    def setup_configuration(self):
        houses = VGroup()
        for x in range(3):
            house = SVGMobject(file_name = "house")
            house.set_stroke(BLACK, 5, background=True)
            house.set_height(self.object_height)
            house.set_fill(GREY_B)
            house.move_to(x*self.h_distance*RIGHT)
            houses.add(house)
        houses.move_to(self.v_distance*UP/2)

        utilities = VGroup(*[
            self.get_utility(u, c).move_to(x*self.h_distance*RIGHT)
            for x, u, c in zip(
                it.count(),
                ["fire", "electricity", "water"], 
                [RED_D, YELLOW_C, BLUE_D]
            )
        ])
        utilities.move_to(self.v_distance*DOWN/2)
        objects = VGroup(houses, utilities)
        bounding_box = SurroundingRectangle(
            objects,   
            buff = MED_LARGE_BUFF,
            stroke_width = 0
        )
        objects.add(bounding_box)
        self.add(objects)
        self.houses = houses
        self.utilities = utilities
        self.objects = objects
        self.bounding_box = bounding_box


    def get_utility(self, name, color):
        circle = Circle(
            fill_color = color,
            fill_opacity = 1,
            stroke_width = 0,
        )
        utility = SVGMobject(
            file_name = name,
            height = 0.65*circle.get_height(),
            fill_color = WHITE,
        )
        utility.insert_n_curves(100)
        utility.set_stroke(width=0)
        if color == YELLOW:
            utility.set_fill(GREY_D)
        utility.move_to(circle)
        circle.add(utility)
        circle.set_height(self.object_height)
        return circle

    def get_line(
        self, utility_index, house_index, 
        *midpoints,
        **kwargs
        ):
        prop = kwargs.pop("prop", 1.0)
        utility = self.utilities[utility_index]
        points = [utility.get_center()]
        points += list(midpoints)
        points += [self.houses[house_index].get_center()]
        line = Line(
            points[0], points[-1],
            color = utility[0].get_color(),
            stroke_width = self.line_width
        )
        line.set_points_smoothly(points)
        line.pointwise_become_partial(line, 0, prop)
        return line

    def get_almost_solution_lines(self):
        bb = self.bounding_box
        return VGroup(
            VGroup(
                self.get_line(0, 0),
                self.get_line(0, 1),
                self.get_line(0, 2, bb.get_top()),
            ),
            VGroup(
                self.get_line(1, 0, bb.get_corner(DOWN+LEFT)),
                self.get_line(1, 1),
                self.get_line(1, 2, bb.get_corner(DOWN+RIGHT)),
            ),
            VGroup(
                self.get_line(2, 0, bb.get_top()),
                self.get_line(2, 1),
                self.get_line(2, 2),
            ),
        )

    def get_straight_lines(self):
        return VGroup(*[
            VGroup(*[self.get_line(i, j) for j in range(3)])
            for i in range(3)
        ])

    def get_no_crossing_words(self):
        arrow = Vector(DOWN)
        arrow.next_to(self.bounding_box.get_top(), UP, SMALL_BUFF)
        words = OldTexText("No crossing!")
        words.next_to(arrow, UP, buff = SMALL_BUFF)
        result = VGroup(words, arrow)
        result.set_color("RED")
        return result

    def get_region(self, *bounding_edges):
        region = VMobject(mark_paths_closed = True)
        for i, edge in enumerate(bounding_edges):
            new_edge = edge.copy()
            if i%2 == 1:
                new_edge.set_points(new_edge.get_points()[::-1])
            region.append_vectorized_mobject(new_edge)
        region.set_stroke(width = 0)
        region.set_fill(WHITE, opacity = 1)
        return region

    def convert_objects_to_dots(self, run_time = 2):
        group = VGroup(*it.chain(self.houses, self.utilities))
        for mob in group:
            mob.target = Dot(color = mob.get_color())
            mob.target.scale(2)
            mob.target.move_to(mob)
        self.play(LaggedStartMap(MoveToTarget, group, run_time = run_time))


class IntroduceRegions(UtilitiesPuzzleScene):
    def construct(self):
        self.setup_configuration()
        houses, utilities = self.houses, self.utilities
        objects = self.objects
        lines, line_groups, regions = self.get_lines_line_groups_and_regions()
        back_region = regions[0]
        front_regions = VGroup(*regions[1:])

        self.convert_objects_to_dots(run_time = 0)
        self.play(LaggedStartMap(
            ShowCreation, lines,
            run_time = 3,
        ))
        self.add_foreground_mobjects(lines, objects)
        self.wait()
        for region in front_regions:
            self.play(FadeIn(region))
        self.play(
            FadeIn(back_region),
            Animation(front_regions),
        )
        self.wait()
        self.play(FadeOut(regions))

        ##Paint bucket
        paint_bucket = SVGMobject(
            file_name = "paint_bucket",
            height = 0.5,
        )
        paint_bucket.flip()
        paint_bucket.move_to(8*LEFT + 5*UP)

        def click(region):
            self.play(
                UpdateFromAlphaFunc(
                    region,
                    lambda m, a : m.set_fill(opacity = int(2*a)),
                ),
                ApplyMethod(
                    paint_bucket.scale, 0.5,
                    rate_func = there_and_back,
                ),
                run_time = 0.25,
            )

        self.play(
            paint_bucket.next_to, utilities, DOWN+LEFT, SMALL_BUFF
        )
        click(regions[1])
        self.play(paint_bucket.next_to, utilities[1], UP+RIGHT, SMALL_BUFF)
        click(regions[2])
        self.play(paint_bucket.next_to, houses[1], RIGHT)
        click(regions[3])
        self.play(paint_bucket.move_to, 4*LEFT + 2*UP)
        self.add_foreground_mobjects(front_regions, lines, objects)
        click(back_region)
        self.remove_foreground_mobjects(front_regions)
        self.wait()
        self.play(
            FadeOut(back_region),
            FadeOut(front_regions[0]),
            FadeOut(paint_bucket),
            *list(map(Animation, front_regions[1:]))
        )

        #Line tries to escape
        point_sets = [
            [
                VGroup(*houses[1:]).get_center(),
                houses[2].get_top() + MED_SMALL_BUFF*UP,
            ],
            [
                houses[1].get_top() + SMALL_BUFF*UP,
                utilities[0].get_center(),
            ],
            [VGroup(houses[1], utilities[1]).get_center()],
            [
                utilities[2].get_center() + 0.75*(DOWN+RIGHT)
            ],
        ]
        escape_lines = VGroup(*[
            Line(LEFT, RIGHT).set_points_smoothly(
                [utilities[2].get_center()] + point_set
            )
            for point_set in point_sets
        ])

        self.wait()
        for line in escape_lines:
            self.play(ShowCreation(line,
                rate_func = lambda t : 0.8*smooth(t)
            ))
            self.play(ShowCreation(line,
                rate_func = lambda t : smooth(1 - t)
            ))

    def get_lines_line_groups_and_regions(self):
        lines = self.get_almost_solution_lines()
        flat_lines = VGroup(*it.chain(*lines))
        flat_lines.remove(lines[2][0])

        line_groups = [
            VGroup(*[lines[i][j] for i, j in ij_set])
            for ij_set in [
                [(0, 0), (1, 0), (1, 1), (0, 1)],
                [(1, 1), (2, 1), (2, 2), (1, 2)],
                [(0, 2), (2, 2), (2, 1), (0, 1)],
                [(0, 0), (1, 0), (1, 2), (0, 2)],
            ]
        ]
        regions = VGroup(*[
            self.get_region(*line_group)
            for line_group in line_groups
        ])
        back_region = FullScreenFadeRectangle(fill_opacity = 1 )
        regions.submobjects.pop()
        regions.submobjects.insert(0, back_region)
        front_regions = VGroup(*regions[1:])

        back_region.set_color(BLUE_E)
        front_regions.set_color_by_gradient(GREEN_E, MAROON_E)

        return flat_lines, line_groups, regions


class LightUpNodes(IntroduceRegions):
    CONFIG = {
        "vertices_word" : "Lit vertices",
    }
    def construct(self):
        self.setup_configuration()
        self.setup_regions()
        self.setup_counters()
        self.describe_one_as_lit()
        self.show_rule_for_lighting()

    def setup_configuration(self):
        IntroduceRegions.setup_configuration(self)
        self.convert_objects_to_dots(run_time = 0)
        self.objects.shift(DOWN)

    def setup_regions(self):
        lines, line_groups, regions = self.get_lines_line_groups_and_regions()
        back_region = regions[0]
        front_regions = VGroup(*regions[1:])
        self.set_variables_as_attrs(
            lines, line_groups, regions,
            back_region, front_regions,
        )

    def setup_counters(self):
        titles = [
            OldTexText("\\# %s"%self.vertices_word),
            OldTexText("\\# Edges"),
            OldTexText("\\# Regions"),
        ]
        for title, vect in zip(titles, [LEFT, ORIGIN, RIGHT]):
            title.shift(FRAME_X_RADIUS*vect/2)
            title.to_edge(UP)
            underline = Line(LEFT, RIGHT)
            underline.stretch_to_fit_width(title.get_width())
            underline.next_to(title, DOWN, SMALL_BUFF)
            title.add(underline)
            self.add(title)
        self.count_titles = titles
        self.v_count, self.e_count, self.f_count = self.counts = list(map(
            Integer, [1, 0, 1]
        ))
        for count, title in zip(self.counts, titles):
            count.next_to(title, DOWN)
            self.add(count)

    def describe_one_as_lit(self):
        houses, utilities = self.houses, self.utilities
        vertices = VGroup(*it.chain(houses, utilities))
        dim_arrows = VGroup()
        for vertex in vertices:
            arrow = Vector(0.5*(DOWN+LEFT), color = WHITE)
            arrow.next_to(vertex, UP+RIGHT, SMALL_BUFF)
            vertex.arrow = arrow
            dim_arrows.add(arrow)
        lit_vertex = utilities[0]
        lit_arrow = lit_vertex.arrow
        lit_arrow.rotate(np.pi/2, about_point = lit_vertex.get_center())
        dim_arrows.remove(lit_arrow)
        lit_word = OldTexText("Lit up")
        lit_word.next_to(lit_arrow.get_start(), UP, SMALL_BUFF)
        dim_word = OldTexText("Dim")
        dim_word.next_to(dim_arrows[1].get_start(), UP, MED_LARGE_BUFF)

        dot = Dot().move_to(self.v_count)

        self.play(
            vertices.set_fill, None, 0,
            vertices.set_stroke, None, 1,
        )
        self.play(ReplacementTransform(dot, lit_vertex))
        self.play(
            FadeIn(lit_word),
            GrowArrow(lit_arrow)
        )
        self.play(*self.get_lit_vertex_animations(lit_vertex))
        self.play(
            FadeIn(dim_word),
            LaggedStartMap(GrowArrow, dim_arrows)
        )
        self.wait()
        self.play(*list(map(FadeOut, [
            lit_word, lit_arrow, dim_word, dim_arrows
        ])))

    def show_rule_for_lighting(self):
        lines = self.lines
        regions = self.regions
        line_groups = self.line_groups
        objects = self.objects
        houses, utilities = self.houses, self.utilities

        #First region, lines 0, 1, 4, 3
        lines[4].rotate(np.pi)
        region = regions[1]

        self.play(ShowCreation(lines[0]))
        self.play(*self.get_count_change_animations(0, 1, 0))
        self.play(*it.chain(
            self.get_lit_vertex_animations(houses[0]),
            self.get_count_change_animations(1, 0, 0)
        ))
        self.wait()
        for line, vertex in (lines[1], houses[1]), (lines[4], utilities[1]):
            self.play(
                ShowCreation(line),
                *self.get_count_change_animations(0, 1, 0)
            )
            self.play(*it.chain(
                self.get_lit_vertex_animations(vertex),
                self.get_count_change_animations(1, 0, 0),
            ))
        self.wait()
        self.play(
            ShowCreation(lines[3], run_time = 2),
            *self.get_count_change_animations(0, 1, 0)
        )
        self.add_foreground_mobjects(line_groups[0])
        self.add_foreground_mobjects(objects)
        self.play(
            FadeIn(region),
            *self.get_count_change_animations(0, 0, 1)
        )
        self.wait()

        #Next region, lines 2, 7, 8
        region = regions[3]
        lines[6].rotate(np.pi)

        for line, vertex in (lines[2], houses[2]), (lines[6], utilities[2]):
            self.play(ShowCreation(line), *it.chain(
                self.get_lit_vertex_animations(
                    vertex,
                    run_time = 2, 
                    squish_range = (0.5, 1),
                ),
                self.get_count_change_animations(1, 1, 0)
            ))
        self.wait()
        self.play(
            ShowCreation(lines[7]),
            *self.get_count_change_animations(0, 1, 1)
        )
        self.add_foreground_mobjects(line_groups[2])
        self.add_foreground_mobjects(objects)
        self.play(FadeIn(region))
        self.wait()

    ####

    def get_count_change_animations(self, *changes):
        anims = []
        for change, count in zip(changes, self.counts):
            if change == 0:
                continue
            new_count = Integer(count.number + 1)
            new_count.move_to(count)
            anims.append(Transform(
                count, new_count,
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ))
            count.number += 1
            anims.append(self.get_plus_one_anim(count))

        return anims

    def get_plus_one_anim(self, count):
        plus_one = OldTex("+1")
        plus_one.set_color(YELLOW)
        plus_one.move_to(count)
        plus_one.next_to(count, DOWN)
        plus_one.generate_target()
        plus_one.target.move_to(count)
        plus_one.target.set_fill(opacity = 0)
        move = MoveToTarget(plus_one, remover = True)
        grow = GrowFromCenter(plus_one)
        return UpdateFromAlphaFunc(
            plus_one,
            lambda m, a : (
                (grow if a < 0.5 else move).update(2*a%1)
            ),
            remover = True,
            rate_func = double_smooth,
            run_time = 2
        )

    def get_lit_vertex_animations(self, vertex, run_time = 1, squish_range = (0, 1)):
        line = Line(
            LEFT, RIGHT,
            stroke_width = 0,
            stroke_color = BLACK,
        )
        line.set_width(0.5*vertex.get_width())
        line.next_to(ORIGIN, buff = 0.75*vertex.get_width())
        lines = VGroup(*[
            line.copy().rotate(angle)
            for angle in np.arange(0, 2*np.pi, np.pi/4)
        ])
        lines.move_to(vertex)
        random.shuffle(lines.submobjects)
        return [
            LaggedStartMap(
                ApplyMethod, lines,
                lambda l : (l.set_stroke, YELLOW, 4),
                rate_func = squish_rate_func(there_and_back, *squish_range),
                lag_ratio = 0.75,
                remover = True,
                run_time = run_time
            ),
            ApplyMethod(
                vertex.set_fill, None, 1,
                run_time = run_time,
                rate_func = squish_rate_func(smooth, *squish_range)
            ),
        ]
