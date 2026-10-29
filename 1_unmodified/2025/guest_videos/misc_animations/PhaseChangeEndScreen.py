# ==============================================================================
# Scene:      PhaseChangeEndScreen
# Source:     videos/_2025/guest_videos/misc_animations.py (lines 192-263)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhaseChangeEndScreen.py PhaseChangeEndScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhaseChangeEndScreen(PatreonEndScreen):
    def construct(self):
        # Attribution
        # background_color = interpolate_color("#FDF6E3", BLACK, 0)
        background_color = BLACK
        text_color = WHITE

        background_rect = FullScreenRectangle(fill_color=background_color)
        background_rect.set_z_index(-2)
        self.add(background_rect)

        elements = VGroup(
            ScreenRectangle(height=3),
            Circle(radius=1),
        )
        elements.arrange(RIGHT, buff=0.5)
        elements.set_width(6.5)
        elements.to_edge(RIGHT, buff=1.0)
        elements.set_y(1)
        elements.set_stroke(text_color, 1)
        # elements.insert_n_curves(100)

        attribution = Text("This guest video was\nproduced by Vilas Winstein", font_size=48, fill_color=text_color)
        watch = Text("Watch part 2 now on Spectral Collective", font_size=36).set_fill(text_color, 0.95)
        attribution.next_to(elements, DOWN, buff=MED_LARGE_BUFF)
        watch.next_to(elements, UP, buff=MED_SMALL_BUFF)

        self.add(elements, attribution, watch)

        # Patron scroll
        v_line = Line(DOWN, UP).set_height(FRAME_HEIGHT)
        v_line.next_to(elements, LEFT, LARGE_BUFF)
        v_line.set_y(0)
        v_line.set_stroke(text_color, 1)

        thanks = Text(
            "This channel is funded via Patreon\nSpecial thanks to these supporters",
            alignment="LEFT",
            font_size=32,
            fill_color=text_color
        )
        thanks.move_to(midpoint(v_line.get_center(), LEFT_SIDE))
        thanks.to_edge(UP)

        solid_rect = Square(side_length=8)
        solid_rect.set_fill(background_color, 1).set_stroke(text_color, 1)
        solid_rect.next_to(v_line, LEFT, 0)
        solid_rect.align_to(thanks, DOWN).shift(MED_SMALL_BUFF * DOWN)

        names = VGroup(map(Text, self.get_names()))
        names.scale(0.5)
        for name in names:
            name.set_width(min(name.get_width(), 2.0))
        names.set_fill(text_color)
        names.arrange_in_grid(n_cols=2, aligned_edge=LEFT)
        names.next_to(solid_rect, DOWN, buff=7).to_edge(LEFT)
        names.set_z_index(-1)

        self.add(solid_rect)
        self.add(v_line)
        self.add(thanks)
        self.add(names)
        self.play(
            names.animate.to_edge(DOWN, buff=1.5).set_anim_args(run_time=25, rate_func=linear),
            LaggedStartMap(
                VShowPassingFlash,
                elements.copy().set_stroke(WHITE, 5).insert_n_curves(1000),
                time_width=2,
                run_time=3
            ),
            FadeIn(elements, time_span=(1, 2))
        )
