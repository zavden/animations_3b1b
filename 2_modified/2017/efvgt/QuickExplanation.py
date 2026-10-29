# ==============================================================================
# Scene:      QuickExplanation
# Source:     videos/_2017/efvgt.py (lines 236-332)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl QuickExplanation.py QuickExplanation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
# ==============================================================================

from manim_imports_ext import *

# CHANGE: The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
from once_useful_constructs.complex_transformation_scene import ComplexTransformationScene


class QuickExplanation(ComplexTransformationScene):
    CONFIG = {
        "plane_config" : {
            "x_line_frequency" : 1,
            "y_line_frequency" : 1,
            "secondary_line_ratio" : 1,
            "space_unit_to_x_unit" : 1.5,
            "space_unit_to_y_unit" : 1.5,
        },
        "background_fade_factor" : 0.2,
        "background_label_scale_val" : 0.7,
        "velocity_color" : RED,
        "position_color" : YELLOW,
    }
    def construct(self):
        # self.add_transformable_plane()
        self.add_equation()
        self.add_explanation()
        self.add_vectors()

    def add_equation(self):
        equation = OldTex(
            "\\frac{d(e^{it})}{dt}",
            "=",
            "i", "e^{it}"
        )
        equation[0].set_color(self.velocity_color)
        equation[-1].set_color(self.position_color)
        equation.add_background_rectangle()        
        brace = Brace(equation, UP)
        equation.add(brace)
        brace_text = OldTexText(
            "Velocity vector", "is a", 
            "$90^\\circ$ \\\\ rotation", 
            "of", "position vector"
        )
        brace_text[0].set_color(self.velocity_color)
        brace_text[-1].set_color(self.position_color)
        brace_text.add_background_rectangle()
        brace_text.scale(0.8)
        brace_text.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        equation.next_to(brace_text, DOWN)

        self.add_foreground_mobjects(brace_text, equation)
        self.brace_text = brace_text

    def add_explanation(self):
        words = OldTexText("""
            Only a walk around the unit
            circle at rate 1 satisfies both
            this property and e^0 = 1.
        """)
        words.scale(0.8)
        words.add_background_rectangle()
        words.to_corner(UP+RIGHT, buff = MED_SMALL_BUFF)
        arrow = Arrow(RIGHT, 1.5*LEFT, color = WHITE)
        arrow.to_edge(UP)

        self.add(words, arrow)

    def add_vectors(self):
        right = self.z_to_point(1)
        s_vector = Arrow(
            ORIGIN, right,
            tip_length = 0.2,
            buff = 0,            
            color = self.position_color,
        )

        v_vector = s_vector.copy().rotate(np.pi/2)
        v_vector.set_color(self.velocity_color)
        circle = Circle(
            radius = self.z_to_point(1)[0],
            color = self.position_color
        )

        self.wait(2)
        self.play(ShowCreation(s_vector))
        self.play(ReplacementTransform(
            s_vector.copy(), v_vector, path_arc = np.pi/2
        ))
        self.wait()
        self.play(v_vector.shift, right)
        self.wait()
        self.vectors = VGroup(s_vector, v_vector)

        kwargs = {
            "rate_func" : None,
            "run_time" : 5,
        }
        rotation = Rotating(self.vectors, about_point = ORIGIN, **kwargs)
        self.play(
            ShowCreation(circle, **kwargs),
            rotation            
        )
        self.play(rotation)
        self.play(rotation)
