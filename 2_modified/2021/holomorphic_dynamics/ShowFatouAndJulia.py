# ==============================================================================
# Scene:      ShowFatouAndJulia
# Source:     videos/_2021/holomorphic_dynamics.py (lines 633-691)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py
#
# Run from this folder:
#     manimgl ShowFatouAndJulia.py ShowFatouAndJulia -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Pierre_Fatou.jpg and Gaston_Julia.jpg (placeholder portraits; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/newton_fractal.py -----

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



# ----- From _2021/holomorphic_dynamics.py -----

class ShowFatouAndJulia(Scene):
    def construct(self):
        time_range = (1900, 2020)
        timeline = NumberLine(
            (*time_range, 1),
            tick_size=0.025,
            longer_tick_multiple=4,
            big_tick_numbers=range(*time_range, 10),
        )
        timeline.stretch(0.25, 0)
        timeline.add_numbers(
            range(*time_range, 10),
            group_with_commas=False,
        )
        timeline.set_y(-3)
        timeline.to_edge(LEFT, buff=0)

        line = Line(timeline.n2p(1917), timeline.n2p(1920))
        line.scale(2)
        brace = Brace(line, UP)
        brace.stretch(1 / 2, 0)
        line.stretch(0.6, 0)
        line.insert_n_curves(20)
        line.set_stroke(BLUE, [1, *3 * [5], 1])

        kw = {"label_direction": UP, "height": 3}
        figures = Group(
            get_figure("Pierre_Fatou", "Pierre Fatou", "1878-1929", **kw),
            get_figure("Gaston_Julia", "Gaston Julia", "1893-1978", **kw),
        )
        figures.set_height(3)
        figures.arrange(RIGHT, buff=LARGE_BUFF)
        figures.next_to(brace, UP)

        self.add(timeline)
        self.add(figures)
        for figure in figures:
            self.remove(*figure[2:])

        frame = self.camera.frame
        frame.save_state()
        frame.align_to(timeline, RIGHT)
        self.play(Restore(frame, run_time=3))
        self.play(LaggedStart(*(
            Write(VGroup(*figure[2:]))
            for figure in figures
        ), lag_ratio=0.7))
        self.play(
            GrowFromCenter(brace),
            ShowCreation(line),
        )
        self.wait()

        # Names
        names = VGroup(*(figure[2][-5:] for figure in figures))
        rects = VGroup(*(SurroundingRectangle(name, buff=0.05) for name in names))
        rects.set_stroke(BLUE, 2)

        self.play(LaggedStartMap(ShowCreation, rects))
