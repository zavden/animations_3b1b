# ==============================================================================
# Scene:      BarChartTest
# Source:     videos/_2020/beta/beta1.py (lines 9-14)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BarChartTest.py BarChartTest -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - BarChart requires the list of values (the original omitted it: a test scene that already failed); example values are passed
# ==============================================================================

from manim_imports_ext import *

# Scenes
class BarChartTest(Scene):
    def construct(self):
        # CHANGE: BarChart requires the list of values (the original omitted it: a test scene that already failed); example values are passed
        bar_chart = BarChart([0.3, 0.8, 0.5, 0.65])
        bar_chart.to_edge(DOWN)
        self.add(bar_chart)
