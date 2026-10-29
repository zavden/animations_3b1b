# ==============================================================================
# Scene:      ArctanSqrtPoint1Angle
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 307-310)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArctanSqrtPoint1Angle.py ArctanSqrtPoint1Angle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FourtyFiveDegreeLine(Scene):
    CONFIG = {
        "angle": 45 * DEGREES,
        "label_config": {
            "num_decimal_places": 0,
            "unit": "^\\circ",
            "label_height": 0.3,
        },
        "degrees": True
    }

    def construct(self):
        angle = self.angle
        arc = Arc(angle, radius=1)
        label = DecimalNumber(0, **self.label_config)
        label.set_height(self.label_config["label_height"])
        label.next_to(arc, RIGHT)
        label.shift(0.5 * SMALL_BUFF * UP)
        line1 = Line(ORIGIN, 3 * RIGHT)
        line2 = line1.copy()

        if self.degrees:
            target_value = int(angle / DEGREES)
        else:
            target_value = angle

        self.add(line1, label)
        self.play(
            ChangeDecimalToValue(label, target_value),
            ShowCreation(arc),
            Rotate(line2, angle, about_point=ORIGIN)
        )
        self.wait()


class ArctanSqrtPoint1Angle(FourtyFiveDegreeLine):
    CONFIG = {
        "angle": np.arctan(np.sqrt(0.1)),
    }
