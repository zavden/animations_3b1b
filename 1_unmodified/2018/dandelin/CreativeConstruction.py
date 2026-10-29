# ==============================================================================
# Scene:      CreativeConstruction
# Source:     videos/_2018/dandelin.py (lines 1356-1454)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CreativeConstruction.py CreativeConstruction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CreativeConstruction(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        self.remove(randy)

        dandelin = ImageMobject("GerminalDandelin")
        dandelin.set_height(4)
        dandelin.move_to(FRAME_WIDTH * RIGHT / 4)

        lightbulb = Lightbulb()
        lightbulb.next_to(dandelin, UP)

        kant = ImageMobject("Kant")
        kant.set_height(3)
        bubble = ThoughtBubble(height=3, width=4)
        bubble.pin_to(kant)
        kant_words = OldTexText(
            "How is synthetic a priori\\\\" +
            "reasoning possible?"
        )
        kant_words.scale(0.75)
        bubble.position_mobject_inside(kant_words)
        kant_group = VGroup(bubble, kant_words, kant)
        kant_group.to_corner(UR)

        self.add(dandelin)
        self.add(lightbulb)
        self.play(
            Write(lightbulb, run_time=1),
            self.get_light_shine(lightbulb)
        )
        self.wait()
        self.play(
            lightbulb.next_to, randy, RIGHT,
            {"buff": LARGE_BUFF, "aligned_edge": UP},
            randy.change, "pondering",
            VFadeIn(randy),
            FadeOut(dandelin, DOWN),
        )

        self.play(
            self.get_light_shine(lightbulb),
            Blink(randy),
        )
        self.wait()
        self.play(
            FadeInFromDown(kant),
            Write(bubble),
            Write(kant_words),
        )

        lightbulb.generate_target()
        q_marks = VGroup()
        for submob in lightbulb.target.family_members_with_points():
            if True or get_norm(submob.get_center() - lightbulb.get_center()) > 0.25:
                q_mark = OldTex("?")
                q_mark.set_height(0.25)
                q_mark.move_to(submob)
                Transform(submob, q_mark).update(1)
                q_marks.add(submob)
        q_marks.space_out_submobjects(2)

        self.wait()
        self.play(randy.change, 'confused', lightbulb)
        self.play(MoveToTarget(
            lightbulb,
            run_time=3,
            rate_func=there_and_back,
            lag_ratio=0.5
        ))
        self.play(Blink(randy))
        self.wait()

    def get_rings(self, center, max_radius, delta_r):
        radii = np.arange(0, max_radius, delta_r)
        rings = VGroup(*[
            Annulus(
                inner_radius=r1,
                outer_radius=r2,
                fill_opacity=0.75 * (1 - fdiv(r1, max_radius)),
                fill_color=YELLOW
            )
            for r1, r2 in zip(radii, radii[1:])
        ])
        rings.move_to(center)
        return rings

    def get_light_shine(self, lightbulb, max_radius=15.0, delta_r=0.025):
        rings = self.get_rings(
            lightbulb.get_center(),
            max_radius=15.0,
            delta_r=0.025,
        )
        return LaggedStartMap(
            FadeIn, rings,
            rate_func=there_and_back,
            run_time=2,
            lag_ratio=0.5
        )
