# ==============================================================================
# Scene:      WhyIsThisWrong
# Source:     videos/_2020/med_test.py (lines 6383-6478)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyIsThisWrong.py WhyIsThisWrong -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


def get_covid_clipboard(disease_name="SARS\\\\CoV-2", sign="+", report="Detected", color=GREEN):
    clipboard = SVGMobject("clipboard")
    clipboard.set_stroke(width=0)
    clipboard.set_fill(interpolate_color(GREY_BROWN, WHITE, 0.5), 1)
    clipboard.set_width(2.5)

    result = OldTexText(
        sign + "\\\\",
        disease_name + "\\\\",
        report,
    )
    result[0].scale(1.5, about_point=result[1].get_top())
    result[0].set_fill(color)
    result[0].set_stroke(color, 2)
    result[2].set_width(1.2 * result[1].get_width())
    result[-1].set_fill(color)
    result.set_width(clipboard.get_width() * 0.7)
    result.move_to(clipboard)
    result.shift(0.2 * DOWN)
    clipboard.add(result)
    return clipboard


class WhyIsThisWrong(TeacherStudentsScene):
    def construct(self):
        # Ask question
        tweet = ImageMobject("twitter_covid_test_poll")
        tweet.replace(self.screen, dim_to_match=0)
        tweet.to_edge(UP)
        tweet.scale(0.9, about_edge=UP)

        self.add(tweet)
        self.student_says(
            "Bayes' rule says\\\\ 8.5\\%, right?",
            target_mode="hooray",
            index=1,
        )
        self.wait()
        self.play(
            PiCreatureSays(
                self.teacher,
                "Well...",
                bubble_config={"height": 2, "width": 2},
                target_mode="hesitant",
            ),
            self.change_students("confused", "erm", "pondering")
        )
        self.wait(3)

        # Highlight symptoms
        self.play(
            RemovePiCreatureBubble(self.students[1]),
            RemovePiCreatureBubble(self.teacher, target_mode="raise_right_hand"),
            tweet.move_to, self.hold_up_spot, DR,
            tweet.shift, RIGHT,
        )

        underline = Line((-1.3, 2.65), (2.1, 2.65))
        underline.shift(RIGHT)
        underline.set_stroke(RED, 3)

        self.play(
            ShowCreation(underline),
            self.teacher.look_at, underline,
            *(ApplyMethod(pi.change, "pondering", underline) for pi in self.students),
        )
        self.wait()

        # Change prior
        ineq = OldTexText("Prior > $\\frac{1}{1,000}$", font_size=72)
        ineq.next_to(tweet, LEFT, LARGE_BUFF)

        self.play(Write(ineq))
        self.look_at(ineq)
        self.wait()

        # More severe symptoms
        for pi in self.students:
            pi.generate_target()
            pi.target.change("sick")
            pi.target.set_color(SICKLY_GREEN)
            pi.target.look(DR)

        self.play(
            LaggedStartMap(MoveToTarget, self.students, lag_ratio=0.3),
            self.teacher.change, "erm"
        )

        clipboard = get_covid_clipboard()
        clipboard.to_corner(UL)

        self.play(
            FadeIn(clipboard, UP),
            FadeOut(ineq, UP),
            *(ApplyMethod(pi.look_at, clipboard) for pi in self.pi_creatures),
        )
        self.wait()

        percent = OldTex("8.3 \\%", font_size=72)
        percent.next_to(clipboard, RIGHT, buff=0.6)
        percent_cross = Cross(percent, stroke_width=8)

        self.play(
            FadeIn(percent),
            self.teacher.change, "tease"
        )
        self.play(ShowCreation(percent_cross))
        self.wait()

        self.student_says(
            "What's the appropriate\\\\math here?",
            index=1,
            added_anims=[
                FadeOut(tweet),
                FadeOut(underline),
                self.teacher.change, "happy"
            ]
        )
        self.wait(2)
