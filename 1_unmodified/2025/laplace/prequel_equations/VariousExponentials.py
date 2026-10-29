# ==============================================================================
# Scene:      VariousExponentials
# Source:     videos/_2025/laplace/prequel_equations.py (lines 249-273)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VariousExponentials.py VariousExponentials -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VariousExponentials(InteractiveScene):
    def construct(self):
        # Test
        exp_st = Tex(R"e^{st}", t2c={"s": YELLOW, "t": BLUE}, font_size=90)
        gen_exp = Tex(R"e^{+0.50 t}", t2c={"+0.50": YELLOW, "t": BLUE}, font_size=90)
        exp_st.to_edge(UP, buff=MED_LARGE_BUFF)
        gen_exp.move_to(exp_st)

        num = gen_exp["+0.50"]
        num.set_opacity(0)
        gen_exp["t"].scale(1.25, about_edge=UL)

        s_num = DecimalNumber(-1.00, edge_to_fix=ORIGIN, include_sign=True)
        s_num.set_color(YELLOW)
        s_num.replace(num, dim_to_match=1)

        self.add(gen_exp, s_num)
        self.play(ChangeDecimalToValue(s_num, 0.5, run_time=4))
        self.wait()
        self.play(LaggedStart(
            ReplacementTransform(gen_exp["e"][0], exp_st["e"][0]),
            ReplacementTransform(s_num, exp_st["s"]),
            ReplacementTransform(gen_exp["t"][0], exp_st["t"][0]),
        ))
        self.wait()
