# ==============================================================================
# Scene:      Triumverate
# Source:     videos/_2022/some2/announcement.py (lines 126-195)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Triumverate.py Triumverate -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The logo in _lib/custom/logo.py passes sheen=0.0 to Circle (an argument manimgl no longer has): add_pupil is redefined without sheen in a local subclass
# ==============================================================================

from manim_imports_ext import *


# CHANGE: Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument; add_pupil is redefined without sheen
class Logo(Logo):
    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            stroke_color=BLACK,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)


class Triumverate(PiCreatureScene):
    def construct(self):
        # Introduce team
        morty, prof, artist = self.pi_creatures
        self.clear()
        self.add(morty)

        prof_label = Text("Domain expert", font_size=36).next_to(prof, DOWN)
        artist_label = Text("Artist/animator", font_size=36).next_to(artist, DOWN)
        morty_label = Text("Animations/Writing\n(Whatever is most helpful)", font_size=36)
        morty_label.next_to(morty, UP)

        self.play(
            FadeIn(prof_label, RIGHT),
            FadeIn(prof, RIGHT),
            morty.change("tease", prof.eyes)
        )
        self.play(prof.change("pondering"))
        self.wait(2)

        self.play(
            FadeIn(artist, RIGHT),
            FadeIn(artist_label, RIGHT),
            morty.change("tease", artist.eyes),
        )
        self.play(
            artist.change("hooray", morty.eyes),
            prof.change("thinking", artist.eyes),
        )
        self.wait(2)
        self.play(FadeIn(morty_label, UP))

        # Show video
        logo = Logo()
        logo.set_height(1.5)
        logo.move_to(UP)
        video = VideoIcon()
        video.set_color(RED_E)
        video.match_width(logo)
        video.next_to(logo, DOWN, LARGE_BUFF)

        self.play(
            Write(logo.iris_background, stroke_width=1),
            GrowFromCenter(logo.spike_layers, lag_ratio=0.1, run_time=2),
            Animation(logo.pupil),
            morty.change("thinking", logo),
            prof.change("pondering", logo),
            artist.change("tease", logo)
        )
        self.play(FadeIn(video, DOWN))

        # Footnote
        footnote = Text("""
            *Needless to say, such a collaboration would not be
            considered for winning SoME2, but I'd be happy to
            compensate collaborators here for their time.
        """, font_size=24, alignment="LEFT")
        footnote.to_corner(DR)
        self.play(FadeIn(footnote))
        self.wait(2)

    def create_pi_creatures(self):
        kw = dict(height=2.0)
        morty = Mortimer(**kw)
        prof = PiCreature(color=GREY_D, **kw)
        artist = PiCreature(color=TEAL, **kw)
        morty.to_edge(RIGHT, buff=1.5)
        VGroup(prof, artist).arrange(DOWN, buff=1.5).to_edge(LEFT, buff=1.5)

        return VGroup(morty, prof, artist)
