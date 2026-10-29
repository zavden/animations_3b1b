# ==============================================================================
# Scene:      BriefMandelbrot
# Source:     videos/_2021/newton_fractal.py (lines 4848-4967)
# Category:   4 · Interactive (runnable)
#
# Run from this folder:
#     manimgl BriefMandelbrot.py BriefMandelbrot -w -m --fps 15
#     manimgl BriefMandelbrot.py BriefMandelbrot        # interactive window
#
# How to interact:
#   Brief explanation of the Mandelbrot set: z_{n+1} = z_n^2 + c with z_0 = 0, and c is the yellow point that can be moved. The first 30 terms of the orbit are drawn as segments and points.
#   Open the interactive window (without -w):  manimgl BriefMandelbrot.py BriefMandelbrot
#   The initial animation draws the first iterations, waits 10 s ('time to play') and then the image of the Mandelbrot set (MandelbrotSet, computed for this project) appears behind the plane.
#   Mouse:
#     - Left click on the yellow point (c) and drag: changes c and the orbit is redrawn live.
#     - Drag on an empty place: pans the frame. Wheel: zoom.
#
#   What to look for: if c is inside the set the orbit stays bounded (sometimes in cycles); outside, it escapes. With -w only the animation is rendered (22 s).
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `unlock_mobject_data()`/`lock_static_mobject_data()` are removed from on_mouse_press (they no longer exist in manimgl; clicking a point would fail with AttributeError)
#   - `drag_to_pan` is turned off while dragging a point (manimgl moves the frame when dragging, and the point did not move) and turned on again on release
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/MandelbrotSet.png (Mandelbrot set computed with numpy; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class BriefMandelbrot(Scene):
    n_iterations = 30

    def construct(self):
        self.add_plane()
        self.add_process_description()
        self.show_iterations()
        self.wait(10)  # Time to play
        self.add_mandelbrot_image()

    def add_plane(self):
        plane = self.plane = ComplexPlane((-2, 1), (-2, 2))

        plane.set_height(4)
        plane.scale(FRAME_HEIGHT / 2.307)
        plane.next_to(2 * LEFT, RIGHT, buff=0)
        plane.add_coordinate_labels(font_size=24)
        self.add(plane)

    def add_process_description(self):
        kw = {
            "tex_to_color_map": {
                "{c}": YELLOW,
            }
        }
        terms = self.terms = VGroup(
            OldTex("z_{n + 1} = z_n^2 + {c}", **kw),
            OldTex("z_0 = 0", **kw),
            OldTex("{c} \\text{ can be changed}", **kw),
        )
        terms.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        terms.next_to(self.plane, LEFT, MED_LARGE_BUFF)

        self.add(terms)

    def show_iterations(self):
        plane = self.plane

        c0 = complex(-0.2, 0.95)

        c_dot = self.c_dot = Dot()
        c_dot.set_fill(YELLOW)
        c_dot.set_stroke(BLACK, 5, background=True)
        c_dot.move_to(plane.n2p(c0))

        lines = VGroup()
        lines.set_stroke(background=True)

        def get_c():
            return plane.p2n(c_dot.get_center())

        def update_lines(lines):
            z1 = 0
            c = get_c()
            new_lines = []

            for n in range(self.n_iterations):
                try:
                    z2 = z1**2 + c
                    new_lines.append(Line(
                        plane.n2p(z1),
                        plane.n2p(z2),
                        stroke_color=GREY,
                        stroke_width=2,
                    ))
                    new_lines.append(Dot(
                        plane.n2p(z2),
                        fill_color=YELLOW,
                        fill_opacity=0.5,
                        radius=0.05,
                    ))
                    z1 = z2
                except Exception:
                    pass

            lines.set_submobjects(new_lines)

        update_lines(lines)
        self.add(lines[:2], c_dot)
        last_dot = Dot(plane.n2p(0)).scale(0)
        for line, dot in zip(lines[0:20:2], lines[1:20:2]):
            self.add(line, dot, c_dot)
            self.play(
                ShowCreation(line),
                TransformFromCopy(last_dot, dot)
            )
            last_dot = dot
        self.remove(*lines)
        lines.add_updater(update_lines)
        self.add(lines, c_dot)

    def add_mandelbrot_image(self):
        image = ImageMobject("MandelbrotSet")
        image.set_height(FRAME_HEIGHT)
        image.shift(self.plane.n2p(-0.7) - image.get_center())

        rect = FullScreenFadeRectangle()
        rect.set_fill(BLACK, 1)
        rect.next_to(self.plane, LEFT, buff=0)

        self.add(image, rect, *self.mobjects)
        self.play(
            FadeIn(image, run_time=2),
            self.plane.animate.set_opacity(0.5)
        )

    def on_mouse_press(self, point, button, mods):
        # TODO, copy-pasted, should factor out
        super().on_mouse_press(point, button, mods)
        mob = self.point_to_mobject(point, search_set=[self.c_dot])
        if mob is None:
            return
        self.mouse_drag_point.move_to(point)
        mob.add_updater(lambda m: m.move_to(self.mouse_drag_point))
        # CHANGE: manimgl now moves the frame when dragging (drag_to_pan); while a point is being dragged
        # it is turned off, otherwise the frame shifts with the cursor and the point does not move
        self.drag_to_pan = False
        # CHANGE: `unlock_mobject_data()` removed: this manimgl no longer has it (there is no cached static data to lock)
        # CHANGE: `lock_static_mobject_data()` removed: this manimgl no longer has it (there is no cached static data to lock)

    def on_mouse_release(self, point, button, mods):
        super().on_mouse_release(point, button, mods)
        self.c_dot.clear_updaters()
        # CHANGE: frame panning is turned back on on release
        self.drag_to_pan = True
