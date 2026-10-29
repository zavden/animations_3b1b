# ==============================================================================
# Scene:      Poem
# Source:     videos/_2018/turbulence.py (lines 1361-1387)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/lost_lecture.py
#
# Run from this folder:
#     manimgl Poem.py Poem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


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



# ----- From _2018/turbulence.py -----

class Poem(Scene):
    def construct(self):
        picture = ImageMobject("Lewis_Richardson")
        picture.set_height(4)
        picture.center().to_edge(LEFT, buff=LARGE_BUFF)

        title = OldTexText("Poem by Lewis F. Richardson")
        title.to_edge(UP)

        poem_text = """
            Big{\\,\\,}whirls have little{\\,\\,}whirls\\\\
            which feed on their velocity,\\\\
            And little{\\,\\,}whirls have lesser{\\,\\,}whirls\\\\
            And so on to viscosity.\\\\
        """
        poem_words = [s for s in poem_text.split(" ") if s]
        poem = OldTexText(*poem_words, alignment="")
        poem.next_to(picture, RIGHT, LARGE_BUFF)

        self.add(picture)
        self.play(FadeIn(title, DOWN))
        self.wait()
        for word in poem:
            if "whirl" in word.get_tex():
                word.set_color(BLUE)
            self.play(ShowWord(word))
            self.wait(0.005 * len(word)**1.5)
