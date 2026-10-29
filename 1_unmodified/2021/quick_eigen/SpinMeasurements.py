# ==============================================================================
# Scene:      SpinMeasurements
# Source:     videos/_2021/quick_eigen.py (lines 1916-2020)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpinMeasurements.py SpinMeasurements -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_prism(verts, depth=2):
    result = VGroup()
    result.add(Polygon(*verts))
    zv = depth * OUT
    for v1, v2 in zip(verts, [*verts[1:], verts[0]]):
        result.add(Polygon(v1, v2, v2 + zv, v1 + zv))
    result.add(Polygon(*verts).shift(zv))
    result.set_stroke(width=0)
    result.set_fill(GREY, 1)
    result.set_gloss(1)
    for mob in list(result):
        m2 = mob.copy()
        m2.reverse_points()
        result.add(m2)
    result.apply_depth_test()
    return result


class SpinMeasurements(ThreeDScene):
    def construct(self):
        # Reorient
        frame = self.camera.frame
        frame.reorient(-70, 70)
        frame.add_updater(lambda m, dt: m.increment_theta(0.01 * dt))
        self.add(frame)

        # Create machine
        north_verts = [UL + 0.5 * DOWN, UR + 0.5 * DOWN, DR, 2 * DOWN, DL]
        south_verts = [DOWN + 2 * LEFT, UP + 2 * LEFT, UL, LEFT, RIGHT, UR, UP + 2 * RIGHT, DOWN + 2 * RIGHT]

        north_bar = get_prism(north_verts, depth=2)
        south_bar = get_prism(south_verts, depth=2)
        N_text = Text("N").move_to(north_bar, OUT).shift(0.025 * OUT)
        S_text = Text("S").move_to(south_bar, OUT).shift(0.025 * OUT)
        S_text.set_y(-0.5)
        north_bar.add(N_text)
        south_bar.add(S_text)
        south_bar.move_to(ORIGIN, UP).shift(0.5 * UP)
        north_bar.move_to(south_bar.get_top(), DOWN)

        machine = VGroup(north_bar, south_bar)
        machine.set_stroke(width=0)
        # for bar in machine:
        #     bar.space_out_submobjects(1.1)

        # Screen
        screen = FullScreenRectangle()
        axes = Axes((-3, 3), (-3, 3))
        for sm in axes.get_family():
            sm.flat_stroke = False
            sm.insert_n_curves(10)
        axes.add(OldTex("+z").next_to(axes.c2p(0, 2), RIGHT))
        axes.add(OldTex("-z").next_to(axes.c2p(0, -2), RIGHT))
        axes.shift(0.1 * OUT)
        screen.set_height(5)
        screen.set_fill(GREY_D, 1)
        screen.set_stroke(WHITE, 2)
        screen.shift(5 * IN)
        axes.shift(5 * IN)

        # Rotate all
        everything = VGroup(screen, axes, machine)
        everything.apply_depth_test()
        self.add(everything)
        self.update_frame()  # Why?
        everything.rotate(89.5 * DEGREES, RIGHT, about_point=ORIGIN)

        self.play(
            FadeIn(screen),
            FadeIn(axes),
            FadeIn(machine, lag_ratio=0.05),
        )
        self.wait()

        # Paths
        def path(t):
            if t < -1:
                z = 0
            elif t < 1:
                z = (1 / 4) * (t + 1)**2
            else:
                z = t

            return [0, t, z]

        high_beam = ParametricCurve(path, (-5, 5))
        high_beam.set_stroke(BLUE, 10)
        high_beam.set_depth(1, stretch=True, about_point=ORIGIN)
        high_beam.apply_depth_test()
        low_beam = high_beam.copy()
        low_beam.stretch(-1, 2, about_point=ORIGIN)

        def hit_anim(spin=1):
            circ = Circle(radius=0.5)
            circ.set_stroke(BLUE, 0)
            circ.rotate(90 * DEGREES, RIGHT)
            circ.move_to(5 * UP + spin * OUT)
            tex = OldTex("+1" if spin == 1 else "-1")
            tex.shift(20 * OUT)
            self.add(tex)
            self.update_frame()
            tex.rotate(90 * DEGREES, RIGHT)
            tex.move_to(circ.get_left())
            pre_circ = circ.copy()
            pre_circ.scale(0)
            pre_circ.set_stroke(BLUE, 10)
            return AnimationGroup(
                Transform(pre_circ, circ, remover=True),
                VFadeInThenOut(tex),
            )

        for x in range(20):
            if random.random() < 0.5:
                beam = high_beam
                spin = +1
            else:
                beam = low_beam
                spin = -1
            self.play(LaggedStart(
                VShowPassingFlash(beam, time_width=0.5),
                hit_anim(spin),
                lag_ratio=0.6
            ))
