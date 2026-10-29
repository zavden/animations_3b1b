# ==============================================================================
# Scene:      AskAboutShadowRelation
# Source:     videos/_2018/sphere_area.py (lines 96-285)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutShadowRelation.py AskAboutShadowRelation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutShadowRelation(SpecialThreeDScene):
    CONFIG = {
        "R_color": YELLOW,
        "space_out_factor": 1.15,
    }

    def construct(self):
        self.show_surface_area()
        self.show_four_circles()
        self.ask_why()
        self.show_all_pieces()

    def show_surface_area(self):
        sphere = self.get_sphere()
        sphere.set_fill(BLUE_E, opacity=0.5)
        sphere.add_updater(
            lambda s, dt: s.rotate(0.1 * dt, axis=OUT)
        )
        pieces = sphere.deepcopy()
        pieces.space_out_submobjects(1.5)
        pieces.shift(IN)
        pieces.set_color(GREEN)

        # radial_line = Line(ORIGIN, sphere.get_right())
        # R_label = OldTex("R")
        # R_label.set_color(BLUE)
        # R_label.rotate(90 * DEGREES, RIGHT)
        # R_label.next_to(radial_line, OUT, SMALL_BUFF)

        sa_equation = OldTex(
            "\\text{Surface area} = 4\\pi R^2",
            tex_to_color_map={"R": BLUE}
        )
        sa_equation.scale(1.5)
        sa_equation.to_edge(UP)

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-90 * DEGREES,
        )
        self.add_fixed_in_frame_mobjects(sa_equation)
        self.play(
            Write(sphere, stroke_width=1),
            FadeInFromDown(sa_equation),
            # ShowCreation(radial_line),
            # FadeIn(R_label, IN),
        )
        # self.play(
        #     Transform(
        #         sphere, pieces,
        #         rate_func=there_and_back_with_pause,
        #         run_time=2
        #     )
        # )
        self.play(LaggedStartMap(
            UpdateFromAlphaFunc, sphere,
            lambda mob: (mob, lambda m, a: m.set_fill(
                color=interpolate_color(BLUE_E, YELLOW, a),
                opacity=interpolate(0.5, 1, a)
            )),
            rate_func=there_and_back,
            lag_ratio=0.1,
            run_time=4
        ))
        self.play(
            sphere.scale, 0.75,
            sphere.shift, 3 * LEFT,
            sa_equation.shift, 3 * LEFT,
        )
        self.wait(2)

        self.sphere = sphere
        self.sa_equation = sa_equation

    def show_four_circles(self):
        sphere = self.sphere
        shadow = Circle(
            radius=sphere.get_width() / 2,
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLUE_E,
            fill_opacity=1,
        )
        radial_line = Line(
            shadow.get_center(),
            shadow.get_right(),
            color=YELLOW
        )
        R_label = OldTex("R").set_color(self.R_color)
        R_label.scale(0.8)
        R_label.next_to(radial_line, DOWN, SMALL_BUFF)
        shadow.add(radial_line, R_label)
        shadow.move_to(
            self.camera.transform_points_pre_display(sphere, [sphere.get_center()])[0]
        )

        shadows = VGroup(*[shadow.copy() for x in range(4)])
        shadows.arrange_in_grid(buff=MED_LARGE_BUFF)
        shadows.to_edge(RIGHT)

        area_label = OldTex(
            "\\pi R^2",
            tex_to_color_map={"R": self.R_color}
        )
        area_label.scale(1.2)
        area_labels = VGroup(*[
            area_label.copy().move_to(interpolate(
                mob.get_center(), mob.get_top(), 0.5
            ))
            for mob in shadows
        ])

        # shadow.move_to(sphere)
        self.add_fixed_in_frame_mobjects(shadow)
        self.play(DrawBorderThenFill(shadow))
        anims = []
        for new_shadow in shadows:
            old_shadow = shadow.copy()
            self.add_fixed_in_frame_mobjects(old_shadow)
            anims.append(Transform(
                old_shadow, new_shadow, remover=True
            ))
        self.remove(shadow)
        self.play(*anims)
        self.add_fixed_in_frame_mobjects(shadows, area_labels)
        self.play(LaggedStartMap(FadeInFromLarge, area_labels))
        self.wait()

        self.shadows = shadows
        self.shadow_area_labels = area_labels

    def ask_why(self):
        pass

    def show_all_pieces(self):
        shadows = self.shadows
        area_labels = self.shadow_area_labels
        sphere = self.sphere

        shadow_pieces_group = VGroup()
        for shadow in shadows:
            pieces = ParametricSurface(
                func=lambda u, v: np.array([
                    u * np.cos(TAU * v),
                    u * np.sin(TAU * v),
                    0,
                ]),
                resolution=(12, 24)
            )
            pieces.replace(shadow)
            pieces.match_style(sphere)
            shadow_pieces_group.add(pieces)

        self.add_fixed_in_frame_mobjects(shadow_pieces_group)
        self.play(
            FadeOut(shadows),
            FadeOut(area_labels),
            FadeIn(shadow_pieces_group)
        )
        self.show_area_pieces(sphere)
        self.wait()
        self.show_area_pieces(*shadow_pieces_group)
        self.wait(2)
        self.unshow_area_pieces(sphere, *shadow_pieces_group)
        self.wait(3)

    def show_area_pieces(self, *mobjects):
        for mob in mobjects:
            mob.generate_target()
            mob.target.space_out_submobjects(self.space_out_factor)
        self.play(*map(MoveToTarget, mobjects))
        self.play(*[
            LaggedStartMap(
                ApplyMethod, mob,
                lambda m: (m.set_fill, YELLOW, 1),
                rate_func=there_and_back,
                lag_ratio=0.25,
                run_time=1.5
            )
            for mob in mobjects
        ])

    def unshow_area_pieces(self, *mobjects):
        self.play(*[
            ApplyMethod(
                mob.space_out_submobjects,
                1.0 / self.space_out_factor
            )
            for mob in mobjects
        ])
