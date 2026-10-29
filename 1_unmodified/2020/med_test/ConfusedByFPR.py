# ==============================================================================
# Scene:      ConfusedByFPR
# Source:     videos/_2020/med_test.py (lines 5257-5360)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusedByFPR.py ConfusedByFPR -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class ConfusedByFPR(Scene):
    def construct(self):
        # Background
        br = FullScreenFadeRectangle()
        br.set_fill(GREY_E, 1)
        self.add(br)

        # State FPR
        randy = Randolph(height=2.5, color=BLUE_C)
        randy.to_corner(DL, buff=LARGE_BUFF)

        clipboard = get_covid_clipboard("Cancer")
        clipboard.set_height(2)
        clipboard.next_to(randy.get_corner(UR), RIGHT)

        doctor = SVGMobject("female_doctor")
        doctor.remove(doctor[0])
        doctor.set_stroke(width=0)
        doctor.set_fill(GREY_B)
        doctor.set_height(2.5)
        doctor.to_corner(DR, buff=LARGE_BUFF)

        fpr_words = OldTexText(
            "This test's\\\\false positive rate\\\\is 9\\%",
            tex_to_color_map={
                "false positive rate": GREEN,
                "9\\%": WHITE,
            }
        )
        bubble = SpeechBubble(height=3, width=4)
        bubble.pin_to(doctor)
        bubble.add_content(fpr_words)

        self.add(randy)
        self.add(doctor)
        self.play(
            FadeIn(clipboard, LEFT),
            randy.change, "guilty"
        )
        self.play(
            DrawBorderThenFill(bubble),
            Write(fpr_words)
        )
        self.play(Blink(randy))
        self.wait()

        # Misinterpret
        false_prob = OldTex(
            "P(\\text{Test is false}) = 9\\%",
            tex_to_color_map={"9\\%": WHITE}
        )
        thought_bubble = ThoughtBubble(height=3, width=4)
        thought_bubble.pin_to(randy)
        thought_bubble.add_content(false_prob)
        cross = Cross(thought_bubble[-1])

        self.play(
            randy.change, 'confused', false_prob,
            DrawBorderThenFill(thought_bubble),
            FadeIn(false_prob),
            clipboard.shift, DOWN,
        )
        self.play(Blink(randy))
        self.play(
            ShowCreation(cross),
            randy.change, "maybe", cross,
        )
        self.wait()

        # Sweep away
        self.play(
            randy.change, "hesitant",
            LaggedStartMap(
                FadeOut, VGroup(thought_bubble, false_prob, cross),
                scale=0.5,
                run_time=1,
            )
        )

        # Mention Bayes factor instead
        bf_words = OldTexText(
            "This test's\\\\positive Bayes factor\\\\is 10",
            tex_to_color_map={
                "positive Bayes factor": YELLOW,
                "10": WHITE,
            }
        )
        bf_words.replace(fpr_words, 1)
        anims = []
        for m1, m2 in zip(fpr_words, bf_words):
            m1.generate_target()
            m1.target.replace(m2, stretch=True)
            m1.target.set_opacity(0)
            anims.append(MoveToTarget(m1, remover=True))

            m2.save_state()
            m2.replace(m1, stretch=True)
            m2.set_opacity(0)
            anims.append(Restore(m2))

        self.play(*anims)
        self.play(randy.change, "pondering")
        self.play(Blink(randy))
        self.wait()
