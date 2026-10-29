# ==============================================================================
# Scene:      NewQuestion
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 456-521)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewQuestion.py NewQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NewQuestion(InteractiveScene):
    def construct(self):
        # Questions
        text_kw = dict(font_size=48)
        questions = VGroup(
            Text("Why does light\nslow down in glass?", **text_kw),
            Text("Why does light's interaction\nwith a layer of glass\nkick back its phase?", **text_kw),
            Text("How much does\nlight slow down?", **text_kw),
            Text("How strong is\nthe phase kick?", **text_kw),
        )
        q1, q2, q3, q4 = questions
        for question, x in zip(questions, [-1, 1, -1, 1]):
            question.set_x(x * FRAME_WIDTH / 4)
            question.set_y(2.75)

        q3.shift(0.5 * RIGHT)
        q4.shift(0.5 * LEFT)

        bad_ap = q2["'"][0]
        good_ap = TexText("'")
        good_ap.replace(bad_ap, dim_to_match=1)
        bad_ap.become(good_ap)

        arrow1 = Arrow(q1, q2)
        arrow2 = Arrow(q3, q4)

        for question in [q1, q3]:
            question.set_opacity(0.5)
            question.save_state()
            question.set_x(0)
            question.set_opacity(1)

        # First pair
        self.play(FadeIn(q1))
        self.wait()
        self.play(
            ShowCreation(arrow1),
            Restore(q1),
            TransformMatchingStrings(q1.copy(), q2, run_time=1),
        )
        self.wait()
        self.play(
            FlashUnder(q2["layer of glass"], color=BLUE),
            q2["layer of glass"].animate.set_color(BLUE)
        )
        self.wait()
        self.play(
            FlashUnder(q2["phase"]),
            q2["phase"].animate.set_color(YELLOW)
        )
        self.wait()

        # Second pair
        self.play(
            FadeOut(q1, UP),
            FadeIn(q3, UP),
            FadeOut(arrow1),
            FadeOut(q2),
        )
        self.wait()
        self.play(
            ShowCreation(arrow2),
            Restore(q3),
            TransformMatchingStrings(q3.copy(), q4, run_time=1),
        )
        self.wait()
