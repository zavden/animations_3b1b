# ==============================================================================
# Scene:      PreviewThreeVideos
# Source:     videos/_2020/beta/beta1.py (lines 451-596)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PreviewThreeVideos.py PreviewThreeVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the thumbnails are the PNGs that Thumbnail1..3 of this same source render (folder renders/2020/beta/beta1); consts.VIDEO_DIR/OUTPUT_DIRECTORY is replaced with that path relative to the file
# ==============================================================================

from manim_imports_ext import *

OUTPUT_DIRECTORY = "bayes/beta1"


class PreviewThreeVideos(Scene):
    def construct(self):
        # Write equations
        equations = VGroup(
            OldTex("{10", "\\over", "10}", "=", "100\\%"),
            OldTex("{48", "\\over", "50}", "=", "96\\%"),
            OldTex("{186", "\\over", "200}", "=", "93\\%"),
        )
        equations.arrange(RIGHT, buff=3)
        equations.to_edge(UP)

        colors = [PINK, BLUE, YELLOW]
        for eq, color in zip(equations, colors):
            eq[-1].set_color(color)
            fix_percent(eq[-1][-1])

        vs_labels = VGroup(*[TexText("vs.") for x in range(2)])
        for eq1, eq2, vs in zip(equations, equations[1:], vs_labels):
            vs.move_to(midpoint(eq1.get_right(), eq2.get_left()))

        self.add(equations)
        self.add(vs_labels)

        # Show topics
        title = OldTexText("To be explained:")
        title.set_height(0.7)
        title.next_to(equations, DOWN, LARGE_BUFF)
        title.to_edge(LEFT)
        title.add(Underline(title))

        topics = VGroup(
            OldTexText("Binomial distributions"),
            OldTexText("Bayesian updating"),
            OldTexText("Probability density functions"),
            OldTexText("Beta distribution"),
        )
        topics.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        topics.next_to(title, DOWN, MED_LARGE_BUFF)
        topics.to_edge(LEFT, buff=LARGE_BUFF)

        bullets = VGroup()
        for topic in topics:
            bullet = Dot()
            bullet.next_to(topic, LEFT)
            bullets.add(bullet)

        self.play(
            Write(title),
            Write(bullets),
            run_time=1,
        )
        self.play(LaggedStart(*[
            FadeIn(topic, lag_ratio=0.1)
            for topic in topics
        ], run_time=3, lag_ratio=0.3))
        self.wait()

        # Show videos
        images = [
            # CHANGE: the thumbnails are the PNGs that Thumbnail1..3 of this same source render (folder renders/2020/beta/beta1); consts.VIDEO_DIR/OUTPUT_DIRECTORY is replaced by that path relative to the file
            ImageMobject(os.path.join(
                Path(__file__).resolve().parents[4], "renders/2020/beta/beta1", name + ".png"
            ))
            for name in ["Thumbnail1", "Thumbnail2", "Thumbnail3"]
        ]
        thumbnails = Group()
        for image in images:
            image.set_width(FRAME_WIDTH / 3 - 1)
            rect = SurroundingRectangle(image, buff=0)
            rect.set_stroke(WHITE, 3)
            rect.set_fill(BLACK, 1)
            thumbnails.add(Group(rect, image))

        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)

        for topic, i in zip(topics, [0, 1, 1, 2]):
            thumbnail = thumbnails[i]
            topic.generate_target()
            topic.target.scale(0.6)
            topic.target.next_to(thumbnail, DOWN, aligned_edge=LEFT)
        topics[2].target.next_to(
            topics[1].target, DOWN,
            aligned_edge=LEFT,
        )

        self.play(
            FadeOut(title, LEFT),
            FadeOut(bullets, LEFT),
            LaggedStartMap(MoveToTarget, topics),
            LaggedStartMap(FadeIn, thumbnails),
        )
        self.wait()

        tn_groups = Group(
            Group(thumbnails[0], topics[0]),
            Group(thumbnails[1], topics[1], topics[2]),
            Group(thumbnails[2], topics[3]),
        )

        setup_words = OldTexText("Set up the model")
        analysis_words = OldTexText("Analysis")
        for words in [setup_words, analysis_words]:
            words.scale(topics[0][0].get_height() / words[0][0].get_height())
            words.set_color(YELLOW)
        setup_words.move_to(topics[0], UL)
        analysis_words.next_to(topics[3], DOWN, aligned_edge=LEFT)

        def set_opacity(mob, alpha):
            for sm in mob.family_members_with_points():
                sm.set_opacity(alpha)
            return mob

        self.play(ApplyFunction(lambda m: set_opacity(m, 0.2), tn_groups[1:]))
        self.play(
            FadeIn(setup_words, lag_ratio=0.1),
            topics[0].next_to, setup_words, DOWN, {"aligned_edge": LEFT},
        )
        tn_groups[0].add(setup_words)
        self.wait(2)
        for i in 0, 1:
            self.play(
                ApplyFunction(lambda m: set_opacity(m, 0.2), tn_groups[i]),
                ApplyFunction(lambda m: set_opacity(m, 1), tn_groups[i + 1]),
            )
            self.wait(2)
        self.play(FadeIn(analysis_words, 0.25 * UP))
        tn_groups[2].add(analysis_words)
        self.wait(2)

        self.play(
            FadeOut(setup_words),
            FadeOut(topics[0]),
            FadeOut(tn_groups[1]),
            FadeOut(tn_groups[2]),
            FadeOut(vs_labels, UP),
            FadeOut(equations, UP),
            ApplyFunction(lambda m: set_opacity(m, 1), thumbnails[0]),
        )
        thumbnails[0].generate_target()
        # thumbnails[0].target.set_width(FRAME_WIDTH)
        # thumbnails[0].target.center()
        thumbnails[0].target.to_edge(UP)
        self.play(MoveToTarget(thumbnails[0], run_time=4))
        self.wait()
