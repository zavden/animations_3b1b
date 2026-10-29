# ==============================================================================
# Scene:      SuperpositionVectorBundle
# Source:     videos/_2024/transformers/mlp.py (lines 2445-2509)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SuperpositionVectorBundle.py SuperpositionVectorBundle -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import torch
from manim_imports_ext import *

class SuperpositionVectorBundle(InteractiveScene):
    def construct(self):
        # Setup
        frame = self.frame
        axes = ThreeDAxes(z_range=(-3, 3))
        axes.scale(0.5)
        vects = VGroup(
            self.get_new_vector(v)
            for v in np.identity(3)
        )

        frame.reorient(23, 71, 0, (0.0, 0.0, 0.5), 3.5)
        frame.add_ambient_rotation(4 * DEGREES)
        self.add(frame)
        self.add(axes)
        self.add(vects)
        self.wait(2)

        # Add a new vector
        n_vects = 10
        for n in range(n_vects):
            new_vect = self.get_new_vector(normalize(np.random.uniform(-1, 1, 3)))
            # self.play(GrowArrow(new_vect))
            vects.add(new_vect)
            self.space_out_vectors(vects, run_time=3 + 0.5 * n)
        self.wait(5)

        # Use tensor flow to repeatedly cram more vectors into a space
        pass

    def get_new_vector(self, coords, color=None, opacity=0.9):
        if color is None:
            color = random_bright_color(hue_range=(0.4, 0.6), luminance_range=(0.5, 0.9))
        vect = Vector(coords, thickness=2.0)
        vect.set_fill(color, opacity=opacity, border_width=2)
        vect.always.set_perpendicular_to_camera(self.frame)
        return vect

    def space_out_vectors(self, vects, run_time=4, learning_rate=0.01):
        num_vectors = len(vects)
        ends = np.array([v.get_end() for v in vects])
        matrix = torch.from_numpy(ends)
        matrix.requires_grad_(True)

        optimizer = torch.optim.Adam([matrix], lr=learning_rate)
        dot_diff_cutoff = 0.01
        id_mat = torch.eye(num_vectors, num_vectors)

        def update_vects(vects):
            optimizer.zero_grad()
            dot_products = matrix @ matrix.T
            # Punish deviation from orthogonal
            diff = dot_products - id_mat
            # loss = (diff.abs() - dot_diff_cutoff).relu().sum()
            loss = diff.pow(6).sum()

            # Extra incentive to keep rows normalized
            loss += num_vectors * diff.diag().pow(2).sum()
            loss.backward()
            optimizer.step()

            for vect, arr in zip(vects, matrix):
                vect.put_start_and_end_on(ORIGIN, arr.detach().numpy())

        self.play(UpdateFromFunc(vects, update_vects, run_time=run_time))
