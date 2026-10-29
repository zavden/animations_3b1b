# ==============================================================================
# Scene:      TechnicalNote
# Source:     videos/_2018/turbulence.py (lines 1481-1510)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TechnicalNote.py TechnicalNote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TechnicalNote(Scene):
    def construct(self):
        title = OldTexText("Technical note:")
        title.to_edge(UP)
        title.set_color(RED)
        self.add(title)

        words = OldTexText("""
            This idea of quantifying the energy held at different
            length scales is typically defined
            in terms of an ``energy spectrum'' involving the Fourier
            transform of a function measuring the correlations
            between the fluid's velocities at different points in space.
            I know, yikes!
            \\quad\\\\
            \\quad\\\\
            Building up the relevant background for that is a bit cumbersome,
            so we'll be thinking about the energy at different scales in
            terms of all eddy's with a given diameter.  This is admittedly
            a less well-defined notion, but it does capture the spirit
            of Kolmogorov's result.
            \\quad\\\\
            \\quad\\\\
            See the links in the description for more details,
            if you're curious.
        """, alignment="")
        words.scale(0.75)
        words.next_to(title, DOWN, LARGE_BUFF)

        self.add(title, words)
