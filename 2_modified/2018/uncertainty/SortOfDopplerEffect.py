# ==============================================================================
# Scene:      SortOfDopplerEffect
# Source:     videos/_2018/uncertainty.py (lines 3270-3401)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SortOfDopplerEffect.py SortOfDopplerEffect -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - MovingCamera does not exist in GL: replaced by an updater that keeps the camera frame on screen_rect
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class SortOfDopplerEffect(PiCreatureScene):
    CONFIG = {
        "omega" : np.pi,
        "arrow_spacing" : 0.25,
    }
    def setup(self):
        PiCreatureScene.setup(self)
        rect = self.screen_rect = ScreenRectangle(height = FRAME_HEIGHT)
        rect.set_stroke(width = 0)
        # CHANGE: MovingCamera does not exist in GL: replaced by an updater that keeps the camera frame on screen_rect
        # Cairo's MovingCamera(rect) kept the camera frame on `rect`; do the same with an updater on the GL frame
        self.frame.add_updater(
            lambda f: f.set_height(rect.get_height()).move_to(rect.get_center())
        )

    def construct(self):
        screen_rect = self.screen_rect

        #x-coordinate gives time
        t_tracker = VectorizedPoint()
        #x-coordinate gives wave number
        k_tracker = VectorizedPoint(2*RIGHT)
        always_shift(t_tracker, RIGHT, 1)
        def get_wave():
            t = t_tracker.get_center()[0]
            k = k_tracker.get_center()[0]
            omega = self.omega
            color = interpolate_color(
                BLUE, RED, (k-2)/2.0
            )
            func = lambda x : 0.5*np.cos(omega*t - k*x)
            graph = FunctionGraph(
                func,
                x_min = -5*FRAME_X_RADIUS,
                x_max = FRAME_X_RADIUS,
                color = color,
            )
            return VGroup(graph, *[
                Arrow(
                    x*RIGHT, x*RIGHT + func(x)*UP, 
                    color = color
                )
                for x in np.arange(
                    -4*FRAME_X_RADIUS, FRAME_X_RADIUS, 
                    self.arrow_spacing
                )
            ])
            return 
        wave = get_wave()
        wave_update = Mobject.add_updater(
            wave, lambda w : Transform(w, get_wave()).update(1)
        )

        rect = ScreenRectangle(height = 2)
        rect.to_edge(RIGHT)
        always_shift(rect, LEFT, 1)
        rect_movement = rect

        randy = self.pi_creature
        randy_look_at = Mobject.add_updater(
            randy, lambda r : r.look_at(rect)
        )

        ref_frame1 = OldTexText("Reference frame 1")
        # ref_frame1.next_to(randy, UP, aligned_edge = LEFT)
        ref_frame1.to_edge(UP)
        ref_frame2 = OldTexText("Reference frame 2")
        ref_frame2.next_to(rect, UP)
        # ref_frame2.set_fill(opacity = 0)
        ref_frame2_follow = Mobject.add_updater(
            ref_frame2, lambda m : m.next_to(rect, UP)
        )
        ref_frame_1_continual_anim = ContinualAnimation(ref_frame1)

        self.add(
            t_tracker, wave_update, rect_movement, randy_look_at,
            ref_frame2_follow, ref_frame_1_continual_anim
        )
        self.add(ref_frame1)
        self.play(randy.change, "pondering")
        self.wait(4)
        start_height = screen_rect.get_height()
        start_center = screen_rect.get_center()
        self.play(
            UpdateFromAlphaFunc(
                screen_rect,
                lambda m, a : m.move_to(
                    interpolate(start_center, rect.get_center(), a)
                )
            ),
            k_tracker.shift, 2*RIGHT,
        )
        self.play(
            MaintainPositionRelativeTo(
                screen_rect, rect,
                run_time = 4
            ),
        )
        self.play(
            screen_rect.move_to, rect.get_right()+FRAME_X_RADIUS*LEFT,
            k_tracker.shift, 2*LEFT,
        )

        #Frequency words
        temporal_frequency = OldTexText("Temporal", "frequency")
        spatial_frequency = OldTexText("Spatial", "frequency")
        temporal_frequency.move_to(screen_rect).to_edge(UP)
        spatial_frequency.next_to(temporal_frequency, DOWN)
        cross = Cross(temporal_frequency[0])

        time = OldTexText("Time")
        space = OldTexText("Space")
        time.next_to(temporal_frequency, RIGHT, buff = 2)
        space.next_to(time, DOWN)
        space.align_to(spatial_frequency)

        self.play(FadeIn(temporal_frequency))
        self.play(ShowCreation(cross))
        self.play(Write(spatial_frequency))
        self.wait()
        self.play(FadeIn(time), FadeIn(space))
        self.play(
            Transform(time, space),
            Transform(space, time),
            lag_ratio = 0.5,
            run_time = 1,
        )
        self.play(FadeOut(time), FadeOut(space))
        self.wait(3)

    ###

    def create_pi_creature(self):
        return Randolph().scale(0.5).to_corner(DOWN+LEFT)
