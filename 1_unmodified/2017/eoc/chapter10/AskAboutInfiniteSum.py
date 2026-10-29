# ==============================================================================
# Scene:      AskAboutInfiniteSum
# Source:     videos/_2017/eoc/chapter10.py (lines 2983-3083)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutInfiniteSum.py AskAboutInfiniteSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutInfiniteSum(TeacherStudentsScene):
    def construct(self):
        self.ask_question()
        self.name_taylor_series()
        self.be_careful()


    def ask_question(self):
        big_rect = Rectangle(
            width = FRAME_WIDTH,
            height = FRAME_HEIGHT,
            stroke_width = 0,
            fill_color =  BLACK,
            fill_opacity = 0.7,
        )
        randy = self.get_students()[1]
        series = OldTex(
            "\\cos(x)", "\\approx", 
            "1 - \\frac{x^2}{2!} + \\frac{x^4}{4!}",
            " - \\frac{x^6}{6!}",
            "+\\cdots"
        )
        series.next_to(randy, UP, 2)
        series.shift_onto_screen()
        rhs = VGroup(*series[2:])
        arrow = Arrow(rhs.get_left(), rhs.get_right())
        arrow.next_to(rhs, UP)
        words = OldTexText("Add infinitely many")
        words.next_to(arrow, UP)

        self.teacher_says(
            "We could call \\\\ it an end here"
        )
        self.play_student_changes(*["erm"]*3)
        self.wait(3)
        self.play(
            RemovePiCreatureBubble(self.teacher),
            self.get_students()[0].change_mode, "plain",
            self.get_students()[2].change_mode, "plain",
            FadeIn(big_rect),
            randy.change_mode, "pondering"
        )
        crowd = VGroup(*self.get_pi_creatures())
        crowd.remove(randy)
        self.crowd_copy = crowd.copy()
        self.remove(crowd)
        self.add(self.crowd_copy, big_rect, randy)

        self.play(Write(series))
        self.play(
            ShowCreation(arrow),
            Write(words)
        )
        self.wait(3)

        self.arrow = arrow
        self.words = words
        self.series = series
        self.randy = randy

    def name_taylor_series(self):
        series_def = OldTexText(
            "Infinite sum $\\Leftrightarrow$ series"
        )
        taylor_series = OldTexText("Taylor series")
        for mob in series_def, taylor_series:
            mob.move_to(self.words)
        brace = Brace(self.series.get_part_by_tex("4!"), DOWN)
        taylor_polynomial = brace.get_text("Taylor polynomial")

        self.play(ReplacementTransform(
            self.words, series_def
        ))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(taylor_polynomial)
        )
        self.wait(2)
        self.play(
            series_def.scale, 0.7,
            series_def.to_corner, UP+RIGHT,
            FadeIn(taylor_series)
        )
        self.play(self.randy.change, "thinking", taylor_series)
        self.wait()

    def be_careful(self):
        self.play(FadeIn(self.teacher))
        self.remove(self.crowd_copy[0])
        self.teacher_says(
            "Be careful",
            bubble_config = {
                "width" : 3,
                "height" : 2
            },
            added_anims = [self.randy.change, "hesitant"]
        )
        self.wait(2)
        self.play(self.randy.change, "confused", self.series)
        self.wait(3)
