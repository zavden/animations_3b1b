# ==============================================================================
# Scene:      HistoryWithNewton
# Source:     videos/_2021/newton_fractal.py (lines 2155-2257)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HistoryWithNewton.py HistoryWithNewton -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_figure(image_name, person_name, year_text, height=3, label_direction=DOWN):
    image = ImageMobject(image_name)
    image.set_height(height)
    rect = SurroundingRectangle(image, buff=0)
    rect.set_stroke(WHITE, 2)
    name = Text(f"{person_name}", font_size=36)
    name.set_color(GREY_A)
    year_label = Text(f"{year_text}", font_size=30)
    year_label.match_color(name)
    year_label.next_to(name, DOWN, buff=0.2)
    VGroup(name, year_label).next_to(image, label_direction)
    return Group(rect, image, name, year_label)


class HistoryWithNewton(Scene):
    def construct(self):
        # Add title
        title = Text("Newton's method", font_size=60)
        title.to_edge(UP)
        self.add(title)

        # Add timeline
        time_range = (1620, 2020)
        timeline = NumberLine(
            (*time_range, 1),
            tick_size=0.025,
            longer_tick_multiple=4,
            big_tick_numbers=range(*time_range, 10),
        )
        timeline.stretch(0.2 / timeline.get_unit_size(), 0)
        timeline_center = 2 * DOWN
        timeline.move_to(timeline_center)
        timeline.to_edge(RIGHT)
        timeline.add_numbers(
            range(*time_range, 10),
            group_with_commas=False,
        )
        timeline.shift(timeline_center - timeline.n2p(1680))

        self.add(timeline)

        # Newton
        newton = get_figure("Newton", "Isaac Newton", "1669")
        newton.next_to(title, DOWN, buff=0.5)
        newton.to_edge(LEFT, buff=1.5)
        newton_point = timeline.n2p(1669)
        newton_arrow = Arrow(newton_point, newton[0].get_right() + DOWN, path_arc=PI / 3)

        newton_words = Text("Overly\ncomplicated", font_size=36)
        newton_words.next_to(newton[0], RIGHT)

        raphson_point = timeline.n2p(1690)
        raphson = get_figure("Newton", "Joseph Raphson", "1690")
        raphson.move_to(newton)
        raphson.set_x(raphson_point[0] + 2)
        raphson[1].set_opacity(0)
        raphson_arrow = Arrow(raphson_point, raphson[0].get_left() + DOWN, path_arc=-PI / 3)
        raphson_word = Text("Simplified", font_size=36)
        raphson_word.next_to(raphson[0], LEFT)

        no_image_group = VGroup(
            Text("No image"),
            Text("(sorry)"),
            # Randolph(mode="shruggie", height=1)
        )
        no_image_group[:2].set_fill(GREY)
        no_image_group.arrange(DOWN, buff=0.5)
        no_image_group.set_width(raphson[0].get_width() - 0.5)
        no_image_group.move_to(raphson[0])

        self.add(newton, newton_arrow)

        frame = self.camera.frame
        frame.save_state()
        title.fix_in_frame()
        frame.move_to(timeline, RIGHT)
        self.play(
            frame.animate.match_width(timeline).set_x(timeline.get_center()[0]),
            run_time=2
        )
        self.play(Restore(frame, run_time=2))

        # self.play(
        #     GrowFromPoint(newton, newton_point),
        #     ShowCreation(newton_arrow)
        # )
        self.wait()
        self.play(Write(newton_words))
        self.wait()
        self.play(
            GrowFromPoint(raphson, raphson_point),
            ShowCreation(raphson_arrow),
        )
        self.play(LaggedStartMap(FadeIn, no_image_group, lag_ratio=0.2))
        self.play(FadeIn(raphson_word))
        self.wait()

        new_title = Text("Newton-Raphson method", font_size=60)
        new_title.to_edge(UP)
        self.play(
            FadeOut(title),
            TransformFromCopy(
                newton[2].get_part_by_text("Newton"),
                new_title.get_part_by_text("Newton"),
            ),
            TransformFromCopy(
                raphson[2].get_part_by_text("Raphson"),
                new_title.get_part_by_text("Raphson"),
            ),
            TransformFromCopy(
                title.get_part_by_text("method"),
                new_title.get_part_by_text("method"),
            ),
            FadeIn(new_title.get_part_by_text("-"))
        )
        self.play(FlashAround(new_title, run_time=2))
        self.wait()
