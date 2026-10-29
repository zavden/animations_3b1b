# ==============================================================================
# Scene:      UniversalGravityLawSymbols
# Source:     videos/_2019/diffyq/part1/staging.py (lines 1067-1197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UniversalGravityLawSymbols.py UniversalGravityLawSymbols -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UniversalGravityLawSymbols(Scene):
    def construct(self):
        x1_tex = "\\vec{\\textbf{x}}_1"
        x2_tex = "\\vec{\\textbf{x}}_2"
        a1_tex = "\\vec{\\textbf{a}}_1"
        new_brown = interpolate_color(GREY_B, LIGHT_BROWN, 0.5)
        law = OldTex(
            "F_1", "=", "m_1", a1_tex, "=",
            "G", "m_1", "m_2",
            "\\left({", x2_tex, "-", x1_tex, "\\over",
            "||", x2_tex, "-", x1_tex, "||", "}\\right)",
            "\\left({", "1", "\\over",
            "||", x2_tex, "-", x1_tex, "||^2", "}\\right)",
            tex_to_color_map={
                x1_tex: BLUE_C,
                "m_1": BLUE_C,
                x2_tex: new_brown,
                "m_2": new_brown,
                a1_tex: YELLOW,
            }
        )
        law.to_edge(UP)

        force = law[:4]
        constants = law[4:8]
        unit_vect = law[8:19]
        inverse_square = law[19:]
        parts = VGroup(
            force, unit_vect, inverse_square
        )

        words = VGroup(
            OldTexText("Force on\\\\mass 1"),
            OldTexText("Unit vector\\\\towards mass 2"),
            OldTexText("Inverse square\\\\law"),
        )

        self.add(law)

        braces = VGroup()
        rects = VGroup()
        for part, word in zip(parts, words):
            brace = Brace(part, DOWN)
            word.scale(0.8)
            word.next_to(brace, DOWN)
            rect = SurroundingRectangle(part)
            rect.set_stroke(YELLOW, 1)
            braces.add(brace)
            rects.add(rect)

        self.play(
            ShowCreationThenFadeOut(rects[0]),
            GrowFromCenter(braces[0]),
            FadeIn(words[0], UP)
        )
        self.wait()
        self.play(
            ShowCreationThenFadeOut(rects[1]),
            GrowFromCenter(braces[1]),
            FadeIn(words[1], UP)
        )
        self.wait()
        self.play(
            ShowCreationThenFadeOut(rects[2]),
            TransformFromCopy(*braces[1:3]),
            FadeIn(words[2], UP),
        )
        self.wait()

        # Position derivative
        v1_tex = "\\vec{\\textbf{v}}_1"
        kw = {
            "tex_to_color_map": {
                x1_tex: BLUE_C,
                v1_tex: RED,
            }
        }
        x_deriv = OldTex(
            "{d", x1_tex, "\\over", "dt}", "=", v1_tex, **kw
        )
        x_deriv.to_corner(UL)
        v_deriv = OldTex(
            "{d", v1_tex, "\\over", "dt}", "=", **kw
        )

        # Make way
        law.generate_target()
        lt = law.target
        lt.to_edge(RIGHT)
        lt[6].fade(1)
        lt[:6].align_to(lt[6], RIGHT)
        lt[:3].fade(1)
        v_deriv.next_to(lt[3], LEFT)

        self.play(
            FadeInFromDown(x_deriv),
            MoveToTarget(law),
            braces[1:].align_to, lt, RIGHT,
            MaintainPositionRelativeTo(words[1:], braces[1:]),
            FadeOut(words[0]),
            FadeOut(braces[0]),
        )
        self.play(ShowCreationThenFadeAround(x_deriv))

        self.play(
            TransformFromCopy(
                x_deriv.get_part_by_tex(v1_tex),
                v_deriv.get_part_by_tex(v1_tex),
            ),
            Write(VGroup(*filter(
                lambda m: m is not v_deriv.get_part_by_tex(v1_tex),
                v_deriv,
            )))
        )

        x_parts = law.get_parts_by_tex(x1_tex)
        self.play(
            TransformFromCopy(
                x_deriv.get_parts_by_tex(x1_tex),
                x_parts.copy(),
                remover=True,
                path_arc=30 * DEGREES,
            )
        )
        self.play(
            LaggedStartMap(
                ShowCreationThenFadeAround,
                x_parts
            )
        )
        self.wait()
