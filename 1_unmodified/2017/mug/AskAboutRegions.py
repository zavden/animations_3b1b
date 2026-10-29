# ==============================================================================
# Scene:      AskAboutRegions
# Source:     videos/_2017/mug.py (lines 848-965)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutRegions.py AskAboutRegions -w -m --fps 15
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


class AskAboutRegions(IntroduceRegions):
    def construct(self):
        self.setup_configuration()
        houses, utilities = self.houses, self.utilities
        self.convert_objects_to_dots(run_time = 0)
        objects = self.objects
        lines, line_groups, regions = self.get_lines_line_groups_and_regions()
        back_region = regions[0]
        front_regions = VGroup(*regions[1:])
        missing_lines = VGroup(
            self.get_line(2, 0, self.objects.get_top()),
            self.get_line(
                2, 0, 
                self.objects.get_bottom() + DOWN,
                self.objects.get_corner(DOWN+LEFT) + DOWN+LEFT,
            )
        )
        missing_lines.set_stroke(width = 5)

        front_regions.save_state()
        front_regions.generate_target()
        front_regions.target.scale(0.5)
        front_regions.target.arrange(RIGHT, buff = LARGE_BUFF)
        front_regions.target.to_edge(UP)

        self.add(front_regions)
        self.add_foreground_mobjects(lines, objects)
        self.wait()
        self.play(MoveToTarget(front_regions))
        self.play(LaggedStartMap(
            ApplyMethod, front_regions,
            lambda m : (m.rotate, np.pi/12),
            rate_func = wiggle,
            lag_ratio = 0.75,
            run_time = 1
        ))
        self.play(front_regions.restore)
        self.wait()

        #Show missing lines
        for line in missing_lines:
            self.play(ShowCreation(
                line,
                rate_func = there_and_back,
                run_time = 2,
            ))

        #Count regions
        count = OldTex("1")
        count.scale(1.5)
        count.to_edge(UP)
        self.play(
            FadeIn(back_region), 
            FadeIn(count),
            Animation(front_regions)
        )
        last_region = None
        for n, region in zip(it.count(2), front_regions):
            new_count = OldTex(str(n))
            new_count.replace(count, dim_to_match = 1)
            self.remove(count)
            self.add(new_count)
            count = new_count

            region.save_state()
            anims = [ApplyMethod(region.set_color, YELLOW)]
            if last_region:
                anims.append(ApplyMethod(last_region.restore))
            anims.append(Animation(front_regions))
            self.play(*anims, run_time = 0.25)
            self.wait(0.5)
            last_region = region
        self.play(last_region.restore)
        self.wait()
        self.play(FadeOut(count))

        #Count edges per region
        fade_rect = FullScreenFadeRectangle(opacity = 0.8)
        line_group = line_groups[0].copy()
        region = front_regions[0].copy()
        self.foreground_mobjects = []
        def show_lines(line_group):
            lg_copy = line_group.copy()
            lg_copy.set_stroke(WHITE, 6)
            self.play(LaggedStartMap(
                FadeIn, lg_copy,
                run_time = 3,
                rate_func = there_and_back,
                lag_ratio = 0.4,
                remover = True,
            ))

        self.play(
            FadeIn(fade_rect),
            Animation(region),
            Animation(line_group),
        )
        show_lines(line_group)
        last_line_group = line_group
        last_region = region
        for i in range(1, 3):
            line_group = line_groups[i].copy()
            region = front_regions[i].copy()
            self.play(
                FadeOut(last_region),
                FadeOut(last_line_group),
                FadeIn(region),
                FadeIn(line_group),
            )
            show_lines(line_group)
            last_line_group = line_group
            last_region = region
        self.play(
            FadeOut(fade_rect),
            FadeOut(last_region),
            FadeOut(last_line_group),
        )
        self.wait()
