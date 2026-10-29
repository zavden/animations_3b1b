# ==============================================================================
# Scene:      ShowTrueDistribution
# Source:     videos/_2018/eop/independence.py (lines 1873-1971)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowTrueDistribution.py ShowTrueDistribution -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - do_about_point(corner, stretch, 0.5, 0) replaced by stretch(0.5, 0, about_point=corner) (do_about_point does not exist)
# ==============================================================================

from manim_imports_ext import *

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


class ShowTrueDistribution(PiCreatureScene):
    def construct(self):
        self.force_skipping()

        self.remove(self.randy)
        self.add_title()
        self.show_distributions()
        self.show_emotion()
        self.imagine_score_0()

        self.revert_to_original_skipping_status()
        self.get_angry()

    def add_title(self):
        title = OldTex("P(", "\\text{Correct}", ")", "=", "0.65")
        title.to_edge(UP)
        title.set_color_by_tex("Correct", GREEN)

        self.add(title)
        self.title = title

    def show_distributions(self):
        dist = get_binomial_distribution(3, 0.65)
        values = np.array(list(map(dist, list(range(4)))))
        alt_values = values + [0.2, 0, 0, 0.2]
        alt_values /= sum(alt_values)
        chart = BarChart(values, bar_names = list(range(4)))
        bars = chart.bars
        old_bars = bars.copy()
        arrows = VGroup()
        for bar, old_bar in zip(bars, old_bars):
            for mob, vect in (bar, RIGHT), (old_bar, LEFT):
                mob.generate_target()
                # CHANGE: do_about_point does not exist (not even in the 2019 Cairo); stretch about the corner directly
                mob.target.stretch(0.5, 0, about_point = mob.get_corner(DOWN+vect))
            old_bar.target.set_color(average_color(RED_E, BLACK))
            old_bar.target.set_stroke(width = 0)
            arrow = Arrow(ORIGIN, UP, buff = 0, color = GREEN)
            arrow.move_to(bar.get_bottom())
            arrow.shift(3*UP)
            arrows.add(arrow)
        for arrow in arrows[1:3]:
            arrow.rotate(np.pi)
            arrow.set_color(RED)
        arrows.set_color_by_gradient(BLUE, YELLOW)

        self.add(chart)
        self.play(*list(map(MoveToTarget, it.chain(bars, old_bars))))
        self.play(
            chart.change_bar_values, alt_values,
            *list(map(ShowCreation, arrows))
        )
        self.wait(2)

        self.bar_chart = chart
        self.old_bars = old_bars

    def show_emotion(self):
        randy = self.randy

        self.play(FadeIn(randy))
        self.play(randy.change, "sad")
        self.play(Blink(randy))

    def imagine_score_0(self):
        prob_rect = SurroundingRectangle(self.title[-1])
        bar_rect = SurroundingRectangle(VGroup(
            self.bar_chart.bars[0], self.old_bars[0],
            self.bar_chart.bar_labels[0],
        ))

        self.play(ShowCreation(prob_rect))
        self.wait()
        self.play(ReplacementTransform(
            prob_rect, bar_rect
        ))
        self.wait()
        self.play(FadeOut(bar_rect))

    def get_angry(self):
        randy = self.randy

        self.play(randy.change, "angry")
        self.wait(2)
        self.play(PiCreatureSays(
            randy, "It's not representative!",
            target_mode = "pleading",
            bubble_config = {"fill_opacity" : 1}
        ))
        self.wait(2)

    #####

    def create_pi_creature(self):
        self.randy = Randolph()
        self.randy.to_corner(DOWN+LEFT)
        return self.randy
