# ==============================================================================
# Scene:      LockhartQuote
# Source:     videos/_2018/dandelin.py (lines 1457-1520)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/lost_lecture.py
#
# Run from this folder:
#     manimgl LockhartQuote.py LockhartQuote -w -m --fps 15
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



# ----- From _2018/dandelin.py -----

class LockhartQuote(Scene):
    CONFIG = {
        "camera_config": {"background_opacity": 1}
    }

    def construct(self):
        mb_string = "Madame\\,\\,Bovary"
        ml_string = "Mona\\,\\,Lisa."
        strings = (mb_string, ml_string)
        quote_text = """
            \\large
            How do people come up with such ingenious arguments?
            It's the same way people come up with %s or %s
            I have no idea how it happens.  I only know that
            when it happens to me, I feel very fortunate.
        """ % strings
        quote_parts = [s for s in quote_text.split(" ") if s]
        quote = OldTexText(
            *quote_parts,
            tex_to_color_map={
                mb_string: BLUE,
                ml_string: YELLOW,
            },
            alignment=""
        )
        quote.set_width(FRAME_WIDTH - 2)
        quote.to_edge(UP)

        measurement = ImageMobject("MeasurementCover")
        madame_bovary = ImageMobject("MadameBovary")
        mona_lisa = ImageMobject("MonaLisa")
        pictures = Group(measurement, madame_bovary, mona_lisa)
        for picture in pictures:
            picture.set_height(4)
        pictures.arrange(RIGHT, buff=LARGE_BUFF)
        pictures.to_edge(DOWN)

        measurement.save_state()
        measurement.set_width(FRAME_WIDTH)
        measurement.center()
        measurement.fade(1)
        self.play(Restore(measurement))
        self.wait()
        for word in quote:
            anims = [ShowWord(word)]
            for text, picture in zip(strings, pictures[1:]):
                if word is quote.get_part_by_tex(text):
                    anims.append(FadeInFromDown(
                        picture, run_time=1
                    ))
            self.play(*anims)
            self.wait(0.005 * len(word)**1.5)
        self.wait(2)
        self.play(
            LaggedStartMap(
                FadeOutAndShiftDown, quote,
                lag_ratio=0.2,
                run_time=5,
            ),
            LaggedStartMap(
                FadeOutAndShiftDown, pictures,
                run_time=3,
            ),
        )
