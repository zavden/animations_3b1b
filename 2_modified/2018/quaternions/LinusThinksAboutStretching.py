# ==============================================================================
# Scene:      LinusThinksAboutStretching
# Source:     videos/_2018/quaternions.py (lines 2174-2228)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LinusThinksAboutStretching.py LinusThinksAboutStretching -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL calls mob.copy(deep=...) (generate_target, play(mob.method)); accept the keyword in the Linus override
# ==============================================================================

from manim_imports_ext import *

class Linus(VGroup):
    CONFIG = {
        "body_config": {
            "stroke_width": 15,
            "stroke_color": GREY_B,
            "sheen": 0.4,
        },
        "height": 2,
    }

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.body = self.get_body_line()
        self.eyes = Eyes(self.body)

        self.add(self.body, self.eyes)
        self.set_height(self.height)
        self.center()

    def change_mode(self, mode, thing_to_look_at=None):
        self.eyes.change_mode(mode, thing_to_look_at)
        if mode == "sad":
            self.become_squiggle()
        elif mode == "confused":
            self.become_squiggle(factor=-0.1)
        elif mode == "pleading":
            self.become_squiggle(factor=0.3)
        else:
            self.become_line()
        return self

    def change(self, *args, **kwargs):
        self.change_mode(*args, **kwargs)
        return self

    def look_at(self, thing_to_look_at=None):
        self.eyes.look_at(thing_to_look_at)
        return self

    def blink(self):
        self.eyes.blink()
        return self

    def get_squiggle(self, factor=0.2):
        sine_curve = FunctionGraph(
            lambda x: factor * np.sin(x),
            x_min=0, x_max=TAU,
        )
        sine_curve.rotate(TAU / 4)
        sine_curve.match_style(self.body)
        sine_curve.match_height(self.body)
        sine_curve.move_to(self.body, UP)
        return sine_curve

    def get_body_line(self, **kwargs):
        config = dict(self.body_config)
        config.update(kwargs)
        line = Line(ORIGIN, 1.5 * UP, **config)
        if hasattr(self, "body"):
            line.match_style(self.body)
            line.match_height(self.body)
            line.move_to(self.body, UP)
        return line

    def become_squiggle(self, **kwargs):
        self.body.become(self.get_squiggle(**kwargs))
        return self

    def become_line(self, **kwargs):
        self.body.become(self.get_body_line(**kwargs))
        return self

    # CHANGE: GL calls mob.copy(deep=...) (generate_target, play(mob.method)); accept the keyword in the Linus override
    def copy(self, deep=False):
        return self.deepcopy()


class LinusThinksAboutStretching(Scene):
    def construct(self):
        linus = Linus()
        top_line = NumberLine(color=GREY)
        top_line.to_edge(UP)
        top_line.add_numbers()

        linus.move_to(3 * LEFT + DOWN)

        self.add(linus, top_line)

        scalars = [3, 0.5, 2]

        for scalar in scalars:
            lower_line = NumberLine(
                x_min=-14,
                x_max=14,
                color=BLUE
            )
            lower_line.next_to(top_line, DOWN, MED_LARGE_BUFF)
            lower_line.numbers = lower_line.get_number_mobjects()
            for number in lower_line.numbers:
                number.add_updater(lambda m: m.next_to(
                    lower_line.number_to_point(m.get_value()),
                    DOWN, MED_SMALL_BUFF,
                ))
            lower_line.save_state()
            lower_line.numbers.save_state()
            self.add(lower_line, *lower_line.numbers)

            words = OldTexText("Multiply by {}".format(scalar))
            words.next_to(lower_line.numbers, DOWN)

            self.play(
                ApplyMethod(
                    lower_line.stretch, scalar, 0,
                    run_time=2
                ),
                # LaggedStartMap(FadeIn, words, run_time=1),
                FadeInFromLarge(words, 1.0 / scalar),
                linus.look_at, top_line.number_to_point(scalar)
            )
            self.play(Blink(linus))
            self.play(
                FadeOut(lower_line),
                FadeOut(lower_line.numbers),
                FadeOut(words),
                FadeIn(lower_line.saved_state, remover=True),
                FadeIn(lower_line.numbers.saved_state, remover=True),
                linus.look_at, top_line.number_to_point(0)
            )
        self.play(linus.change, "confused", DOWN + RIGHT)
        self.wait(2)
        self.play(Blink(linus))
        self.wait(2)
