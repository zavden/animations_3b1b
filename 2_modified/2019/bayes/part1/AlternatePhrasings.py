# ==============================================================================
# Scene:      AlternatePhrasings
# Source:     videos/_2019/bayes/part1.py (lines 3587-3678)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AlternatePhrasings.py AlternatePhrasings -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
#   - Keep the column order and Cairo spacing in the grid so that the indices of people and cells correspond to the right region.
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


class Linda(Steve):
    CONFIG = {
        "file_name": "linda",
        "name": "Linda"
    }


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class Person(SVGMobject):
    CONFIG = {
        "file_name": "person",
        "height": 1.5,
        "stroke_width": 0,
        "fill_opacity": 1,
        "fill_color": GREY_B,
    }


class AlternatePhrasings(PiCreatureScene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E,
        }
    }

    def construct(self):
        randy = self.pi_creature

        phrases = VGroup(
            OldTexText("40 out of 100"),
            OldTex("40\\%"),
            OldTex("0.4"),
            OldTexText("What's more likely$\\dots$"),
        )
        for phrase in phrases:
            phrase.scale(1.5)
            phrase.next_to(randy, RIGHT, buff=LARGE_BUFF)
            phrase.align_to(randy, UP)

        def push_down(phrase):
            phrase.scale(0.8, about_edge=LEFT)
            phrase.shift(1 * DOWN)
            phrase.set_opacity(0.5)
            return phrase

        bubble = randy.get_bubble()
        content_width = 4.5

        people = VGroup(*[Person() for x in range(100)])
        # CHANGE: preserve Cairo column order and spacing for indexed grid members.
        cairo_arrange_in_grid(people, n_cols=20)
        people.set_width(content_width)
        people.move_to(bubble.get_bubble_center())
        people.shift(SMALL_BUFF * UP)
        people[:40].set_color(YELLOW)

        bar = ProbabilityBar(0.9999)
        bar.set_width(content_width)
        bar.move_to(people)

        steve = Steve()
        steve.set_height(1)
        steve_words = OldTexText("seems bookish...")
        steve_words.next_to(steve, RIGHT, MED_LARGE_BUFF)
        steve.add(steve_words)

        linda = Linda()
        linda.set_height(1)
        linda_words = OldTexText("seems activist...")
        linda_words.next_to(linda, RIGHT, MED_LARGE_BUFF)
        linda.add(linda_words)

        stereotypes = VGroup(steve, linda)
        stereotypes.arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        stereotypes.move_to(people)

        self.play(
            FadeIn(phrases[0], UP),
            randy.change, "pondering",
        )
        self.play(
            DrawBorderThenFill(bubble, lag_ratio=0.1),
            FadeIn(people, lag_ratio=0.1),
            randy.change, "thinking", people,
        )
        self.wait()
        self.play(
            FadeIn(phrases[1], UP),
            randy.change, "confused", phrases[1],
            FadeOut(people),
            ApplyFunction(push_down, phrases[0]),
            FadeIn(bar),
        )
        self.play(bar.p_tracker.set_value, 0.4)
        bar.clear_updaters()
        self.play(
            FadeIn(phrases[2], UP),
            ApplyFunction(push_down, phrases[:2]),
            FadeOut(bar.percentages),
            randy.change, "guilty",
        )
        self.wait()
        bar.remove(bar.percentages)
        self.play(
            FadeIn(phrases[3], UP),
            ApplyFunction(push_down, phrases[:3]),
            FadeOut(bar),
            FadeIn(stereotypes),
            randy.change, "shruggie", stereotypes,
        )
        self.wait(6)
