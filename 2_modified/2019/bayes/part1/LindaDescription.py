# ==============================================================================
# Scene:      LindaDescription
# Source:     videos/_2019/bayes/part1.py (lines 3561-3584)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LindaDescription.py LindaDescription -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class ProbabilityBar(VGroup):
    CONFIG = {
        "color1": BLUE_D,
        "color2": GREY_BROWN,
        "height": 0.5,
        "width": 6,
        "rect_style": {
            "stroke_width": 1,
            "stroke_color": WHITE,
            "fill_opacity": 1,
        },
        "include_braces": False,
        "brace_direction": UP,
        "include_percentages": True,
        "percentage_background_stroke_width": 2,
    }

    def __init__(self, p=0.5, **kwargs):
        super().__init__(**kwargs)
        self.add_backbone()
        self.add_p_tracker(p)
        self.add_bars()
        if self.include_braces:
            self.braces = always_redraw(lambda: self.get_braces())
            self.add(self.braces)
        if self.include_percentages:
            self.percentages = always_redraw(lambda: self.get_percentages())
            self.add(self.percentages)

    def add_backbone(self):
        backbone = Line()
        backbone.set_opacity(0)
        backbone.set_width(self.width)
        self.backbone = backbone
        self.add(backbone)

    def add_p_tracker(self, p):
        self.p_tracker = ValueTracker(p)

    def add_bars(self):
        bars = VGroup(Rectangle(), Rectangle())
        bars.set_height(self.height)
        colors = [self.color1, self.color2]
        for bar, color in zip(bars, colors):
            bar.set_style(**self.rect_style)
            bar.set_fill(color=color)

        bars.add_updater(self.update_bars)
        self.bars = bars
        self.add(bars)

    def update_bars(self, bars):
        vects = [LEFT, RIGHT]
        p = self.p_tracker.get_value()
        values = [p, 1 - p]
        total_width = self.backbone.get_width()
        for bar, vect, value in zip(bars, vects, values):
            bar.set_width(value * total_width, stretch=True)
            bar.move_to(self.backbone, vect)
        return bars

    def get_braces(self):
        return VGroup(*[
            Brace(
                bar,
                self.brace_direction,
                min_num_quads=1,
                buff=SMALL_BUFF,
            )
            for bar in self.bars
        ])

    def get_percentages(self):
        p = self.p_tracker.get_value()
        labels = VGroup(*[
            Integer(value, unit="\\%")
            for value in [
                np.floor(p * 100),
                100 - np.floor(p * 100),
            ]
        ])
        for label, bar in zip(labels, self.bars):
            label.set_height(0.75 * bar.get_height())
            min_width = 0.75 * bar.get_width()
            if label.get_width() > min_width:
                label.set_width(min_width)
            label.move_to(bar)
            label.set_stroke(
                BLACK,
                self.percentage_background_stroke_width,
                background=True
            )
        return labels

    def add_icons(self, *icons, buff=SMALL_BUFF):
        if hasattr(self, "braces"):
            refs = self.braces
        else:
            refs = self.bars

        for icon, ref in zip(icons, refs):
            icon.ref = ref
            icon.add_updater(lambda i: i.next_to(
                i.ref,
                self.brace_direction,
                buff=buff
            ))
        self.icons = VGroup(*icons)
        self.add(self.icons)


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class Steve(SVGMobject):
    CONFIG = {
        "file_name": "steve",
        "fill_color": GREY,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "stroke_width": 0,
        "height": 3,
        "include_name": True,
        "name": "Steve"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.include_name:
            self.add_name()

    def add_name(self):
        self.name = OldTexText(self.name)
        self.name.match_width(self)
        self.name.next_to(self, DOWN, SMALL_BUFF)
        self.add(self.name)


class Linda(Steve):
    CONFIG = {
        "file_name": "linda",
        "name": "Linda"
    }


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class LibrarianIcon(SVGMobject):
    CONFIG = {
        "file_name": "book",
        "stroke_width": 0,
        "fill_color": GREY_B,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 0.75,
    }


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class FarmerIcon(SVGMobject):
    CONFIG = {
        "file_name": "farming",
        "stroke_width": 0,
        "fill_color": GREEN_E,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 1.5,
    }


class DescriptionOfSteve(Scene):
    def construct(self):
        self.write_description()
        self.compare_probabilities()

    def write_description(self):
        steve = Steve(height=3)
        steve.to_corner(UR)

        description = self.get_description()
        description.to_edge(LEFT)
        description.align_to(steve, UP)

        mt_parts = VGroup(
            description.get_part_by_tex("meek"),
            description.get_part_by_tex("soul"),
        )
        mt_parts.set_color(WHITE)

        self.add(steve)
        self.play(
            FadeIn(description),
            run_time=3,
            lag_ratio=0.01,
            rate_func=linear,
        )
        self.wait(3)

        lines = VGroup(*[
            Line(mob.get_corner(DL), mob.get_corner(DR), color=YELLOW)
            for mob in mt_parts
        ])
        self.play(
            ShowCreation(lines),
            mt_parts.set_color, YELLOW,
        )
        self.play(FadeOut(lines))
        self.wait()

    def compare_probabilities(self):
        bar = ProbabilityBar(
            0.5, width=10,
            include_braces=True,
            percentage_background_stroke_width=2,
        )
        icons = VGroup(
            LibrarianIcon(),
            FarmerIcon(),
        )
        for icon, text, half in zip(icons, ["Librarian", "Farmer"], bar.bars):
            icon.set_height(0.7)
            label = OldTexText(text)
            label.next_to(icon, DOWN, buff=SMALL_BUFF)
            label.set_color(
                interpolate_color(half.get_color(), WHITE, 0.5)
            )
            icon.add(label)

        bar.add_icons(*icons)
        bar.move_to(1.75 * DOWN)

        bar.icons.set_opacity(0)

        q_marks = OldTex(*"???")
        q_marks.scale(1.5)
        q_marks.space_out_submobjects(1.5)
        q_marks.next_to(bar, DOWN)

        self.play(FadeIn(bar))
        self.wait()
        self.play(
            bar.p_tracker.set_value, 0.9,
            bar.icons[0].set_opacity, 1,
        )
        self.wait()
        self.play(
            bar.p_tracker.set_value, 0.1,
            bar.icons[1].set_opacity, 1,
        )
        self.play(
            LaggedStartMap(
                FadeInFrom, q_marks,
                lambda m: (m, UP),
                run_time=2,
            ),
            ApplyMethod(
                bar.p_tracker.set_value, 0.7,
                run_time=8,
            )
        )
        for value in 0.3, 0.7:
            self.play(
                bar.p_tracker.set_value, 0.3,
                run_time=7,
            )

    def get_description(self):
        return OldTexText(
            """
            Steve is very shy and withdrawn,\\\\
            invariably helpful but with very\\\\
            little interest in people or in the\\\\
            world of reality. A meek and tidy\\\\
            soul, he has a need for order and\\\\
            structure, and a passion for detail.\\\\
            """,
            tex_to_color_map={
                "shy and withdrawn": BLUE,
                "meek and tidy": YELLOW,
                "soul": YELLOW,
            },
            alignment="",
        )


class IntroduceLinda(DescriptionOfSteve):
    def construct(self):
        # Kahneman and Tversky
        images = self.get_images()

        self.play(
            LaggedStartMap(
                FadeInFrom, images,
                lambda m: (m, LEFT),
                lag_ratio=0.3,
                run_time=3,
            )
        )
        self.wait()

        # Add steve
        steve = Steve()
        steve.set_height(3)
        steve.move_to(2 * RIGHT)
        steve.to_edge(DOWN, buff=LARGE_BUFF)
        steve_words = self.get_description()
        steve_words.scale(0.8)
        steve_words.next_to(steve, UP, LARGE_BUFF)

        self.play(LaggedStart(
            FadeIn(steve, LEFT),
            FadeIn(steve_words, LEFT),
        ))
        self.wait()

        # Replace with Linda
        linda = Linda()
        linda_words = self.get_linda_description()
        linda_words.scale(0.8)
        linda.replace(steve)
        linda_words.move_to(steve_words)

        self.play(
            LaggedStart(
                FadeOut(steve_words, 2 * RIGHT),
                FadeOut(steve, 2 * RIGHT),
                FadeIn(linda, 2 * LEFT),
                lag_ratio=0.15,
            )
        )
        self.wait()

        self.play(
            FadeIn(linda_words),
            lag_ratio=0.1,
            run_time=6,
            rate_func=linear,
        )
        self.wait()

        # Ask question
        options = VGroup(
            OldTexText("1) Linda is a bank teller."),
            OldTexText(
                "2) Linda is a bank teller and is active\\\\",
                "\\phantom{2)} in the feminist movement.",
                alignment="",
            ),
        )
        options.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        options.to_edge(DOWN, buff=LARGE_BUFF)

        self.play(
            linda.match_height, linda_words,
            linda.next_to, linda_words, LEFT, LARGE_BUFF,
            LaggedStartMap(
                FadeOutAndShift, images,
                lambda m: (m, 2 * LEFT),
            )
        )
        for option in options:
            self.play(FadeIn(option, lag_ratio=0.1, run_time=2))
            self.wait()

        # Show result
        rect = SurroundingRectangle(options[1], color=RED)
        options.generate_target()
        rect.generate_target()
        VGroup(options.target, rect.target).to_edge(LEFT)

        result = VGroup(
            Integer(85, unit="\\%"),
            OldTexText("chose this!")
        )
        result.arrange(RIGHT)
        result.scale(1.25)
        result.set_color(RED)
        result.move_to(rect)
        result.to_edge(RIGHT)
        result.shift(2 * UP)
        arrow = Arrow(result.get_bottom(), rect.target.get_corner(UR))

        self.play(
            MoveToTarget(options),
            MoveToTarget(rect),
            VFadeIn(rect),
            FadeIn(result, LEFT),
            GrowArrow(arrow)
        )
        self.wait()

        # Show subsets
        fb_words = OldTexText("Active feminist\\\\bank tellers")
        fb_words.scale(0.5)
        fb_words.set_stroke(BLACK, 0, background=True)
        fb_set = Circle()
        fb_set.flip(RIGHT)
        fb_set.rotate(3 * TAU / 8)
        fb_set.set_stroke(WHITE, 1)
        fb_set.set_fill(YELLOW, 0.5)
        fb_set.replace(fb_words, stretch=True)
        fb_set.scale(1.2)
        fb_set.stretch(1.4, 1)
        fb_group = VGroup(fb_set, fb_words)
        fb_group.move_to(linda_words, RIGHT)

        b_set = fb_set.copy()
        b_set.set_fill(BLUE)
        b_set.scale(3, about_edge=RIGHT)
        b_set.stretch(1.5, 1)
        b_set.to_corner(UR)
        b_words = OldTexText("Bank\\\\tellers")
        b_words.next_to(b_set.get_left(), RIGHT, LARGE_BUFF)

        self.play(
            FadeOut(linda_words),
            TransformFromCopy(rect, fb_set),
            ReplacementTransform(
                VectorizedPoint(rect.get_center()),
                fb_words,
            ),
        )
        self.add(fb_set, fb_words)
        self.wait()
        self.add(b_set, fb_set, fb_words)
        self.play(
            DrawBorderThenFill(b_set),
            TransformFromCopy(
                options[0][0][10:], b_words[0]
            ),
        )
        sets_group = VGroup(b_set, b_words, fb_set, fb_words)
        self.add(sets_group)
        self.wait()

        # Reduce 85
        number = result[0]

        self.play(
            LaggedStart(
                FadeOut(arrow),
                FadeOut(result[1]),
                FadeOut(rect),
                FadeOut(options[0]),
                FadeOut(options[1]),
            ),
            number.scale, 1.5,
            number.move_to, DOWN,
        )
        self.play(
            ChangeDecimalToValue(number, 0),
            UpdateFromAlphaFunc(
                number,
                lambda m, a: m.set_color(interpolate_color(
                    RED, GREEN, a,
                ))
            ),
            run_time=2,
        )
        self.wait()

        self.play(
            FadeOut(number),
            FadeOut(sets_group),
            FadeIn(linda_words),
        )

        # New options
        words = OldTexText("100 people fit this description.  How many are:")
        words.set_color(BLUE_B)
        kw = {"tex_to_color_map": {"\\underline{\\qquad}": WHITE}}
        new_options = VGroup(
            OldTexText("1) Bank tellers? \\underline{\\qquad} of 100", **kw),
            OldTexText(
                "2) Bank tellers and active in the",
                " feminist movement? \\underline{\\qquad} of 100",
                **kw
            ),
        )
        new_options.scale(0.9)
        new_options.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        new_options.to_edge(DOWN, buff=LARGE_BUFF)

        words.next_to(new_options, UP, LARGE_BUFF)

        self.play(
            FadeIn(words, lag_ratio=0.1, rate_func=linear)
        )
        self.wait()
        for option in new_options:
            self.play(FadeIn(option))
            self.wait()

        example_numbers = VGroup(Integer(8), Integer(5))
        for exn, option in zip(example_numbers, new_options):
            line = option.get_part_by_tex("underline")
            exn.scale(1.1)
            exn.next_to(line, UP, buff=0.05)
            exn.set_color(YELLOW)
            self.play(Write(exn))
        self.wait()

    def get_images(self):
        images = Group(
            ImageMobject("kahneman"),
            ImageMobject("tversky"),
        )
        images.set_height(3.5)
        images.arrange(DOWN, buff=0.5)
        images.to_edge(LEFT, buff=MED_LARGE_BUFF)

        names = VGroup(
            OldTexText("Kahneman", alignment=""),
            OldTexText("Tversky", alignment=""),
        )
        for name, image in zip(names, images):
            name.next_to(image, DOWN)
            image.name = name
            image.add(name)
        images.arrange(DOWN, buff=1, aligned_edge=LEFT)
        images.set_height(FRAME_HEIGHT - 1)
        images.to_edge(LEFT)
        return images

    def get_linda_description(self):
        result = OldTexText(
            "Linda is 31 years old, single, outspoken, and\\\\",
            "very bright. She majored in philosophy. As a \\\\",
            "student, she was deeply concerned with issues\\\\",
            "of discrimination and social justice, and also\\\\",
            "participated in anti-nuclear demonstrations.\\\\",
            alignment="",
            tex_to_color_map={
                "deeply concerned with issues": YELLOW,
                "of discrimination": YELLOW,
            }
        )
        return result


class LindaDescription(IntroduceLinda):
    def construct(self):
        words = self.get_linda_description()
        words.set_color(WHITE)

        highlighted_part = VGroup(
            *words.get_part_by_tex("deeply"),
            *words.get_part_by_tex("discrimination"),
        )

        self.add(words)
        self.play(
            FadeIn(words),
            run_time=3,
            lag_ratio=0.01,
            rate_func=linear,
        )
        self.wait(1)
        self.play(
            highlighted_part.set_color, YELLOW,
            lag_ratio=0.1,
            run_time=2
        )
        self.wait()
