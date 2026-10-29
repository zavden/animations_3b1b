# ==============================================================================
# Scene:      FeynmanElementaryQuote
# Source:     videos/_2018/lost_lecture.py (lines 991-1084)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FeynmanElementaryQuote.py FeynmanElementaryQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo accepted the color name string "RED"; GL needs the RED constant
# ==============================================================================

from manim_imports_ext import *

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


class FeynmanElementaryQuote(Scene):
    def construct(self):
        quote_text = """
            \\large
            I am going to give what I will call an
            \\emph{elementary} demonstration.  But elementary
            does not mean easy to understand.  Elementary
            means that very little is required
            to know ahead of time in order to understand it,
            except to have an infinite amount of intelligence.
        """
        quote_parts = [s for s in quote_text.split(" ") if s]
        quote = OldTexText(
            *quote_parts,
            tex_to_color_map={
                "\\emph{elementary}": BLUE,
                "elementary": BLUE,
                "Elementary": BLUE,
                "infinite": YELLOW,
                "amount": YELLOW,
                "of": YELLOW,
                "intelligence": YELLOW,
                "very": RED,
                "little": RED,
            },
            alignment=""
        )
        quote[-1].shift(2 * SMALL_BUFF * LEFT)
        quote.set_width(FRAME_WIDTH - 1)
        quote.to_edge(UP)
        quote.get_part_by_tex("of").set_color(WHITE)

        nothing = OldTexText("nothing")
        nothing.scale(0.9)
        very = quote.get_part_by_tex("very")
        nothing.shift(very[0].get_left() - nothing[0].get_left())
        nothing.set_color(RED)

        for word in quote:
            if word is very:
                self.add_foreground_mobjects(nothing)
                self.play(ShowWord(nothing))
                self.wait(0.2)
                nothing.sort(lambda p: -p[0])
                self.play(LaggedStartMap(
                    FadeOut, nothing,
                    run_time=1
                ))
                self.remove_foreground_mobject(nothing)
            back_word = word.copy().set_stroke(BLACK, 5)
            self.add_foreground_mobjects(back_word, word)
            self.play(
                ShowWord(back_word),
                ShowWord(word),
            )
            self.wait(0.005 * len(word)**1.5)
        self.wait()

        # Show thumbnails
        images = Group(
            ImageMobject("Calculus_Thumbnail"),
            ImageMobject("Fourier_Thumbnail"),
        )
        for image in images:
            image.set_height(3)
        images.arrange(RIGHT, buff=LARGE_BUFF)
        images.to_edge(DOWN, buff=LARGE_BUFF)
        images[1].move_to(images[0])
        crosses = VGroup(*list(map(Cross, images)))
        # CHANGE: Cairo accepted the color name string "RED"; GL needs the RED constant
        crosses.set_stroke(RED, 10)

        for image, cross in zip(images, crosses):
            image.rect = SurroundingRectangle(
                image,
                stroke_width=3,
                stroke_color=WHITE,
                buff=0
            )
            cross.scale(1.1)
        self.play(
            FadeInFromDown(images[0]),
            FadeInFromDown(images[0].rect)
        )
        self.play(ShowCreation(crosses[0]))
        self.wait()
        self.play(
            FadeOutAndShiftDown(images[0]),
            FadeOutAndShiftDown(images[0].rect),
            FadeOutAndShiftDown(crosses[0]),
            FadeInFromDown(images[1]),
            FadeInFromDown(images[1].rect),
        )
        self.play(ShowCreation(crosses[1]))
        self.wait()
