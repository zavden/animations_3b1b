# ==============================================================================
# Scene:      ThousandPossibleQuizzes
# Source:     videos/_2018/eop/independence.py (lines 823-1219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThousandPossibleQuizzes.py ThousandPossibleQuizzes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class ThousandPossibleQuizzes(Scene):
    CONFIG = {
        "n_quiz_rows" : 25,
        "n_quiz_cols" : 40,
        "n_movers" : 100,
        # "n_quiz_rows" : 5,
        # "n_quiz_cols" : 8,
        # "n_movers" : 4,
        "quizzes_height" : 4,
    }
    def construct(self):
        self.draw_all_quizzes()
        self.show_division_by_first_question()
        self.ask_about_second_question()
        self.show_uncorrelated_division_by_second()
        self.increase_second_correct_slice()
        self.second_division_among_first_wrong()
        self.show_that_second_is_still_80()
        self.emphasize_disproportionate_divide()
        self.show_third_question_results()

    def draw_all_quizzes(self):
        quizzes = self.get_thousand_quizzes()
        title = OldTexText("$1{,}000$ possible quizzes")
        title.scale(1.5)
        title.next_to(quizzes, UP)
        full_quizzes = VGroup(
            get_quiz(
                "Define ``Brachistochrone''",
                "Define ``Tautochrone''",
                "Define ``Cycloid''",
            ),
            get_quiz(
                "Define $\\dfrac{df}{dx}$",
                "Define $\\displaystyle \\lim_{h \\to 0} f(h)$",
                "Prove $\\dfrac{d(x^2)}{dx} = 2x$ ",
            ),
            get_quiz(
                "Find all primes $p$ \\\\ where $p+2$ is prime.",
                "Find all primes $p$ \\\\ where $2^{p}-1$ is prime.",
                "Solve $\\zeta(s) = 0$",
            ),
        )
        full_quizzes.arrange(RIGHT)
        target_quizzes = VGroup(*quizzes[:len(full_quizzes)])

        for quiz in full_quizzes:
            self.play(FadeIn(quiz, run_time = 3, lag_ratio = 0.5))
        self.play(
            Transform(full_quizzes, target_quizzes),
            FadeIn(title)
        )
        self.play(
            LaggedStartMap(
                FadeIn, quizzes, 
                run_time = 3,
                lag_ratio = 0.2,
            ),
            Animation(full_quizzes, remover = True)
        )
        self.wait()

        self.quizzes = quizzes
        self.title = title

    def show_division_by_first_question(self):
        n = int(0.8*len(self.quizzes))
        top_split = VGroup(*self.quizzes[:n])
        bottom_split = VGroup(*self.quizzes[n:])
        for split, color, vect in (top_split, GREEN, UP), (bottom_split, RED, DOWN):
            split.sort(lambda p : p[0])
            split.generate_target()
            split.target.shift(MED_LARGE_BUFF*vect)
            for quiz in split.target:
                quiz[0].set_color(color)

        labels = VGroup()
        for num, b, split in (800, True, top_split), (200, False, bottom_split):
            label = VGroup(
                OldTex(str(num)),
                get_slot_group([b], buff = SMALL_BUFF, include_qs = False)
            )
            label.arrange(DOWN)
            label.next_to(split.target, LEFT, buff = LARGE_BUFF)
            labels.add(label)

        self.play(
            FadeOut(self.title),
            MoveToTarget(top_split),
            MoveToTarget(bottom_split),
        )
        for label in labels:
            self.play(FadeIn(label))
            self.wait()

        self.splits = VGroup(top_split, bottom_split)
        self.q1_split_labels = labels

    def ask_about_second_question(self):
        top_split = self.splits[0]
        sg1, sg2 = slot_groups = VGroup(*[
            get_slot_group(
                [True, b], 
                include_qs = False,
                buff = SMALL_BUFF
            )
            for b in (True, False)
        ])
        question = VGroup(
            OldTexText("Where are"), sg1,
            OldTexText("and"), sg2, OldTexText("?"),
        )
        question.arrange(RIGHT, aligned_edge = DOWN)
        question[-1].next_to(question[-2], RIGHT, SMALL_BUFF)
        question.next_to(top_split, UP, MED_LARGE_BUFF)
        slot_groups.shift(SMALL_BUFF*DOWN)
        little_rects = VGroup(*[
            SurroundingRectangle(
                VGroup(sg.lines[1], sg.content[1])
            )
            for sg in slot_groups
        ])
        big_rect = SurroundingRectangle(top_split)

        self.play(Write(question))
        self.play(ShowCreation(little_rects))
        self.wait()
        self.play(FadeOut(little_rects))
        self.play(ShowCreation(big_rect))
        self.play(
            FadeOut(big_rect),
            FadeOut(question),
        )
        self.wait()

    def show_uncorrelated_division_by_second(self):
        top_split = self.splits[0]
        top_label = self.q1_split_labels[0]
        n = int(0.8*len(top_split))
        left_split = VGroup(*top_split[:n])
        right_split = VGroup(*top_split[n:])
        for split, color in (left_split, GREEN_E), (right_split, RED_E):
            split.generate_target()
            for quiz in split.target:
                quiz[1].set_color(color)
        left_split.target.shift(LEFT)

        left_label = VGroup(
            OldTex("(0.8)", "800 =", "640"),
            get_slot_group([True, True], buff = SMALL_BUFF, include_qs = False)
        )
        left_label.arrange(RIGHT, buff = MED_LARGE_BUFF)
        left_label.next_to(left_split.target, UP)

        self.play(
            MoveToTarget(left_split),
            MaintainPositionRelativeTo(top_label, left_split),
            MoveToTarget(right_split),
        )
        self.play(FadeIn(left_label))
        self.play(LaggedStartMap(
            ApplyMethod, left_split,
            lambda m : (m.set_color, YELLOW),
            rate_func = there_and_back,
            lag_ratio = 0.2,
        ))
        self.wait()

        self.top_left_label = left_label
        self.top_splits = VGroup(left_split, right_split)

    def increase_second_correct_slice(self):
        left_split, right_split = self.top_splits
        left_label = self.top_left_label
        left_label_equation = left_label[0]
        movers = VGroup(*right_split[:self.n_movers])
        movers.generate_target()
        for quiz in movers.target:
            quiz[1].set_color(left_split[0][1].get_color())
        movers.target.shift(LEFT)

        new_equation = OldTex("(0.925)", "800 =", "740")
        for i in 0, 2:
            new_equation[i].set_color(YELLOW)
        new_equation.move_to(left_label_equation)

        self.play(
            MoveToTarget(
                movers, 
                lag_ratio = 0.5,
                run_time = 3,
            ),
            Transform(left_label_equation, new_equation)
        )
        self.wait(2)
        self.play(Indicate(left_label_equation[0]))
        self.wait()

        left_split.add(*movers)
        right_split.remove(*movers)
        self.top_left_split = left_split
        self.top_right_split = right_split
        self.top_movers = movers
        self.top_equation = left_label_equation

    def second_division_among_first_wrong(self):
        top_label, bottom_label = self.q1_split_labels
        top_split, bottom_split = self.splits
        top_left_label = self.top_left_label
        top_group = VGroup(top_split, top_left_label, top_label)

        n = int(0.8*len(bottom_split))
        left_split = VGroup(*bottom_split[:n])
        right_split = VGroup(*bottom_split[n:])
        for split, color in (left_split, GREEN_E), (right_split, RED_E):
            split.generate_target()
            for quiz in split.target:
                quiz[1].set_color(color)
        left_split.target.shift(LEFT)

        movers = VGroup(*left_split[-self.n_movers:])
        movers.generate_target()
        for quiz in movers.target:
            quiz[1].set_color(right_split.target[0][1].get_color())

        equation = OldTex("(0.8)", "200 = ", "160")
        slot_group = get_slot_group([False, True], buff = SMALL_BUFF, include_qs = False)
        label = VGroup(equation, slot_group)
        label.arrange(DOWN, buff = SMALL_BUFF)
        label.next_to(left_split.target, UP, SMALL_BUFF, LEFT)
        alt_equation = OldTex("(0.3)", "200 = ", "60")
        for i in 0, 2:
            alt_equation[i].set_color(YELLOW)
        alt_equation.move_to(equation)

        self.play(top_group.to_edge, UP, SMALL_BUFF)
        self.play(
            bottom_label.shift, LEFT,
            *list(map(MoveToTarget, [left_split, right_split]))
        )
        self.play(FadeIn(label))
        self.wait()
        self.play(
            MoveToTarget(
                movers, 
                lag_ratio = 0.5,
                run_time = 3,
            ),
            Transform(equation, alt_equation)
        )
        self.wait()

        left_split.remove(*movers)
        right_split.add(*movers)
        self.bottom_left_split = left_split
        self.bottom_right_split = right_split
        self.bottom_movers = movers
        self.bottom_equation = equation
        self.bottom_left_label = label

    def show_that_second_is_still_80(self):
        second_right = VGroup(
            self.bottom_left_split, self.top_left_split
        )
        second_wrong = VGroup(
            self.bottom_right_split, self.top_right_split
        )
        rects = VGroup(*[
            SurroundingRectangle(mob, buff = SMALL_BUFF)
            for mob in second_right
        ])

        num1 = self.top_equation[-1].copy()
        num2 = self.bottom_equation[-1].copy()

        equation = OldTex("740", "+", "60", "=", "800")
        for tex in "740", "60":
            equation.set_color_by_tex(tex, YELLOW)
        slot_group = get_slot_group([True, True])
        slot_group.content[0].set_fill(BLACK, 0)
        label = VGroup(equation, slot_group)
        label.arrange(DOWN)
        label.next_to(self.quizzes, LEFT, LARGE_BUFF)

        self.play(
            FadeOut(self.q1_split_labels),
            ShowCreation(rects)
        )
        self.play(
            FadeIn(slot_group),
            Transform(
                num1, equation[0],
                rate_func = squish_rate_func(smooth, 0, 0.7),
            ),
            Transform(
                num2, equation[2],
                rate_func = squish_rate_func(smooth, 0.3, 1),
            ),
            run_time = 2
        )
        self.play(
            Write(equation),
            *list(map(Animation, [num1, num2]))
        )
        self.remove(num1, num2)
        self.wait()
        self.play(FadeOut(rects))

    def emphasize_disproportionate_divide(self):
        top_movers = self.top_movers
        bottom_movers = self.bottom_movers
        both_movers = VGroup(top_movers, bottom_movers)
        both_movers.save_state()

        top_movers.target = bottom_movers.copy().shift(LEFT)
        bottom_movers.target = top_movers.copy().shift(RIGHT)
        for quiz in top_movers.target:
            quiz[0].set_color(RED)
        for quiz in bottom_movers.target:
            quiz[0].set_color(GREEN)

        line = Line(UP, DOWN, color = YELLOW)
        line.set_height(self.quizzes.get_height())
        line.next_to(bottom_movers.target, LEFT, MED_LARGE_BUFF, UP)

        self.revert_to_original_skipping_status()
        self.play(*list(map(MoveToTarget, both_movers)))
        self.play(ShowCreation(line))
        self.play(FadeOut(line))
        self.wait()
        self.play(both_movers.restore)
        self.wait()

    def show_third_question_results(self):
        all_splits = VGroup(
            self.top_left_split, self.top_right_split,
            self.bottom_left_split, self.bottom_right_split
        )
        proportions = [0.9, 0.8, 0.8, 0.4]
        for split, prop in zip(all_splits, proportions):
            n = int(prop*len(split))
            split.sort(lambda p : -p[1])
            split.generate_target()
            top_part = VGroup(*split.target[:n])
            top_part.shift(MED_SMALL_BUFF*UP)
            bottom_part = VGroup(*split.target[n:])
            bottom_part.shift(MED_SMALL_BUFF*DOWN)
            for quiz in top_part:
                quiz[-1].set_color(GREEN)
            for quiz in bottom_part:
                quiz[-1].set_color(RED)

        split = self.top_left_split
        n_all_right = int(proportions[0]*len(split))
        all_right = VGroup(*split[:n_all_right])

        self.play(
            FadeOut(self.top_left_label),
            FadeOut(self.bottom_left_label),
        )
        for split in all_splits:
            self.play(MoveToTarget(split))
        self.wait()
        self.play(LaggedStartMap(
            ApplyMethod, all_right,
            lambda m : (m.set_color, YELLOW),
            rate_func = there_and_back,
            lag_ratio = 0.2,
            run_time = 2
        ))
        self.wait(2)

    #####

    def get_thousand_quizzes(self):
        rows = VGroup()
        for x in range(self.n_quiz_rows):
            quiz = VGroup(*[
                Rectangle(
                    height = SMALL_BUFF,
                    width = 0.5*SMALL_BUFF
                )
                for x in range(3)
            ])
            quiz.arrange(RIGHT, buff = 0)
            quiz.set_stroke(width = 0)
            quiz.set_fill(GREY_B, 1)
            row = VGroup(*[quiz.copy() for y in range(self.n_quiz_cols)])
            row.arrange(RIGHT, buff = SMALL_BUFF)
            rows.add(row)

        rows.arrange(DOWN, buff = SMALL_BUFF)
        quizzes = VGroup(*it.chain(*rows))
        quizzes.set_height(self.quizzes_height)
        quizzes.to_edge(RIGHT)
        quizzes.shift(MED_LARGE_BUFF*DOWN)
        return quizzes
