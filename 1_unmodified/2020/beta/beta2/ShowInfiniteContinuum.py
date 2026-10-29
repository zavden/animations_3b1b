# ==============================================================================
# Scene:      ShowInfiniteContinuum
# Source:     videos/_2020/beta/beta2.py (lines 292-400)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl ShowInfiniteContinuum.py ShowInfiniteContinuum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

COIN_COLOR_MAP = {
    "H": BLUE_E,
    "T": RED_E,
}


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


def get_prob_coin_label(symbol="H", color=None, p=0.5, num_decimal_places=2):
    label = OldTex("P", "(", "00", ")", "=",)
    coin = get_coin(symbol, color)
    template = label.get_part_by_tex("00")
    coin.replace(template)
    label.replace_submobject(label.index_of_part(template), coin)
    rhs = DecimalNumber(p, num_decimal_places=num_decimal_places)
    rhs.next_to(label, RIGHT, buff=MED_SMALL_BUFF)
    label.add(rhs)
    return label


def get_q_box(mob):
    box = SurroundingRectangle(mob)
    box.set_stroke(WHITE, 1)
    box.set_fill(GREY_E, 1)
    q_marks = OldTex("???")
    max_width = 0.8 * box.get_width()
    max_height = 0.8 * box.get_height()

    if q_marks.get_width() > max_width:
        q_marks.set_width(max_width)

    if q_marks.get_height() > max_height:
        q_marks.set_height(max_height)

    q_marks.move_to(box)
    box.add(q_marks)
    return box


def get_beta_dist_axes(y_max=20, y_unit=2, label_y=False, **kwargs):
    config = {
        "x_min": 0,
        "x_max": 1,
        "x_axis_config": {
            "unit_size": 0.1,
            "tick_frequency": 0.1,
            "include_tip": False,
        },
        "y_min": 0,
        "y_max": y_max,
        "y_axis_config": {
            "unit_size": 1,
            "tick_frequency": y_unit,
            "include_tip": False,
        },
    }
    result = Axes(**config)
    origin = result.c2p(0, 0)
    kw = {
        "about_point": origin,
        "stretch": True,
    }
    result.x_axis.set_width(11, **kw)
    result.y_axis.set_height(6, **kw)

    x_vals = np.arange(0, 1, 0.2) + 0.2
    result.x_axis.add_numbers(
        *x_vals,
        num_decimal_places=1
    )

    if label_y:
        result.y_axis.add_numbers(
            *np.arange(y_unit, y_max, y_unit)
        )
        label = OldTexText("Probability density")
        label.scale(0.5)
        label.next_to(result.y_axis.get_top(), UR, SMALL_BUFF)
        label.next_to(result.y_axis, UP, SMALL_BUFF)
        label.align_to(result.y_axis.numbers, LEFT)
        result.add(label)
        result.y_axis_label = label

    result.to_corner(DR, LARGE_BUFF)

    return result


def scaled_pdf_axes(scale_factor=3.5):
    axes = get_beta_dist_axes(
        label_y=True,
        y_unit=1,
    )
    axes.y_axis.numbers.set_submobjects([
        *axes.y_axis.numbers[:5],
        *axes.y_axis.numbers[4::5]
    ])
    sf = scale_factor
    axes.y_axis.stretch(sf, 1, about_point=axes.c2p(0, 0))
    for number in axes.y_axis.numbers:
        number.stretch(1 / sf, 1)
    axes.y_axis_label.to_edge(LEFT)
    axes.y_axis_label.add_background_rectangle(opacity=1)
    axes.set_stroke(background=True)
    return axes



# ----- From _2020/beta/beta2.py -----

class ShowInfiniteContinuum(Scene):
    def construct(self):
        # Axes
        axes = scaled_pdf_axes()
        axes.to_edge(DOWN, buff=MED_SMALL_BUFF)
        axes.y_axis.numbers.set_opacity(0)
        axes.y_axis_label.set_opacity(0)
        self.add(axes)

        # Label
        p_label = get_prob_coin_label()
        p_label.set_height(0.7)
        p_label.to_edge(UP)
        box = get_q_box(p_label[-1])
        p_label.add(box)

        brace = Brace(box, DOWN, buff=SMALL_BUFF)
        h_label = OldTex("h")
        h_label.next_to(brace, DOWN)
        h_label.set_color(YELLOW)
        eq = OldTex("=")
        eq.next_to(h_label, RIGHT)
        value = DecimalNumber(0, num_decimal_places=4)
        value.match_height(h_label)
        value.next_to(eq, RIGHT)
        value.set_color(YELLOW)

        self.add(p_label)
        self.add(brace)
        self.add(h_label)

        # Moving h
        h_part = h_label.copy()
        x_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        x_line.set_stroke(YELLOW, 3)

        self.play(
            h_part.next_to, x_line.get_start(), UR, SMALL_BUFF,
            Write(eq),
            FadeInFromPoint(value, h_part.get_center()),
        )

        # Scan continuum
        h_part.tracked = x_line
        value.tracked = x_line
        value.x_axis = axes.x_axis
        self.play(
            ShowCreation(x_line),
            UpdateFromFunc(
                h_part,
                lambda m: m.next_to(m.tracked.get_end(), UR, SMALL_BUFF)
            ),
            UpdateFromFunc(
                value,
                lambda m: m.set_value(
                    m.x_axis.p2n(m.tracked.get_end())
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(
            FadeOut(eq),
            FadeOut(value),
        )

        # Arrows
        arrows = VGroup()
        arrow_template = Vector(DOWN)

        def get_arrow(s, denom, arrow_template=arrow_template, axes=axes):
            arrow = arrow_template.copy()
            arrow.set_height(4 / denom)
            arrow.move_to(axes.c2p(s, 0), DOWN)
            arrow.set_color(interpolate_color(
                GREY_A, GREY_C, random.random()
            ))
            return arrow

        for k in range(2, 50):
            for n in range(1, k):
                if np.gcd(n, k) != 1:
                    continue
                s = n / k
                arrows.add(get_arrow(s, k))
        for k in range(50, 1000):
            arrows.add(get_arrow(1 / k, k))
            arrows.add(get_arrow(1 - 1 / k, k))

        kw = {
            "lag_ratio": 0.05,
            "run_time": 5,
            "rate_func": lambda t: t**5,
        }
        arrows.save_state()
        for arrow in arrows:
            arrow.stretch(0, 0)
            arrow.set_stroke(width=0)
            arrow.set_opacity(0)
        self.play(Restore(arrows, **kw))
        self.play(LaggedStartMap(
            ApplyMethod, arrows,
            lambda m: (m.scale, 0, {"about_edge": DOWN}),
            lag_ratio=10 / len(arrows),
            rate_func=smooth,
            run_time=3,
        ))
        self.remove(arrows)
        self.wait()
