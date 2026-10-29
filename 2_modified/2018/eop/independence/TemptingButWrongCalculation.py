# ==============================================================================
# Scene:      TemptingButWrongCalculation
# Source:     videos/_2018/eop/independence.py (lines 747-821)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TemptingButWrongCalculation.py TemptingButWrongCalculation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ApplyMethod(mob.scale, f, point): GL scale() takes the point as about_point, not as 2nd positional argument; pass {"about_point": point}
# ==============================================================================

from manim_imports_ext import *

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


def get_quiz(*questions):
    q_mobs = VGroup(*list(map(TexText, [
        "%d. %s"%(i+1, question)
        for i, question in enumerate(questions)
    ])))
    q_mobs.arrange(
        DOWN, 
        buff = MED_LARGE_BUFF,
        aligned_edge = LEFT, 
    )
    content = VGroup(
        OldTexText("Quiz").scale(1.5),
        Line(q_mobs.get_left(), q_mobs.get_right()),
        q_mobs
    )
    content.arrange(DOWN, buff = MED_SMALL_BUFF)
    rect = SurroundingRectangle(content, buff = MED_LARGE_BUFF)
    rect.shift(MED_SMALL_BUFF*DOWN)
    rect.set_color(WHITE)
    quiz = VGroup(rect, content)
    quiz.questions = q_mobs
    quiz.scale(0.7)
    return quiz


def get_slot_group(
    bool_list, 
    buff = MED_LARGE_BUFF, 
    include_qs = True,
    min_bool_list_len = 3,
    ):
    if len(bool_list) < min_bool_list_len:
        bool_list += [None]*(min_bool_list_len - len(bool_list))
    n = len(bool_list)

    lines = VGroup(*[
        Line(ORIGIN, MED_LARGE_BUFF*RIGHT)
        for x in range(n)
    ])
    lines.arrange(RIGHT, buff = buff)
    if include_qs:
        labels = VGroup(*[
            OldTexText("Q%d"%d) for d in range(1, n+1)
        ])
    else:
        labels = VGroup(*[VectorizedPoint() for d in range(n)])
    for label, line in zip(labels, lines):
        label.scale(0.7)
        label.next_to(line, DOWN, SMALL_BUFF)
    slot_group = VGroup()
    slot_group.lines = lines
    slot_group.labels = labels
    slot_group.content = VGroup()
    slot_group.digest_mobject_attrs()
    slot_group.to_edge(RIGHT)
    slot_group.bool_list = bool_list

    total_height = FRAME_Y_RADIUS
    base = 2.3

    for i, line in enumerate(lines):
        if i >= len(bool_list) or bool_list[i] is None:
            mob = VectorizedPoint()
        elif bool_list[i]:
            mob = OldTex("\\checkmark")
            mob.set_color(GREEN)
            slot_group.shift(total_height*DOWN / (base**(i+1)))
        else:
            mob = OldTex("\\times")
            mob.set_color(RED)
            slot_group.shift(total_height*UP / (base**(i+1)))
        mob.next_to(line, UP, SMALL_BUFF)
        slot_group.content.add(mob)
    return slot_group


class IntroduceQuiz(PiCreatureScene):
    def construct(self):
        self.add_quiz()
        self.ask_about_probabilities()
        self.show_distribution()
        self.show_single_question_probability()

    def add_quiz(self):
        quiz = self.get_example_quiz()
        quiz.next_to(self.randy, UP+RIGHT)

        self.play(
            Write(quiz),
            self.randy.change, "pondering", quiz
        )
        self.wait()

        self.quiz = quiz

    def ask_about_probabilities(self):
        probabilities, abbreviated_probabilities = [
            VGroup(*[
                OldTex(
                    "P(", s_tex, "=", str(score), ")", rhs
                ).set_color_by_tex_to_color_map({
                    str(score) : YELLOW,
                    "text" : GREEN,
                })
                for score in range(4)
            ])
            for s_tex, rhs in [
                ("\\text{Score}", "= \\, ???"),
                ("\\text{S}", "")
            ]
        ]
        for group in probabilities, abbreviated_probabilities:
            group.arrange(
                DOWN, 
                buff = MED_LARGE_BUFF,
                aligned_edge = LEFT
            )
            group.to_corner(UP+LEFT)

        self.play(
            LaggedStartMap(FadeIn, probabilities, run_time = 3),
            self.quiz.set_height, 0.7*self.randy.get_height(),
            self.quiz.next_to, self.randy, RIGHT,
            self.randy.change, "confused", probabilities
        )
        self.wait()

        self.probabilities = probabilities
        self.abbreviated_probabilities = abbreviated_probabilities

    def show_distribution(self):
        dist = get_binomial_distribution(3, 0.7)
        values = list(map(dist, list(range(4))))
        chart = BarChart(
            values, 
            width = 7,
            bar_names = list(range(4))
        )
        chart.to_edge(RIGHT)
        for short_p, bar in zip(self.abbreviated_probabilities, chart.bars):
            short_p.set_width(1.75*bar.get_width())
            short_p.next_to(bar, UP)

        self.play(
            LaggedStartMap(Write, VGroup(
                *[m for m in chart if m is not chart.bars]
            )),
        )
        self.play(*[
            ReplacementTransform(
                bar.copy().stretch_to_fit_height(0).move_to(bar.get_bottom()),
                bar
            )
            for bar in chart.bars
        ])
        self.play(*[
            ReplacementTransform(p.copy(), short_p)
            for p, short_p in zip(
                self.probabilities,
                self.abbreviated_probabilities,
            )
        ])
        self.wait()

        self.bar_chart = chart

    def show_single_question_probability(self):
        prob = OldTex(
            "P(", "\\text{Can answer a given question}", ")",
            "= 0.8"
        )
        prob.to_corner(UP+RIGHT)
        prob.set_color_by_tex("text", GREEN)
        rect = SurroundingRectangle(prob, buff = MED_SMALL_BUFF)

        self.play(
            Write(prob),
            self.randy.change, "happy", prob
        )
        self.play(ShowCreation(rect))
        self.wait()

        self.single_question_probability = VGroup(
            prob, rect
        )


    ######

    def create_pi_creature(self):
        randy = Randolph()
        randy.scale(0.7)
        randy.to_corner(DOWN+LEFT)
        self.randy = randy
        return randy

    def get_example_quiz(self):
        return get_quiz(
            "Define ``Brachistochrone'' ",
            "Define ``Tautochrone'' ",
            "Define ``Cycloid'' ",
        )


class BreakDownQuestionPatterns(IntroduceQuiz):
    def construct(self):
        self.add_parts_from_last_scene()
        self.break_down_possibilities()
        self.count_patterns()

    def add_parts_from_last_scene(self):
        self.force_skipping()
        IntroduceQuiz.construct(self)
        self.revert_to_original_skipping_status()

        chart_group = VGroup(
            self.bar_chart,
            self.abbreviated_probabilities
        )
        self.play(
            self.single_question_probability.scale, 0.8,
            self.single_question_probability.to_corner, UP+LEFT,
            # CHANGE: GL scale() takes the point as about_point (Cairo took it positionally)
            chart_group.scale, 0.7, {"about_point": chart_group.get_top()},
            chart_group.to_edge, LEFT,
            FadeOut(self.probabilities)
        )

    def break_down_possibilities(self):
        slot_group_groups = VGroup(*[VGroup() for x in range(4)])
        bool_lists = [[]]
        while bool_lists:
            bool_list = bool_lists.pop()
            slot_group = self.get_slot_group(bool_list)
            slot_group_groups[len(bool_list)].add(slot_group)
            if len(bool_list) < 3:
                bool_lists += [
                    list(bool_list) + [True],
                    list(bool_list) + [False],
                ]

        group_group = slot_group_groups[0]
        self.revert_to_original_skipping_status()
        self.play(Write(group_group, run_time = 1))
        self.wait()
        for new_group_group in slot_group_groups[1:]:
            self.play(Transform(group_group, new_group_group))
            self.wait(2)

        self.slot_groups = slot_group_groups[-1]

    def count_patterns(self):
        brace = Brace(self.slot_groups, LEFT)
        count = OldTex("2^3 = 8")
        count.next_to(brace, LEFT)

        self.play(
            GrowFromCenter(brace),
            Write(count)
        )
        self.wait()

    #######

    def get_slot_group(self, bool_list):
        return get_slot_group(bool_list, include_qs = len(bool_list) < 3)


class TemptingButWrongCalculation(BreakDownQuestionPatterns):
    def construct(self):
        self.add_title()
        self.write_simple_product()

    def add_title(self):
        title = OldTexText("Tempting$\\dots$")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)
        self.title = title

    def write_simple_product(self):
        lhs = OldTex("P\\big(", "Filler Blah", "\\big)", "= ")
        lhs.next_to(ORIGIN, UP+LEFT)
        p_of = lhs.get_part_by_tex("P\\big(")
        filler = lhs.get_part_by_tex("Filler")
        rp = lhs.get_part_by_tex("\\big)")
        slot_group = self.get_slot_group([True, True, False])
        slot_group.replace(filler, dim_to_match = 0)
        lhs.submobjects.remove(filler)

        rhs = VGroup(*[
            OldTex("P(", "\\checkmark" if b else "\\times", ")")
            for b in slot_group.bool_list
        ])
        rhs.arrange(RIGHT, SMALL_BUFF)
        rhs.next_to(lhs, RIGHT, SMALL_BUFF)
        for part, b in zip(rhs, slot_group.bool_list):
            part.set_color_by_tex_to_color_map({
                "checkmark" : GREEN,
                "times" : RED,
            })
            brace = Brace(part, UP)
            if b:
                value = OldTex("(0.8)")
            else:
                value = OldTex("(0.2)")
            value.set_color(part[1].get_color())
            value.next_to(brace, UP)
            part.brace = brace
            part.value = value

        question = OldTexText("What about correlations?")
        question.next_to(rhs, DOWN, LARGE_BUFF)

        self.play(
            Write(lhs),
            ShowCreation(slot_group.lines),
            LaggedStartMap(FadeIn, slot_group.content, run_time = 3),
            self.randy.change, "pondering"
        )
        self.wait(2)
        for part, mob in zip(rhs, slot_group.content):
            self.play(*[
                ReplacementTransform(
                    mob.copy(), subpart,
                    path_arc = np.pi/6
                )
                for subpart, mob in zip(part, [
                    p_of, mob, rp
                ])
            ])
            self.play(GrowFromCenter(part.brace))
            self.play(FadeIn(part.value))
            self.wait()
        self.wait()
        self.play(
            Write(question),
            self.randy.change, "confused"
        )
        self.wait(3)

        self.question = question
        self.rhs = rhs
