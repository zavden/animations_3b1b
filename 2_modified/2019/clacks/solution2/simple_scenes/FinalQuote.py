# ==============================================================================
# Scene:      FinalQuote
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 600-631)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/lost_lecture.py
#
# Run from this folder:
#     manimgl FinalQuote.py FinalQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject


# ----- From _2018/lost_lecture.py -----

class ShowWord(Animation):
    CONFIG = {
        "time_per_char": 0.06,
        "rate_func": linear,
    }

    def __init__(self, word, **kwargs):
        assert(isinstance(word, SingleStringTex))
        digest_config(self, kwargs)
        run_time = kwargs.pop(
            "run_time",
            self.time_per_char * len(word)
        )
        self.stroke_width = word.get_stroke_width()
        Animation.__init__(self, word, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha):
        word = self.mobject
        stroke_width = self.stroke_width
        count = int(alpha * len(word))
        remainder = (alpha * len(word)) % 1
        word[:count].set_fill(opacity=1)
        word[:count].set_stroke(width=stroke_width)
        if count < len(word):
            word[count].set_fill(opacity=remainder)
            word[count].set_stroke(width=remainder * stroke_width)
            word[count + 1:].set_fill(opacity=0)
            word[count + 1:].set_stroke(width=0)



# ----- From _2019/clacks/solution2/simple_scenes.py -----

class FinalQuote(Scene):
    def construct(self):
        quote_text = """
            A change of perspective\\\\
            is worth 80 IQ points.
        """
        quote_parts = [s for s in quote_text.split(" ") if s]
        quote = OldTexText(
            *quote_parts,
        )
        quote.scale(1.2)
        quote.shift(2 * RIGHT + UP)

        image = ImageMobject("AlanKay")
        image.set_height(6)
        image.to_corner(UL)
        image.shift(2 * LEFT + 0.5 * UP)
        name = OldTexText("Alan Kay")
        name.scale(1.5)
        name.next_to(image, DOWN)
        name.shift_onto_screen()

        self.play(
            FadeInFromDown(image),
            Write(name),
        )
        self.wait()

        for word in quote:
            self.play(ShowWord(word))
            self.wait(0.005 * len(word)**1.5)
        self.wait()
