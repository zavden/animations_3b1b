# ==============================================================================
# Scene:      SimpleIPTProof
# Source:     videos/_2018/basel/basel2.py (lines 2353-2433)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleIPTProof.py SimpleIPTProof -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class SimpleIPTProof(Scene):
    def construct(self):
        A = 5*RIGHT
        B = 3*UP
        C = ORIGIN
        #Dumb and inefficient
        alphas = np.linspace(0, 1, 500)
        i = np.argmin([get_norm(interpolate(A, B, a)) for a in alphas])
        H = interpolate(A, B, alphas[i])
        triangle = VGroup(
            Line(C, A, color = BLUE),
            Line(C, B, color = RED),
            Line(A, B, color = WHITE),
            Line(C, H, color = GREEN)
        )
        for line, char in zip(triangle, ["a", "b", "c", "h"]):
            label = OldTex(char)
            label.match_color(line)
            vect = line.get_center() - triangle.get_center()
            vect /= get_norm(vect)
            label.next_to(line.get_center(), vect)
            triangle.add(label)
            if char == "h":
                label.next_to(line.get_center(), UP+LEFT, SMALL_BUFF)

        triangle.to_corner(UP+LEFT)
        self.add(triangle)

        argument_lines = VGroup(
            OldTex(
                "\\text{Area} = ", 
                "{1 \\over 2}", "a", "b", "=",
                "{1 \\over 2}", "c", "h"
            ),
            OldTex("\\Downarrow"),
            OldTex("a^2", "b^2", "=", "c^2", "h^2"),
            OldTex("\\Downarrow"),
            OldTex(
                "a^2", "b^2", "=", 
                "(",  "a^2", "+", "b^2", ")", "h^2"
            ),
            OldTex("\\Downarrow"),
            OldTex(
                "{1 \\over ", "h^2}", "=", 
                "{1 \\over ", "b^2}", "+", 
                "{1 \\over ", "a^2}",
            ),
        )
        argument_lines.arrange(DOWN)
        for line in argument_lines:
            line.set_color_by_tex_to_color_map({
                "a" : BLUE,
                "b" : RED,
                "h" : GREEN,
                "Area" : WHITE,
                "Downarrow" : WHITE,
            })
            all_equals = line.get_parts_by_tex("=")
            if all_equals:
                line.alignment_mob = all_equals[-1]
            else:
                line.alignment_mob = line[0]
            line.shift(-line.alignment_mob.get_center()[0]*RIGHT)
        argument_lines.next_to(triangle, RIGHT)
        argument_lines.to_edge(UP)

        prev_line = argument_lines[0]
        self.play(FadeIn(prev_line))
        for arrow, line in zip(argument_lines[1::2], argument_lines[2::2]):
            line.save_state()
            line.shift(
                prev_line.alignment_mob.get_center() - \
                line.alignment_mob.get_center() 
            )
            line.fade(1)
            self.play(
                line.restore,
                GrowFromPoint(arrow, arrow.get_top())
            )
            self.wait()
            prev_line = line
