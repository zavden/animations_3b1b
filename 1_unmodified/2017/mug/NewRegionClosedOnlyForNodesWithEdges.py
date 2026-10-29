# ==============================================================================
# Scene:      NewRegionClosedOnlyForNodesWithEdges
# Source:     videos/_2017/mug.py (lines 967-1022)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewRegionClosedOnlyForNodesWithEdges.py NewRegionClosedOnlyForNodesWithEdges -w -m --fps 15
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


class NewRegionClosedOnlyForNodesWithEdges(UtilitiesPuzzleScene):
    def construct(self):
        self.setup_configuration()
        self.convert_objects_to_dots(run_time = 0)
        objects = self.objects
        houses, utilities = self.houses, self.utilities

        bb = self.bounding_box
        lines = VGroup(
            self.get_line(2, 1),
            self.get_line(0, 1),
            self.get_line(0, 2,
                bb.get_corner(UP+LEFT),
                bb.get_top() + MED_LARGE_BUFF*UP,
            ),
            self.get_line(2, 2),
        )
        lit_line = lines[2].copy()
        lit_line.set_points(lit_line.get_points()[::-1])
        lit_line.set_stroke(WHITE, 5)

        region = self.get_region(*lines)
        region.set_fill(MAROON_E)

        arrow = Vector(DOWN+LEFT, color = WHITE)
        arrow.next_to(houses[2], UP+RIGHT, buff = SMALL_BUFF)
        words = OldTexText("Already has \\\\ an edge")
        words.next_to(arrow.get_start(), UP, SMALL_BUFF)

        for line in lines[:-1]:
            self.play(ShowCreation(line))
        lines[-1].pointwise_become_partial(lines[-1], 0, 0.92)
        lines[-1].save_state()
        self.wait()
        self.play(ShowCreation(lines[-1]))
        self.add(region, lines, objects)
        self.wait()
        self.remove(region)
        self.play(ShowCreation(lines[-1], 
            rate_func = lambda t : smooth(1-2*t*(1-t))
        ))
        self.add(region, lines, objects)
        self.wait()
        self.remove(region)
        self.play(
            ShowCreation(lines[-1],
                rate_func = lambda t : smooth(1-0.5*t)
            ),
            FadeIn(words),
            GrowArrow(arrow),
        )
        for x in range(2):
            self.play(ShowCreationThenDestruction(lit_line))
        self.play(lines[-1].restore)
        self.add(region, lines, objects)
        self.wait(2)
