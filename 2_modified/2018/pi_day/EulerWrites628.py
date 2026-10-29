# ==============================================================================
# Scene:      EulerWrites628
# Source:     videos/_2018/pi_day.py (lines 472-550)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EulerWrites628.py EulerWrites628 -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/replacement images made by _lib/assets/generated/2018/pi_day/make_pi_day_assets.py (Handmann portrait copy, pixelated/revealed variants, placeholder printed pages)
#
# Notes:
#   Uses MEDIA_DIR (defined in cairo_compat) + file lookup by name in _lib/assets/raster_images.
# ==============================================================================

from manim_imports_ext import *

RESOURCE_DIR = os.path.join(MEDIA_DIR, "3b1b_videos", "π Day 2018", "images")


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


class EulerWrites628(Scene):
    CONFIG = {
        "camera_config" : {
            "background_opacity" : 1,
        }
    }
    def construct(self):
        image = ImageMobject(os.path.join(RESOURCE_DIR, "dalembert_zoom"))
        image.set_width(FRAME_WIDTH - 1)
        image.to_edge(UP, buff = MED_SMALL_BUFF)
        image.fade(0.15)
        rect = Rectangle(
            width = 12, 
            height = 0.5,
            stroke_width = 0,
            fill_opacity = 0.3,
            fill_color = GREEN,
        )
        rect.insert_n_curves(20)
        rect.apply_function(lambda p : np.array([p[0], p[1] - 0.005*p[0]**2, p[2]]))
        rect.rotate(0.012*TAU)
        rect.move_to(image)
        rect.shift(0.15*DOWN)

        words = OldTexText(
            "``Let", "$\\pi$", "be the", "circumference", 
            "of a circle whose", "radius = 1''",
        )
        words.set_color_by_tex_to_color_map({
            "circumference" : YELLOW,
            "radius" : GREEN,
        })
        words.next_to(image, DOWN)
        pi = words.get_part_by_tex("\\pi").copy()

        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 1, 
            positioning_func = lambda circ : circ.next_to(words, DOWN, buff = 1.25)
        )
        circle, radius, one, decimal = terms

        unwrapped_perimeter = Line(ORIGIN, TAU*RIGHT)
        unwrapped_perimeter.match_style(circle)
        unwrapped_perimeter.next_to(circle, DOWN)
        brace = Brace(unwrapped_perimeter, UP, buff = SMALL_BUFF)

        perimeter = OldTex(
            "\\pi\\epsilon\\rho\\iota\\mu\\epsilon\\tau\\rho\\text{o}\\varsigma",
            "\\text{ (perimeter)}",
            "="
        )
        perimeter.next_to(brace, UP, submobject_to_align = perimeter[1], buff = SMALL_BUFF)
        perimeter[0][0].set_color(GREEN)

        self.play(FadeInFromDown(image))
        self.play(
            Write(words), 
            GrowFromPoint(rect, rect.point_from_proportion(0.9))
        )
        self.wait()
        self.play(*generate_anims1())
        self.play(*generate_anims2())
        self.play(terms.shift, UP)
        self.play(
            pi.scale, 2,
            pi.shift, DOWN, 
            pi.set_color, GREEN
        )
        self.wait()
        self.play(
            GrowFromCenter(brace),
            circle.set_stroke, YELLOW, 1,
            ReplacementTransform(circle.copy(), unwrapped_perimeter),
            decimal.scale, 1.25,
            decimal.next_to, perimeter[-1].get_right(), RIGHT,
            ReplacementTransform(pi, perimeter[0][0]),
            Write(perimeter),
        )
        self.wait()
