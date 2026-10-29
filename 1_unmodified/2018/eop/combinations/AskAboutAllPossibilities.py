# ==============================================================================
# Scene:      AskAboutAllPossibilities
# Source:     videos/_2018/eop/combinations.py (lines 1265-1282)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutAllPossibilities.py AskAboutAllPossibilities -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class ProbabilityOfKWomenInGroupOfFive(Scene):
    CONFIG = {
        "random_seed" : 0,
        "n_people_per_lineup" : 5,
        "n_examples" : 18,
        "item_line_width" : 0.4,
    }
    def construct(self):
        self.ask_question()
        self.show_all_possibilities()
        self.stack_all_choices_by_number_of_women()
        self.go_through_stacks()
        self.remember_this_sensation()
        self.show_answer_to_question()
        self.ask_about_pattern()

    def ask_question(self):
        title = OldTexText("5 randomly chosen people")
        title.to_edge(UP)
        self.add(title)

        lineup_point = 1.5*UP
        prob_words = VGroup(*[
            OldTexText(
                "Probability of", str(n), "women?"
            ).set_color_by_tex(str(n), YELLOW)
            for n in range(self.n_people_per_lineup+1)
        ])
        prob_words.arrange(DOWN)
        prob_words.next_to(lineup_point, DOWN, MED_LARGE_BUFF)

        def get_lineup():
            lineup = self.get_random_lineup_of_men_and_women()
            lineup.scale(1.5)
            lineup.move_to(lineup_point, DOWN)
            return lineup

        last_lineup = get_lineup()
        self.play(LaggedStartMap(FadeIn, last_lineup, run_time = 1))

        for x in range(self.n_examples):
            lineup = get_lineup()
            anims = [last_lineup.items.fade, 1]
            anims += list(map(GrowFromCenter, lineup.items))
            if x >= 12 and x-12 < len(prob_words):
                anims.append(FadeIn(prob_words[x-12]))
            self.play(*anims, run_time = 0.75)
            self.remove(last_lineup)
            self.add(lineup)
            self.wait(0.25)
            last_lineup = lineup

        self.title = title
        self.prob_words = prob_words
        self.lineup = last_lineup

    def show_all_possibilities(self):
        man, woman = Male(), Female()

        vects = [
            1.5*UP,
            0.65*UP,
            0.25*UP,
            3.5*RIGHT,
            1.5*RIGHT,
        ]
        lineup_groups = VGroup()
        for k in range(6):
            lineup_group = VGroup()
            for tup in it.product(*[[woman, man]]*k):
                lineup = self.get_lineup(*list(tup) + (5-k)*[None])
                lineup.scale(1.4*(0.9)**k)
                lineup.move_to(0.5*DOWN)
                for mob, vect in zip(tup, vects):
                    if mob is woman:
                        lineup.shift(vect)
                    else:
                        lineup.shift(-vect)
                lineup_group.add(lineup)
            lineup_groups.add(lineup_group)

        n_possibilities = OldTex(
            "2 \\cdot", "2 \\cdot", "2 \\cdot", "2 \\cdot", "2",
            "\\text{ Possibilities}"
        )
        n_possibilities.next_to(self.title, DOWN)
        twos = VGroup(*n_possibilities[-2::-1])
        twos.set_color(YELLOW)
        two_anims = [
            ReplacementTransform(
                VectorizedPoint(twos[0].get_center()), 
                twos[0]
            )
        ] + [
            ReplacementTransform(t1.copy(), t2)
            for t1, t2 in zip(twos, twos[1:])
        ]

        curr_lineup_group = lineup_groups[0]
        self.play(
            ReplacementTransform(self.lineup, curr_lineup_group[0]),
            FadeOut(self.prob_words)
        )
        for i, lineup_group in enumerate(lineup_groups[1:]):
            anims = [ReplacementTransform(curr_lineup_group, lineup_group)]
            anims += two_anims[:i+1]
            if i == 0:
                anims.append(FadeIn(n_possibilities[-1]))
            self.remove(twos)
            self.play(*anims)

            men, women = VGroup(), VGroup()
            for lineup in lineup_group:
                item = lineup.items[i]
                if "female" in item.get_tex():
                    women.add(item)
                else:
                    men.add(item)
            for group in men, women:
                self.play(LaggedStartMap(
                    ApplyMethod, group,
                    lambda m : (m.shift, MED_SMALL_BUFF*RIGHT),
                    rate_func = there_and_back,
                    lag_ratio = 0.9**i,
                    run_time = 1,
                ))
            self.wait()
            curr_lineup_group = lineup_group
        self.lineups = curr_lineup_group

        eq_32 = OldTex("=", "32")
        eq_32.move_to(twos.get_right())
        eq_32.set_color_by_tex("32", YELLOW)
        self.play(
            n_possibilities[-1].next_to, eq_32, RIGHT,
            twos.next_to, eq_32, LEFT,
            FadeIn(eq_32),
        )
        self.wait()

        n_possibilities.add(*eq_32)
        self.set_variables_as_attrs(n_possibilities)

    def stack_all_choices_by_number_of_women(self):
        lineups = self.lineups
        stacks = VGroup(*[VGroup() for x in range(6)])
        for lineup in lineups:
            lineup.women = VGroup(*[m for m in lineup.items if "female" in m.get_tex()])
            stacks[len(lineup.women)].add(lineup)
        stacks.generate_target()
        stacks.target.scale(0.75)
        for stack in stacks.target:
            stack.arrange(DOWN, buff = 1.5*SMALL_BUFF)
        stacks.target.arrange(
            RIGHT, buff = MED_LARGE_BUFF, aligned_edge = DOWN
        )
        stacks.target.to_edge(DOWN)

        self.play(MoveToTarget(
            stacks, 
            run_time = 2,
            path_arc = np.pi/2
        ))
        self.wait()

        self.stacks = stacks

    def go_through_stacks(self):
        stacks = self.stacks
        n = len(stacks) - 1
        equations = VGroup()
        for k, stack in enumerate(stacks):
            items = VGroup()
            lines = VGroup()
            women = VGroup()
            for lineup in stack:
                items.add(lineup.items)
                lines.add(lineup.lines)
                for item in lineup.items:
                    if "female" in item.get_tex():
                        women.add(item)
            equation = OldTex(
                "{%d \\choose %d}"%(n, k),
                "=",
                str(len(stack))
            )
            equation[0].scale(0.6)
            equation.arrange(RIGHT, SMALL_BUFF)
            equation.set_color(YELLOW)
            equation.set_color_by_tex("=", WHITE)
            equation.next_to(stack, UP)
            equations.add(equation)

            self.play(
                items.set_fill, None, 1,
                lines.set_stroke, WHITE, 3,
                Write(equation, run_time = 1)
            )
            self.play(LaggedStartMap(Indicate, women, rate_func = there_and_back))
        self.wait()

        self.equations = equations
        self.numbers = VGroup(*[eq[-1] for eq in equations])

    def remember_this_sensation(self):
        n_possibilities = self.n_possibilities
        n_possibilities_rect = SurroundingRectangle(n_possibilities)
        twos = VGroup(*n_possibilities[:5])
        numbers = self.numbers

        self.play(ShowCreation(n_possibilities_rect))
        self.play(LaggedStartMap(
            Indicate, twos, 
            rate_func = wiggle
        ))
        self.play(FadeOut(n_possibilities_rect))
        for number in numbers:
            self.play(Indicate(number, color = PINK, run_time = 0.5))
        self.wait()

    def show_answer_to_question(self):
        stacks = self.stacks
        numbers = self.numbers
        n_possibilities = VGroup(
            self.n_possibilities[-1],
            self.n_possibilities[-3]
        )
        n_possibilities_part_to_fade = VGroup(
            self.n_possibilities[-2],
            *self.n_possibilities[:-3]
        )
        total = n_possibilities[-1]
        title = self.title
        n = self.n_people_per_lineup

        self.play(
            FadeOut(title),
            FadeOut(n_possibilities_part_to_fade),
            n_possibilities.to_corner, UP+RIGHT
        )
        for k, stack, num in zip(it.count(), stacks, numbers):
            rect = SurroundingRectangle(stack)
            num.save_state()
            prob_words = OldTex(
                "P(", "\\#", "\\female", "=", str(k), ")"
                "=", "{\\quad \\over", "32}",
                "\\approx", "%0.3f"%(choose(n, k)/32.0)
            )
            prob_words.set_color_by_tex_to_color_map({
                "female" : MAROON_B,
                "32" : YELLOW,
            })
            frac_line = prob_words.get_parts_by_tex("over")
            prob_words.to_corner(UP+LEFT)

            self.play(
                num.next_to, frac_line, UP, SMALL_BUFF,
                FadeIn(prob_words)
            )
            self.play(ShowCreation(rect))
            self.wait(2)
            self.play(
                num.restore,
                FadeOut(rect),
                FadeOut(prob_words)
            )

    def ask_about_pattern(self):
        question = OldTexText("Where do these \\\\ numbers come from?")
        question.to_edge(UP)
        numbers = self.numbers
        circles = VGroup(*[
            Circle().replace(num, dim_to_match = 1).scale(1.5)
            for num in numbers
        ])
        circles.set_color(WHITE)

        self.play(LaggedStartMap(FadeIn, question))
        self.play(LaggedStartMap(ShowCreationThenDestruction, circles))
        self.wait(2)

    ######

    def get_random_lineup_of_men_and_women(self):
        man, woman = Male(), Female()
        lineup = self.get_lineup(*[
            woman if random.choice([True, False]) else man
            for y in range(self.n_people_per_lineup)
        ])
        return lineup

    def get_lineup(self, *mobjects, **kwargs):
        buff = kwargs.get("buff", MED_SMALL_BUFF)
        lines = VGroup(*[
            Line(ORIGIN, self.item_line_width*RIGHT)
            for mob in mobjects
        ])
        lines.arrange(RIGHT, buff = buff)
        items = VGroup()
        for line, mob in zip(lines, mobjects):
            item = VectorizedPoint() if mob is None else mob.copy()
            item.next_to(line, UP, SMALL_BUFF)
            items.add(item)
        result = VGroup(lines, items)
        result.lines = lines
        result.items = items
        return result


class AskAboutAllPossibilities(ProbabilityOfKWomenInGroupOfFive):
    def construct(self):
        man, woman = Male(), Female()
        all_lineups = VGroup()
        for bits in it.product(*[[False, True]]*5):
            mobs = [
                woman.copy() if bit else man.copy()
                for bit in bits
            ]
            all_lineups.add(self.get_lineup(*mobs))
        brace = Brace(all_lineups, UP)
        question = brace.get_text("What are all possibilities?")

        self.add(brace, question)
        for lineup in all_lineups:
            self.add(lineup)
            self.wait(0.25)
            self.remove(lineup)
