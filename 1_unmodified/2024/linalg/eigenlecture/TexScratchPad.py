# ==============================================================================
# Scene:      TexScratchPad
# Source:     videos/_2024/linalg/eigenlecture.py (lines 21-236)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TexScratchPad.py TexScratchPad -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TexScratchPad(InteractiveScene):
    def construct(self):
        # ODE
        tex = Tex(R"""
            \left[\begin{array}{c} x'(t) \\ y'(t) \end{array}\right] =
            \left[\begin{array}{cc} 1 & 2 \\ 3 & 1 \end{array}\right]
            \left[\begin{array}{c} x(t) \\ y(t) \end{array}\right]
        """)

        # ODE in new coordinates
        tex = Tex(
            R"""
            \left[\begin{array}{c} \tilde{x}'(t) \\ \tilde{y}'(t) \end{array}\right] =
            \left[\begin{array}{cc} \lambda_1 & 0 \\ 0 & \lambda_2 \end{array}\right]
            \left[\begin{array}{c} \tilde{x}(t) \\ \tilde{y}(t) \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )

        # Solution to ODE in new coordinates
        tex = Tex(
            R"""
            \tilde{x}(t) = \tilde{x}_0 e^{\lambda_1 t} \\
            \tilde{y}(t) = \tilde{y}_0 e^{\lambda_2 t} \\
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(tex)

        # Meaning of the alternate coordinates
        tex = Tex(
            R"""
            x \hat{\textbf{\i}} + y \hat{\textbf{\j}} =
            \tilde{x} \vec{\textbf{v}}_1 + \tilde{y} \vec{\textbf{v}}_2
            """,
            t2c={
                R"\lambda_1": TEAL,
                R"\lambda_2": YELLOW,
                R"\vec{\textbf{v}}_1": TEAL,
                R"\vec{\textbf{v}}_2": YELLOW,
                R"\hat{\textbf{\i}}": GREEN,
                R"\hat{\textbf{\j}}": RED,
            }
        )
        self.add(tex)

        # Change of basis matrix
        mat_tex = Tex(
            R"""
            \left[\begin{array}{cc} a & b \\ c & d \end{array}\right]
            """,
        )
        old_cols = VGroup(
            mat_tex[1:4:2],
            mat_tex[2:5:2],
        )
        old_cols.set_opacity(0)
        new_cols = VGroup(
            Tex(R"\vec{\textbf{v}}_1").set_color(TEAL),
            Tex(R"\vec{\textbf{v}}_2").set_color(YELLOW),
        )
        for new_col, old_col in zip(new_cols, old_cols):
            lines = Line(UP, DOWN).set_height(0.35).replicate(2)
            lines[0].next_to(new_col, UP, SMALL_BUFF)
            lines[1].next_to(new_col, DOWN, SMALL_BUFF)
            new_col.add(lines)
            new_col.match_height(mat_tex)
            new_col.move_to(old_col)
        new_cols[1].align_to(new_cols[0], UP)
        cob_matrix = VGroup(mat_tex, new_cols)

        og_matrix = Tex(
            R"""
            \left[\begin{array}{cc} a & b \\ c & d \end{array}\right]
            """,
        )

        inv_cob = cob_matrix.copy()
        inv_cob.add(Tex(R"-1", font_size=24).next_to(inv_cob, RIGHT, SMALL_BUFF, aligned_edge=UP))

        diag_matrix = Tex(
            R"""
            \left[\begin{array}{cc} \lambda_1 & 0 \\ 0 & \lambda_2 \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )

        expr = VGroup(
            inv_cob, og_matrix, cob_matrix,
            Tex("="), diag_matrix
        )
        expr.arrange(RIGHT, buff=MED_SMALL_BUFF)

        self.add(expr)

        # Show powers
        diag_matrix = Tex(
            R"""
            \left[\begin{array}{cc} \lambda_1 & 0 \\ 0 & \lambda_2 \end{array}\right]^n = 
            \left[\begin{array}{cc} \lambda_1^n & 0 \\ 0 & \lambda_2^n \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(diag_matrix)

        # Solve
        diag_matrix = Tex(
            R"""
            \left[\begin{array}{cc} 0 & 1 \\ 1 & 1 \end{array}\right]^n = 
            \left[\begin{array}{cc} \lambda_1^n & 0 \\ 0 & \lambda_2^n \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(diag_matrix)

        # Write eigenvectors
        eigen1_equation = Tex(
            R"""
            \left[\begin{array}{cc} 0 & 1 \\ 1 & 1 \end{array}\right]
            \left[\begin{array}{c} 1  \\ \lambda_1 \end{array}\right] =
            \left[\begin{array}{c} \lambda_1  \\ \lambda_1 + 1 \end{array}\right] =
            \left[\begin{array}{c} \lambda_1  \\ \lambda_1^2 \end{array}\right] =
            \lambda_1 \left[\begin{array}{c} 1  \\ \lambda_1 \end{array}\right] =
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        eigen1 = Tex(
            R"""
            \vec{\textbf{v}}_1 = \left[\begin{array}{c} 1  \\ \lambda_1 \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        eigen2 = Tex(
            R"""
            \vec{\textbf{v}}_2 = \left[\begin{array}{c} 1 \\ \lambda_2 \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(eigen2)

        # Eigen matrix
        fib_cob = Tex(
            R"""
            S = \left[\begin{array}{cc} 1 & 1  \\ \lambda_1 & \lambda_2 \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(fib_cob)

        # Fibonacci expression
        fib_expr = Tex(
            R"""
            A^n \left[\begin{array}{c} 0 \\ 1 \end{array}\right] =
            \left[\begin{array}{c} F_n \\ F_{n + 1} \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(fib_expr)

        # Fib formula
        fib_formula = Tex(
            R"""
            F_n = \frac{\lambda_1^n - \lambda_2^n}{\lambda_1 - \lambda_2}
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(fib_formula)

        # Translation
        diag_matrix = Tex(
            R"""
            S \left[\begin{array}{cc} \lambda_1^n & 0 \\ 0 & \lambda_2^n \end{array}\right] S^{-1} = 
            A^n
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(diag_matrix)

        # Matrix
        tex = Tex(R"""
            \left[\begin{array}{cc} 3 & 1 \\ 0 & 2 \end{array}\right]
        """)
        tex[1:4:2].set_color(GREEN)
        tex[2:5:2].set_color(RED)
        self.add(tex)

        # Basis
        basis_syms = VGroup(
            Tex(R"\hat{\textbf{\i}}").set_color(GREEN),
            Tex(R"\hat{\textbf{\j}}").set_color(RED),
        )
        basis_syms.arrange(RIGHT)
        self.add(basis_syms)

        # Equation
        tex = Tex(R"""
            \left[\begin{array}{c} x \\ y \end{array}\right] =
            \left[\begin{array}{c} 1 \\ 1 + \sqrt{5} \end{array}\right]
        """, t2c={R"\lambda": TEAL})
        self.add(tex)

        # List bases
        tex = Tex(R"""
            \left[\begin{array}{c} 1 \\ 0 \end{array}\right],
            \left[\begin{array}{c} 0 \\ 1 \end{array}\right]
        """)
        self.add(tex)

        # Diagonal matrix
        tex = Tex(
            R"""
                \left[\begin{array}{cc} \lambda_1 & 0 \\ 0 & \lambda_2 \end{array}\right]
            """,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        self.add(tex)
