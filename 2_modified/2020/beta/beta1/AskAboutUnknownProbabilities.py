# ==============================================================================
# Scene:      AskAboutUnknownProbabilities
# Source:     videos/_2020/beta/beta1.py (lines 1680-1895)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl AskAboutUnknownProbabilities.py AskAboutUnknownProbabilities -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Before, pr[1] was the content because mobject[0] was the container itself (split() = [self] + submobjects); in ManimGL only the submobjects: the content is submobjects[0]
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

COIN_COLOR_MAP = {
    "H": BLUE_E,
    "T": RED_E,
}


def get_random_process(choices, shuffle_time=2, total_time=3, change_rate=0.05,
                       h_buff=0.1, v_buff=0.1):
    content = choices[0]

    container = Square()
    container.set_opacity(0)
    container.set_width(content.get_width() + 2 * h_buff, stretch=True)
    container.set_height(content.get_height() + 2 * v_buff, stretch=True)
    container.move_to(content)
    container.add(content)
    container.time = 0
    container.last_change_time = 0

    def update(container, dt):
        container.time += dt

        t = container.time
        change = all([
            (t % total_time) < shuffle_time,
            container.time - container.last_change_time > change_rate
        ])
        if change:
            mob = container.submobjects[0]
            new_mob = random.choice(choices)
            new_mob.match_height(mob)
            new_mob.move_to(container, DL)
            new_mob.shift(2 * np.random.random() * h_buff * RIGHT)
            new_mob.shift(2 * np.random.random() * v_buff * UP)
            container.set_submobjects([new_mob])
            container.last_change_time = container.time

    container.add_updater(update)
    return container


def get_die_faces():
    dot = Dot()
    dot.set_width(0.15)
    dot.set_color(BLUE_B)

    square = Square()
    square.round_corners(0.25)
    square.set_stroke(WHITE, 2)
    square.set_fill(GREY_E, 1)
    square.set_width(0.6)

    edge_groups = [
        (ORIGIN,),
        (UL, DR),
        (UL, ORIGIN, DR),
        (UL, UR, DL, DR),
        (UL, UR, ORIGIN, DL, DR),
        (UL, UR, LEFT, RIGHT, DL, DR),
    ]

    arrangements = VGroup(*[
        VGroup(*[
            dot.copy().move_to(square.get_bounding_box_point(ec))
            for ec in edge_group
        ])
        for edge_group in edge_groups
    ])
    square.set_width(1)

    faces = VGroup(*[
        VGroup(square.copy(), arrangement)
        for arrangement in arrangements
    ])
    faces.arrange(RIGHT)

    return faces


def get_random_die(**kwargs):
    return get_random_process(get_die_faces(), **kwargs)


def get_random_card(height=1, **kwargs):
    cards = DeckOfCards()
    cards.set_height(height)
    return get_random_process(cards, **kwargs)


# Coins
def get_coin(symbol, color=None):
    if color is None:
        color = COIN_COLOR_MAP.get(symbol, GREY_E)
    coin = VGroup()
    circ = Circle()
    circ.set_fill(color, 1)
    circ.set_stroke(WHITE, 1)
    circ.set_height(1)
    label = OldTexText(symbol)
    label.set_height(0.5 * circ.get_height())
    label.move_to(circ)
    coin.add(circ, label)
    coin.symbol = symbol
    return coin


def get_random_coin(**kwargs):
    return get_random_process([get_coin("H"), get_coin("T")], **kwargs)



# ----- From _2020/beta/beta1.py -----

class AskAboutUnknownProbabilities(Scene):
    def construct(self):
        # Setup
        unknown_title, prob_title = titles = self.get_titles()

        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        v_line.set_stroke([WHITE, GREY_B], 3)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN)

        processes = VGroup(
            get_random_coin(shuffle_time=1),
            get_random_die(shuffle_time=1.5),
            get_random_card(shuffle_time=2),
        )
        processes.arrange(DOWN, buff=0.7)
        processes.next_to(unknown_title, DOWN, LARGE_BUFF)
        processes_rect = BackgroundRectangle(processes)
        processes_rect.set_fill(BLACK, 1)

        prob_labels = VGroup(
            OldTex("P(", "00", ")", "=", "1 / 2"),
            OldTex("P(", "00", ")", "=", "1 / 6}"),
            OldTex("P(", "00", ")", "=", "1 / 52}"),
        )
        prob_labels.scale(1.5)
        prob_labels.arrange(DOWN, aligned_edge=LEFT)
        prob_labels.match_x(prob_title)
        for pl, pr in zip(prob_labels, processes):
            pl.match_y(pr)
            # CHANGE: Before, pr[1] was the content because mobject[0] was the container itself (split() = [self] + submobjects); in ManimGL only the submobjects: the content is submobjects[0]
            content = pr.submobjects[0].copy()
            content.replace(pl[1], dim_to_match=0)
            pl.replace_submobject(1, content)

        # Putting numbers to the unknown
        number_rects = VGroup(*[
            SurroundingRectangle(pl[-1])
            for pl in prob_labels
        ])
        number_rects.set_stroke(YELLOW, 2)

        for pl in prob_labels:
            pl.save_state()
            pl[:3].match_x(prob_title)
            pl[3:].match_x(prob_title)
            pl.set_opacity(0)

        self.add(processes)
        self.play(
            LaggedStartMap(FadeInFromDown, titles),
            LaggedStart(
                ShowCreation(v_line),
                ShowCreation(h_line),
                lag_ratio=0.1,
            ),
            LaggedStartMap(Restore, prob_labels),
            run_time=1
        )
        self.wait(10)
        # self.play(
        #     LaggedStartMap(
        #         ShowCreationThenFadeOut,
        #         number_rects,
        #         run_time=3,
        #     )
        # )
        # self.wait(2)

        # Highlight coin flip
        fade_rects = VGroup(*[
            VGroup(
                BackgroundRectangle(pl, buff=MED_SMALL_BUFF),
                BackgroundRectangle(pr, buff=MED_SMALL_BUFF),
            )
            for pl, pr in zip(prob_labels, processes)
        ])
        fade_rects.set_fill(BLACK, 0.8)

        prob_half = prob_labels[0]
        half = prob_half[-1]
        half_underline = Line(LEFT, RIGHT)
        half_underline.set_width(half.get_width() + MED_SMALL_BUFF)
        half_underline.next_to(half, DOWN, buff=SMALL_BUFF)
        half_underline.set_stroke(YELLOW, 3)

        self.play(
            FadeIn(fade_rects[1]),
            FadeIn(fade_rects[2]),
        )
        self.wait(2)
        self.play(
            FadeIn(fade_rects[0]),
            FadeOut(fade_rects[1]),
        )
        self.wait(3)
        self.play(
            FadeOut(fade_rects[0]),
            FadeOut(fade_rects[2]),
        )
        self.wait(4)

        # Transition to question
        processes.suspend_updating()
        self.play(
            LaggedStart(
                FadeOut(unknown_title, UP),
                FadeOut(prob_title, UP),
                lag_ratio=0.2,
            ),
            FadeOut(h_line, UP, lag_ratio=0.1),
            FadeOut(processes, LEFT, lag_ratio=0.1),
            FadeOut(prob_labels[1]),
            FadeOut(prob_labels[2]),
            v_line.rotate, 90 * DEGREES,
            v_line.shift, 0.6 * FRAME_HEIGHT * UP,
            prob_half.center,
            prob_half.to_edge, UP,
            run_time=2,
        )
        self.clear()
        self.add(prob_half)

        arrow = Vector(UP)
        arrow.next_to(half, DOWN)
        question = OldTexText("What exactly does\\\\this mean?")
        question.next_to(arrow, DOWN)

        self.play(
            GrowArrow(arrow),
            FadeIn(question, UP),
        )
        self.wait(2)
        self.play(
            FadeOut(question, RIGHT),
            Rotate(arrow, 90 * DEGREES),
            VFadeOut(arrow),
        )

        # Show long run averages
        self.show_many_coins(20, 50)
        self.show_many_coins(40, 100)

        # Make probability itself unknown
        q_marks = OldTex("???")
        q_marks.set_color(YELLOW)
        q_marks.replace(half, dim_to_match=0)

        randy = Randolph(mode="confused")
        randy.center()
        randy.look_at(prob_half)

        self.play(
            FadeOut(half, UP),
            FadeIn(q_marks, DOWN),
        )
        self.play(FadeIn(randy))
        self.play(Blink(randy))
        self.wait()

        # self.embed()

    def get_titles(self):
        unknown_label = OldTexText("Random process")
        prob_label = OldTexText("Long-run frequency")
        titles = VGroup(unknown_label, prob_label)
        titles.scale(1.25)

        unknown_label.move_to(FRAME_WIDTH * LEFT / 4)
        prob_label.move_to(FRAME_WIDTH * RIGHT / 4)
        titles.to_edge(UP, buff=MED_SMALL_BUFF)
        titles.set_color(BLUE)
        return titles

    def show_many_coins(self, n_rows, n_cols):
        coin_choices = VGroup(
            get_coin("H"),
            get_coin("T"),
        )
        coin_choices.set_stroke(width=0)
        coins = VGroup(*[
            random.choice(coin_choices).copy()
            for x in range(n_rows * n_cols)
        ])

        def organize_coins(coin_group):
            coin_group.scale(1 / coin_group[0].get_height())
            coin_group.arrange_in_grid(n_rows=n_rows)
            coin_group.set_width(FRAME_WIDTH - 1)
            coin_group.to_edge(DOWN, MED_LARGE_BUFF)

        organize_coins(coins)

        sorted_coins = VGroup()
        for coin in coins:
            coin.generate_target()
            sorted_coins.add(coin.target)
        sorted_coins.submobjects.sort(key=lambda m: m.symbol)
        organize_coins(sorted_coins)

        self.play(LaggedStartMap(
            FadeInFrom, coins,
            lambda m: (m, 0.2 * DOWN),
            run_time=3,
            rate_func=linear
        ))
        self.wait()
        self.play(LaggedStartMap(
            MoveToTarget, coins,
            path_arc=30 * DEGREES,
            run_time=2,
            lag_ratio=1 / len(coins),
        ))
        self.wait()
        self.play(FadeOut(coins))
