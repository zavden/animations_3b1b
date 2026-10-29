# ==============================================================================
# Scene:      JewelPairPlane
# Source:     videos/_2017/borsuk.py (lines 2375-2403)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl JewelPairPlane.py JewelPairPlane -w -m --fps 15
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


class JewelPairPlane(GraphScene):
    CONFIG = {
        "camera_class" : ThreeDCamera,
        "x_labeled_nums" : [],
        "y_labeled_nums" : [],
        "thief_number" : 1,
        "colors" : [BLUE, GREEN],
    }
    def construct(self):
        self.setup_axes()
        point = self.coords_to_point(4, 5)
        dot = Dot(point, color = WHITE)
        coord_pair = OldTex(
            "\\big(", 
            "\\text{Thief %d }"%self.thief_number, "X", ",", 
            "\\text{Thief %d }"%self.thief_number, "X", 
            "\\big)"
        )
        # coord_pair.scale(1.5)
        to_replace = [coord_pair[i] for i in [2, 5]]
        for mob, color in zip(to_replace, self.colors):
            jewel = Jewel(color = color)
            jewel.replace(mob)
            coord_pair.remove(mob)
            coord_pair.add(jewel)
        coord_pair.next_to(dot, UP+RIGHT, buff = 0)

        self.example_coords = VGroup(dot, coord_pair)
        self.add(self.example_coords)
