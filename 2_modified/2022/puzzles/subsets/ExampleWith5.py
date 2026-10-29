# ==============================================================================
# Scene:      ExampleWith5
# Source:     videos/_2022/puzzles/subsets.py (lines 860-1498)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExampleWith5.py ExampleWith5 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_subsets(range(1,26)) stored the 2^25 subsets in a list (SIGKILL for memory); they are filtered lazily with combinations, same order
# ==============================================================================

from manim_imports_ext import *

def get_set_tex(values, max_shown=7, **kwargs):
    if len(values) > max_shown:
        value_mobs = [
            *map(Integer, values[:max_shown - 2]),
            Tex("\\dots"),
            Integer(values[-1], group_with_commas=False),
        ]
    else:
        value_mobs = list(map(Integer, values))

    commas = Tex(",").replicate(len(value_mobs) - 1)
    result = VGroup()
    result.add(Tex("\\{"))
    result.add(*it.chain(*zip(value_mobs, commas)))
    if len(value_mobs) > 0:
        result.add(value_mobs[-1].align_to(value_mobs[0], UP))
    result.add(Tex("\\}"))
    result.arrange(RIGHT, buff=SMALL_BUFF)
    if len(values) > 0:
        commas.set_y(value_mobs[0].get_y(DOWN))
    if len(values) > max_shown:
        result[-4].match_y(commas)
    result.values = values
    return result


def get_part_by_value(set_tex, value):
    try:
        return next(sm for sm in set_tex if isinstance(sm, Integer) and sm.get_value() == value)
    except StopIteration:
        return VMobject().move_to(set_tex)


def get_brackets(set_tex):
    return VGroup(set_tex[0], set_tex[-1])


def get_integer_parts(set_tex):
    result = VGroup(*(
        sm for sm in set_tex
        if isinstance(sm, Integer)
    ))
    if len(result) == 0:
        result.move_to(set_tex)
    return result


def set_tex_transform(set_tex1, set_tex2):
    bracket_anim = TransformFromCopy(
        get_brackets(set_tex1),
        get_brackets(set_tex2),
    )
    matching_anims = [
        TransformFromCopy(
            get_part_by_value(set_tex1, value),
            get_part_by_value(set_tex2, value),
        )
        for value in filter(
            lambda v: v in set_tex2.values,
            set_tex1.values,
        )
    ]
    mismatch_animations = [
        FadeInFromPoint(
            get_part_by_value(set_tex2, value),
            set_tex1.get_center()
        )
        for value in set(set_tex2.values).difference(set_tex1.values)
    ]
    anims = [bracket_anim, *matching_anims, *mismatch_animations]
    if len(set_tex2.values) > 1:
        commas = []
        for st in set_tex1, set_tex2:
            if len(st.values) > 1:
                commas.append(st[2:-1:2])
            else:
                commas.append(Tex(",").set_opacity(0).move_to(st, DOWN))
        comma_animations = TransformFromCopy(*commas)
        anims.append(comma_animations)
    for part in set_tex2:
        if isinstance(part, Tex) and part.get_tex() == "\\dots":
            anims.append(FadeInFromPoint(part, set_tex1.get_bottom()))
    return AnimationGroup(*anims)


def get_sum_group(set_tex, sum_color=YELLOW):
    height = set_tex.get_height()
    buff = 0.75 * height
    arrow = Vector(height * RIGHT)
    arrow.next_to(set_tex, RIGHT, buff=buff)
    sum_value = Integer(sum(set_tex.values))
    sum_value.set_color(sum_color)
    sum_value.set_height(0.66 * height)
    sum_value.next_to(arrow, RIGHT, buff=buff)

    return VGroup(arrow, sum_value)


def get_sum_animation(set_tex, sum_group, path_arc=-10 * DEGREES):
    arrow, sum_value = sum_group

    return AnimationGroup(
        GrowArrow(arrow),
        FadeTransform(
            get_integer_parts(set_tex).copy(),
            sum_value,
            path_arc=path_arc,
        ),
    )


def get_subsets(full_set):
    return list(it.chain(*(
        it.combinations(full_set, k)
        for k in range(len(full_set) + 1)
    )))


class ExampleWith5(InteractiveScene):
    elem_colors = color_gradient([BLUE_B, BLUE_D], 5)

    def construct(self):
        # Add full set
        N = 5
        full_set = list(range(1, N + 1))
        set_tex = get_set_tex(full_set)
        set_tex.to_edge(UP)
        self.add(set_tex)
        self.wait()

        # Construct all subsets
        subsets = self.construct_all_subsets(set_tex)

        # Show n choose k stacks
        stacks = self.get_subset_stacks(full_set)

        anims = []
        for stack in stacks:
            for new_subset in stack:
                for subset in subsets:
                    if set(subset.values) == set(new_subset.values):
                        anims.append(FadeTransform(subset, new_subset))

        self.play(LaggedStart(*anims, lag_ratio=0.05))
        self.wait()

        # Show their sums
        sum_stacks = self.get_subset_sums(stacks)
        covered_sums = []
        n_selections = 6
        for n in range(n_selections):
            self.wait(note=f"Example sum {n + 1} / {n_selections}")
            # Show sum based on what's in self.selection
            anims = []
            for stack, sum_stack in zip(stacks, sum_stacks):
                for subset, sum_mob in zip(stack, sum_stack):
                    if set(subset.get_family()).intersection(self.selection.get_family()):
                        if sum_mob not in covered_sums:
                            covered_sums.append(sum_mob)
                            anims.append(get_sum_animation(subset, sum_mob))
            self.clear_selection()
            self.play(LaggedStart(*anims))
        self.add(sum_stacks)

        # Group by sum
        self.highlight_rects = self.get_highlight_rects(stacks, sum_stacks)
        self.highlight_rects.set_stroke(width=0)
        self.group_by_sum(stacks, sum_stacks)
        self.wait()

        # Count Answer
        highlights = VGroup()
        for stack in self.common_sum_stacks[::5]:
            for subset in stack:
                highlights.add(VHighlight(subset, max_stroke_addition=10))

        answer_word, answer_count = answer = VGroup(
            Text("Answer: "),
            Integer(0)
        )
        answer.arrange(RIGHT)
        answer.next_to(self.common_sum_stacks[0], UP, LARGE_BUFF)
        answer_count.set_color(TEAL)

        self.add(highlights, self.common_sum_stacks, answer)
        self.play(
            ShowIncreasingSubsets(highlights),
            UpdateFromFunc(answer_count, lambda m: m.set_value(len(highlights))),
            run_time=1.5
        )
        self.play(FadeOut(highlights))

        # Contrast with 1/5
        count = OldTexText(
            "Total subsets:", " $2^5 = $", " $32$"
        )
        count.set_color_by_tex("32", BLUE)
        count.match_x(set_tex).match_y(answer)
        counter = Integer(32)
        counter.set_color(BLUE)
        counter.replace(count[-1])

        all_highlights = VGroup()
        for stack in self.common_sum_stacks:
            for subset in stack:
                all_highlights.add(VHighlight(subset, max_stroke_addition=10))

        fifth_arrow = Vector(RIGHT)
        fifth_arrow.next_to(count, RIGHT)
        fifth = Tex("\\times 1 / 5", font_size=24)
        fifth.next_to(fifth_arrow, UP, buff=SMALL_BUFF)
        fifth_rhs = DecimalNumber(32 / 5, num_decimal_places=1)
        fifth_rhs.next_to(fifth_arrow, RIGHT)

        self.add(all_highlights, self.common_sum_stacks)
        self.play(
            FadeIn(count[:2]),
            ShowIncreasingSubsets(all_highlights, run_time=2),
            UpdateFromFunc(counter, lambda m: m.set_value(len(all_highlights))),
        )
        self.play(FadeOut(all_highlights))
        self.wait()
        self.play(
            GrowArrow(fifth_arrow),
            Write(fifth),
        )
        self.wait()
        self.play(FadeTransform(count[-1].copy(), fifth_rhs, path_arc=-60 * DEGREES))
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(
            answer, *count[:2], counter, fifth_arrow, fifth, fifth_rhs,
        )))

        # Show generating function
        self.show_generating_function(set_tex)
        self.transition_to_full_generating_function(set_tex)

    def construct_all_subsets(self, set_tex):
        # Preview binary choices
        value_parts = VGroup(*(
            get_part_by_value(set_tex, v) for v in range(1, 6)
        ))
        rects = VGroup(*(
            SurroundingRectangle(vp, buff=0.1).round_corners()
            for vp in value_parts
        ))
        rects.set_stroke(BLUE, 2)

        words = Text("5 binary choices")
        words.next_to(set_tex, DOWN, buff=1.5)
        lines = VGroup(*(
            Line(words.get_top(), rect.get_bottom(), buff=0.15)
            for rect in rects
        ))
        lines.match_style(rects)

        def match_n(rects, n):
            bits = it.chain(
                str(bin(n)[-1:1:-1]),
                it.repeat("0")
            )
            for rect, bit in zip(rects, bits):
                rect.set_stroke(opacity=float(bit == "1"))

        self.add(rects)
        self.play(
            Write(words),
            Write(lines),
            UpdateFromAlphaFunc(
                rects, lambda r, a: match_n(r, int(31 * a)),
                run_time=4,
                rate_func=linear,
            )
        )
        self.wait()
        self.play(
            FadeOut(rects),
            LaggedStartMap(Uncreate, lines),
            FadeOut(words, 0.1 * DOWN),
        )

        # Show construction
        subsets = VGroup(get_set_tex([]))
        for value in range(1, 6):
            value_mob = get_part_by_value(set_tex, value)
            marks = VGroup(Exmark(), Checkmark())
            marks.match_height(value_mob)
            marks.next_to(value_mob, DOWN)

            subsets.generate_target()
            added_subsets = VGroup(*(
                get_set_tex([*ss.values, value]).move_to(ss)
                for ss in subsets
            ))
            for ss in added_subsets:
                self.color_set_tex(ss)
                get_integer_parts(ss)[-1].set_opacity(0)

            vect = [RIGHT, DOWN, RIGHT, DOWN, RIGHT][value - 1]
            buff = [2.25, 0.75, 2.0, 0.75, 1.0][value - 1]
            added_subsets.next_to(subsets, vect, buff=buff)
            new_subsets = VGroup(*subsets.target, *added_subsets)
            new_subsets.set_max_width(FRAME_WIDTH - 1)
            new_subsets.center()
            subsets_copy = subsets.copy()
            for ssc, nss in zip(subsets_copy, added_subsets):
                ssc.match_height(nss)
                ssc.move_to(nss)

            # self.wait()
            elem = get_part_by_value(set_tex, value)
            if value == 1:
                self.play(set_tex_transform(set_tex, subsets[0]))
                self.add(subsets)
                self.wait()
            self.play(
                MoveToTarget(subsets, path_arc=30 * DEGREES),
                ReplacementTransform(
                    subsets.copy(),
                    subsets_copy,
                    path_arc=30 * DEGREES,
                )
            )
            self.remove(subsets_copy)
            self.play(
                LaggedStart(*(
                    Transform(
                        elem.copy(),
                        get_integer_parts(st)[-1].copy().set_opacity(1),
                        remover=True,
                    )
                    for st in added_subsets
                ), lag_ratio=0.1),
                *(
                    set_tex_transform(st1, st2)
                    for st1, st2 in zip(subsets_copy, added_subsets)
                ),
                elem.animate.set_color(self.elem_colors[value - 1]),
                FlashAround(elem, color=self.elem_colors[value - 1]),
            )
            self.remove(subsets_copy, new_subsets)
            subsets.set_submobjects(list(new_subsets))
            self.add(subsets)
            subsets.set_opacity(1)
            # self.wait()
        self.wait()

        # Equation
        equation = Tex("2 \\cdot 2 \\cdot 2 \\cdot 2 \\cdot 2 = 2^5 = 32")
        equation.set_width(4)
        equation.to_corner(UL)
        equation.set_color(YELLOW)
        self.play(Write(equation))
        self.wait()
        self.play(FadeOut(equation))

        return subsets

    def get_highlight_rects(self, stacks, sum_stacks):
        rects = VGroup()
        anims = []
        for stack, sum_stack in zip(stacks, sum_stacks):
            for set_tex, sum_group in zip(stack, sum_stack):
                if sum(set_tex.values) % 5 == 0:
                    rect = SurroundingRectangle(VGroup(set_tex, sum_group))
                    rect.value = sum(set_tex.values)
                    rects.add(rect)
                else:
                    anims.append(set_tex.animate.set_opacity(0.25))
                    anims.append(sum_group.animate.set_opacity(0.25))
        rects.set_stroke(TEAL, 2)
        for rect in rects:
            rect.round_corners()
        return rects

    def highlight_multiple_of_5(self, stacks, sum_stacks):
        # Blah
        rects = self.get_highlight_rects(stacks, sum_stacks)

        counter = Integer(0, font_size=72)
        counter.to_corner(UR)
        counter.set_color(TEAL)

        self.play(*anims, run_time=1)
        self.wait()
        self.play(
            FadeIn(rects, lag_ratio=0.9),
            ChangeDecimalToValue(counter, len(rects)),
            run_time=1.5
        )
        self.wait()

        self.highlight_rects = rects
        self.counter = counter

    def group_by_sum(self, stacks, sum_stacks):
        # Lock sums to subsets
        subset_groups = VGroup()
        for stack, sum_stack in zip(stacks, sum_stacks):
            for set_tex, sum_group in zip(stack, sum_stack):
                set_tex.sum_group = sum_group
                sum_group.set_tex = set_tex
                subset_groups.add(VGroup(set_tex, sum_group))

        # Reorganize
        common_sum_stacks = VGroup()
        max_sum = max(sum(ssg[0].values) for ssg in subset_groups)
        for n in range(max_sum + 1):
            stack = VGroup(*filter(
                lambda ssg: sum(ssg[0].values) == n,
                subset_groups
            ))
            common_sum_stacks.add(stack)

        common_sum_stacks.generate_target()
        csst = common_sum_stacks.target
        for stack in common_sum_stacks.target:
            stack.arrange(DOWN, aligned_edge=RIGHT, buff=SMALL_BUFF)

        csst.arrange_in_grid(4, 5, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        csst[10:15].set_y(np.mean([csst[5].get_y(DOWN), csst[15].get_y(UP)]))
        csst.refresh_bounding_box()
        csst.set_width(FRAME_WIDTH - 1)
        csst.to_corner(DL)
        csst.set_opacity(1)

        # Create new rectangles
        common_sum_rects = VGroup()
        for stack in common_sum_stacks.target:
            rect = SurroundingRectangle(stack, buff=SMALL_BUFF)
            rect.round_corners(radius=0.05)
            rect.value = sum(stack[0][0].values)
            color = TEAL if rect.value % 5 == 0 else GREY_B
            rect.set_stroke(color, 1)
            common_sum_rects.add(rect)

        rect_anims = []
        for highlight_rect in self.highlight_rects:
            for rect in common_sum_rects:
                if rect.value == highlight_rect.value:
                    rect_anims.append(Transform(highlight_rect, rect))
        self.disable_interaction(common_sum_rects)

        # Transition to common sum
        self.play(
            MoveToTarget(common_sum_stacks),
            *rect_anims,
            run_time=2
        )
        self.play(
            FadeOut(self.highlight_rects),
            FadeIn(common_sum_rects),
        )
        self.wait()

        self.subset_groups = subset_groups
        self.common_sum_stacks = common_sum_stacks
        self.common_sum_rects = common_sum_rects

    def show_generating_function(self, set_tex):
        # Setup expressions
        css = self.common_sum_stacks
        csr = self.common_sum_rects
        lower_group = self.lower_group = VGroup(csr, css)

        factored_terms = "(1 + x^1)", "(1 + x^2)", "(1 + x^3)", "(1 + x^4)", "(1 + x^5)"
        factored = Tex("".join(factored_terms), isolate=factored_terms)
        expanded_terms = ["1"]
        for n in range(1, 16):
            k = len(css[n])
            expanded_terms.append(str(k) + f"x^{{{n}}}")
        expanded = Tex("+".join(expanded_terms), isolate=["+", *expanded_terms])
        expanded.set_width(FRAME_WIDTH - 1)
        factored.next_to(set_tex, DOWN, MED_LARGE_BUFF)
        expanded.next_to(factored, DOWN, MED_LARGE_BUFF)
        lhs = OldTex("p(x) = ")
        lhs.next_to(factored, LEFT)

        self.play(FadeIn(lhs))
        for term, elem in zip(factored_terms, get_integer_parts(set_tex)):
            part = factored.get_part_by_tex(term)
            self.play(
                FlashAround(elem, color=elem.get_color()),
                FadeIn(part[:-2]),
                FadeIn(part[-1]),
            )
            part[-2].match_style(elem)
            self.play(FadeTransform(elem.copy(), part[-2]))
            self.wait()
        self.add(factored)

        self.wait()
        self.play(lower_group.animate.set_height(3.0, about_edge=DOWN))

        # Emphasize 5 binary choices
        parts = VGroup(*(
            factored.get_part_by_tex(term)
            for term in factored_terms
        ))
        rects = VGroup(*(
            SurroundingRectangle(part, buff=0.05).round_corners()
            for part in parts
        ))
        rects.set_stroke(BLUE, 2)
        words = Text("5 binary choices", color=BLUE)
        words.next_to(rects, DOWN, MED_LARGE_BUFF)

        self.play(
            LaggedStartMap(
                VFadeInThenOut, rects,
                lag_ratio=0.25,
                run_time=4,
            ),
            Write(words),
        )
        self.play(FadeOut(words))

        # Animate expansion
        fac_term_parts = [factored.get_part_by_tex(term) for term in factored_terms]
        expanded_parts = [expanded.get_part_by_tex(term) for term in expanded_terms]
        super_expanded = VGroup()
        super_expanded.next_to(factored, DOWN, MED_LARGE_BUFF)
        collection_anims = []

        subset_groups = self.subset_groups
        subset_groups.submobjects.sort(
            key=lambda ssg: sum(ssg[0].values)
        )

        for subset_group in subset_groups:
            bits = [i + 1 in subset_group[0].values for i in range(5)]
            top_terms = [
                part[3:-1] if bit else part[1]
                for bit, part in zip(bits, fac_term_parts)
            ]
            top_rects = VGroup(*(
                # VHighlight(part, color_bounds=(BLUE, BLUE_E), max_stroke_addition=3.0)
                SurroundingRectangle(part).set_stroke(BLUE, 2).round_corners()
                for part in top_terms
            ))
            n = sum(b * k for k, b in zip(range(1, 6), bits))
            if n == 0:
                new_term = Tex("1", font_size=36)
                super_expanded.add(new_term)
            else:
                new_plus = Tex("+", font_size=36)
                new_term = Tex(f"x^{{{n}}}", font_size=36)
                super_expanded.add(new_plus, new_term)
                collection_anims.append(FadeOut(new_plus))
            super_expanded.arrange(RIGHT, aligned_edge=DOWN, buff=SMALL_BUFF)
            super_expanded.next_to(factored, DOWN, MED_LARGE_BUFF)
            super_expanded.to_edge(LEFT)
            if len(super_expanded) > 33:
                super_expanded[33:].next_to(
                    super_expanded[0], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT
                )
            low_rect = SurroundingRectangle(new_term, buff=0.5 * SMALL_BUFF)
            low_rect.set_stroke(BLUE, 2).round_corners()
            collection_anims.append(
                FadeTransform(new_term, expanded_parts[n], path_arc=10 * DEGREES)
            )

            self.add(top_rects)
            self.add(super_expanded, low_rect)
            subset_groups.set_opacity(0.25)
            subset_group.set_opacity(1)
            self.wait()
            self.remove(top_rects, low_rect)
        self.wait()

        # Reorganize to expanded
        lower_group.generate_target()
        lower_group.target.set_height(4, about_edge=DOWN)
        lower_group.target[1].set_opacity(1)
        self.play(
            LaggedStart(*collection_anims),
            LaggedStartMap(FadeIn, expanded.get_parts_by_tex("+")),
            MoveToTarget(
                lower_group,
                rate_func=squish_rate_func(smooth, 0.5, 1.0)
            ),
            run_time=3,
        )
        self.add(expanded)
        self.wait(note="Highlight multiples of 5")

        self.factored_func = VGroup(*lhs, *factored)
        self.expanded_func = expanded

    def transition_to_full_generating_function(self, set_tex):
        # Expressions
        factored = Tex(
            "f(x) = (1 + x^1)(1 + x^2)(1 + x^3) \\cdots \\left(1 + x^{1{,}999}\\right)\\left(1 + x^{2{,}000}\\right)",
        )
        expanded = Tex(
            "f(x) = 1+x+x^{2}+2 x^{3}+2 x^{4}+ 3x^{5} +\\cdots + x^{2{,}001{,}000}",
            isolate="+",
        )
        new_set_tex = get_set_tex(range(1, 2001))
        new_set_tex.move_to(set_tex)
        self.color_set_tex(new_set_tex)
        get_integer_parts(new_set_tex)[-1].set_color(
            interpolate_color(BLUE_E, BLUE_D, 0.5)
        )

        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.set_stroke(GREY_C, 1)
        h_line.set_y(0.5)

        factored_word = Text("Factored", font_size=60, color=BLUE_B)
        factored_word.next_to(set_tex, DOWN, MED_LARGE_BUFF)
        factored.next_to(factored_word, DOWN, MED_LARGE_BUFF)
        expanded_word = Text("Expanded", font_size=60, color=TEAL)
        expanded_word.next_to(h_line, DOWN, buff=1.25)
        expanded.next_to(expanded_word, DOWN, MED_LARGE_BUFF)
        for mob in [factored, factored_word, expanded, expanded_word]:
            mob.to_edge(LEFT)

        small_group = VGroup(set_tex, self.factored_func)
        self.play(
            small_group.animate.set_y(-1.5),
            FadeOut(self.expanded_func, 2 * DOWN),
            FadeOut(self.lower_group, DOWN),
        )
        self.play(TransformMatchingShapes(set_tex.copy(), new_set_tex))
        self.play(FadeTransform(self.factored_func.copy(), factored))
        self.wait()
        for n, i, j in [(1, 5, 11), (2, 11, 17), (3, 17, 23), (2000, 36, 46)]:
            value_part = get_part_by_value(new_set_tex, n)
            self.play(
                FadeTransform(value_part.copy(), factored[i + 4:j - 1].copy(), remover=True),
                FlashAround(factored[i:j], color=BLUE),
            )
        self.add(factored)
        self.wait()
        self.play(
            Write(factored_word),
            FadeOut(small_group, DOWN)
        )
        self.play(
            FadeTransform(factored_word.copy(), expanded_word),
            ShowCreation(h_line),
        )
        self.play(FadeIn(expanded, run_time=2, lag_ratio=0.5))
        self.wait()

        # Emphasize scale
        words = OldTexText("Imagine collecting $2^{2{,}000}$ terms!")
        words.set_color(RED)
        words.next_to(h_line, DOWN)
        words.to_edge(RIGHT)
        morty = Mortimer(height=2)
        morty.next_to(words, DOWN, MED_LARGE_BUFF)
        morty.to_edge(RIGHT)

        self.play(
            VFadeIn(morty),
            morty.change("surprised", expanded),
            Write(words)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(FadeOut(words), FadeOut(morty))

        # Show example term
        n = 25
        # CHANGE: get_subsets(range(1, 26)) builds a list with the 2^25 subsets (>5 GB, SIGKILL); they are traversed lazily in the same order
        subsets = [
            s
            for k in range(n + 1)
            for s in it.combinations(range(1, n + 1), k)
            if sum(s) == n
        ]
        coef = len(subsets)
        term = OldTex(str(coef), f"x^{{{n}}}", "+", "\\cdots")
        term[:2].set_color(TEAL)
        term[2:].set_color(WHITE)
        tail = expanded[-11:]
        term.move_to(tail, DL)
        tail.generate_target()
        tail.target.next_to(term, RIGHT, buff=0.15, aligned_edge=DOWN)

        self.play(
            Write(term),
            MoveToTarget(tail),
        )
        self.wait()

        subset_mobs = VGroup(*map(get_set_tex, subsets))
        subset_mobs.arrange_in_grid(n_cols=10)
        subset_mobs.set_width(FRAME_WIDTH - 1)
        subset_mobs.to_edge(UP)
        subset_mobs.set_color(TEAL)
        top_rect = FullScreenFadeRectangle()
        top_rect.set_fill(BLACK, opacity=0.9)
        top_rect.set_height(4, about_edge=UP, stretch=True)

        term_rect = SurroundingRectangle(term[:2])
        term_rect.round_corners()
        term_rect.set_stroke(YELLOW, 2)
        term_words = Text("Is there a snazzy\nway to deduce this?", font_size=36)
        term_words.next_to(term_rect, DOWN)
        term_words.set_color(YELLOW)

        self.play(
            FadeIn(top_rect),
            ShowIncreasingSubsets(subset_mobs, run_time=5)
        )
        self.wait()
        self.play(
            ShowCreation(term_rect),
            Write(term_words),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, subset_mobs, shift=0.2 * UP),
            FadeOut(top_rect, rate_func=squish_rate_func(smooth, 0.6, 1)),
            run_time=3
        )
        self.wait()

    ##

    def color_set_tex(self, set_tex):
        for value in set_tex.values:
            elem = get_part_by_value(set_tex, value)
            if value - 1 < len(self.elem_colors):
                elem.set_color(self.elem_colors[value - 1])

    def get_subset_stacks(self, full_set, buff=3.5):
        stacks = VGroup(*(
            VGroup(*(
                get_set_tex(subset)
                for subset in it.combinations(full_set, k)
            ))
            for k in range(len(full_set) + 1)
        ))
        for stack in stacks:
            stack.arrange(DOWN)
            for ss in stack:
                self.color_set_tex(ss)
        stacks.arrange(RIGHT, buff=buff, aligned_edge=DOWN)

        stacks[0].move_to(stacks[1]).align_to(stacks[2], UP)
        stacks[4].align_to(stacks[3], UP)
        stacks[5].match_x(stacks[4])

        stacks.set_max_height(FRAME_HEIGHT - 3)
        stacks.set_max_width(FRAME_WIDTH - 2)
        stacks.center().to_edge(DOWN)
        return stacks

    def get_subset_sums(self, stacks):
        return VGroup(*(
            VGroup(*(
                get_sum_group(set_tex)
                for set_tex in stack
            ))
            for stack in stacks
        ))
