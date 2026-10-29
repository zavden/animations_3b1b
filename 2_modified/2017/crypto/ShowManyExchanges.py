# ==============================================================================
# Scene:      ShowManyExchanges
# Source:     videos/_2017/crypto.py (lines 4994-5083)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowManyExchanges.py ShowManyExchanges -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo drew frames by hand (update_frame/add_frames/ProgressDisplay): drive the exchange animations from a time-based updater and wait
# ==============================================================================

from manim_imports_ext import *

class EthereumLogo(SVGMobject):
    CONFIG = {
        "file_name" : "ethereum_logo",
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "color_chars" : "8B8B48",
        "height" : 0.5,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        for part, char in zip(self.submobjects, self.color_chars):
            part.set_color("#" + 6*char)


class LitecoinLogo(SVGMobject):
    CONFIG = {
        "file_name" : "litecoin_logo",
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "fill_color" : GREY_B,
        "height" : 0.5,
    }


class Exchange(Animation):
    CONFIG = {
        "rate_func" : linear,
    }
    def __init__(self, exchange, **kwargs):
        # CHANGE: GL animations must be begun before update(alpha)
        self.swap = Swap(
            exchange.left,
            exchange.right,
        )
        self.swap.begin()
        self.changed_symbols_yet = False
        Animation.__init__(self, exchange, **kwargs)

    def interpolate_mobject(self, alpha):
        exchange = self.mobject
        if alpha < 1./3:
            self.swap.update(3*alpha)
        elif alpha < 2./3:
            sub_alpha = alpha*3 - 1
            group = VGroup(exchange.left, exchange.right)
            group.set_fill(opacity = 1-smooth(sub_alpha))
        else:
            if not self.changed_symbols_yet:
                new_left = random.choice(
                    exchange.cryptocurrencies
                ).copy()
                new_left.move_to(exchange.right)
                new_right = random.choice(
                    exchange.currencies
                ).copy()
                new_right.move_to(exchange.left)
                # CHANGE: Transform(a, b).update(1) without begin(): use become (same end state)
                exchange.left.become(new_left)
                exchange.right.become(new_right)
                self.changed_symbols_yet = True
            sub_alpha = 3*alpha - 2
            group = VGroup(exchange.left, exchange.right)
            group.set_fill(opacity = smooth(sub_alpha))


class ShowManyExchanges(Scene):
    CONFIG = {
        "n_rows" : 2,
        "n_cols" : 8,
        "shift_radius" : 0.5,
        "run_time" : 30,
    }
    def construct(self):
        cryptocurrencies = self.get_cryptocurrencies()
        currencies = self.get_currencies()
        for currency in it.chain(currencies, cryptocurrencies):
            currency.set_height(0.5)
            currency.align_data_and_family(EthereumLogo())
        exchange = VGroup(*[
            Arrow(
                p1, p2,
                path_arc = np.pi,
                buff = MED_LARGE_BUFF
            )
            for p1, p2 in [(LEFT, RIGHT), (RIGHT, LEFT)]
        ]).set_color(WHITE)
        exchanges = VGroup(*[
            VGroup(*[
                exchange.copy()
                for x in range(3)
            ]).arrange(RIGHT, buff = 2*LARGE_BUFF)
            for y in range(3)
        ]).arrange(DOWN, buff = MED_LARGE_BUFF)
        exchanges = VGroup(*it.chain(*exchanges))
        self.add(exchanges)
        start_times = list(np.linspace(0, 2, len(exchanges)))
        random.shuffle(start_times)
        for exchange, start_time in zip(exchanges, start_times):
            left = random.choice(cryptocurrencies).copy()
            right = random.choice(currencies).copy()
            left.move_to(exchange.get_left())
            right.move_to(exchange.get_right())

            exchange.left = left
            exchange.right = right
            exchange.start_time = start_time
            exchange.add(left, right)
            exchange.currencies = currencies
            exchange.cryptocurrencies = cryptocurrencies
            exchange.animation = Exchange(exchange)

        # CHANGE: Cairo drew frames by hand (update_frame/add_frames/ProgressDisplay): drive the exchange animations from a time-based updater and wait
        clock = [0.0]
        def update_exchanges(group, dt):
            clock[0] += dt
            t = clock[0]
            for exchange in exchanges:
                sub_t = t - exchange.start_time
                if sub_t < 0:
                    continue
                elif sub_t > 3:
                    exchange.start_time = t
                    sub_t = 0
                    exchange.animation = Exchange(exchange)
                exchange.animation.interpolate_mobject(sub_t/3.0)
        exchanges.add_updater(update_exchanges)
        self.add(exchanges)
        self.wait(self.run_time)
        exchanges.remove_updater(update_exchanges)

    def get_cryptocurrencies(self):
        return [
            BitcoinLogo(),
            BitcoinLogo(),
            BitcoinLogo(),
            EthereumLogo(),
            LitecoinLogo()
        ]

    def get_currencies(self):
        return [
            OldTex("\\$").set_color(GREEN),
            OldTex("\\$").set_color(GREEN),
            OldTex("\\$").set_color(GREEN),
            SVGMobject(
                file_name = "euro_symbol",
                stroke_width = 0,
                fill_opacity = 1,
                fill_color = BLUE,
            ),
            SVGMobject(
                file_name = "yen_symbol",
                stroke_width = 0,
                fill_opacity = 1,
                fill_color = RED,
            )
        ]
