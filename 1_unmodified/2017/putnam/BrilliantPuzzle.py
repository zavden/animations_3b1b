# ==============================================================================
# Scene:      BrilliantPuzzle
# Source:     videos/_2017/putnam.py (lines 1326-1450)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BrilliantPuzzle.py BrilliantPuzzle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BrilliantPuzzle(PiCreatureScene):
    CONFIG = {
        "random_seed" : 2,
    }
    def construct(self):
        students = self.students
        tests = VGroup()
        for student in students:
            test = self.get_test()
            test.move_to(0.75*student.get_center())
            tests.add(test)
            student.test = test
        for i, student in enumerate(students):
            student.right = students[(i+1)%len(students)]
            student.left = students[(i-1)%len(students)]
        arrows = VGroup()
        for s1, s2 in adjacent_pairs(self.students):
            arrow = Arrow(
                s1.get_center(), s2.get_center(), 
                path_arc = np.pi/2,
                buff = 0.8
            )
            arrow.tip.shift(SMALL_BUFF*arrow.get_vector())
            arrow.tip.shift(-0.1*SMALL_BUFF*arrow.tip.get_center())
            # arrow.shift(-MED_SMALL_BUFF*arrow.get_vector())
            arrow.set_color(RED)
            arrow.pointing_right = True
            arrows.add(arrow)
            s1.arrow = arrow
            arrow.student = s1

        title = OldTexText("Puzzle from Brilliant")
        title.scale(0.75)
        title.to_corner(UP+LEFT)

        question = OldTexText("Expected number of \\\\ circled students?")
        question.to_corner(UP+RIGHT)

        self.remove(students)
        self.play(Write(title))
        self.play(LaggedStartMap(GrowFromCenter, students))
        self.play(
            LaggedStartMap(Write, tests),
            LaggedStartMap(
                ApplyMethod, students,
                lambda m : (m.change, "horrified", m.test)
            )
        )
        self.wait()
        self.play(LaggedStartMap(
            ApplyMethod, students,
            lambda m : (m.change, "conniving")
        ))
        self.play(LaggedStartMap(ShowCreation, arrows))
        for x in range(2):
            self.swap_arrows_randomly(arrows)
        self.wait()
        circles = self.circle_students()
        self.play(Write(question))
        for x in range(10):
            self.swap_arrows_randomly(arrows, FadeOut(circles))
            circles = self.circle_students()
            self.wait()

    ####

    def get_test(self):
        lines = VGroup(*[Line(ORIGIN, 0.5*RIGHT) for x in range(6)])
        lines.arrange(DOWN, buff = SMALL_BUFF)
        rect = SurroundingRectangle(lines)
        rect.set_stroke(WHITE)
        lines.set_stroke(WHITE, 2)
        test = VGroup(rect, lines)
        test.set_height(0.5)
        return test

    def create_pi_creatures(self):
        self.students = VGroup(*[
            PiCreature(
                color = random.choice([BLUE_C, BLUE_D, BLUE_E, GREY_BROWN])
            ).scale(0.25).move_to(3*vect)
            for vect in compass_directions(8)
        ])
        return self.students

    def get_arrow_swap_anim(self, arrow):
        arrow.generate_target()
        if arrow.pointing_right:
            target_color = GREEN
            target_angle = np.pi - np.pi/4
        else:
            target_color = RED
            target_angle = np.pi + np.pi/4
        arrow.target.set_color(target_color)
        arrow.target.rotate(
            target_angle, 
            about_point = arrow.student.get_center()
        )
        arrow.pointing_right = not arrow.pointing_right
        return MoveToTarget(arrow, path_arc = np.pi)

    def swap_arrows_randomly(self, arrows, *added_anims):
        anims = []
        for arrow in arrows:
            if random.choice([True, False]):
                anims.append(self.get_arrow_swap_anim(arrow))
        self.play(*anims + list(added_anims))

    def circle_students(self):
        circles = VGroup()
        circled_students = list(self.students)
        for student in self.students:
            if student.arrow.pointing_right:
                to_remove = student.right
            else:
                to_remove = student.left
            if to_remove in circled_students:
                circled_students.remove(to_remove)
        for student in circled_students:
            circle = Circle(color = YELLOW)
            circle.set_height(1.2*student.get_height())
            circle.move_to(student)
            circles.add(circle)
            self.play(ShowCreation(circle))
        return circles
