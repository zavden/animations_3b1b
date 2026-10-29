# ==============================================================================
# Scene:      ThisPuzzleIsHard
# Source:     videos/_2017/mug.py (lines 342-508)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisPuzzleIsHard.py ThisPuzzleIsHard -w -m --fps 15
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


class ThisPuzzleIsHard(UtilitiesPuzzleScene, PiCreatureScene):
    def construct(self):
        self.introduce_components()
        self.failed_attempts()
        self.ask_meta_puzzle()

    def introduce_components(self):
        randy = self.pi_creature

        try_it = OldTexText("Try it yourself!")
        try_it.to_edge(UP)

        self.setup_configuration()
        houses, utilities = self.houses, self.utilities
        self.remove(self.objects)
        house = houses[0]

        puzzle_words = OldTexText("""
            Puzzle: Connect each house to \\\\
            each utility without crossing lines.
        """)
        # puzzle_words.next_to(self.objects, UP)
        puzzle_words.to_edge(UP)

        self.add(try_it)
        self.play(Animation(try_it))
        self.play(
            LaggedStartMap(DrawBorderThenFill, houses),
            LaggedStartMap(GrowFromCenter, utilities),
            try_it.set_width, house.get_width(),
            try_it.fade, 1,
            try_it.move_to, house,
            self.pi_creature.change, "happy",
        )
        self.play(LaggedStartMap(FadeIn, puzzle_words))

        self.add_foreground_mobjects(self.objects)
        self.set_variables_as_attrs(puzzle_words)

    def failed_attempts(self):
        bb = self.bounding_box
        utilities = self.utilities
        houses = self.houses
        randy = self.pi_creature

        line_sets = [
            [
                self.get_line(0, 0),
                self.get_line(1, 1),
                self.get_line(2, 2),
                self.get_line(0, 1),
                self.get_line(2, 1),
                self.get_line(0, 2, bb.get_corner(UP+LEFT)),
                self.get_line(
                    2, 0, bb.get_corner(DOWN+LEFT),
                    prop = 0.85,
                ),
                self.get_line(
                    2, 0, bb.get_corner(UP+RIGHT), bb.get_top(),
                    prop = 0.73,
                ),
            ],
            [
                self.get_line(0, 0),
                self.get_line(1, 1),
                self.get_line(2, 2),
                self.get_line(0, 1),
                self.get_line(1, 2),
                self.get_line(
                    2, 0, 
                    bb.get_bottom(),
                    bb.get_corner(DOWN+LEFT)
                ),
                self.get_line(0, 2, bb.get_top()),
                self.get_line(
                    2, 1,
                    utilities[1].get_bottom() + MED_SMALL_BUFF*DOWN,
                    utilities[1].get_left() + MED_SMALL_BUFF*LEFT,
                ),
                self.get_line(
                    1, 0, houses[2].get_corner(UP+LEFT) + MED_LARGE_BUFF*LEFT,
                    prop = 0.49,
                ),
                self.get_line(
                    1, 2, bb.get_right(),
                    prop = 0.25,
                ),
            ],
            [
                self.get_line(0, 0),
                self.get_line(0, 1),
                self.get_line(0, 2, bb.get_top()),
                self.get_line(1, 0, bb.get_corner(DOWN+LEFT)),
                self.get_line(1, 1),
                self.get_line(1, 2, bb.get_corner(DOWN+RIGHT)),
                self.get_line(2, 1),
                self.get_line(2, 2),
                self.get_line(2, 0, bb.get_top(), prop = 0.45),
                self.get_line(2, 0, prop = 0.45),
            ],
        ]
        modes = ["confused", "sassy", "angry"]

        for line_set, mode in zip(line_sets, modes):
            good_lines = VGroup(*line_set[:-2])
            bad_lines = line_set[-2:]
            self.play(LaggedStartMap(ShowCreation, good_lines))
            for bl in bad_lines:
                self.play(
                    ShowCreation(
                        bl,
                        rate_func = bezier([0, 0, 0, 1, 1, 1, 1, 1, 0.3, 1, 1]),
                        run_time = 1.5
                    ),
                    randy.change, mode,
                )
                self.play(ShowCreation(
                    bl, rate_func = lambda t : smooth(1-t),
                ))
                self.remove(bl)
            self.play(LaggedStartMap(FadeOut, good_lines))

    def ask_meta_puzzle(self):
        randy = self.pi_creature
        group = VGroup(
            self.puzzle_words,
            self.objects,
        )
        rect = SurroundingRectangle(group, color = BLUE, buff = MED_LARGE_BUFF)
        group.add(rect)
        group.generate_target()
        group.target.scale(0.75)
        group.target.shift(DOWN)
        group[-1].set_stroke(width = 0)

        meta_puzzle_words = OldTexText("""
            Meta-puzzle: Prove that this\\\\
            is impossible.
        """)
        meta_puzzle_words.next_to(group.target, UP)
        meta_puzzle_words.set_color(BLUE)

        self.play(
            MoveToTarget(group),
            randy.change, "pondering"
        )
        self.play(Write(meta_puzzle_words))
        self.play(randy.change, "confused")

        straight_lines = self.get_straight_lines()
        almost_solution_lines = self.get_almost_solution_lines()
        self.play(LaggedStartMap(
            ShowCreation, straight_lines,
            run_time = 2,
            lag_ratio = 0.8
        ), Blink(randy))
        self.play(Transform(
            straight_lines, almost_solution_lines,
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait()

    ######

    def create_pi_creature(self):
        return Randolph().to_corner(DOWN+LEFT)
