# ==============================================================================
# Scene:      IntroduceKahnemanAndTversky
# Source:     videos/_2019/bayes/part1.py (lines 1022-1268)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceKahnemanAndTversky.py IntroduceKahnemanAndTversky -w -m --fps 15
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


class IntroduceKahnemanAndTversky(DescriptionOfSteve):
    def construct(self):
        # Introduce K and T
        images = Group(
            ImageMobject("kahneman"),
            ImageMobject("tversky"),
        )
        danny, amos = images
        images.set_height(3.5)
        images.arrange(DOWN, buff=0.5)
        images.to_edge(LEFT, buff=MED_LARGE_BUFF)

        names = VGroup(
            OldTexText("Daniel\\\\Kahneman", alignment=""),
            OldTexText("Amos\\\\Tversky", alignment=""),
        )
        for name, image in zip(names, images):
            name.scale(1.25)
            name.next_to(image, RIGHT)
            image.name = name

        prize = ImageMobject("nobel_prize", height=1)
        prize.move_to(danny, UR)
        prize.shift(MED_SMALL_BUFF * UR)

        books = Group(
            ImageMobject("thinking_fast_and_slow"),
            ImageMobject("undoing_project"),
        )
        books.set_height(5)
        books.arrange(RIGHT, buff=0.5)
        books.to_edge(RIGHT, buff=MED_LARGE_BUFF)

        self.play(
            FadeIn(danny, DOWN),
            FadeIn(danny.name, LEFT),
        )
        self.play(
            FadeIn(amos, UP),
            FadeIn(amos.name, LEFT),
        )
        self.wait()
        self.play(FadeInFromLarge(prize))
        self.wait()
        for book in books:
            self.play(FadeIn(book, LEFT))
        self.wait()

        # Show them thinking
        for image in images:
            image.generate_target()
        amos.target.to_corner(DL)
        danny.target.to_corner(DR)
        targets = Group(amos.target, danny.target)

        bubble = ThoughtBubble(
            width=7, height=4,
        )
        bubble.next_to(targets, UP)
        new_stem = bubble[:-1].copy()
        new_stem.rotate(PI, UP, about_point=targets.get_top())
        new_stem.shift(SMALL_BUFF * DR)
        bubble.add_to_back(*new_stem)
        bubble[-1].scale(1.2)
        bubble[-1].to_edge(UP, buff=0)
        bubble[:-1].shift(DOWN)
        bubble.set_fill(GREY_D, 1)

        randy = Randolph(color=BLUE_B)
        randy.set_height(1)
        randy.next_to(bubble[-1].get_center(), DL)
        randy.shift(LEFT)

        lil_bubble = ThoughtBubble(height=1.5, width=2)
        lil_bubble.next_to(randy, UR, buff=0)
        lil_bubble[:-1].rotate(
            PI, axis=UR, about_point=lil_bubble[:-1].get_corner(UL),
        )
        lil_bubble.move_to(randy.get_top(), DL)
        for i, part in enumerate(lil_bubble[-2::-1]):
            part.rotate(90 * DEGREES)
            part.shift(0.05 * i * UR)
        lil_bubble[-1].scale(0.8)

        librarian = OldTexText("Librarian")
        librarian.set_color(BLUE)
        librarian.scale(0.5)
        librarian.move_to(lil_bubble[-1])

        bar = ProbabilityBar(percentage_background_stroke_width=1)
        bar.add_icons(
            LibrarianIcon(height=1),
            FarmerIcon(height=1),
        )
        bar.scale(0.5)
        bar.next_to(randy, RIGHT, buff=0.75)
        bar.update()

        self.play(
            LaggedStartMap(MoveToTarget, images),
            LaggedStartMap(FadeOutAndShiftDown, books),
            LaggedStartMap(FadeOut, Group(prize, *names)),
        )
        self.play(
            DrawBorderThenFill(bubble),
            FadeIn(
                randy, UR,
                rate_func=squish_rate_func(smooth, 0.5, 1),
                run_time=2,
            )
        )
        self.play(
            DrawBorderThenFill(lil_bubble),
            randy.change, "pondering",
        )
        self.play(Blink(randy))
        self.play(Write(librarian))
        self.add(bar, lil_bubble, librarian)
        self.play(FadeIn(bar))
        self.play(
            bar.p_tracker.set_value, 1 / 6,
            randy.change, "thinking", bar,
        )
        self.play(Blink(randy))
        self.wait()

        # Zoom in
        description = self.get_description()
        description.scale(0.4)
        description.next_to(randy, UL)
        description.shift(1.25 * RIGHT + 0.75 * UP)
        description.set_color(WHITE)

        frame = self.camera_frame

        steve = Steve()
        steve.match_height(description)
        steve.align_to(bar, RIGHT)
        steve.align_to(description, UP)

        # cross = Cross(librarian)

        book_border = bar.icons[0].copy()
        farm_border = bar.icons[1].copy()
        for border in [book_border, farm_border]:
            border.set_fill(opacity=0)
            border.set_stroke(YELLOW, 1)

        seems_bookish = OldTexText("Seems\\\\bookish")
        seems_bookish.match_width(librarian)
        seems_bookish.scale(0.8)
        seems_bookish.move_to(librarian)

        self.play(
            frame.scale, 0.5,
            frame.move_to, bubble[-1], DOWN,
            frame.shift, 0.75 * LEFT,
            FadeOut(bubble),
            FadeOut(images),
            FadeOut(lil_bubble),
            FadeOut(librarian),
            FadeIn(description, lag_ratio=0.05),
            randy.change, "pondering", description,
            run_time=6,
        )
        self.play(randy.change, "happy", description)
        self.play(
            description.get_part_by_tex("shy").set_color, BLUE,
            lag_ratio=0.1,
        )
        self.play(
            description.get_part_by_tex("meek").set_color, YELLOW,
            description.get_part_by_tex("soul").set_color, YELLOW,
            lag_ratio=0.1,
        )
        self.play(
            bar.p_tracker.set_value, 0.9,
            FadeIn(lil_bubble),
            Write(librarian),
        )
        self.play(ShowCreationThenFadeOut(book_border))
        self.play(Blink(randy))
        self.play(
            FadeInFromDown(steve),
            randy.look_at, steve,
        )
        self.play(
            randy.change, "tease", steve,
            FadeOut(librarian),
            FadeIn(seems_bookish),
        )
        lil_bubble.add(seems_bookish)
        self.wait()
        self.play(Blink(randy))

        self.play(
            LaggedStartMap(
                FadeOutAndShift, lil_bubble,
                lambda m: (m, LEFT),
                run_time=1,
            ),
            bar.p_tracker.set_value, 1 / 6,
            randy.change, "confused", bar,
        )
        self.play(
            ShowCreationThenFadeOut(farm_border)
        )
        self.wait()

        # Transition to next scene
        fh = frame.get_height()
        fw = frame.get_width()
        center = frame.get_center()
        right = (fw / FRAME_WIDTH) * RIGHT
        up = (fh / FRAME_HEIGHT) * UP
        left = -right
        down = -up

        book, farm = bar.icons.deepcopy()
        bar.clear_updaters()
        bar.icons.set_opacity(0)

        for mob in book, farm:
            mob.clear_updaters()
            mob.generate_target(use_deepcopy=True)
            mob.target.set_height(get_norm(up))
            mob.target.move_to(center + down + 2 * left)
        farm.target.shift(4 * right)

        steve.generate_target()
        steve.target.match_width(book.target)
        steve.target.move_to(book.target, DOWN)
        steve.target.shift(3 * up)
        steve_copy = steve.target.copy()
        steve_copy.match_x(farm.target),

        self.play(
            TransformFromCopy(steve, steve_copy),
            LaggedStartMap(MoveToTarget, VGroup(steve, book, farm)),
            LaggedStartMap(
                FadeOutAndShift,
                description,
                lambda m: (m, LEFT)
            ),
            FadeOut(randy, LEFT),
            FadeOut(bar, LEFT),
        )
