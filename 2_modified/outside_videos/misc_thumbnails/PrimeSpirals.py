# ==============================================================================
# Scene:      PrimeSpirals
# Source:     videos/outside_videos/misc_thumbnails.py (lines 255-269)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PrimeSpirals.py PrimeSpirals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - missing import sympy (in the original it came through Grant's manim_imports_ext)
# ==============================================================================

# CHANGE: missing import sympy (in the original it came through Grant's manim_imports_ext)
from manim_imports_ext import *
import sympy

class PrimeSpirals(InteractiveScene):
    def construct(self):
        N = 10000
        primes = np.array(list(sympy.primerange(0, 10000)))
        points = np.array([
            primes * np.cos(primes),
            primes * np.sin(primes),
            np.zeros(len(primes))
        ]).T
        dots = DotCloud(points)
        dots.set_width(15, about_point=ORIGIN)
        dots.make_3d()
        dots.set_color(TEAL)
        dots.set_radii(np.linspace(0.02, 0.1, len(primes)))
        self.add(dots)
