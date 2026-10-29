# ==============================================================================
# Scene:      IntroducePascalsTriangle
# Source:     videos/_2018/eop/combinations.py (lines 1746-2010)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroducePascalsTriangle.py IntroducePascalsTriangle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_stack(
    obj1, obj2, n, k,
    fixed_start = None,
    fixed_end = None,
    obj_to_obj_buff = SMALL_BUFF,
    vertical_buff = MED_SMALL_BUFF,
    ):
    stack = VGroup()
    for indices in it.combinations(list(range(n)), k):
        term = VGroup(*[
             obj1.copy() if i in indices else obj2.copy()
            for i in range(n)
        ])
        if fixed_start:
            term.add_to_back(fixed_start.copy())
        if fixed_end:
            term.add(fixed_end.copy())
        term.arrange(RIGHT, buff = obj_to_obj_buff)
        stack.add(term)
    stack.arrange(DOWN, buff = vertical_buff)
    return stack


def get_stacks(obj1, obj2, n, **kwargs):
    stacks = VGroup()
    for k in range(n+1):
        stacks.add(get_stack(obj1, obj2, n, k, **kwargs))
    stacks.arrange(
        RIGHT, 
        buff = MED_LARGE_BUFF,
        aligned_edge = DOWN
    )
    return stacks


class Male(Tex):
    CONFIG = {
        "height" : 0.4,
        "tex" : "\\male",
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Tex.__init__(self, self.tex, **kwargs)
        self.set_height(self.height)
        self.set_color(self.color)


class Female(Male):
    CONFIG = {
        "tex" : "\\female",
        "color" : MAROON_B,
    }


class PascalsTriangle(VGroup):
    CONFIG = {
        "n_rows" : 9,
        "distance" : 0.8,
        "max_width_to_distance_ratio" : 0.7,
        "angle" : 0.2*np.pi,
    }
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)

        distance = self.distance
        angle = self.angle
        max_width = self.max_width_to_distance_ratio * distance
        t_down = rotate_vector(distance*DOWN, -angle)
        t_right = 2*distance*np.sin(angle)*RIGHT

        for n in range(self.n_rows):
            row = VGroup()
            for k in range(n+1):
                num = OldTex(str(choose(n, k)))
                num.shift(n*t_down + k*t_right)
                row.add(num)
            self.add(row)
        self.center()


class IntroducePascalsTriangle(Scene):
    CONFIG = {
        "max_n" : 9,
    }
    def construct(self):
        self.show_triangle()
        self.show_sum_of_two_over_rule()
        self.keep_in_mind_what_these_mean()
        self.issolate_9_choose_4_term()
        self.show_9_choose_4_pattern()
        self.cap_off_triangle()

    def show_triangle(self):
        rows = PascalsTriangle(n_rows = self.max_n+1)
        self.play(FadeIn(rows[1]))
        for last_row, curr_row in zip(rows[1:], rows[2:]):
            self.play(*[
                Transform(
                    last_row.copy(), VGroup(*mobs),
                    remover = True
                )
                for mobs in (curr_row[1:], curr_row[:-1])
            ])
            self.add(curr_row)
        self.wait()

        self.rows = rows

    def show_sum_of_two_over_rule(self):
        rows = self.rows

        example = rows[5][3]
        ex_top1 = rows[4][2]
        ex_top2 = rows[4][3]

        rects = VGroup()
        for mob, color in (example, GREEN), (ex_top1, BLUE), (ex_top2, YELLOW):
            mob.rect = SurroundingRectangle(mob, color = color)
            rects.add(mob.rect)

        rows_to_fade = VGroup(*rows[1:4], *rows[6:])
        rows_to_fade.save_state()

        top_row = rows[4]
        low_row = rows[5]
        top_row_copy = top_row.copy()
        top_row.save_state()
        top_row.add(ex_top2.rect)
        top_row_copy.add(ex_top1.rect)
        h_line = Line(LEFT, RIGHT)
        h_line.stretch_to_fit_width(low_row.get_width() + 2)
        h_line.next_to(low_row, UP, 1.5*SMALL_BUFF)
        plus = OldTex("+")
        plus.next_to(h_line.get_left(), UP+RIGHT, buff = 1.5*SMALL_BUFF)

        self.play(ShowCreation(example.rect))
        self.play(
            ReplacementTransform(example.rect.copy(), ex_top1.rect),
            ReplacementTransform(example.rect.copy(), ex_top2.rect),
        )
        self.wait(2)
        self.play(rows_to_fade.fade, 1)
        self.play(
            top_row.align_to, low_row, LEFT,
            top_row_copy.next_to, top_row, UP,
            top_row_copy.align_to, low_row, RIGHT,
        )
        self.play(
            ShowCreation(h_line),
            Write(plus)
        )
        self.wait(2)
        for row in top_row, top_row_copy:
            row.remove(row[-1])
        self.play(
            rows_to_fade.restore,
            top_row.restore,
            Transform(
                top_row_copy, top_row.saved_state,
                remover = True
            ),
            FadeOut(VGroup(h_line, plus)),
            FadeOut(rects),
        )
        self.wait()

    def keep_in_mind_what_these_mean(self):
        morty = Mortimer().flip()
        morty.scale(0.7)
        morty.to_edge(LEFT)
        morty.shift(DOWN)

        numbers = VGroup(*it.chain(*self.rows[1:]))
        random.shuffle(numbers.submobjects)

        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, "Keep in mind \\\\ what these mean.",
            bubble_config = {
                "width" : 3.5,
                "height" : 2.5,
            }
        ))
        self.play(
            Blink(morty),
            LaggedStartMap(
                Indicate, numbers,
                rate_func = wiggle,
                color = PINK,
            )
        )
        self.play(*list(map(FadeOut, [
            morty, morty.bubble, morty.bubble.content
        ])))

    def issolate_9_choose_4_term(self):
        rows = self.rows

        for n in range(1, self.max_n+1):
            num = rows[n][0]
            line = get_stack(Female(), Male(), n, 0)[0]
            if n < self.max_n:
                line.next_to(num, LEFT)
            else:
                line.next_to(num, DOWN, MED_LARGE_BUFF)
            self.set_color_num(num)
            self.add(line)
            if n < self.max_n:
                self.wait(0.25)
            else:
                self.wait(1.25)
            self.dehighlight_num(num)
            self.remove(line)
        for k in range(1, 5):
            num = rows[self.max_n][k]
            line = get_stack(Female(), Male(), self.max_n, k)[0]
            line.next_to(num, DOWN, MED_LARGE_BUFF)
            self.set_color_num(num)
            self.add(line)
            self.wait(0.5)
            self.dehighlight_num(num)
            self.remove(line)
        num.set_color(YELLOW)
        num.scale(1.2)
        self.add(line)
        self.wait()

        self.nine_choose_four_term = num
        self.nine_choose_four_line = line

    def show_9_choose_4_pattern(self):
        rows = VGroup(*self.rows[1:])
        all_stacks = get_stacks(Female(), Male(), 9)
        stack = all_stacks[4]
        all_lines = VGroup(*it.chain(*all_stacks))

        self.play(
            rows.shift, 3*UP,
            self.nine_choose_four_line.shift, 2.5*UP,
        )
        self.remove(self.nine_choose_four_line)

        for n, line in enumerate(stack):
            line.next_to(self.nine_choose_four_term, DOWN, LARGE_BUFF)
            num = Integer(n+1)
            num.next_to(line, DOWN, MED_LARGE_BUFF)
            self.add(line, num)
            self.wait(0.1)
            self.remove(line, num)
        self.add(line, num)
        self.wait()
        self.curr_line = line

        #Probability
        expr = OldTex(
            "P(4", "\\female", "\\text{ out of }", "9", ")", "="
        )
        expr.move_to(num.get_left())
        expr.set_color_by_tex("female", MAROON_B)
        nine_choose_four_term = self.nine_choose_four_term.copy()
        nine_choose_four_term.generate_target()
        nine_choose_four_term.target.scale(1./1.2)
        over_512 = OldTex("\\quad \\over 2^9")
        frac = VGroup(nine_choose_four_term.target, over_512)
        frac.arrange(DOWN, buff = SMALL_BUFF)
        frac.next_to(expr, RIGHT, SMALL_BUFF)
        eq_result = OldTex("\\approx 0.246")
        eq_result.next_to(frac, RIGHT)

        def show_random_lines(n, wait_time = 1):
            for x in range(n):
                if x == n-1:
                    wait_time = 0
                new_line = random.choice(all_lines)
                new_line.move_to(self.curr_line)
                self.remove(self.curr_line)
                self.curr_line = new_line
                self.add(self.curr_line)
                self.wait(wait_time)

        self.play(FadeOut(num), FadeIn(expr))
        show_random_lines(4)
        self.play(
            MoveToTarget(nine_choose_four_term),
            Write(over_512)
        )
        show_random_lines(4)
        self.play(Write(eq_result))
        show_random_lines(6)
        self.play(
            self.nine_choose_four_term.scale, 1./1.2,
            self.nine_choose_four_term.set_color, WHITE,
            *list(map(FadeOut, [
                expr, nine_choose_four_term,
                over_512, eq_result, self.curr_line
            ]))
        )
        self.play(rows.shift, 3*DOWN)

    def cap_off_triangle(self):
        top_row = self.rows[0]
        circle = Circle(color = YELLOW)
        circle.replace(top_row, dim_to_match = 1)
        circle.scale(1.5)

        line_groups = VGroup()
        for n in range(4, -1, -1):
            line = VGroup(*[
                random.choice([Male, Female])()
                for k in range(n)
            ])
            if n == 0:
                line.add(Line(LEFT, RIGHT).scale(0.1).set_stroke(BLACK, 0))
            line.arrange(RIGHT, SMALL_BUFF)
            line.shift(FRAME_X_RADIUS*RIGHT/2 + FRAME_Y_RADIUS*UP/2)
            brace = Brace(line, UP)
            if n == 1:
                label = "1 Person"
            else:
                label = "%d People"%n
            brace_text = brace.get_text(label)
            line_group = VGroup(line, brace, brace_text)
            line_groups.add(line_group)

        self.play(ShowCreation(circle))
        self.play(Write(top_row))
        self.wait()
        curr_line_group = line_groups[0]
        self.play(FadeIn(curr_line_group))
        for line_group in line_groups[1:]:
            self.play(ReplacementTransform(
                curr_line_group, line_group
            ))
            curr_line_group = line_group
        self.wait()

    ###

    def set_color_num(self, num):
        num.set_color(YELLOW)
        num.scale(1.2)

    def dehighlight_num(self, num):
        num.set_color(WHITE)
        num.scale(1.0/1.2)
