# ==============================================================================
# Scene:      AskInverseQuestion
# Source:     videos/_2020/beta/beta1.py (lines 2240-2342)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl AskInverseQuestion.py AskInverseQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"


def get_prob_positive_experience_label(include_equals=False,
                                       include_decimal=False,
                                       include_q_mark=False):
    label = OldTex(
        "P", "(", "00000", ")",
    )

    pe = OldTexText("Positive\\\\experience")
    pe.set_color(GREEN)
    pe.replace(label[2], dim_to_match=0)
    label.replace_submobject(2, pe)
    VGroup(label[1], label[3]).match_height(
        pe, stretch=True, about_edge=DOWN,
    )
    if include_equals:
        eq = OldTex("=").next_to(label, RIGHT)
        label.add(eq)
    if include_decimal:
        decimal = DecimalNumber(0.95)
        decimal.next_to(label, RIGHT)
        decimal.set_color(YELLOW)
        label.decimal = decimal
        label.add(decimal)
    if include_q_mark:
        q_mark = OldTex("?")
        q_mark.relative_mob = label[-1]
        q_mark.add_updater(
            lambda m: m.next_to(m.relative_mob, RIGHT, SMALL_BUFF)
        )
        label.add(q_mark)

    return label



# ----- From _2020/beta/beta1.py -----

class WhatsTheModel(Scene):
    CONFIG = {
        "random_seed": 5,
    }

    def construct(self):
        self.add_questions()
        self.introduce_buyer_and_seller()

        for x in range(3):
            self.play(*self.experience_animations(self.seller, self.buyer))
        self.wait()

        self.add_probability_label()
        self.bring_up_goal()

    def add_questions(self):
        questions = VGroup(
            OldTexText("What's the model?"),
            OldTexText("What are you optimizing?"),
        )
        for question, vect in zip(questions, [LEFT, RIGHT]):
            question.move_to(vect * FRAME_WIDTH / 4)
        questions.arrange(DOWN, buff=LARGE_BUFF)
        questions.scale(1.5)

        # Intro questions
        self.play(FadeIn(questions[0]))
        self.play(FadeIn(questions[1], UP))
        self.wait()
        questions[1].save_state()

        self.questions = questions

    def introduce_buyer_and_seller(self):
        if hasattr(self, "questions"):
            questions = self.questions
            added_anims = [
                questions[0].to_edge, UP,
                questions[1].set_opacity, 0.5,
                questions[1].scale, 0.25,
                questions[1].to_corner, UR,
            ]
        else:
            added_anims = []

        seller = Randolph(mode="coin_flip_1")
        seller.to_edge(LEFT)
        seller.label = OldTexText("Seller")

        buyer = Mortimer()
        buyer.to_edge(RIGHT)
        buyer.label = OldTexText("Buyer")

        VGroup(buyer, seller).shift(DOWN)

        labels = VGroup()
        for pi in seller, buyer:
            pi.set_height(2)
            pi.label.scale(1.5)
            pi.label.next_to(pi, DOWN, MED_LARGE_BUFF)
            labels.add(pi.label)
        buyer.make_eye_contact(seller)

        self.play(
            LaggedStartMap(
                FadeInFromDown, VGroup(seller, buyer, *labels),
                lag_ratio=0.2
            ),
            *added_anims
        )
        self.wait()

        self.buyer = buyer
        self.seller = seller

    def add_probability_label(self):
        seller = self.seller
        buyer = self.buyer

        label = get_prob_positive_experience_label()
        label.add(OldTex("=").next_to(label, RIGHT))
        rhs = DecimalNumber(0.75)
        rhs.next_to(label, RIGHT)
        rhs.align_to(label[0], DOWN)
        label.add(rhs)
        label.scale(1.5)
        label.next_to(seller, UP, MED_LARGE_BUFF, aligned_edge=LEFT)

        rhs.set_color(YELLOW)
        brace = Brace(rhs, UP)
        success_rate = brace.get_text("Success rate")[0]
        s_sym = brace.get_tex("s").scale(1.5, about_edge=DOWN)
        success_rate.match_color(rhs)
        s_sym.match_color(rhs)

        self.add(label)

        self.play(
            GrowFromCenter(brace),
            FadeIn(success_rate, 0.5 * DOWN)
        )
        self.wait()
        self.play(
            TransformFromCopy(success_rate[0], s_sym),
            FadeOut(success_rate, 0.1 * RIGHT, lag_ratio=0.1),
        )
        for x in range(2):
            self.play(*self.experience_animations(seller, buyer, arc=30 * DEGREES))
        self.wait()

        grey_box = SurroundingRectangle(rhs, buff=SMALL_BUFF)
        grey_box.set_stroke(GREY_E, 0.5)
        grey_box.set_fill(GREY_D, 1)
        lil_q_marks = OldTex("???")
        lil_q_marks.scale(0.5)
        lil_q_marks.next_to(buyer, UP)

        self.play(
            FadeOut(rhs, 0.5 * DOWN),
            FadeIn(grey_box, 0.5 * UP),
            FadeIn(lil_q_marks, DOWN),
            buyer.change, "confused", grey_box,
        )
        rhs.set_opacity(0)
        for x in range(2):
            self.play(*self.experience_animations(seller, buyer, arc=30 * DEGREES))
        self.play(buyer.change, "confused", lil_q_marks)
        self.play(Blink(buyer))

        self.prob_group = VGroup(
            label, grey_box, brace, s_sym,
        )
        self.buyer_q_marks = lil_q_marks

    def bring_up_goal(self):
        prob_group = self.prob_group
        questions = self.questions
        questions.generate_target()
        questions.target[1].replace(questions[0], dim_to_match=1)
        questions.target[1].match_style(questions[0])
        questions.target[0].replace(questions[1], dim_to_match=1)
        questions.target[0].match_style(questions[1])

        prob_group.generate_target()
        prob_group.target.scale(0.5)
        prob_group.target.next_to(self.seller, RIGHT)

        self.play(
            FadeOut(self.buyer_q_marks),
            self.buyer.change, "pondering", questions[0],
            self.seller.change, "pondering", questions[0],
            MoveToTarget(prob_group),
            MoveToTarget(questions),
        )
        self.play(self.seller.change, "coin_flip_1")
        for x in range(3):
            self.play(*self.experience_animations(self.seller, self.buyer))
        self.wait()

    #
    def experience_animations(self, seller, buyer, arc=-30 * DEGREES, p=0.75):
        positive = (random.random() < p)
        words = OldTexText(
            "Positive\\\\experience"
            if positive else
            "Negative\\\\experience"
        )
        words.set_color(GREEN if positive else RED)
        if positive:
            new_mode = random.choice([
                "hooray",
                "coin_flip_1",
            ])
        else:
            new_mode = random.choice([
                "tired",
                "angry",
                "sad",
            ])

        words.move_to(seller.get_corner(UR))
        result = [
            ApplyMethod(
                words.move_to, buyer.get_corner(UL),
                path_arc=arc,
                run_time=2
            ),
            VFadeInThenOut(words, run_time=2),
            ApplyMethod(
                buyer.change, new_mode, seller.eyes,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.5, 1),
            ),
            ApplyMethod(
                seller.change, "coin_flip_2", buyer.eyes,
                rate_func=there_and_back,
            ),
        ]
        return result


class AskInverseQuestion(WhatsTheModel):
    def construct(self):
        self.force_skipping()
        self.introduce_buyer_and_seller()
        self.bs_group = VGroup(
            self.buyer,
            self.seller,
            self.buyer.label,
            self.seller.label,
        )
        self.bs_group.to_edge(DOWN)
        self.revert_to_original_skipping_status()

        self.add_probability_label()
        self.show_many_review_animations()
        self.ask_question()

    def add_probability_label(self):
        label = get_prob_positive_experience_label(True, True, False)
        label.decimal.set_value(0.95)
        label.next_to(self.seller, UP, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        self.add(label)
        self.probability_label = label

    def show_many_review_animations(self):
        for x in range(7):
            self.play(*self.experience_animations(
                self.seller,
                self.buyer,
                arc=30 * DEGREES,
                p=0.95,
            ))

    def ask_question(self):
        pis = [self.buyer, self.seller]
        labels = VGroup(
            self.get_prob_review_label(10, 0),
            self.get_prob_review_label(48, 2),
            self.get_prob_review_label(186, 14),
        )
        labels.arrange(DOWN)
        labels.to_edge(UP)

        labels[0].save_state()
        labels[0].set_opacity(0)
        words = labels[0][-3:-1]
        words.set_opacity(1)
        words.scale(1.5)
        words.center().to_edge(UP)

        self.play(
            FadeInFromDown(words),
        )
        self.wait()
        self.play(
            Restore(labels[0]),
            *[
                ApplyMethod(pi.change, 'pondering', labels)
                for pi in pis
            ]
        )
        self.play(Blink(pis[0]))
        self.play(Blink(pis[1]))
        self.play(LaggedStartMap(FadeInFromDown, labels[1:]))
        self.wait(2)

        # Succinct
        short_label = OldTex(
            "P(\\text{data} | s)",
            tex_to_color_map={
                "\\text{data}": GREY_B,
                "s": YELLOW
            }
        )
        short_label.scale(2)
        short_label.next_to(labels, DOWN, LARGE_BUFF),
        rect = SurroundingRectangle(short_label, buff=MED_SMALL_BUFF)
        bs_group = self.bs_group
        bs_group.add(self.probability_label)

        self.play(
            FadeIn(short_label, UP),
            bs_group.scale, 0.5, {"about_edge": DOWN},
        )
        self.play(ShowCreation(rect))
        self.wait()

    def get_prob_review_label(self, n_positive, n_negative):
        label = OldTex(
            "P(",
            f"{n_positive}\\,{CMARK_TEX}", ",\\,",
            f"{n_negative}\\,{XMARK_TEX}",
            "\\,\\text{ Given that }",
            "s = 0.95",
            ")",
        )
        label.set_color_by_tex_to_color_map({
            CMARK_TEX: GREEN,
            XMARK_TEX: RED,
            "0.95": YELLOW,
        })
        return label
