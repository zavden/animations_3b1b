# ==============================================================================
# Scene:      GoThroughAllSubsetsFast
# Source:     videos/_2022/puzzles/subsets.py (lines 688-690)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoThroughAllSubsetsFast.py GoThroughAllSubsetsFast -w -m --fps 15
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


class GoThroughAllSubsets(InteractiveScene):
    n_searched = 2**6
    rate = 1

    def construct(self):
        full_set = get_set_tex(range(1, 2001), max_shown=25)
        full_set.set_width(0.9 * FRAME_WIDTH)
        full_set.center()
        full_set_elements = [sm for sm in full_set if isinstance(sm, Integer)]

        sum_mob = Integer(0)
        sum_mob.next_to(full_set, DOWN, buff=1.0)
        sum_lhs = Text("Sum = ")
        sum_lhs.next_to(sum_mob, LEFT)
        sum_label = VGroup(sum_lhs, sum_mob)
        sum_label.align_to(full_set, LEFT).shift(RIGHT)

        counter = VGroup(
            Text("Count so far: "), Integer(0, edge_to_fix=LEFT)
        )
        counter.arrange(RIGHT)
        counter.next_to(sum_mob, RIGHT)
        counter.align_to(full_set, RIGHT).shift(LEFT)

        for elem in full_set_elements:
            elem.rect = SurroundingRectangle(elem, buff=0.05)
            elem.rect.set_stroke(BLUE, 2)
            elem.rect.round_corners()
            elem.line = Line(elem.rect.get_bottom(), sum_mob.get_top(), buff=0.2)
            elem.line.set_stroke(BLUE, 2)
        self.add(full_set)
        self.add(counter)
        self.add(sum_label)

        group = VGroup(
            VGroup(),  # Rects
            VGroup(),  # Lines
            sum_mob,
            counter[1],
            VGroup(),  # Mark
        )

        n_tracker = ValueTracker(0)

        all_counts = np.cumsum([
            int(sum((int(bit) * n for n, bit in zip(it.count(1), reversed(bin(n)[2:])))) % 5 == 0)
            for n in range(self.n_searched)
        ])

        def update_group(group):
            n = int(n_tracker.get_value())
            rects, lines, sum_mob, count, mark = group

            bits = str(bin(n))[2:]
            elems = []
            subset = []
            for i, elem, bit in zip(it.count(1), full_set_elements, reversed(bits)):
                if bit == '1':
                    elems.append(elem)
                    subset.append(i)

            total = sum(subset)
            sum_mob.set_value(total)

            rects.set_submobjects([elem.rect for elem in elems])
            lines.set_submobjects([elem.line for elem in elems])

            if total % 5 == 0:
                count.set_value(all_counts[n])
                count.set_color(GREEN)
                sum_mob.set_color(GREEN)
                check = Checkmark()
                check.next_to(sum_mob, RIGHT)
                mark.set_submobjects([check])
            else:
                sum_mob.set_color(WHITE)
                mark.set_submobjects([])

        self.add(group, n_tracker)
        self.play(
            n_tracker.animate.set_value(self.n_searched),
            UpdateFromFunc(group, update_group),
            run_time=self.n_searched / self.rate,
            rate_func=linear,
        )


class GoThroughAllSubsetsFast(GoThroughAllSubsets):
    n_searched = 2**13
    rate = 120
