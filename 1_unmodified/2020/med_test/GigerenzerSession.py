# ==============================================================================
# Scene:      GigerenzerSession
# Source:     videos/_2020/med_test.py (lines 1438-1734)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GigerenzerSession.py GigerenzerSession -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GigerenzerSession(Scene):
    def construct(self):
        # Gigerenzer intro
        years = OldTexText("2006-2007", font_size=72)
        years.to_edge(UP)

        image = ImageMobject("Gerd_Gigerenzer")
        image.set_height(4)
        image.flip()
        name = OldTexText("Gerd Gigerenzer", font_size=72)
        name.next_to(image, DOWN)
        image_group = Group(image, name)

        self.play(FadeIn(years, shift=0.5 * UP))
        self.wait()
        self.play(
            FadeIn(image),
            Write(name)
        )
        self.wait()

        # Seminar words
        title = OldTexText("Statistics Seminar", font_size=72)
        title.to_edge(UP)

        title_underline = Underline(title, buff=SMALL_BUFF)
        title_underline.scale(1.1)
        title_underline.set_stroke(GREY_B)

        self.play(
            FadeIn(title, shift=0.5 * UP),
            FadeOut(years, shift=0.5 * UP),
        )
        self.play(ShowCreation(title_underline))
        title.add(title_underline)

        # Docs
        doctors = ImageMobject("doctor_pair", height=2)
        doctors.to_corner(DL, buff=1)
        doctors_label = OldTexText("Practicing Gynecologists")
        doctors_label.match_width(doctors)
        doctors_label.next_to(doctors, DOWN)
        doctors_label.set_fill(GREY_A)

        self.play(
            FadeIn(doctors, scale=1.1),
            Write(doctors_label, run_time=1),
            image_group.scale, 0.75,
            image_group.to_corner, DR,
        )
        self.wait()

        # Description of patient
        prompt = OldTexText(
            """
            A 50-year-old woman, no symptoms, participates\\\\
            in routine mammography screening.
            """,
            """She tests positive,\\\\
            is alarmed, and wants to know from you whether she\\\\
            has breast cancer for certain or what the chances are.\\\\
            \\quad \\\\
            """,
            """
            Apart from the screening results, you know nothing\\\\
            else about this woman.\\\\
            """,
            alignment="",
            font_size=36,
        )
        prompt.next_to(title_underline, DOWN, MED_LARGE_BUFF)
        prompt[2].shift(0.5 * UP)
        no_symptoms_part = prompt[0][18:28]
        no_symptoms_underline = Underline(
            no_symptoms_part,
            buff=0,
            stroke_width=3,
            stroke_color=YELLOW,
        )

        clipboard = SVGMobject(
            "clipboard",
            stroke_width=0,
            fill_color=interpolate_color(GREY_BROWN, WHITE, 0.2)
        )
        clipboard.next_to(prompt, DOWN)
        clipboard.set_width(2.5)

        clipboard_contents = VGroup(
            OldTexText("+", color=GREEN, font_size=96, stroke_width=3),
            OldTexText("Cancer\\\\detected", color=GREY_A),
        )
        clipboard_contents.arrange(DOWN)
        clipboard_contents.set_width(0.7 * clipboard.get_width())
        clipboard_contents.move_to(clipboard)
        clipboard_contents.shift(0.1 * DOWN)
        clipboard.add(clipboard_contents)

        self.play(FadeIn(prompt[0], lag_ratio=0.01))
        self.wait()
        self.play(ShowCreationThenFadeOut(no_symptoms_underline))
        self.wait()
        self.play(
            FadeIn(prompt[1], lag_ratio=0.01),
            prompt[0].set_opacity, 0.5,
        )
        self.play(
            FadeIn(clipboard, shift=0.5 * UP, scale=1.1),
            image_group.scale, 0.75, {"about_edge": DR},
        )
        self.wait()

        self.play(
            FadeIn(prompt[2], lag_ratio=0.01),
            prompt[1].set_opacity, 0.5,
            clipboard.scale, 0.7, {"about_edge": DOWN},
        )
        self.wait()

        # Push prompt lower
        prompt.generate_target()
        prompt.target.set_opacity(0.8)
        prompt.target.replace(image_group, 0)
        prompt.target.scale(1.5, about_edge=RIGHT)

        h_line = DashedLine(FRAME_WIDTH * LEFT / 2, FRAME_WIDTH * RIGHT / 2)
        h_line.set_stroke(GREY_C)
        h_line.next_to(clipboard, UP)
        h_line.set_x(0)

        self.play(
            FadeOut(title, shift=UP),
            MoveToTarget(prompt),
            ShowCreation(h_line),
            FadeOut(image_group, shift=DR),
            clipboard.shift, 0.5 * LEFT,
        )

        # Test statistics
        stats = VGroup(
            OldTexText("Prevalence: ", "1\\%"),
            OldTexText("Sensitivity: ", "90\\%"),
            OldTexText("Specificity: ", "91\\%"),
        )
        stats.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        stats.to_corner(UL, buff=LARGE_BUFF)
        colors = [YELLOW, GREEN_B, GREY_B]
        for stat, color in zip(stats, colors):
            stat[0].set_color(color)
            stat[1].align_to(stats[0][1], LEFT)

        for stat in stats:
            self.play(FadeIn(stat[0], shift=0.25 * UP))
            self.play(Write(stat[1]))
            self.wait()
        self.wait()

        # Show randy knowing the answer
        randy = Randolph(height=2)
        randy.flip()
        randy.next_to(h_line, UP)
        randy.to_edge(RIGHT)

        bubble = randy.get_bubble(
            height=2,
            width=2,
        )
        bubble.shift(0.2 * LEFT)
        bubble.write("$\\frac{1}{11}$")

        self.play(FadeIn(randy))
        self.play(
            randy.change, "thinking",
            ShowCreation(bubble),
            Write(bubble.content),
        )
        self.play(Blink(randy))
        self.wait()

        # Show population
        dot = Dot()
        globals()['dot'] = dot
        dots = VGroup(*(dot.copy() for x in range(1000)))
        dots.arrange_in_grid(25, 40, buff=SMALL_BUFF)
        dots.set_height(4)
        dots.to_corner(UR)
        dots.set_fill(GREY_D)
        VGroup(*random.sample(list(dots), 10)).set_fill(YELLOW)

        cross = Cross(dots)
        cross.set_stroke(RED, 30)

        self.play(
            LaggedStartMap(FadeOut, VGroup(randy, bubble, bubble.content)),
            ShowIncreasingSubsets(dots, run_time=2)
        )
        self.wait()
        self.play(ShowCreation(cross))
        self.play(FadeOut(dots), FadeOut(cross))
        self.wait()
        self.play(LaggedStart(*(
            ShowCreationThenFadeOut(SurroundingRectangle(
                stat[1], color=stat[0].get_color()
            ))
            for stat in stats
        )))

        # Ask question
        question = OldTexText(
            "How many women who test positive\\\\actually have breast cancer?",
            font_size=36
        )
        question.to_corner(UR)
        question.shift(LEFT)

        self.play(FadeIn(question, lag_ratio=0.1))

        choices = VGroup(
            OldTexText("A) 9 in 10"),
            OldTexText("B) 8 in 10"),
            OldTexText("C) 1 in 10"),
            OldTexText("D) 1 in 100"),
        )
        choices.arrange_in_grid(2, 2, h_buff=1.0, v_buff=0.5, aligned_edge=LEFT)
        choices.next_to(question, DOWN, buff=0.75)
        choices.set_fill(GREY_A)

        self.play(LaggedStart(*(
            FadeIn(choice, scale=1.2)
            for choice in choices
        ), lag_ratio=0.3))
        self.wait()

        # Comment on choices
        a_rect = SurroundingRectangle(choices[0])
        a_rect.set_color(BLUE)
        q_mark = OldTex("?")
        q_mark.match_height(a_rect)
        q_mark.next_to(a_rect, LEFT)
        q_mark.match_color(a_rect)
        q_mark2 = q_mark.copy()
        q_mark2.move_to(doctors, UR)

        c_rect = SurroundingRectangle(choices[2])
        c_rect.set_color(GREEN)
        checkmark = Checkmark().next_to(c_rect, LEFT)

        self.play(
            ShowCreation(a_rect),
            Write(q_mark2)
        )
        self.play(TransformFromCopy(q_mark2, q_mark))
        self.wait()

        # One fifth of doctors
        curr_doc_group = Group(
            doctors,
            clipboard,
            doctors_label,
            q_mark2,
        )

        new_doctors = VGroup(
            SVGMobject("female_doctor"),
            SVGMobject("female_doctor"),
            SVGMobject("female_doctor"),
            SVGMobject("male_doctor"),
            SVGMobject("male_doctor"),
        )
        for doc in new_doctors:
            doc.remove(doc[0])
            doc.set_stroke(width=0)
            doc.set_fill(GREY_B)
        new_doctors.arrange_in_grid(2, 2, buff=MED_LARGE_BUFF)
        new_doctors[4].move_to(new_doctors[:4])
        new_doctors.set_height(2.75)
        new_doctors.move_to(doctors, UP)

        marks = VGroup()
        for n, doc in enumerate(new_doctors):
            mark = Checkmark() if n == 0 else Exmark()
            mark.move_to(doc.get_corner(UL))
            mark.shift(SMALL_BUFF * DR)
            marks.add(mark)

        new_doctors[0].set_color(GREEN)

        self.play(
            LaggedStartMap(FadeOut, curr_doc_group, scale=0.5, run_time=1),
            FadeIn(new_doctors, lag_ratio=0.1)
        )
        self.play(
            ReplacementTransform(a_rect, c_rect),
            FadeOut(q_mark),
            Write(checkmark)
        )
        self.wait()
