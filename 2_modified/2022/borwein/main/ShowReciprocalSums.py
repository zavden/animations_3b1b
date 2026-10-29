# ==============================================================================
# Scene:      ShowReciprocalSums
# Source:     videos/_2022/borwein/main.py (lines 987-1028)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowReciprocalSums.py ShowReciprocalSums -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex requires a StringMobject and OldTex is not one; it matches glyphs by shape)
# ==============================================================================

from manim_imports_ext import *

class ShowReciprocalSums(InteractiveScene):
    max_shown_parts = 10

    def construct(self):
        # Equations
        equations = VGroup(*(
            self.get_sum(n)
            for n in range(1, 8)
        ))
        for equation in equations:
            t2c = dict(zip(
                [f"1 / {2 * k + 1}" for k in range(1, 10)],
                color_gradient([BLUE, YELLOW, RED], 8)
            ))
            equation.set_color_by_tex_to_color_map(t2c)
        equations[-1][-1].set_color(RED)
        equations.arrange(DOWN, aligned_edge=RIGHT, buff=MED_LARGE_BUFF)
        equations.center()

        self.add(equations[0])
        for eq1, eq2 in zip(equations, equations[1:]):
            # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
            self.play(TransformMatchingShapes(eq1.copy(), eq2))
            self.wait()
        self.wait()

    def get_sum(self, n):
        tex_parts = []
        tally = 0
        msp = self.max_shown_parts
        for k in range(1, n + 1):
            new_parts = [f"1 / {2 * k + 1}", "+"]
            if n > msp:
                if k < msp - 1 or k == n:
                    tex_parts.extend(new_parts)
                elif k == msp - 1:
                    tex_parts.extend([R"\cdots", "+"])
            else:
                tex_parts.extend(new_parts)
            tally += 1 / (2 * k + 1)
        tex_parts[-1] = "="
        tex_parts.append(R"{:.06f}\dots".format(tally))
        return OldTex(*tex_parts)
