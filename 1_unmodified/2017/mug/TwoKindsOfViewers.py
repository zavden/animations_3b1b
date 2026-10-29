# ==============================================================================
# Scene:      TwoKindsOfViewers
# Source:     videos/_2017/mug.py (lines 633-710)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoKindsOfViewers.py TwoKindsOfViewers -w -m --fps 15
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


class TwoKindsOfViewers(PiCreatureScene, UtilitiesPuzzleScene):
    def construct(self):
        self.setup_configuration()
        objects = self.objects
        objects.remove(self.bounding_box)
        lines = self.get_straight_lines()
        objects.add_to_back(lines)
        objects.scale(0.75)
        objects.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        self.remove(objects)

        pi1, pi2 = self.pi_creatures
        words = OldTexText(
            "$(V-E+F)$", "kinds of viewers"
        )
        words.to_edge(UP)
        eulers = words.get_part_by_tex("V-E+F")
        eulers.set_color(GREEN)
        non_eulers = VGroup(*[m for m in words if m is not eulers])

        self.add(words)
        self.wait()
        self.play(
            pi1.shift, 2*LEFT,
            pi2.shift, 2*RIGHT,
        )

        know_eulers = OldTexText("Know about \\\\ Euler's formula")
        know_eulers.next_to(pi1, DOWN)
        know_eulers.set_color(GREEN)
        dont = OldTexText("Don't")
        dont.next_to(pi2, DOWN)
        dont.set_color(RED)

        self.play(
            FadeIn(know_eulers),
            pi1.change, "hooray",
        )
        self.play(
            FadeIn(dont),
            pi2.change, "maybe", eulers,
        )
        self.wait()
        self.pi_creature_thinks(
            pi1, "",
            bubble_config = {"width" : 3, "height" : 2},
            target_mode = "thinking"
        )
        self.play(pi2.change, "confused", eulers)
        self.wait()

        ### Out of thin air
        self.play(*list(map(FadeOut, [
            non_eulers, pi1, pi2, pi1.bubble,
            know_eulers, dont
        ])))
        self.play(eulers.next_to, ORIGIN, LEFT, LARGE_BUFF)
        arrow = Arrow(eulers, objects, color = WHITE)
        self.play(
            GrowArrow(arrow),
            LaggedStartMap(DrawBorderThenFill, VGroup(*it.chain(*objects)))
        )
        self.wait()
        self.play(
            objects.move_to, eulers, RIGHT,
            eulers.move_to, objects, LEFT,
            path_arc = np.pi,
            run_time = 1.5,
        )
        self.wait(2)

    ###

    def create_pi_creatures(self):
        group = VGroup(Randolph(color = BLUE_C), Randolph())
        group.scale(0.7)
        group.shift(MED_LARGE_BUFF*DOWN)
        return group
