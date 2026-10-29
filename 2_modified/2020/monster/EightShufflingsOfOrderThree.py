# ==============================================================================
# Scene:      EightShufflingsOfOrderThree
# Source:     videos/_2020/monster.py (lines 2584-2631)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EightShufflingsOfOrderThree.py EightShufflingsOfOrderThree -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the Dot has only one submobject (the numeric label); index 1 does not exist
# ==============================================================================

from manim_imports_ext import *

def get_permutation_arrows(mobs, permutation, arc=PI / 2):
    arrows = VGroup()
    for i in range(len(permutation)):
        j = permutation[i]
        u = -1 if mobs[i].get_x() < mobs[j].get_x() else 1
        arrow = Arrow(
            mobs[i].get_edge_center(u * UP),
            mobs[j].get_edge_center(u * UP),
            buff=SMALL_BUFF,
            path_arc=arc,
        )
        arrow.insert_n_curves(10)
        arrow.set_stroke(BLACK, 2, background=True)
        arrow.set_fill(BLUE, 0.8)
        arrows.add(arrow)
    return arrows


def permutation_animation(mobs, perm=None, arc=PI / 2, lag_factor=3, run_time=None):
    if perm is None:
        targets = list(mobs)
        random.shuffle(targets)
    else:
        targets = [mobs[i] for i in perm]

    kw = {"lag_ratio": lag_factor / len(mobs)}
    if run_time is not None:
        kw["run_time"] = run_time
    return LaggedStart(
        *[
            ApplyMethod(m1.move_to, m2, path_arc=arc)
            for m1, m2 in zip(mobs, targets)
        ],
        **kw
    )


class EightShufflingsOfOrderThree(Scene):
    def construct(self):
        bg_rect = FullScreenFadeRectangle()
        bg_rect.set_fill(GREY_E, 1)
        bg_rect.set_stroke(width=0)
        self.add(bg_rect)

        # Setup dots
        dots_template = VGroup(*[Dot() for x in range(4)])
        dots_template.set_height(0.5)
        dots_template.arrange(RIGHT, buff=MED_SMALL_BUFF)
        dots_template.set_color(GREY_B)

        for n, dot in enumerate(dots_template):
            label = Integer(n + 1)
            label.set_height(0.25)
            label.set_color(BLACK)
            label.move_to(dot)
            dot.add(label)

        all_dots = VGroup(*[dots_template.copy() for x in range(8)])
        all_dots.arrange_in_grid(4, 2, buff=1.25)
        VGroup(all_dots[0::2], all_dots[1::2]).arrange(RIGHT, buff=2)

        d_gen = iter(all_dots)
        for trip in it.combinations(range(4), 3):
            trip = np.array(trip)
            perm1 = np.array(list(range(4)))
            perm2 = np.array(list(range(4)))
            perm1[trip] = trip[[1, 2, 0]]
            perm2[trip] = trip[[2, 0, 1]]
            for perm in [perm1, perm2]:
                dots = next(d_gen)
                arrows = get_permutation_arrows(dots, perm)
                dots.add(arrows)
                dots.perm = perm
                for i in trip:
                    dots[i].set_stroke(YELLOW, 1)
                    # CHANGE: the Dot has only one submobject (the numeric label); index 1 does not exist
                    dots[i][0].set_stroke(width=0)

        self.play(ShowIncreasingSubsets(all_dots, run_time=4, rate_func=linear))
        self.wait()
        for x in range(3):
            self.play(*[
                permutation_animation(dots, dots.perm, lag_factor=0)
                for dots in all_dots
            ])
        self.wait()
