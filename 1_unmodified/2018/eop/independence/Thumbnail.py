# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/eop/independence.py (lines 3512-3537)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


class DangerInProbability(Scene):
    def construct(self):
        warning = self.get_warning_sign()
        probability = OldTexText("Probability")
        probability.scale(2)

        self.play(Write(warning, run_time = 1))
        self.play(
            warning.next_to, probability, UP, LARGE_BUFF,
            LaggedStartMap(FadeIn, probability)
        )
        self.wait()


    #####

    def get_warning_sign(self):
        triangle = RegularPolygon(n = 3, start_angle = np.pi/2)
        triangle.set_stroke(RED, 12)
        triangle.set_height(2)
        bang = OldTexText("!")
        bang.set_height(0.6*triangle.get_height())
        bang.move_to(interpolate(
            triangle.get_bottom(),
            triangle.get_top(),
            0.4,
        ))
        triangle.add(bang)
        return triangle


class Thumbnail(DangerInProbability):
    def construct(self):
        n, p = 15, 0.5
        dist = get_binomial_distribution(n, p)
        values = np.array(list(map(dist, list(range(n+1)))))
        values *= 2
        chart = BarChart(
            values = values,
            label_y_axis = False,
            width = FRAME_WIDTH - 3,
            height = 1.5*FRAME_Y_RADIUS
        )
        chart.to_edge(DOWN)
        self.add(chart)


        warning = self.get_warning_sign()
        warning.set_height(2)
        warning.to_edge(UP)
        self.add(warning)


        words = OldTexText("Independence")
        words.scale(2.5)
        words.next_to(warning, DOWN)
        self.add(words)
