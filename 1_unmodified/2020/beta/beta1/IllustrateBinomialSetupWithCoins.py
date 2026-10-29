# ==============================================================================
# Scene:      IllustrateBinomialSetupWithCoins
# Source:     videos/_2020/beta/beta1.py (lines 3284-3338)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl IllustrateBinomialSetupWithCoins.py IllustrateBinomialSetupWithCoins -w -m --fps 15
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

class IllustrateBinomialSetupWithCoins(Scene):
    def construct(self):
        coins = [
            get_coin("H"),
            get_coin("T"),
        ]

        coin_row = VGroup()
        for x in range(12):
            coin_row.add(random.choice(coins).copy())

        coin_row.arrange(RIGHT)
        coin_row.to_edge(UP)

        first_coin = get_random_coin(shuffle_time=2, total_time=2)
        first_coin.move_to(coin_row[0])

        brace = Brace(coin_row, UP)
        brace_label = brace.get_text("$N$ times")

        prob_label = OldTex(
            "P(\\# 00 = k)",
            tex_to_color_map={
                "00": WHITE,
                "k": GREEN,
            }
        )
        heads = get_coin("H")
        template = prob_label.get_part_by_tex("00")
        heads.replace(template)
        prob_label.replace_submobject(
            prob_label.index_of_part(template),
            heads,
        )
        prob_label.set_height(1)
        prob_label.next_to(coin_row, DOWN, LARGE_BUFF)

        self.camera.frame.set_height(1.5 * FRAME_HEIGHT)

        self.add(first_coin)
        for x in range(4):
            self.wait()
            first_coin.suspend_updating()
            self.wait()
            first_coin.resume_updating()

        self.remove(first_coin)
        self.play(
            ShowIncreasingSubsets(coin_row, int_func=np.ceil),
            GrowFromPoint(brace, brace.get_left()),
            FadeIn(brace_label, 3 * LEFT)
        )
        self.wait()
        self.play(FadeIn(prob_label, lag_ratio=0.1))
        self.wait()
