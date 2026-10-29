# ==============================================================================
# Scene:      NablaNotation
# Source:     videos/_2018/div_curl.py (lines 3297-3456)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NablaNotation.py NablaNotation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - in Cairo camera_frame was a drawable ScreenRectangle; GL CameraFrame cannot be stroked, so draw an equivalent Rectangle
# ==============================================================================

from manim_imports_ext import *

class NablaNotation(PiCreatureScene, MovingCameraScene):
    CONFIG = {
        "default_pi_creature_kwargs": {
            "color": GREY_BROWN,
        },
        "default_pi_creature_start_corner": DL,
    }

    def setup(self):
        MovingCameraScene.setup(self)
        PiCreatureScene.setup(self)

    def construct(self):
        self.show_notation()
        self.show_expansion()
        self.zoom_out()

    def show_notation(self):
        morty = self.pi_creature

        tex_to_color_map = {
            "\\text{div}": BLUE,
            "\\nabla \\cdot": BLUE,
            "\\text{curl}": YELLOW,
            "\\nabla \\times": YELLOW,
        }
        div_equation = OldTex(
            "\\text{div} \\, \\textbf{F} = \\nabla \\cdot \\textbf{F}",
            tex_to_color_map=tex_to_color_map
        )
        div_nabla = div_equation.get_part_by_tex("\\nabla")
        curl_equation = OldTex(
            "\\text{curl} \\, \\textbf{F} = \\nabla \\times \\textbf{F}",
            tex_to_color_map=tex_to_color_map
        )
        curl_nabla = curl_equation.get_part_by_tex("\\nabla")
        equations = VGroup(div_equation, curl_equation)
        equations.arrange(DOWN, buff=LARGE_BUFF)
        equations.next_to(morty, UP, 2)
        equations.to_edge(LEFT)

        self.play(
            FadeInFromDown(div_equation),
            morty.change, "raise_right_hand"
        )
        self.wait()
        self.play(WiggleOutThenIn(div_nabla, scale_value=1.5))
        self.wait()
        self.play(
            FadeInFromDown(curl_equation),
            morty.change, "raise_left_hand"
        )
        self.wait()
        self.play(WiggleOutThenIn(curl_nabla, scale_value=1.5))
        self.wait()

        self.equations = equations

    def show_expansion(self):
        equations = self.equations
        morty = self.pi_creature

        nabla_vector = Matrix([
            ["\\partial \\over \\partial x"],
            ["\\partial \\over \\partial y"],
        ], v_buff=1.5)
        F_vector = Matrix([
            ["\\textbf{F}_x"],
            ["\\textbf{F}_y"],
        ], v_buff=1.2)
        nabla_vector.match_height(F_vector)

        div_lhs, curl_lhs = lhs_groups = VGroup(*[
            VGroup(
                nabla_vector.deepcopy(),
                OldTex(tex).scale(1.5),
                F_vector.copy(),
                OldTex("=")
            )
            for tex in ("\\cdot", "\\times")
        ])
        colors = [BLUE, YELLOW]
        for lhs, color in zip(lhs_groups, colors):
            lhs.arrange(RIGHT, buff=MED_SMALL_BUFF)
            VGroup(lhs[0].brackets, lhs[1]).set_color(color)
        div_lhs.to_edge(UP)
        curl_lhs.next_to(div_lhs, DOWN, buff=LARGE_BUFF)

        div_rhs = OldTex(
            "{\\partial F_x \\over \\partial x} + " +
            "{\\partial F_y \\over \\partial y}"
        )
        curl_rhs = OldTex(
            "{\\partial F_y \\over \\partial x} - " +
            "{\\partial F_x \\over \\partial y}"
        )
        rhs_groups = VGroup(div_rhs, curl_rhs)
        for rhs, lhs in zip(rhs_groups, lhs_groups):
            rhs.next_to(lhs, RIGHT)

        for rhs, tex, color in zip(rhs_groups, ["div", "curl"], colors):
            rhs.rect = SurroundingRectangle(rhs, color=color)
            rhs.label = OldTex(
                "\\text{%s}" % tex,
                "\\, \\textbf{F}"
            )
            rhs.label.set_color(color)
            rhs.label.next_to(rhs.rect, UP)

        for i in 0, 1:
            self.play(
                ReplacementTransform(
                    equations[i][2].copy(),
                    lhs_groups[i][0].brackets
                ),
                ReplacementTransform(
                    equations[i][3].copy(),
                    lhs_groups[i][2],
                ),
                morty.change, "pondering",
                *[
                    GrowFromPoint(mob, equations[i].get_right())
                    for mob in [
                        lhs_groups[i][0].get_entries(),
                        lhs_groups[i][1],
                        lhs_groups[i][3]
                    ]
                ],
                run_time=2
            )
            self.wait()
        self.wait()
        for rhs in rhs_groups:
            self.play(
                Write(rhs),
                morty.change, 'confused'
            )
            self.play(
                ShowCreation(rhs.rect),
                FadeInFromDown(rhs.label),
            )
            self.wait()
        self.play(morty.change, "erm")
        self.wait(3)

    def zoom_out(self):
        # CHANGE: in Cairo camera_frame was a drawable ScreenRectangle; GL CameraFrame cannot be stroked, so draw an equivalent Rectangle
        screen_rect = Rectangle(width=self.camera_frame.get_width(), height=self.camera_frame.get_height()).move_to(self.camera_frame.get_center())
        screen_rect.set_stroke(WHITE, 3)
        screen_rect.scale(1.01)
        words = OldTexText("Something deeper at play...")
        words.scale(1.3)
        words.next_to(screen_rect, UP)

        self.add(screen_rect)
        self.play(
            self.camera_frame.set_height, FRAME_HEIGHT + 3,
            Write(words, rate_func=squish_rate_func(smooth, 0.3, 1)),
            run_time=2,
        )
        self.wait()
