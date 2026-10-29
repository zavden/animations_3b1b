# ==============================================================================
# Scene:      AboutToyPuzzles
# Source:     videos/_2017/mug.py (lines 219-340)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AboutToyPuzzles.py AboutToyPuzzles -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Cube is a surface without set_stroke/pose_at_angle; CairoCube is the Cairo VGroup of six faces
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


class AboutToyPuzzles(UtilitiesPuzzleScene, TeacherStudentsScene, ThreeDScene):
    def construct(self):
        self.remove(self.pi_creatures)
        self.lay_out_puzzle()
        self.point_to_abstractions()
        self.show_this_video()

    def lay_out_puzzle(self):
        self.setup_configuration()
        houses, utilities = self.houses, self.utilities
        lines = VGroup(*it.chain(*self.get_almost_solution_lines()))
        no_crossing_words = self.get_no_crossing_words()

        self.remove(self.objects)
        self.play(
            ReplacementTransform(
                VGroup(houses[1], houses[1]).copy().fade(1),
                VGroup(houses[0], houses[2]),
                rate_func = squish_rate_func(smooth, 0.35, 1),
                run_time = 2,
            ),
            FadeIn(houses[1]),
            LaggedStartMap(DrawBorderThenFill, utilities, run_time = 2)
        )
        self.play(
            LaggedStartMap(
                ShowCreation, lines, 
                run_time = 3
            ),
            Animation(self.objects)
        )
        self.play(
            Write(no_crossing_words[0]),
            GrowArrow(no_crossing_words[1]),
        )
        self.wait()

        self.objects.add_to_back(lines, no_crossing_words)

    def point_to_abstractions(self):
        objects = self.objects
        objects.generate_target()
        objects.target.scale(0.5)
        objects.target.move_to(
            (FRAME_Y_RADIUS*DOWN + FRAME_X_RADIUS*LEFT)/2
        )

        eulers = OldTex(*"V-E+F=2")
        eulers.set_color_by_tex_to_color_map({
            "V" : RED,
            "E" : GREEN,
            "F" : BLUE,
        })
        eulers.to_edge(UP, buff = 2)

        # CHANGE: GL Cube is a surface without set_stroke/pose_at_angle; CairoCube is the Cairo VGroup of six faces
        cube = CairoCube()
        cube.set_stroke(WHITE, 2)
        cube.set_height(0.75)
        cube.pose_at_angle()
        cube.next_to(eulers, UP)

        tda = OldTexText("Topological \\\\ Data Analysis")
        tda.move_to(DOWN + 4*RIGHT)

        arrow_from_eulers = Arrow(
            eulers.get_bottom(), tda.get_corner(UP+LEFT),
            color = WHITE
        )

        self.play(
            objects.scale, 0.5,
            objects.move_to, DOWN + 4*LEFT,
        )
        arrow_to_eulers = Arrow(
            self.houses[2].get_corner(UP+LEFT),
            eulers.get_bottom(),
            color = WHITE
        )
        always_rotate(cube, axis=UP)
        self.play(
            GrowArrow(arrow_to_eulers),
            Write(eulers),
            FadeIn(cube)
        )
        self.wait(5)
        self.play(
            GrowArrow(arrow_from_eulers),
            Write(tda)
        )
        self.wait(2)

        self.set_variables_as_attrs(
            eulers, cube, tda,
            arrows = VGroup(arrow_to_eulers, arrow_from_eulers),
        )

    def show_this_video(self):
        screen_rect = FullScreenFadeRectangle(
            stroke_color = WHITE,
            stroke_width = 2,
            fill_opacity = 0,
        )
        everything = VGroup(
            self.objects, self.arrows, self.eulers, 
            self.cube, self.tda,
            screen_rect,
        )

        self.teacher.save_state()
        self.teacher.fade(1)

        self.play(
            everything.scale, 0.5,
            everything.next_to, self.teacher, UP+LEFT,
            self.teacher.restore,
            self.teacher.change, "raise_right_hand", UP+LEFT,
            LaggedStartMap(FadeIn, self.students)
        )
        self.play_student_changes(
            *["pondering"]*3, look_at = everything
        )
        self.wait(5)
