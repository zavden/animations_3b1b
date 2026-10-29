# ==============================================================================
# Scene:      IntroducePutnam
# Source:     videos/_2017/putnam.py (lines 6-126)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroducePutnam.py IntroducePutnam -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroducePutnam(Scene):
    CONFIG = {
        "dont_animate" : False,
    }
    def construct(self):
        title = OldTexText("Putnam Competition")
        title.to_edge(UP, buff = MED_SMALL_BUFF)
        title.set_color(BLUE)
        six_hours = OldTexText("6", "hours")
        three_hours = OldTexText("3", "hours")
        for mob in six_hours, three_hours:
            mob.next_to(title, DOWN, MED_LARGE_BUFF)
            # mob.set_color(BLUE)
        three_hours.shift(FRAME_X_RADIUS*LEFT/2)
        three_hours_copy = three_hours.copy()
        three_hours_copy.shift(FRAME_X_RADIUS*RIGHT)

        question_groups = VGroup(*[
            VGroup(*[
                OldTexText("%s%d)"%(c, i))
                for i in range(1, 7)
            ]).arrange(DOWN, buff = MED_LARGE_BUFF)
            for c in ("A", "B")
        ]).arrange(RIGHT, buff = FRAME_X_RADIUS - MED_SMALL_BUFF)
        question_groups.to_edge(LEFT)
        question_groups.to_edge(DOWN, MED_LARGE_BUFF)
        flat_questions = VGroup(*it.chain(*question_groups))

        rects = VGroup()
        for questions in question_groups:
            rect = SurroundingRectangle(questions, buff = MED_SMALL_BUFF)
            rect.set_stroke(WHITE, 2)
            rect.stretch_to_fit_width(FRAME_X_RADIUS - 1)
            rect.move_to(questions.get_left() + MED_SMALL_BUFF*LEFT, LEFT)
            rects.add(rect)

        out_of_tens = VGroup()
        for question in flat_questions:
            out_of_ten = OldTex("/10")
            out_of_ten.set_color(GREEN)
            out_of_ten.move_to(question)
            dist = rects[0].get_width() - 1.2
            out_of_ten.shift(dist*RIGHT)
            out_of_tens.add(out_of_ten)

        out_of_120 = OldTex("/120")
        out_of_120.next_to(title, RIGHT, LARGE_BUFF)
        out_of_120.set_color(GREEN)

        out_of_120.generate_target()
        out_of_120.target.to_edge(RIGHT, LARGE_BUFF)
        median = OldTex("2")
        median.next_to(out_of_120.target, LEFT, SMALL_BUFF)
        median.set_color(RED)
        median.align_to(out_of_120[-1])
        median_words = OldTexText("Typical median $\\rightarrow$")
        median_words.next_to(median, LEFT)

        difficulty_strings = [
            "Pretty hard",
            "Hard",
            "Harder",
            "Very hard",
            "Ughhh",
            "Can I go home?"
        ]
        colors = color_gradient([YELLOW, RED], len(difficulty_strings))
        difficulties = VGroup()
        for i, s, color in zip(it.count(), difficulty_strings, colors):
            for question_group in question_groups:
                question = question_group[i]
                text = OldTexText("\\dots %s \\dots"%s)
                text.scale(0.7)
                text.next_to(question, RIGHT)
                text.set_color(color)
                difficulties.add(text)


        if self.dont_animate:        
            test = VGroup()
            test.rect = rects[0]
            test.questions = question_groups[0]
            test.out_of_tens = VGroup(*out_of_tens[:6])
            test.difficulties = VGroup(*difficulties[::2])
            test.digest_mobject_attrs()
            self.test = test
            return

        self.add(title)
        self.play(Write(six_hours))
        self.play(LaggedStartMap(
            GrowFromCenter, flat_questions,
            run_time = 3,
        ))
        self.play(
            ReplacementTransform(six_hours, three_hours),
            ReplacementTransform(six_hours.copy(), three_hours_copy),
            *list(map(ShowCreation, rects))
        )
        self.wait()
        self.play(LaggedStartMap(
            DrawBorderThenFill, out_of_tens,
            run_time = 3,
            stroke_color = YELLOW
        ))
        self.wait()
        self.play(ReplacementTransform(
            out_of_tens.copy(), VGroup(out_of_120),
            lag_ratio = 0.5,
            run_time = 2,
        ))
        self.wait()
        self.play(
            title.next_to, median_words.copy(), LEFT, LARGE_BUFF,
            MoveToTarget(out_of_120),
            Write(median_words)
        )
        self.play(Write(median))
        for difficulty in difficulties:
            self.play(FadeIn(difficulty))
        self.wait()
