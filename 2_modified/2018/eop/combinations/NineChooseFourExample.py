# ==============================================================================
# Scene:      NineChooseFourExample
# Source:     videos/_2018/eop/combinations.py (lines 3001-3156)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NineChooseFourExample.py NineChooseFourExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL OldTex/OldTexText keep "\\{ \\}" as one piece: build the two braces from separate strings so "lb, rb = braces" unpacks (Cairo split glyphs)
#   - ApplyMethod(mob.scale, f, point): GL scale() takes the point as about_point, not as 2nd positional argument; pass {"about_point": point}
#   - slice indices use // instead of / (Python 2 integer division)
#   - in play(): last_ones.restore listed before ones.set_color (the 2018 method-merge in Scene.play swallowed a trailing restore as an argument of set_color, so it never ran)
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


class InitialFiveChooseThreeExample(Scene):
    CONFIG = {
        "n" : 5,
        "zero_color" : BLUE,
        "one_color" : PINK,
    }
    def construct(self):
        self.show_all_stacks()
        self.add_title()
        self.show_binomial_name()
        self.issolate_single_stack()
        self.count_chosen_stack()
        self.count_ways_to_fill_slots()
        self.walk_though_notation()
        self.emphasize_pattern_over_number()

    def show_all_stacks(self):
        stacks = get_stacks(
            self.get_obj1(), self.get_obj2(), self.n,
            vertical_buff = SMALL_BUFF
        )
        stacks.to_edge(DOWN, buff = MED_LARGE_BUFF)

        for stack in stacks:
            self.play(FadeIn(
                stack, 
                run_time = 0.2*len(stack),
                lag_ratio = 0.5
            ))
        self.wait()

        self.set_variables_as_attrs(stacks)

    def add_title(self):
        n = self.n
        stacks = self.stacks

        n_choose_k = OldTex("n \\choose k")
        n_choose_k_words = OldTexText("``n choose k''")
        nCk_group = VGroup(n_choose_k, n_choose_k_words)
        nCk_group.arrange(RIGHT)
        nCk_group.to_edge(UP)

        binomials = VGroup(*[
            OldTex("%d \\choose %d"%(n, k))
            for k in range(n+1)
        ])
        binomial_equations = VGroup()
        for k, binomial in enumerate(binomials):
            binomial.scale(0.75)
            number = OldTex(str(choose(n, k)))
            equation = VGroup(binomial, OldTex("="), number)
            equation.arrange(RIGHT, buff = SMALL_BUFF)
            equation.set_color(YELLOW)
            equation[1].set_color(WHITE)
            binomial_equations.add(equation)

        for stack, eq in zip(stacks, binomial_equations):
            eq.set_width(0.9*stack.get_width())
            eq.next_to(stack, UP)

        mover = VGroup()
        for eq in binomial_equations:
            point = VectorizedPoint(n_choose_k.get_center())
            group = VGroup(n_choose_k, point, point).copy()
            group.target = eq
            mover.add(group)

        self.play(FadeIn(nCk_group))
        self.play(LaggedStartMap(
            MoveToTarget, mover,
            run_time = 3,
        ))
        self.remove(mover)
        self.add(binomial_equations)
        self.wait()

        self.set_variables_as_attrs(
            n_choose_k, n_choose_k_words,
            binomial_equations
        )

    def show_binomial_name(self):
        new_words = OldTexText("``Binomial coefficients''")
        new_words.move_to(self.n_choose_k_words, LEFT)

        self.play(Transform(self.n_choose_k_words, new_words))
        self.wait(2)

    def issolate_single_stack(self):
        stack = self.stacks[3]
        equation = self.binomial_equations[3]

        to_fade = VGroup(*self.stacks)
        to_fade.add(*self.binomial_equations)
        to_fade.add(self.n_choose_k, self.n_choose_k_words)
        to_fade.remove(stack, equation)

        self.play(
            FadeOut(to_fade),
            # CHANGE: GL scale() takes the point as about_point (Cairo took it positionally)
            equation.scale, 1.5, {"about_point": equation.get_bottom()},
        )
        self.wait()
        for line in stack:
            ones = VGroup(*[mob for mob in line if "1" in mob.get_tex()])
            line.ones = ones
            self.play(LaggedStartMap(
                ApplyMethod, ones,
                lambda mob : (mob.set_color, YELLOW),
                rate_func = there_and_back,
                lag_ratio = 0.7,
                run_time = 1,
            ))

    def count_chosen_stack(self):
        stack = self.stacks[3]
        for i, line in enumerate(stack):
            number = OldTex(str(i+1))
            number.next_to(stack, LEFT)
            brace = Brace(VGroup(*stack[:i+1]), LEFT)
            number.next_to(brace, LEFT)
            line.save_state()
            line.set_color(YELLOW)
            self.add(number, brace)
            self.wait(0.25)
            self.remove(number, brace)
            line.restore()
        self.add(number, brace)
        self.wait()

        self.set_variables_as_attrs(
            stack_brace = brace,
            stack_count = number
        )

    def count_ways_to_fill_slots(self):
        lines = VGroup(*[Line(ORIGIN, 0.25*RIGHT) for x in range(5)])
        lines.arrange(RIGHT)
        lines.next_to(self.stacks[3], LEFT, LARGE_BUFF, UP)

        self.play(ShowCreation(lines))
        count = 1
        for indices in it.combinations(list(range(5)), 3):
            ones = VGroup(*[
                self.get_obj1().next_to(lines[i], UP)
                for i in indices
            ])
            num = OldTex(str(count))
            num.next_to(lines, DOWN)
            self.add(ones, num)
            self.wait(0.35)
            self.remove(ones, num)
            count += 1
        self.add(num, ones)
        self.wait()
        self.play(*list(map(FadeOut, [lines, num, ones])))

    def walk_though_notation(self):
        equation = self.binomial_equations[3]
        rect = SurroundingRectangle(equation[0])
        rect.set_color(WHITE)
        words = OldTexText("``5 choose 3''")
        words.next_to(rect, UP)

        self.play(Write(words))
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.wait(2)

    def emphasize_pattern_over_number(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        words = OldTexText("Remember the pattern \\\\ not the number")
        words.next_to(morty, UP)
        words.shift_onto_screen()

        self.play(FadeIn(morty))
        self.play(
            morty.change, "speaking",
            Write(words, run_time = 2)
        )
        self.play(
            Blink(morty),
            morty.change, "happy"
        )
        self.revert_to_original_skipping_status()
        last_ones = VGroup()
        last_ones.save_state()
        for x in range(2):
            for line in self.stacks[3]:
                ones = line.ones
                ones.save_state()
                # CHANGE: last_ones.restore moved first: the CL18-D play() method merge treats a trailing restore as an argument of the previous method
                self.play(
                    last_ones.restore,
                    ones.set_color, YELLOW,
                    morty.look_at, ones,
                    run_time = 0.25
                )
                last_ones = ones
            self.wait()

    ####

    def get_obj1(self):
        return OldTex("1").set_color(self.one_color)

    def get_obj2(self):
        return OldTex("0").set_color(self.zero_color)


class ChooseThreeFromFive(InitialFiveChooseThreeExample, PiCreatureScene):
    CONFIG = {
        "n" : 5,
        "k" : 3,
        "pi_creature_scale_val" : 0.3,
        "people_colors" : [
             PURPLE, BLUE, GREEN, GOLD_E, GREY,
        ],
    }
    def construct(self):
        self.remove(self.people)
        self.show_binary_strings()
        self.add_people()
        self.choose_triplets()
        self.show_association_with_binary(3)
        self.show_association_with_binary(5)
        self.order_doesnt_matter()
        self.that_phrase_is_confusing()
        self.pattern_is_unambiguous()

    def show_binary_strings(self):
        n, k = self.n, self.k
        stack = get_stack(
            self.get_obj1(), self.get_obj2(), n, k,
            vertical_buff = SMALL_BUFF,
        )
        stack.to_edge(DOWN, buff = LARGE_BUFF)
        equation = OldTex(
            "{%d \\choose %d}"%(n, k),
            "=", str(choose(n, k)),
        )
        equation[0].scale(0.75, about_point = equation[0].get_right())
        equation.next_to(stack, UP)

        for i, line in enumerate(stack):
            num = OldTex(str(i+1))
            num.next_to(stack, UP)
            self.add(line, num)
            self.wait(0.25)
            self.remove(num)
        self.play(
            Write(VGroup(*equation[:-1])),
            ReplacementTransform(num, equation[-1])
        )
        self.wait()

        self.set_variables_as_attrs(stack, equation)

    def add_people(self):
        people = self.people

        names = self.get_names(people)
        braces = self.get_people_braces(people)

        self.play(
            Write(braces),
            LaggedStartMap(FadeIn, people),
            VGroup(self.stack, self.equation).to_edge, RIGHT, LARGE_BUFF
        )
        self.play(LaggedStartMap(FadeIn, names))

        self.set_variables_as_attrs(names, braces)

    def choose_triplets(self):
        movers = VGroup()
        movers.generate_target()
        max_name_width = max([n.get_width() for n in self.names])
        for name_triplet in it.combinations(self.names, 3):
            mover = VGroup(*name_triplet).copy()
            mover.generate_target()
            if hasattr(self, "stack"):
                mover.target.set_height(self.stack[0].get_height())
            for name in mover.target[:2]:
                name[-1].set_fill(opacity = 1)
            mover.target.arrange(RIGHT, MED_SMALL_BUFF)
            movers.add(mover)
            movers.target.add(mover.target)
        movers.target.arrange(
            DOWN, buff = SMALL_BUFF,
            aligned_edge = LEFT,
        )
        movers.target.next_to(self.people, DOWN, MED_LARGE_BUFF)
        if hasattr(self, "stack"):
            movers.target.align_to(self.stack, UP)

        self.play(LaggedStartMap(
            MoveToTarget, movers,
            lag_ratio = 0.2,
            run_time = 4,
        ))
        self.wait()

        self.name_triplets = movers
        
    def show_association_with_binary(self, index):
        people = self.people
        names = self.names
        for mob in people, names:
            mob.save_state()
            mob.generate_target()

        line = self.stack[index].copy()
        triplet = self.name_triplets[index]
        triplet.save_state()
        line.generate_target()
        for bit, name in zip(line.target, self.names):
            bit.next_to(name, UP)

        line_rect = SurroundingRectangle(line)
        full_line_rect = SurroundingRectangle(VGroup(line, triplet))
        people_rects = VGroup()
        for pi, name, obj in zip(people.target, names.target, line):
            if "1" in obj.get_tex():
                rect = SurroundingRectangle(VGroup(pi, name))
                people_rects.add(rect)
                pi.change_mode("hooray")
            else:
                pi.fade(0.5)
                name.fade(0.5)

        self.play(ShowCreation(line_rect))
        self.play(MoveToTarget(line))
        self.play(
            LaggedStartMap(ShowCreation, people_rects),
            MoveToTarget(people),
            MoveToTarget(names),
        )
        self.wait()
        self.play(
            ReplacementTransform(line_rect, full_line_rect),
            triplet.set_color, YELLOW
        )
        self.wait(2)
        self.play(
            people.restore,
            names.restore,
            triplet.restore,
            FadeOut(line),
            FadeOut(full_line_rect),
            FadeOut(people_rects),
        )

    def order_doesnt_matter(self):
        triplet = self.name_triplets[0].copy()
        triplet.set_fill(opacity = 1)
        triplet.next_to(
            self.name_triplets, RIGHT,
            buff = LARGE_BUFF,
            aligned_edge = UP,
        )
        updownarrow = OldTex("\\Updownarrow")
        updownarrow.set_color(YELLOW)
        updownarrow.next_to(triplet, DOWN, SMALL_BUFF)
        permutations = VGroup()
        for indices in it.permutations(list(range(len(triplet)))):
            perm = triplet.copy()
            resorter = VGroup(*[
                perm[i] for i in indices
            ])
            resorter.arrange(RIGHT, MED_SMALL_BUFF)
            resorter.next_to(updownarrow, DOWN)
            permutations.add(perm)

        words = OldTexText("``Order doesn't matter''")
        words.scale(0.75)
        words.set_color(BLUE)
        words.next_to(permutations, DOWN)

        self.play(ReplacementTransform(
            self.name_triplets[0].copy(), triplet
        ))
        curr_perm = permutations[0]
        self.play(
            ReplacementTransform(triplet.copy(), curr_perm),
            Write(updownarrow)
        )
        for i in range(8):
            new_perm = permutations[i%(len(permutations)-1)+1]
            anims = [
                Transform(
                    curr_perm, new_perm,
                    path_arc = np.pi,
                )
            ]
            if i == 1:
                self.wait()
            if i == 4:
                anims.append(Write(words, run_time = 1))
            self.play(*anims)
        self.play(*list(map(FadeOut, [triplet, curr_perm, updownarrow])))

        self.order_doesnt_matter_words = words

    def that_phrase_is_confusing(self):
        odm_words = self.order_doesnt_matter_words
        odm_words_outline = VGroup()
        for letter in odm_words:
            mob = VMobject()
            mob.set_points(letter.get_points())
            odm_words_outline.add(mob)
        odm_words_outline.set_fill(opacity = 0)
        odm_words_outline.set_stroke(YELLOW, 1)

        line = self.stack[0].copy()

        q_marks = OldTexText("???")
        q_marks.next_to(odm_words, DOWN)
        q_marks.set_color(YELLOW)

        self.play(
            LaggedStartMap(
                ShowCreationThenDestruction, odm_words_outline,
                lag_ratio = 0.2,
                run_time = 1,
            ),
            LaggedStartMap(
                ApplyMethod, self.people,
                lambda pi : (pi.change, "confused", odm_words,)
            ),
            LaggedStartMap(FadeIn, q_marks),
        )
        self.play(line.next_to, odm_words, UP)
        for x in range(6):
            line.generate_target()
            resorter = VGroup(*line.target)
            resorter.sort(lambda p : random.random())
            resorter.arrange(RIGHT, buff = SMALL_BUFF)
            resorter.move_to(line)
            self.play(MoveToTarget(line, path_arc = np.pi))
        self.play(FadeOut(q_marks))

        line.sort(lambda p : p[0])
        words = VGroup(*list(map(TexText, ["First", "Second", "Fifth"])))
        words.set_color(YELLOW)
        words.scale(0.75)
        word_arrow_groups = VGroup()
        for i, word in zip([0, 1, 4], words):
            arrow = Vector(0.5*DOWN)
            arrow.set_color(YELLOW)
            arrow.next_to(line[i], UP, SMALL_BUFF)
            word.next_to(arrow, UP, SMALL_BUFF)
            word_arrow_groups.add(VGroup(word, arrow))

        for x in range(2):
            for i in range(len(word_arrow_groups)+1):
                anims = []
                if i > 0:
                    anims.append(FadeOut(word_arrow_groups[i-1]))
                if i < len(word_arrow_groups):
                    anims.append(FadeIn(word_arrow_groups[i]))
                self.play(*anims)
            self.wait()
            word_arrow_groups.submobjects = [
                word_arrow_groups[j]
                for j in (1, 2, 0)
            ]
        self.play(*list(map(FadeOut, [line, odm_words])))

    def pattern_is_unambiguous(self):
        all_ones = VGroup()
        for line in self.stack:
            ones = VGroup(*[m for m in line if "1" in m.get_tex()]).copy()
            ones.set_color(YELLOW)
            all_ones.add(ones)

        self.play(
            LaggedStartMap(
                FadeIn, all_ones,
                lag_ratio = 0.2,
                run_time = 3,
                rate_func = there_and_back
            ),
            LaggedStartMap(
                ApplyMethod, self.people,
                lambda pi : (pi.change, "happy", ones),
            )
        )
        self.wait()
        for trip in it.combinations(self.people, 3):
            rects = VGroup(*list(map(SurroundingRectangle, trip)))
            self.add(rects)
            self.wait(0.3)
            self.remove(rects)
        self.wait()

    ###

    def create_pi_creatures(self):
        people = VGroup(*[
            PiCreature(color = color).scale(self.pi_creature_scale_val)
            for color in self.people_colors
        ])
        people.arrange(RIGHT)
        people.shift(3*LEFT)
        people.to_edge(UP, buff = 1.25)
        self.people = people
        return people

    def get_names(self, people):
        names = VGroup(*[
            OldTexText(name + ",")
            for name in ("Ali", "Ben", "Cam", "Denis", "Evan")
        ])
        for name, pi in zip(names, people):
            name[-1].set_fill(opacity = 0)
            name.scale(0.75)
            name.next_to(pi, UP, 2*SMALL_BUFF)
            pi.name = name
        return names

    def get_people_braces(self, people):
        group = VGroup(people, *[pi.name for pi in people])
        # CHANGE: GL keeps "\{ \}" as a single piece; build the two braces from separate strings so lb, rb unpack as in Cairo
        lb, rb = braces = OldTex("\\{", "\\}")
        braces.scale(2)
        braces.stretch_to_fit_height(1.3*group.get_height())
        lb.next_to(group, LEFT, SMALL_BUFF)
        rb.next_to(group, RIGHT, SMALL_BUFF)
        return braces


class HowToComputeNChooseK(ChooseThreeFromFive):
    CONFIG = {
        "n" : 5,
        "k" : 3,
        "line_colors" : [GREEN, YELLOW],
        "n_permutaitons_to_show" : 5,
    }
    def construct(self):
        self.force_skipping()

        self.setup_people()
        self.choose_example_ordered_triplets()
        self.count_possibilities()
        self.show_permutations_of_ABC()
        self.count_permutations_of_ABC()
        self.reset_stage()
        self.show_whats_being_counted()

        self.revert_to_original_skipping_status()
        self.indicate_final_answer()

    def setup_people(self):
        people = self.people
        names = self.get_names(people)
        braces = self.get_people_braces(people)
        people_group = VGroup(people, names, braces)
        people_group.center().to_edge(UP, buff = MED_LARGE_BUFF)

        self.add(people_group)
        self.set_variables_as_attrs(
            names, people_group,
            people_braces = braces
        )

    def choose_example_ordered_triplets(self):
        n, k = self.n, self.k
        names = self.names

        lines, place_words = self.get_lines_and_place_words()

        for x in range(3):
            chosen_names = VGroup(*random.sample(names, k))
            chosen_names.save_state()
            for name, line, word in zip(chosen_names, lines, place_words):
                name.generate_target()
                name.target.next_to(line, UP, SMALL_BUFF)
                anims = [MoveToTarget(name)]
                if x == 0:
                    anims += [ShowCreation(line), FadeIn(word)]
                self.play(*anims)
            self.wait()
            self.play(chosen_names.restore)
        self.wait()

        self.set_variables_as_attrs(lines, place_words)

    def count_possibilities(self):
        n, k = self.n, self.k
        lines = self.lines

        choice_counts = self.get_choice_counts(n, k)
        arrows = self.get_choice_count_arrows(choice_counts)

        name_rects = VGroup()
        for name in self.names:
            name.rect = SurroundingRectangle(name)
            name_rects.add(name.rect)

        chosen_names = VGroup(*random.sample(self.names, k))
        self.names.save_state()

        for name, line, count, arrow in zip(chosen_names, lines, choice_counts, arrows):
            self.play(
                FadeIn(count),
                LaggedStartMap(
                    FadeIn, name_rects,
                    rate_func = there_and_back,
                    remover = True,
                )
            )
            self.play(
                name.next_to, line, UP, SMALL_BUFF,
                GrowArrow(arrow)
            )
            self.wait()

            name_rects.remove(name.rect)
            name_rects.set_stroke(YELLOW, 3)

        #Consolidate choice counts
        choice_numbers = VGroup(*[
            cc.submobjects.pop(1) 
            for cc in choice_counts
        ])
        choice_numbers.generate_target()
        dots = VGroup(*[Tex("\\cdot") for x in range(k-1)])
        product = VGroup(*it.chain(*list(zip(choice_numbers.target, dots))))
        product.add(choice_numbers.target[-1])
        product.arrange(RIGHT, buff = SMALL_BUFF)
        chosen_names_brace = Brace(chosen_names, UP)
        product.next_to(chosen_names_brace, UP)

        self.play(
            FadeOut(choice_counts),
            FadeOut(arrows),
            MoveToTarget(choice_numbers),
            Write(dots),
            GrowFromCenter(chosen_names_brace),
        )
        self.wait()

        self.set_variables_as_attrs(
            chosen_names, chosen_names_brace, choice_numbers,
            choice_numbers_dots = dots,
        )

    def show_permutations_of_ABC(self):
        chosen_names = self.chosen_names
        lines = self.lines

        n_perms = self.n_permutaitons_to_show + 1
        for indices in list(it.permutations(list(range(3))))[1:n_perms]:
            self.play(*[
                ApplyMethod(
                    name.next_to, lines[i], UP, SMALL_BUFF,
                    path_arc = np.pi
                )
                for i, name in zip(indices, chosen_names)
            ])
            self.wait(0.5)

    def count_permutations_of_ABC(self):
        n, k = self.n, self.k
        lines = self.lines

        chosen_names = self.chosen_names
        brace = self.chosen_names_brace
        numerator = VGroup(
            self.choice_numbers, self.choice_numbers_dots,
        )
        frac_line = Line(LEFT, RIGHT)
        frac_line.replace(numerator, dim_to_match = 0)
        frac_line.to_edge(RIGHT)

        choice_counts = self.get_choice_counts(k, k)
        arrows = self.get_choice_count_arrows(choice_counts)

        self.play(
            chosen_names.shift, UP,
            chosen_names.to_edge, LEFT,
            numerator.next_to, frac_line, UP, SMALL_BUFF,
            FadeOut(brace),
        )
        shuffled_names = random.sample(chosen_names, k)
        for line, name, count, arrow in zip(lines, shuffled_names, choice_counts, arrows):
            self.play(FadeIn(count), GrowArrow(arrow))
            self.play(
                name.next_to, line, UP, SMALL_BUFF,
                path_arc = -np.pi/3,
            )
            self.wait()

        #Consolidate choice counts
        choice_numbers = VGroup(*[
            cc.submobjects.pop(1) 
            for cc in choice_counts
        ])
        choice_numbers.generate_target()
        dots = VGroup(*[Tex("\\cdot") for x in range(k-1)])
        product = VGroup(*it.chain(*list(zip(choice_numbers.target, dots))))
        product.add(choice_numbers.target[-1])
        product.arrange(RIGHT, buff = SMALL_BUFF)
        product.next_to(frac_line, DOWN, SMALL_BUFF)

        self.play(
            FadeOut(choice_counts),
            FadeOut(arrows),
            MoveToTarget(choice_numbers),
            Write(dots),
            ShowCreation(frac_line),
        )
        self.wait()

        self.fraction = VGroup(
            numerator, frac_line, VGroup(choice_numbers, dots)
        )

    def reset_stage(self):
        n, k = self.n, self.k
        n_choose_k_equals = OldTex(
            "{%d \\choose %d} ="%(n, k)
        )
        n_choose_k_equals.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        n_choose_k_equals.to_edge(UP, LARGE_BUFF)

        self.play(
            self.names.restore,
            FadeOut(self.lines),
            FadeOut(self.place_words),
        )
        self.play(
            self.people_group.to_edge, LEFT,
            FadeIn(n_choose_k_equals),
            self.fraction.next_to, n_choose_k_equals, RIGHT, SMALL_BUFF
        )

    def show_whats_being_counted(self):
        n, k = self.n, self.k
        letters = VGroup(*[name[0] for name in self.names])

        rhs = OldTex("=", "{60", "\\over", "6}")
        rhs.next_to(self.fraction, RIGHT)

        all_groups = VGroup()
        lines = VGroup()
        for ordered_triplet in it.combinations(letters, k):
            line = VGroup()
            for triplet in it.permutations(ordered_triplet):
                group = VGroup(*triplet).copy()
                group.save_state()
                group.arrange(RIGHT, buff = SMALL_BUFF)
                line.add(group)
                all_groups.add(group)
            line.arrange(RIGHT, buff = LARGE_BUFF)
            lines.add(line)
        lines.arrange(DOWN)
        lines.scale(0.8)
        lines.to_edge(DOWN)
        rects = VGroup(*[
            SurroundingRectangle(
                line, buff = 0,
                stroke_width = 0,
                fill_color = BLUE,
                fill_opacity = 0.5,
            )
            for line in lines
        ])

        self.play(
            Write(VGroup(*rhs[:-1])),
            LaggedStartMap(
                ApplyMethod, all_groups,
                lambda g : (g.restore,),
                rate_func = lambda t : smooth(1-t),
                run_time = 4,
                lag_ratio = 0.2,
            ),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, rects),
            Write(rhs[-1])
        )
        self.wait()

        self.ordered_triplets = lines
        self.triplet_group_rects = rects
        self.rhs = rhs

    def indicate_final_answer(self):
        ordered_triplets = self.ordered_triplets
        rects = self.triplet_group_rects
        fraction = VGroup(*self.rhs[1:])
        frac_rect = SurroundingRectangle(fraction)

        brace = Brace(rects, LEFT)
        brace_tex = brace.get_tex("10")

        self.play(FocusOn(fraction))
        self.play(ShowCreation(frac_rect))
        self.play(FadeOut(frac_rect))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(brace_tex),
        )
        self.wait()


    ####

    def get_choice_counts(self, n, k):
        people_braces = self.people_braces
        choice_counts = VGroup(*[
            OldTexText(
                "(", str(n0), " choices", ")",
                arg_separator = ""
            )
            for n0 in range(n, n-k, -1)
        ])
        choice_counts.arrange(RIGHT, buff = SMALL_BUFF)
        choice_counts.set_color_by_gradient(*self.line_colors)
        choice_counts.next_to(people_braces, DOWN)
        return choice_counts

    def get_choice_count_arrows(self, choice_counts):
        lines = self.lines
        return VGroup(*[
            Arrow(
                count.get_bottom(), 
                line.get_center() + MED_LARGE_BUFF*UP,
                color = line.get_color()
            )
            for count, line in zip(choice_counts, lines)
        ])

    def get_lines_and_place_words(self):
        n, k = self.n, self.k
        width = max([n.get_width() for n in self.names]) + MED_SMALL_BUFF
        lines = VGroup(*[
            Line(ORIGIN, width*RIGHT)
            for x in range(k)
        ])
        lines.arrange(RIGHT)
        lines.next_to(ORIGIN, DOWN, buff = LARGE_BUFF)
        place_words = VGroup(*[
            OldTex("%d^\\text{%s}"%(i+1, s))
            for i, s in zip(
                list(range(k)), 
                it.chain(["st", "nd", "rd"], it.repeat("th"))
            )
        ])
        for mob in place_words, lines:
            mob.set_color_by_gradient(*self.line_colors)
        for word, line in zip(place_words, lines):
            word.next_to(line, DOWN, SMALL_BUFF)

        self.set_variables_as_attrs(lines, place_words)
        return lines, place_words


class NineChooseFourExample(HowToComputeNChooseK):
    CONFIG = {
        "random_seed" : 2,
        "n" : 9,
        "k" : 4,
        "line_colors" : [RED, MAROON_B],
        "n_permutaitons_to_show" : 3,
    }
    def construct(self):
        self.setup_people()
        self.show_n_choose_k()
        self.show_n_choose_k_pattern()
        self.choose_k_people()
        self.count_how_to_choose_k()
        self.show_permutations()
        self.finish_computation()

    def setup_people(self):
        self.remove(self.people)
        self.people = OldTexText(" ".join([
            chr(ord('A') + i )
            for i in range(self.n)
        ]))
        self.people.set_color_by_gradient(BLUE, YELLOW)
        self.names = self.people
        self.people.to_edge(UP, buff = LARGE_BUFF + MED_SMALL_BUFF)
        # CHANGE: GL keeps "\{ \}" as a single piece; build the two braces from separate strings so lb, rb unpack as in Cairo
        lb, rb = braces = OldTexText("\\{", "\\}")
        braces.scale(1.5)
        lb.next_to(self.people, LEFT, SMALL_BUFF)
        rb.next_to(self.people, RIGHT, SMALL_BUFF)

        self.people_group = VGroup(braces, self.people)
        self.people_braces = braces

    def show_n_choose_k(self):
        n, k = self.n, self.k
        n_choose_k = OldTex("{%d \\choose %d}"%(n, k))
        n_choose_k.to_corner(UP + LEFT)
        self.play(FadeIn(n_choose_k))
        self.set_variables_as_attrs(n_choose_k)

    def show_n_choose_k_pattern(self):
        n, k = self.n, self.k
        stack = get_stack(
            OldTex("1").set_color(PINK),
            OldTex("0").set_color(BLUE),
            n, k
        )
        l = len(stack)
        n_stacks = 6
        columns = VGroup(*[
            # CHANGE: Python 2 integer division in slice indices; use // (Python 3)
            VGroup(*stack[(i*l)//n_stacks:((i+1)*l)//n_stacks])
            for i in range(n_stacks)
        ])
        columns.arrange(
            RIGHT, 
            aligned_edge = UP,
            buff = MED_LARGE_BUFF
        )
        columns.set_height(7)
        columns.to_corner(DOWN + RIGHT)

        for line in stack:
            self.play(FadeIn(line, run_time = 0.1))
        self.wait(2)
        self.play(FadeOut(
            stack, lag_ratio = 0.5, run_time = 2
        ))

    def choose_k_people(self):
        n, k = self.n, self.k
        people = self.people
        braces = self.people_braces

        n_items = OldTexText("%d items"%n)
        choose_k = OldTexText("choose %d"%k)
        n_items.next_to(people, UP, buff = MED_LARGE_BUFF)
        choose_k.next_to(people, DOWN, buff = LARGE_BUFF)

        chosen_subset = VGroup(*random.sample(people, k))

        self.play(
            Write(braces),
            LaggedStartMap(FadeIn, people, run_time = 1),
            FadeIn(n_items),
        )
        self.wait()
        self.play(
            FadeIn(choose_k),
            LaggedStartMap(
                ApplyMethod, chosen_subset,
                lambda m : (m.shift, MED_LARGE_BUFF*DOWN)
            )
        )
        self.wait()
        self.play(
            chosen_subset.shift, MED_LARGE_BUFF*UP,
            n_items.next_to, n_items.get_center(), LEFT,
            choose_k.next_to, n_items.get_center(), RIGHT,
        )

    def count_how_to_choose_k(self):
        lines, place_words = self.get_lines_and_place_words()
        self.play(
            LaggedStartMap(FadeIn, lines),
            LaggedStartMap(FadeIn, place_words),
            run_time = 1
        )
        self.count_possibilities()

    def show_permutations(self):
        self.show_permutations_of_ABC()
        self.count_permutations_of_ABC()

    def finish_computation(self):
        equals = OldTex("=")
        equals.shift(2*LEFT)
        fraction = self.fraction
        six = fraction[0][0][3]
        eight = fraction[0][0][1]
        two_three = VGroup(*fraction[2][0][1:3])
        four = fraction[2][0][0]

        rhs = OldTex("= 9 \\cdot 2 \\cdot 7 = 126")

        self.play(
            self.names.restore,
            FadeOut(self.lines),
            FadeOut(self.place_words),
            self.n_choose_k.next_to, equals, LEFT,
            self.fraction.next_to, equals, RIGHT,
            FadeIn(equals),
        )
        self.wait()

        for mob in six, eight, two_three, four:
            mob.cross = Cross(mob)
            mob.cross.set_stroke("red", 5)
        two = OldTex("2")
        two.set_color(eight.get_fill_color())
        two.next_to(eight, UP)
        rhs.next_to(fraction, RIGHT)

        self.play(
            ShowCreation(six.cross),
            ShowCreation(two_three.cross),
        )
        self.wait()
        self.play(
            ShowCreation(eight.cross),
            ShowCreation(four.cross),
            FadeIn(two)
        )
        self.wait()
        self.play(Write(rhs))
        self.wait()
