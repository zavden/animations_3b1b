# ==============================================================================
# Scene:      AnalysisQuote
# Source:     videos/_2018/pi_day.py (lines 148-175)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AnalysisQuote.py AnalysisQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - align_to(alignment_vect=) kwarg removed: GL does not accept it and Cairo ignored it (no-op)
#
# Placeholder assets (not Grant's originals):
#   - raster_images/replacement images made by _lib/assets/generated/2018/pi_day/make_pi_day_assets.py (Handmann portrait copy, pixelated/revealed variants, placeholder printed pages)
#
# Notes:
#   Uses MEDIA_DIR (defined in cairo_compat) + file lookup by name in _lib/assets/raster_images.
# ==============================================================================

from manim_imports_ext import *

HIGHLIGHT_COLOR = YELLOW


class AnalysisQuote(Scene):

    def construct(self):

        text = OldTexText('``We therefore set the radius of \\\\'\
         'the circle\dots to be = 1, and \dots\\\\'\
         'through approximations the \\\\'\
         'semicircumference of said circle  \\\\'\
         'has been found to be $= 3.14159\dots$,\\\\'\
         'for which number, for the sake of \\\\'\
         'brevity, I will write $\pi$\dots"',
         alignment = '')
        for char in text.submobjects[12:24]:
            char.set_fill(HIGHLIGHT_COLOR)
        for char in text.submobjects[42:44]:
            char.set_fill(HIGHLIGHT_COLOR)
        for char in text.submobjects[75:92]:
            char.set_fill(HIGHLIGHT_COLOR)
        for char in text.submobjects[120:131]:
            char.set_fill(HIGHLIGHT_COLOR)
        text.submobjects[-5].set_fill(HIGHLIGHT_COLOR)

        text.to_edge(LEFT, buff = 1)

        self.play(LaggedStartMap(FadeIn,text), run_time = 5)
        self.wait()
        self.play(FadeOut(text))
        self.wait()


RESOURCE_DIR = os.path.join(MEDIA_DIR, "3b1b_videos", "π Day 2018", "images")


def get_image(name):
    return ImageMobject(os.path.join(RESOURCE_DIR, name))


def get_circle_drawing_terms(radius = 1, positioning_func = lambda m : m.center()):
    circle = Circle(color = YELLOW, radius = 1.25)
    positioning_func(circle)
    radius = Line(circle.get_center(), circle.get_points()[0])
    radius.set_color(WHITE)
    one = OldTex("1")
    one.scale(0.75)
    one_update = UpdateFromFunc(
        one, lambda m : m.move_to(
            radius.get_center() + \
            0.25*rotate_vector(radius.get_vector(), TAU/4)
        ),
    )
    decimal = DecimalNumber(0, num_decimal_places = 4, show_ellipsis = True)
    decimal.scale(0.75)
    def reposition_decimal(decimal):
        vect = radius.get_vector()
        unit_vect = vect/get_norm(vect)
        angle = radius.get_angle()
        alpha = (-np.cos(2*angle) + 1)/2
        interp_length = interpolate(decimal.get_width(), decimal.get_height(), alpha)
        buff = interp_length/2 + MED_SMALL_BUFF
        decimal.move_to(radius.get_end() + buff*unit_vect)
        decimal.shift(UP*decimal.get_height()/2)
        return decimal

    kwargs = {"run_time" : 3, "rate_func" : bezier([0, 0, 1, 1])} 
    changing_decimal = ChangingDecimal(
        decimal, lambda a : a*TAU,
        position_update_func = reposition_decimal,
        **kwargs
    )

    terms = VGroup(circle, radius, one, decimal)
    generate_anims1 = lambda : [ShowCreation(radius), Write(one)]
    generate_anims2 = lambda : [
        ShowCreation(circle, **kwargs),
        Rotating(radius, about_point = radius.get_start(), **kwargs),
        changing_decimal,
        one_update,
    ]

    return terms, generate_anims1, generate_anims2


class AnalysisQuote(Scene):
    def construct(self):
        analysis = get_image("Analysis_page_showing_pi")
        analysis.set_height(FRAME_HEIGHT)
        analysis.to_edge(LEFT, buff = 0)

        text = OldTexText(
            "``\\dots set the radius of",
            "the circle\\dots to be = 1, \\dots \\\\",
            "through approximations the",
            "semicircumference \\\\", "of said circle",
            "has been found to be", "$= 3.14159\\dots$,\\\\",
            "for which number, for the sake of",
            "brevity, \\\\ I will write", "$\pi$\\dots''",
            alignment = ''
        )
        pi_formula = OldTex(
            "\\pi", "=", "{ \\text{semicircumference}", "\\over", "\\text{radius}}"
        )
        text.set_width(FRAME_X_RADIUS)
        text.next_to(analysis, RIGHT, LARGE_BUFF)
        text.to_edge(UP)

        HIGHLIGHT_COLOR= GREEN
        for mob in text, pi_formula:
            mob.set_color_by_tex_to_color_map({
                "semicircumference" : HIGHLIGHT_COLOR,
                "3.14" : HIGHLIGHT_COLOR,
                "\pi" : HIGHLIGHT_COLOR
            })

        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 1,
            positioning_func = lambda circ : circ.next_to(text, DOWN, LARGE_BUFF)
        )
        terms[0].set_color(HIGHLIGHT_COLOR)
        terms[-1].set_color(HIGHLIGHT_COLOR)

        pi_formula.next_to(terms, DOWN, buff = 0)
        # CHANGE: align_to(alignment_vect=) is not accepted by GL; in Cairo that kwarg was ignored (only direction aligned), so the call was a no-op
        pi_formula.align_to(text)
        pi_formula[0].scale(2, about_edge = RIGHT)

        self.add(analysis)
        self.play(*generate_anims2(), rate_func = lambda t : 0.5*smooth(t))
        self.play(LaggedStartMap(FadeIn,text), run_time = 5)
        self.play(FadeIn(pi_formula))
        self.wait()
