# ==============================================================================
# Scene:      IllustrateAreaModelExpectation
# Source:     videos/_2018/eop/chapter1/area_model_expectation.py (lines 6-92)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/histograms.py
#
# Run from this folder:
#     manimgl IllustrateAreaModelExpectation.py IllustrateAreaModelExpectation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - bar.height/init_points() replaced: zero-height bars are built with height 0.01 directly (GL Rectangle has no height attribute)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/histograms.py -----

class Histogram(VMobject):

    CONFIG = {
        "start_color" : RED,
        "end_color" : BLUE,
        "x_scale" : 1.0,
        "y_scale" : 1.0,
        "x_labels" : "auto", # widths, mids, auto, none, [...]
        "y_labels" : "auto", # auto, none, [...]
        "y_label_position" : "top", # "center"
        "x_min" : 0,
        "bar_stroke_width" : 5,
        "outline_stroke_width" : 0,
        "stroke_color" : WHITE
    }

    def __init__(self, x_values, y_values, mode = "widths", **kwargs):
        # mode = "widths" : x_values means the widths of the bars
        # mode = "posts"  : x_values means the delimiters btw the bars 

        digest_config(self, kwargs)

        if mode == "widths" and len(x_values) != len(y_values):
            raise Exception("Array lengths do not match up!")
        elif mode == "posts" and len(x_values) != len(y_values) + 1:
            raise Exception("Array lengths do not match up!")


        self.y_values = y_values
        self.x_values = x_values
        self.mode = mode
        self.process_values()

        VMobject.__init__(self, **kwargs)
        

    def process_values(self):

         # preliminaries
        self.y_values = np.array(self.y_values)

        if self.mode == "widths":
            self.widths = self.x_values
            self.posts = np.cumsum(self.widths)
            self.posts = np.insert(self.posts, 0, 0)
            self.posts += self.x_min
            self.x_max = self.posts[-1]
        elif self.mode == "posts":
            self.posts = self.x_values
            self.widths = self.x_values[1:] - self.x_values[:-1]
            self.x_min = self.posts[0]
            self.x_max = self.posts[-1]
        else:
            raise Exception("Invalid mode or no mode specified!")

        self.x_mids = 0.5 * (self.posts[:-1] + self.posts[1:])

        self.widths_scaled = self.x_scale * self.widths
        self.posts_scaled = self.x_scale * self.posts
        self.x_min_scaled = self.x_scale * self.x_min
        self.x_max_scaled = self.x_scale * self.x_max

        self.y_values_scaled = self.y_scale * self.y_values



    def init_points(self):

        self.process_values()
        for submob in self.submobjects:
            self.remove(submob)

        def empty_string_array(n):
            arr = []
            for i in range(n):
                arr.append("")
            return arr

        def num_arr_to_string_arr(arr): # converts number array to string array
            ret_arr = []
            for x in arr:
                if x == np.floor(x):
                    new_x = int(np.floor(x))
                else:
                    new_x = x
                ret_arr.append(str(new_x))
            return ret_arr

        previous_bar = ORIGIN
        self.bars = VGroup()
        self.x_labels_group = VGroup()
        self.y_labels_group = VGroup()
        outline_points = []

        if self.x_labels == "widths":
            self.x_labels = num_arr_to_string_arr(self.widths)
        elif self.x_labels == "mids":
            self.x_labels = num_arr_to_string_arr(self.x_mids)
        elif self.x_labels == "auto":
            self.x_labels = num_arr_to_string_arr(self.x_mids)
        elif self.x_labels == "none":
            self.x_labels = empty_string_array(len(self.widths))

        if self.y_labels == "auto":
            self.y_labels = num_arr_to_string_arr(self.y_values)
        elif self.y_labels == "none":
            self.y_labels = empty_string_array(len(self.y_values))




        for (i,x) in enumerate(self.x_mids):

            # CHANGE: GL Rectangle has no .height attribute nor init_points(); give zero-height bars the 0.01 height from the start
            bar = Rectangle(
                width = self.widths_scaled[i],
                height = self.y_values_scaled[i] if self.y_values_scaled[i] != 0 else 0.01,
                stroke_width = self.bar_stroke_width,
                stroke_color = self.stroke_color,
            )

            t = float(x - self.x_min)/(self.x_max - self.x_min)
            bar_color = interpolate_color(
                self.start_color,
                self.end_color,
                t
            )
            bar.set_fill(color = bar_color, opacity = 1)
            bar.next_to(previous_bar,RIGHT,buff = 0, aligned_edge = DOWN)
            
            self.bars.add(bar)

            x_label = OldTexText(self.x_labels[i])
            x_label.next_to(bar,DOWN)
            self.x_labels_group.add(x_label)

            y_label = OldTexText(self.y_labels[i])
            if self.y_label_position == "top":
                y_label.next_to(bar, UP)
            elif self.y_label_position == "center":
                y_label.move_to(bar)
            else:
                raise Exception("y_label_position must be top or center")
            self.y_labels_group.add(y_label)

            if i == 0:
                # start with the lower left
                outline_points.append(bar.get_anchors()[-2])

            # upper two points of each bar
            outline_points.append(bar.get_anchors()[0])
            outline_points.append(bar.get_anchors()[1])

            previous_bar = bar
        # close the outline
            # lower right
        outline_points.append(bar.get_anchors()[2])
            # lower left
        outline_points.append(outline_points[0])

        self.outline = Polygon(*outline_points,
            stroke_width = self.outline_stroke_width,
            stroke_color = self.stroke_color)
        self.add(self.bars, self.x_labels_group, self.y_labels_group, self.outline)

        self.move_to(ORIGIN)

    def get_lower_left_point(self):
        return self.bars[0].get_anchors()[-2]



# ----- From _2018/eop/chapter1/area_model_expectation.py -----

class IllustrateAreaModelExpectation(Scene):

    def construct(self):

        formula = OldTex("E[X] = \sum_{i=1}^N p_i x_i").move_to(3 * LEFT + UP)
        self.play(Write(formula))


        x_scale = 5.0
        y_scale = 1.0

        probabilities = np.array([1./8, 3./8, 3./8, 1./8])
        prob_strings = ["{1\over 8}","{3\over 8}","{3\over 8}","{1\over 8}"]
        cumulative_probabilities = np.cumsum(probabilities)
        cumulative_probabilities = np.insert(cumulative_probabilities, 0, 0)
        y_values = np.array([0, 1, 2, 3])

        hist = Histogram(probabilities, y_values,
            mode = "widths",
            x_scale = x_scale,
            y_scale = y_scale,
            x_labels = "none"
        )

        flat_hist = Histogram(probabilities, 0 * y_values,
            mode = "widths",
            x_scale = x_scale,
            y_scale = y_scale,
            x_labels = "none"
        )

        self.play(FadeIn(flat_hist))
        self.play(
            ReplacementTransform(flat_hist, hist)
        )

        braces = VGroup()
        p_labels = VGroup()
        # add x labels (braces)
        for (p,string,bar) in zip(probabilities, prob_strings,hist.bars):
            brace = Brace(bar, DOWN, buff = 0.1)
            p_label = OldTex(string).next_to(brace, DOWN, buff = SMALL_BUFF).scale(0.7)
            group = VGroup(brace, p_label)
            braces.add(brace)
            p_labels.add(p_label)
            
        self.play(
            LaggedStartMap(FadeIn,braces),
            LaggedStartMap(FadeIn, p_labels)
        )



        y_average = np.mean(y_values)
        averaged_y_values = y_average * np.ones(np.shape(y_values))

        averaged_hist = flat_hist = Histogram(probabilities, averaged_y_values,
            mode = "widths",
            x_scale = x_scale,
            y_scale = y_scale,
            x_labels = "none",
            y_labels = "none"
        ).fade(0.2)

        ghost_hist = hist.copy().fade(0.8)
        self.bring_to_back(ghost_hist)

        self.play(Transform(hist, averaged_hist, run_time = 3))
        self.wait()

        average_brace = Brace(averaged_hist, RIGHT, buff = 0.1)
        average_label = OldTex(str(y_average)).scale(0.7)
        average_label.next_to(average_brace, RIGHT, SMALL_BUFF)
        average_group = VGroup(average_brace, average_label)

        one_brace = Brace(averaged_hist, DOWN, buff = 0.1)
        one_p_label = OldTex(str(1)).next_to(one_brace, DOWN, buff = SMALL_BUFF).scale(0.7)
        one_group = VGroup(one_brace, one_p_label)

        self.play(
            FadeIn(average_group),
            Transform(braces, one_brace),
            Transform(p_labels, one_p_label),
        )
        
        rect = SurroundingRectangle(formula, buff = 0.5 * MED_LARGE_BUFF)
        self.play(ShowCreation(rect))
