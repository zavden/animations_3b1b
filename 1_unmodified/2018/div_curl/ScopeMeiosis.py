# ==============================================================================
# Scene:      ScopeMeiosis
# Source:     videos/_2018/div_curl.py (lines 937-1009)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ScopeMeiosis.py ScopeMeiosis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ScopeMeiosis(PiCreatureScene):
    CONFIG = {
        "default_pi_creature_kwargs": {
            "flip_at_start": True,
            "color": GREY_BROWN,
        },
        "default_pi_creature_start_corner": DR,
    }

    def construct(self):
        morty = self.pi_creature
        section_titles = VGroup(*list(map(TexText, [
            "Background on div/curl",
            "Conformal maps",
            "Conformal map $\\Rightarrow" +
            "\\text{div}\\textbf{F} = " +
            "\\text{curl}\\textbf{F} = 0$",
            "Complex derivatives",
        ])))
        sections = VGroup(*[
            VGroup(title, self.get_lines(title, 3))
            for title in section_titles
        ])
        sections.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        sections.to_edge(UP)

        top_title = section_titles[0]
        lower_sections = sections[1:]

        self.add(sections)
        modes = [
            "pondering",
            "pondering",
            "bump",
            "bump",
            "concerned_musician",
            "concerned_musician",
        ]

        for n, mode in zip(list(range(6)), modes):
            if n % 2 == 1:
                top_title = lines
                lines = self.get_lines(top_title, 4)
            else:
                lines = self.get_lines(top_title, 6)
            lower_sections.generate_target()
            lower_sections.target.next_to(
                lines, DOWN, MED_LARGE_BUFF, LEFT,
            )
            self.play(
                ShowCreation(lines),
                MoveToTarget(lower_sections),
                morty.change, mode, lines,
            )

    def get_lines(self, title, n_lines):
        lines = VGroup(*[
            Line(3 * LEFT, 3 * RIGHT, color=GREY_B)
            for x in range(n_lines)
        ])
        lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        lines.next_to(
            title, DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        lines[-1].pointwise_become_partial(
            lines[-1], 0, random.random()
        )
        return lines
