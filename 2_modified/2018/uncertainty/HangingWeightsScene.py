# ==============================================================================
# Scene:      HangingWeightsScene
# Source:     videos/_2018/uncertainty.py (lines 3403-3672)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HangingWeightsScene.py HangingWeightsScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Transform(...).update(1) in a per-frame updater creates a new animation (and copies) every frame, taking seconds per frame; become() gives the same state
#
# Notes:
#   Rendered at 854x480 and 10 fps (--res 854x480 --fps 10 --timeout 1800): at 720p15 it hit the 900 s timeout. Takes ~28 min.
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class HangingWeightsScene(MovingCameraScene):
    CONFIG = {
        "frequency" : 0.5,
        "ceiling_radius" : 3*FRAME_X_RADIUS,
        "n_springs" : 72,
        "amplitude" : 0.6,
        "spring_radius" : 0.15,
    }
    def construct(self):
        self.setup_springs()
        self.setup_weights()
        self.introduce()
        self.show_analogy_with_electron()
        self.metaphor_for_something()
        self.moving_reference_frame()

    def setup_springs(self):
        ceiling = self.ceiling = Line(LEFT, RIGHT)
        ceiling.scale(self.ceiling_radius)
        ceiling.to_edge(UP, buff = LARGE_BUFF)
        self.add(ceiling)

        def get_spring(alpha, height = 2):
            t_max = 6.5
            r = self.spring_radius
            s = (height - r)/(t_max**2)
            spring = ParametricCurve(
                lambda t : op.add(
                    r*(np.sin(TAU*t)*RIGHT+np.cos(TAU*t)*UP),
                    s*((t_max - t)**2)*DOWN,
                ),
                t_min = 0, t_max = t_max,
                color = WHITE,
                stroke_width = 2,
            )
            spring.alpha = alpha
            spring.move_to(ceiling.point_from_proportion(alpha), UP)
            spring.color_using_background_image("grey_gradient")
            return spring
        alphas = np.linspace(0, 1, self.n_springs)
        bezier([0, 1, 0, 1])
        springs = self.springs = VGroup(*list(map(get_spring, alphas)))

        k_tracker = self.k_tracker = VectorizedPoint()
        t_tracker = self.t_tracker = VectorizedPoint()
        always_shift(t_tracker, RIGHT, 1)
        self.t_tracker_walk = t_tracker
        equilibrium_height = springs.get_height()
        def update_springs(springs):
            for spring in springs:
                k = k_tracker.get_center()[0]
                t = t_tracker.get_center()[0]
                f = self.frequency
                x = spring.get_top()[0]
                A = self.amplitude
                d_height = A*np.cos(TAU*f*t - k*x)
                new_spring = get_spring(spring.alpha, 2+d_height)
                # CHANGE: Transform(...).update(1) in a per-frame updater creates a new animation (and copies) every frame, taking seconds per frame; become() gives the same state
                spring.become(new_spring)
        spring_update_anim = Mobject.add_updater(springs, update_springs)
        self.spring_update_anim = spring_update_anim
        spring_update_anim.update(0)

        self.play(
            ShowCreation(ceiling),
            LaggedStartMap(ShowCreation, springs)
        )

    def setup_weights(self):
        weights = self.weights = VGroup()
        weight_anims = weight_anims = []
        for spring in self.springs:
            x = spring.get_top()[0]
            mass = np.exp(-0.1*x**2)
            weight = Circle(radius = 0.15)
            weight.start_radius = 0.15
            weight.target_radius = 0.25*mass #For future update
            weight.spring = spring
            weight_anim = Mobject.add_updater(
                weight, lambda w : w.move_to(w.spring.get_bottom())
            )
            weight_anim.update(0)
            weight_anims.append(weight_anim)
            weights.add(weight)
        weights.set_fill(opacity = 1)
        weights.set_color_by_gradient(BLUE_D, BLUE_E, BLUE_D)
        weights.set_stroke(WHITE, 1)

        self.play(LaggedStartMap(GrowFromCenter, weights))
        self.add(self.t_tracker_walk)
        self.add(self.spring_update_anim)
        self.add(*weight_anims)

    def introduce(self):
        arrow = Arrow(4*LEFT, LEFT)
        arrows = VGroup(arrow, arrow.copy().flip(about_point = ORIGIN))
        arrows.set_color(WHITE)

        self.wait(3)
        self.play(*list(map(GrowArrow, arrows)))
        self.play(*[
            UpdateFromAlphaFunc(
                weight, lambda w, a : w.set_width(
                    2*interpolate(w.start_radius, w.target_radius, a)
                ),
                run_time = 2
            )
            for weight in self.weights
        ])
        self.play(FadeOut(arrows))
        self.wait(3)

    def show_analogy_with_electron(self):
        words = OldTexText(
            "Analogous to the energy of a particle \\\\",
            "(in the sense of $E=mc^2$)"
        )
        words.move_to(DOWN)

        self.play(Write(words))
        self.wait(3)
        self.play(FadeOut(words))

    def metaphor_for_something(self):
        de_broglie = ImageMobject("de_Broglie")
        de_broglie.set_height(3.5)
        de_broglie.to_corner(DOWN+RIGHT)
        words = OldTexText("""
            If a photon's energy is carried as a wave \\\\
            is this true for any particle?
        """)
        words.next_to(de_broglie, LEFT)

        einstein = ImageMobject("Einstein")
        einstein.match_height(de_broglie)
        einstein.to_corner(DOWN+LEFT)

        for picture in de_broglie, einstein:
            picture.backdrop = Rectangle()
            picture.backdrop.replace(picture, stretch = True)
            picture.backdrop.set_fill(BLACK, 1)
            picture.backdrop.set_stroke(BLACK, 0)

        self.play(
            Animation(de_broglie.backdrop, remover = True),
            FadeIn(de_broglie)
        )
        self.play(Write(words))
        self.wait(7)
        self.play(
            FadeOut(words),
            Animation(einstein.backdrop, remover = True),
            FadeIn(einstein)
        )
        self.wait(2)

        self.de_broglie = de_broglie
        self.einstein = einstein

    def moving_reference_frame(self):
        rect = ScreenRectangle(height = 2.1*FRAME_Y_RADIUS)
        rect_movement = always_shift(rect, direction = LEFT, rate = 2)
        camera_frame = self.camera_frame

        self.add(rect)
        self.play( 
            Animation(self.de_broglie.backdrop, remover = True),
            FadeOut(self.de_broglie),
            Animation(self.einstein.backdrop, remover = True),
            FadeOut(self.einstein),
        )
        self.play(camera_frame.scale, 3, {"about_point" : 2*UP})
        self.play(rect.shift, FRAME_WIDTH*RIGHT, path_arc = -TAU/2)
        self.add(rect_movement)
        self.wait(3)

        def zoom_into_reference_frame():
            original_height = camera_frame.get_height()
            original_center = camera_frame.get_center()
            self.play(
                UpdateFromAlphaFunc(
                    camera_frame, lambda c, a : c.set_height(
                        interpolate(original_height, 0.95*rect.get_height(), a)
                    ).move_to(
                        interpolate(original_center, rect.get_center(), a)
                    )
                ),
                ApplyMethod(self.k_tracker.shift, RIGHT)
            )
            self.play(MaintainPositionRelativeTo(
                camera_frame, rect,
                run_time = 6
            ))
            self.play(
                camera_frame.set_height, original_height,
                camera_frame.move_to, original_center,
                ApplyMethod(self.k_tracker.shift, LEFT)
            )

        zoom_into_reference_frame()
        self.wait()
        self.play(
            UpdateFromAlphaFunc(rect, lambda m, a : m.set_stroke(width = 2*(1-a)))
        )

        index = int(0.5*len(self.springs))
        weights = VGroup(self.weights[index], self.weights[index+4])
        flashes = list(map(self.get_peak_flash_anim, weights))
        weights.save_state()
        weights.set_fill(RED)
        self.add(*flashes)
        self.wait(5)

        rect.align_to(camera_frame, RIGHT)
        self.play(UpdateFromAlphaFunc(rect, lambda m, a : m.set_stroke(width = 2*a)))

        randy = Randolph(mode = "pondering")
        randy.look(UP+RIGHT)
        de_broglie = ImageMobject("de_Broglie")
        de_broglie.set_height(6)
        de_broglie.next_to(4*DOWN, DOWN)
        self.add(
            Mobject.add_updater(
                randy, lambda m : m.next_to(
                    rect.get_corner(DOWN+LEFT), UP+RIGHT, MED_LARGE_BUFF,
                ).look_at(weights)
            ),
            de_broglie
        )
        self.wait(2)

        zoom_into_reference_frame()
        self.wait(8)

    ###

    def get_peak_flash_anim(self, weight):
        mobject = Mobject() #Dummy
        mobject.last_y = 0
        mobject.last_dy = 0
        mobject.curr_anim = None
        mobject.curr_anim_time = 0
        mobject.time_since_last_flash = 0
        def update(mob, dt):
            mob.time_since_last_flash += dt
            point = weight.get_center()
            y = point[1]
            mob.dy = y - mob.last_y
            different_dy = np.sign(mob.dy) != np.sign(mob.last_dy)
            if different_dy and mob.time_since_last_flash > 0.5:
                mob.curr_anim = Flash(
                    VectorizedPoint(point),
                    flash_radius = 0.5,
                    line_length = 0.3,
                    run_time = 0.2,
                )
                mob.submobjects = [mob.curr_anim.mobject]
                mob.time_since_last_flash = 0
            mob.last_y = float(y)
            mob.last_dy = float(mob.dy)
            ##
            if mob.curr_anim:
                mob.curr_anim_time += dt
                if mob.curr_anim_time > mob.curr_anim.run_time:
                    mob.curr_anim = None
                    mob.submobjects = []
                    mob.curr_anim_time = 0
                    return
                mob.curr_anim.update(mob.curr_anim_time/mob.curr_anim.run_time)

        return Mobject.add_updater(mobject, update)
