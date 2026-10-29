# ==============================================================================
# Scene:      CarbonDecayingInMammoth
# Source:     videos/_2019/diffyq/part3/staging.py (lines 853-901)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CarbonDecayingInMammoth.py CarbonDecayingInMammoth -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the local Mammoth.svg has 5 strokes and the full silhouette is index 4 (Grant's original had the body at 9)
# ==============================================================================

from manim_imports_ext import *

class CarbonDecayingInMammoth(Scene):
    def construct(self):
        mammoth = SVGMobject("Mammoth")
        mammoth.set_color(
            interpolate_color(GREY_BROWN, WHITE, 0.25)
        )
        mammoth.set_height(4)
        # CHANGE: the local Mammoth.svg has 5 strokes and the full silhouette is index 4 (Grant's original had the body at 9)
        body = mammoth[4]

        atoms = VGroup(*[
            self.get_atom(body)
            for n in range(600)
        ])

        p_decay = 0.2

        def update_atoms(group, dt):
            for atom in group:
                if np.random.random() < dt * p_decay:
                    group.remove(atom)
            return group
        atoms.add_updater(update_atoms)

        self.add(mammoth)
        self.add(atoms)
        self.wait(20)

    def get_atom(self, body):
        atom = Dot(color=GOLD)
        atom.set_height(0.05)

        dl = body.get_corner(DL)
        ur = body.get_corner(UR)

        wn = 0
        while wn == 0:
            point = np.array([
                interpolate(dl[0], ur[0], np.random.random()),
                interpolate(dl[1], ur[1], np.random.random()),
                0
            ])
            wn = get_winding_number([
                body.point_from_proportion(a) - point
                for a in np.linspace(0, 1, 300)
            ])
            wn = int(np.round(wn))

        atom.move_to(point)
        return atom
