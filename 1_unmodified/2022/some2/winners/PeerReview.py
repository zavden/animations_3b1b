# ==============================================================================
# Scene:      PeerReview
# Source:     videos/_2022/some2/winners.py (lines 180-288)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PeerReview.py PeerReview -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PeerReview(InteractiveScene):
    def construct(self):
        # Add everyone
        n_peers = 10
        peers = VGroup(*(
            PiCreature(color=random.choice([BLUE_E, BLUE_D, BLUE_C, BLUE_B]))
            for x in range(n_peers)
        ))
        peers.arrange(RIGHT)
        peers.set_width(FRAME_WIDTH - 1)
        peers.to_edge(DOWN)
        copies = VGroup(peers.copy().set_y(0), peers.copy().to_edge(UP, LARGE_BUFF))
        all_pis = VGroup(*peers, *it.chain(*copies))

        videos = VGroup(*(VideoIcon() for peer in all_pis))
        for video, pi in zip(videos, all_pis):
            video.set_height(0.25)
            video.set_color(random_bright_color())
            video.next_to(pi.get_corner(UR), UP, SMALL_BUFF)

        self.add(peers)
        pairs = list(zip(videos, all_pis))
        random.shuffle(pairs)
        self.play(LaggedStart(*(
            AnimationGroup(
                pi.change("raise_right_hand"),
                FadeIn(video, 0.5 * UP)
            )
            for video, pi in pairs
        )))

        # Entry box
        entry_box = Rectangle(4, 4)
        entry_box.set_fill(GREY_E, 1)
        entry_box.set_stroke(WHITE, 1)
        entry_box.to_edge(UP, buff=0.5)
        entry_box_label = Text("All entries")
        entry_box_label.next_to(entry_box.get_top(), DOWN, SMALL_BUFF)
        entry_box_label.set_backstroke(BLACK, 5)
        videos.generate_target()
        videos.target.arrange_in_grid(buff=0.25)
        videos.target.move_to(entry_box)

        self.add(entry_box, videos, entry_box_label)
        self.play(
            FadeIn(entry_box),
            FadeIn(entry_box_label),
            FadeOut(copies, lag_ratio=0.1),
            MoveToTarget(videos),
            LaggedStart(*(peer.change("tease", ORIGIN) for peer in peers))
        )

        # Peer review process
        peers.shuffle()
        for pi in peers:
            pi.watchlist = list(videos.copy())
            random.shuffle(pi.watchlist)

        self.play(LaggedStart(*(
            AnimationGroup(
                pi.watchlist[0].animate.next_to(pi.get_top(), UL, buff=0.1).shift(0.025 * RIGHT),
                pi.watchlist[1].animate.next_to(pi.get_top(), UR, buff=0.1).shift(0.025 * LEFT),
                pi.change("pondering", pi.get_top() + UP),
            )
            for pi in peers
        ), lag_ratio=0.1))

        for x in range(10):
            self.play(LaggedStart(*(
                AnimationGroup(
                    pi.change(
                        ["raise_right_hand", "raise_left_hand"][1 - bit],
                        pi.watchlist[x + bit],
                    ).set_anim_args(run_time=0.5),
                    pi.watchlist[x + bit].animate.scale(1.2),
                    pi.watchlist[x + 1 - bit].animate.scale(0.8),
                )
                for pi in peers
                for bit in [random.randint(0, 1)]
            ), lag_ratio=0.1))
            self.play(LaggedStart(*(
                AnimationGroup(
                    pi.change("sassy", pi.get_top() + UP).set_anim_args(run_time=0.5),
                    FadeOut(pi.watchlist[x], scale=0.5),
                    pi.watchlist[x + 1].animate.set_height(0.25).next_to(pi.get_top(), UL, buff=0.1).shift(0.025 * RIGHT),
                    pi.watchlist[x + 2].animate.next_to(pi.get_top(), UR, buff=0.1).shift(0.025 * LEFT),
                )
                for pi in peers
            )))

    def get_judgement_animation(self, pi, videos):
        vids = list(videos.copy())
        random.shuffle(vids)

        anims = [Animation(Mobject(), run_time=3 * random.random())]
        anims.append(AnimationGroup(
            vids[0].animate.next_to(pi.get_top(), UL, buff=0.1),
            vids[1].animate.next_to(pi.get_top(), UR, buff=0.1),
            pi.change("pondering", pi.get_top() + UP),
        ))
        for i in range(8):
            anims.append(pi.animate.change(random.choice(["raise_right_hand", "raise_left_hand"])))
            anims.append(AnimationGroup(
                FadeOut(vids[i], LEFT),
                vids[i + 1].animate.next_to(pi.get_top(), UL, buff=0.1),
                videos[i + 2].animate.next_to(pi.get_top(), UR, buff=0.1),
            ))

        return Succession(*anims)
