# ==============================================================================
# Scene:      RewriteEquation
# Source:     videos/_2018/WindingNumber.py (lines 1460-1501)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RewriteEquation.py RewriteEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7


class RewriteEquation(Scene):
    def construct(self):
        # Can maybe use get_center() to perfectly center Groups before and after transform

        f_old = OldTex("f(x)")
        f_new = f_old.copy()
        equals_old = OldTex("=")
        equals_old_2 = equals_old.copy()
        equals_new = equals_old.copy()
        g_old = OldTex("g(x)")
        g_new = g_old.copy()
        minus_new = OldTex("-")
        zero_new = OldTex("0")
        f_old.next_to(equals_old, LEFT)
        g_old.next_to(equals_old, RIGHT)
        minus_new.next_to(g_new, LEFT)
        f_new.next_to(minus_new, LEFT)
        equals_new.next_to(g_new, RIGHT)
        zero_new.next_to(equals_new, RIGHT)

        # where_old = OldTexText("Where does ")
        # where_old.next_to(f_old, LEFT)
        # where_new = where_old.copy()
        # where_new.next_to(f_new, LEFT)
        
        # qmark_old = OldTexText("?")
        # qmark_old.next_to(g_old, RIGHT)
        # qmark_new = qmark_old.copy()
        # qmark_new.next_to(zero_new, RIGHT)
        
        self.add(f_old, equals_old, equals_old_2, g_old) #, where_old, qmark_old)
        self.wait()
        self.play(
            ReplacementTransform(f_old, f_new),
            ReplacementTransform(equals_old, equals_new), 
            ReplacementTransform(g_old, g_new), 
            ReplacementTransform(equals_old_2, minus_new),
            ShowCreation(zero_new),
            # ReplacementTransform(where_old, where_new),
            # ReplacementTransform(qmark_old, qmark_new),
        )
        self.wait()
