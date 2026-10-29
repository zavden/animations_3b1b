# ==============================================================================
# Scene:      ShowFullDistribution
# Source:     videos/_2018/eop/independence.py (lines 1654-1859)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFullDistribution.py ShowFullDistribution -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


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


def get_probability_of_slot_group(bool_list, conditioned_list = None):
    filler_tex = "Fi"*max(len(bool_list), 3)
    if conditioned_list is None:
        result = OldTex("P(", filler_tex, ")")
    else:
        result = OldTex("P(", filler_tex, "|", filler_tex, ")")
    fillers = result.get_parts_by_tex(filler_tex)
    for filler, bl in zip(fillers, [bool_list, conditioned_list]):
        slot_group = get_slot_group(
            bl, buff = SMALL_BUFF, include_qs = False,
        )
        slot_group.replace(filler, dim_to_match = 0)
        slot_group.shift(0.5*SMALL_BUFF*DOWN)
        index = result.index_of_part(filler)
        result.submobjects[index] = slot_group
    return result


class ShowFullDistribution(Scene):
    def construct(self):
        self.add_scores_one_and_two()
        self.add_scores_zero_and_three()
        self.show_bar_chart()
        self.compare_to_binomial_pattern()
        self.show_alternate_values_of_p()

    def add_scores_one_and_two(self):
        scores = VGroup(
            OldTex(
                "P(", "\\text{Score} = 0", ")",
                "=", "(0.2)", "^3",
                "=", "0.008",
            ),
            OldTex(
                "P(", "\\text{Score} = 1", ")",
                "=", "3", "(0.8)", "(0.2)", "^2", 
                "=", "0.096",
            ),
            OldTex(
                "P(", "\\text{Score} = 2", ")",
                "=", "3", "(0.8)", "^2", "(0.2)",
                "=", "0.384",
            ),
            OldTex(
                "P(", "\\text{Score} = 3", ")",
                "=", "(0.8)", "^3",
                "=", "0.512",
            ),
        )
        scores.arrange(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        scores.shift(MED_LARGE_BUFF*UP)
        scores.to_edge(LEFT)
        for score in scores:
            score.set_color_by_tex_to_color_map({
                "0.8" : GREEN,
                "0.2" : RED,
            })
            score[-1].set_color(YELLOW)

        self.add(*scores[1:3])
        self.scores = scores

    def add_scores_zero_and_three(self):
        self.p_slot_groups = VGroup()

        self.wait()
        self.add_edge_score(0, UP, False)
        self.add_edge_score(3, DOWN, True)

    def add_edge_score(self, index, vect, q_bool):
        score = self.scores[index]
        prob = VGroup(*score[:3])
        brace = Brace(prob, vect)
        p_slot_group = get_probability_of_slot_group([q_bool]*3)
        p_slot_group.next_to(brace, vect)
        group = VGroup(*it.chain(p_slot_group, brace, score))

        self.play(LaggedStartMap(
            FadeIn, group,
            run_time = 2,
            lag_ratio = 0.7,
        ))
        self.wait(2)
        self.p_slot_groups.add(brace, p_slot_group)

    def show_bar_chart(self):
        p_terms = VGroup()
        to_fade = VGroup(self.p_slot_groups)
        value_mobs = VGroup()
        for score in self.scores:
            p_terms.add(VGroup(*score[:3]))
            to_fade.add(VGroup(*score[3:-1]))
            value_mobs.add(score[-1])
        dist = get_binomial_distribution(3, 0.8)
        values = list(map(dist, list(range(4))))
        chart = BarChart(
            values, bar_names = list(range(4)),
        )
        chart.shift(DOWN)

        new_p_terms = VGroup(*[
            OldTex("P(", "S=%d"%k, ")")
            for k in range(4)
        ])
        for term, bar in zip(new_p_terms, chart.bars):
            term[1].set_color(YELLOW)
            term.set_width(1.5*bar.get_width())
            term.next_to(bar, UP)

        self.play(
            ReplacementTransform(
                value_mobs, chart.bars,
                lag_ratio = 0.5,
                run_time = 2
            )
        )
        self.play(
            LaggedStartMap(FadeIn, VGroup(*it.chain(*[
                submob 
                for submob in chart
                if submob is not chart.bars
            ]))),
            Transform(p_terms, new_p_terms),
            FadeOut(to_fade),
        )
        self.wait(2)

        chart.bar_top_labels = p_terms
        chart.add(p_terms)
        self.bar_chart = chart

    def compare_to_binomial_pattern(self):
        dist = get_binomial_distribution(3, 0.5)
        values = list(map(dist, list(range(4))))
        alt_chart = BarChart(values)
        alt_chart.move_to(self.bar_chart)
        bars = alt_chart.bars
        bars.set_fill(GREY, opacity = 0.5)
        vect = 4*UP
        bars.shift(vect)
        nums = VGroup(*list(map(Tex, list(map(str, [1, 3, 3, 1])))))
        for num, bar in zip(nums, bars):
            num.next_to(bar, UP)
        bars_copy = bars.copy()

        self.play(
            LaggedStartMap(FadeIn, bars),
            LaggedStartMap(FadeIn, nums),
        )
        self.wait(2)
        self.play(bars_copy.shift, -vect)
        self.play(ReplacementTransform(
            bars_copy, self.bar_chart.bars
        ))
        self.wait(2)
        self.play(
            VGroup(self.bar_chart, bars, nums).to_edge, LEFT
        )

        self.alt_bars = bars
        self.alt_bars_labels = nums

    def show_alternate_values_of_p(self):
        new_prob = OldTex(
            "P(", "\\text{Correct}", ")", "=", "0.8"
        )
        new_prob.set_color_by_tex("Correct", GREEN)
        new_prob.shift(FRAME_X_RADIUS*RIGHT/2)
        new_prob.to_edge(UP)

        alt_ps = 0.5, 0.65, 0.25
        alt_rhss = VGroup()
        alt_charts = VGroup()
        for p in alt_ps:
            rhs = OldTex(str(p))
            rhs.set_color(YELLOW)
            rhs.move_to(new_prob[-1])
            alt_rhss.add(rhs)

            dist = get_binomial_distribution(3, p)
            values = list(map(dist, list(range(4))))
            chart = self.bar_chart.copy()
            chart.change_bar_values(values)
            for label, bar in zip(chart.bar_top_labels, chart.bars):
                label.next_to(bar, UP)
            alt_charts.add(chart)

        self.play(FadeIn(new_prob))
        self.play(Transform(new_prob[-1], alt_rhss[0]))
        point_5_probs = self.show_point_5_probs(new_prob)
        self.wait()
        self.play(Transform(self.bar_chart, alt_charts[0]))
        self.wait()
        self.play(FadeOut(point_5_probs))
        for rhs, chart in list(zip(alt_rhss, alt_charts))[1:]:
            self.play(Transform(new_prob[-1], rhs))
            self.play(Transform(self.bar_chart, chart))
            self.wait(2)

    def show_point_5_probs(self, mob):
        probs = VGroup()
        last = mob
        for k in range(4):
            buff = MED_LARGE_BUFF
            for indices in it.combinations(list(range(3)), k):
                bool_list = np.array([False]*3)
                bool_list[list(indices)] = True
                prob = get_probability_of_slot_group(bool_list)
                rhs = OldTex("= (0.5)^3")
                rhs.next_to(prob, RIGHT)
                prob.add(rhs)
                prob.scale(0.9)
                prob.next_to(last, DOWN, buff)
                probs.add(prob)
                last = prob
                buff = SMALL_BUFF

        self.play(LaggedStartMap(FadeIn, probs))
        self.wait()
        return probs
