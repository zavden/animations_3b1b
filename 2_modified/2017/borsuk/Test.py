# ==============================================================================
# Scene:      Test
# Source:     videos/_2017/borsuk.py (lines 2629-2643)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Test.py Test -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
#   - painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
# ==============================================================================

from manim_imports_ext import *

class Jewel(VMobject):
    CONFIG = {
        "color" : WHITE,
        "fill_opacity" : 0.75,
        "stroke_width" : 0,
        "height" : 0.5,
        "num_equator_points" : 5,
        "sun_vect" : OUT+LEFT+UP,
    }
    def init_points(self):
        for vect in OUT, IN:
            compass_vects = list(compass_directions(self.num_equator_points))
            if vect is IN:
                compass_vects.reverse()
            for vect_pair in adjacent_pairs(compass_vects):
                self.add(Polygon(vect, *vect_pair))
        self.set_height(self.height)
        self.rotate(-np.pi/2-np.pi/24, RIGHT)        
        self.rotate(-np.pi/12, UP)
        self.submobjects.sort(
            # CHANGE: undefined name m1 in the sort key (NameError once init_points runs); sort the faces by z
            # CHANGE: painter order: draw the faces from back to front (smaller z first); the first fix had the sign reversed
            key=lambda m: m.get_center()[2]
        )
        return self


class Necklace(VMobject):
    CONFIG = {
        "width" : FRAME_WIDTH - 1,
        "jewel_buff" : MED_SMALL_BUFF,
        "chain_color" : GREY,
        "default_colors" : [(4, BLUE), (6, WHITE), (4, GREEN)]
    }
    def __init__(self, *colors, **kwargs):
        digest_config(self, kwargs, locals())
        if len(colors) == 0:
            self.colors = self.get_default_colors()
        VMobject.__init__(self, **kwargs)

    def get_default_colors(self):
        result = list(it.chain(*[
            num*[color]
            for num, color in self.default_colors
        ]))
        random.shuffle(result)
        return result

    def init_points(self):
        jewels = VGroup(*[
            Jewel(color = color)
            for color in self.colors
        ])
        jewels.arrange(buff = self.jewel_buff)
        jewels.set_width(self.width)
        jewels.center()
        j_to_j_dist = (jewels[1].get_center()-jewels[0].get_center())[0]

        chain = Line(
            jewels[0].get_center() + j_to_j_dist*LEFT/2, 
            jewels[-1].get_center() + j_to_j_dist*RIGHT/2, 
            color = self.chain_color,
        )
        self.add(chain, *jewels)
        self.chain = chain
        self.jewels = jewels


class Test(Scene):
    CONFIG = {
        "camera_class" : ThreeDCamera,
    }
    def construct(self):
        randy = Randolph()
        necklace = Necklace()
        necklace.insert_n_curves(20)
        # necklace.apply_function(
        #     lambda (x, y, z) : x*RIGHT + (y + 0.1*x**2)*UP
        # )
        necklace.set_width(randy.get_width() + 1)
        necklace.move_to(randy)

        self.add(randy, necklace)
