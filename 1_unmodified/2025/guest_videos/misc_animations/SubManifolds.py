# ==============================================================================
# Scene:      SubManifolds
# Source:     videos/_2025/guest_videos/misc_animations.py (lines 52-150)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SubManifolds.py SubManifolds -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SubManifolds(InteractiveScene):
    def construct(self):
        # Set up spaces
        blob = Circle(radius=1).stretch(2.4, 0, about_edge=LEFT)
        blob.shift(0.5 * RIGHT)
        blob.set_fill(BLUE, 0.5)
        blob.set_stroke(BLUE, 1)
        blobs = VGroup()
        for angle in np.arange(0, TAU, TAU / 5):
            new_blob = blob.copy()
            new_blob.scale(random.uniform(0.5, 1), about_edge=LEFT)
            new_blob.stretch(random.uniform(0.9, 1.3), 1)
            new_blob.rotate(angle + random.uniform(-0.5, 0.5), about_point=ORIGIN)
            new_blob.set_color(random_bright_color())
            blobs.add(new_blob)

        middle = Intersection(*blobs)
        middle.match_style(blob)
        middle.reverse_points()

        big_circle = Circle(radius=3.8)
        big_circle.stretch(1.5, 0)
        big_circle.set_fill(TEAL, 0.2)
        big_circle.set_stroke(TEAL, 1)

        # Label all videos
        all_videos_text = Text("Space of\nall videos")
        all_videos_text.next_to(big_circle.pfp(0.1), UR, SMALL_BUFF)
        self.add(all_videos_text)
        self.add(big_circle)

        # Show middle blob
        prompt_words = TexText(R"""
            Videos consistent with \\
            ``An astronaut on the moon\\
            riding a horse that turns\\
            into a giant cat''
        """, alignment="", font_size=24)
        prompt_words[len("Videos consistent with".replace(" ", "")):].set_color(BLUE_B)
        prompt_words.next_to(big_circle.pfp(3 / 8), DR, SMALL_BUFF)
        prompt_words.set_backstroke(BLACK, 5)
        arrow = Arrow(prompt_words.get_right(), middle.get_top(), buff=0.1, path_arc=-60 * DEG)

        self.play(LaggedStart(
            FadeIn(prompt_words, lag_ratio=0.1),
            Write(arrow),
            TransformFromCopy(big_circle, middle, run_time=2),
        ))
        self.wait()

        # No training data here
        no_training_words = Text("No training\ndata here", font_size=24)
        no_training_words.next_to(middle, RIGHT, SMALL_BUFF)
        no_training_words.set_z_index(1)
        no_training_words.set_backstroke(BLACK, 2)

        def get_training_data_examples(n_samples, min_scale=0.2):
            training_data = DotCloud(np.array([
                big_circle.pfp(random.random()) * random.uniform(min_scale, 1)
                for n in range(n_samples)
            ]))
            training_data.set_radius(0.04)
            training_data.make_3d()
            training_data.set_z_index(-1)
            return training_data

        training_data = get_training_data_examples(100)

        self.play(
            ShowCreation(training_data, run_time=3),
            Write(no_training_words, run_time=1),
        )
        self.wait()

        # Show other blobs
        blobs.set_fill(opacity=0.25)
        more_data = get_training_data_examples(1000)

        blob_words = VGroup(
            Text(word, font_size=24) for word in [
                "cats",
                "horses",
                "astronauts",
                "transformation",
                "on the\nmoon",
            ]
        )
        for word, blob in zip(blob_words, blobs):
            word.move_to(blob.get_center() * 1.5)
        blob_words.set_backstroke(BLACK, 2)

        self.play(
            ShowCreation(more_data, run_time=6),
            LaggedStartMap(Write, blobs),
            LaggedStartMap(FadeIn, blob_words),
            no_training_words.animate.scale(0.5).move_to(middle).set_backstroke(BLACK, 0).set_fill(BLACK),
            prompt_words.animate.set_backstroke(BLACK, 10),
        )
        self.wait()
