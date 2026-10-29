# ==============================================================================
# Scene:      CyclesHaveAtLeastFour
# Source:     videos/_2017/mug.py (lines 1430-1494)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CyclesHaveAtLeastFour.py CyclesHaveAtLeastFour -w -m --fps 15
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


class CyclesHaveAtLeastFour(UtilitiesPuzzleScene):
    def construct(self):
        self.setup_configuration()
        houses, utilities = self.houses, self.utilities
        vertices = VGroup(
            houses[0], utilities[0],
            houses[1], utilities[1], houses[0],
        )
        lines = [
            VectorizedPoint(),
            self.get_line(0, 0),
            self.get_line(0, 1),
            self.get_line(1, 1),
            self.get_line(1, 0, self.objects.get_corner(DOWN+LEFT)),
        ]
        for line in lines[1::2]:
            line.set_points(line.get_points()[::-1])
        arrows = VGroup()
        for vertex in vertices:
            vect = vertices.get_center() - vertex.get_center()
            arrow = Vector(vect, color = WHITE)
            arrow.next_to(vertex, -vect, buff = 0)
            vertex.arrow = arrow
            arrows.add(arrow)
        word_strings = [
            "Start at a house",
            "Go to a utility",
            "Go to another house",
            "Go to another utility",
            "Back to the start",
        ]
        words = VGroup()
        for word_string, arrow in zip(word_strings, arrows):
            vect = arrow.get_vector()[1]*UP
            word = OldTexText(word_string)
            word.next_to(arrow.get_start(), -vect)
            words.add(word)

        count = Integer(-1)
        count.fade(1)
        count.to_edge(UP)

        last_word = None
        last_arrow = None

        for line, word, arrow in zip(lines, words, arrows):
            anims = []
            for mob in last_word, last_arrow:
                if mob:
                    anims.append(FadeOut(mob))
            new_count = Integer(count.number + 1)
            new_count.move_to(count)
            anims += [
                FadeIn(word),
                GrowArrow(arrow),
                ShowCreation(line),
                FadeOut(count),
                FadeIn(new_count),
            ]
            self.play(*anims)
            self.wait()
            last_word = word
            last_arrow = arrow
            count = new_count
        self.wait(2)
