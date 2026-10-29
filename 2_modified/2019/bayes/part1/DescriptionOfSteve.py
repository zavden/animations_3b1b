# ==============================================================================
# Scene:      DescriptionOfSteve
# Source:     videos/_2019/bayes/part1.py (lines 907-1019)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DescriptionOfSteve.py DescriptionOfSteve -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
# ==============================================================================

from manim_imports_ext import *

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
