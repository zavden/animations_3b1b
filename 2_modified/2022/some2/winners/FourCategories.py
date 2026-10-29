# ==============================================================================
# Scene:      FourCategories
# Source:     videos/_2022/some2/winners.py (lines 675-1048)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FourCategories.py FourCategories -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DOC_DIR (Grant's output folder in the original) -> os.path.join(get_directories()["data"], "2022/some2/winners/"), with the placeholder data in _lib/data/2022/some2/winners/
#   - url_to_image(self, url) was called with a single argument in the url_to_image method (TypeError in the original): now url_to_image(self, url)
#   - self.tiles = VGroup() -> Group(): the tiles are Groups and VGroup.add now requires a VMobject
#
# Placeholder assets (not Grant's originals):
#   - featured_entries.csv + placeholder thumbnails in _lib/data/2022/some2/winners/; icons teaching.svg, gem.svg, memory.svg in svg_images/ (make_some2_assets.py)
# ==============================================================================

from manim_imports_ext import *
import pandas as pd

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DOC_DIR = os.path.join(get_directories()["data"], "2022/some2/winners/")


def get_entry_tile():
    rect = ScreenRectangle(height=1)
    rect.set_fill(GREY_D, 1)
    rect.set_stroke(WHITE, 1)
    rect.set_gloss(0)
    qmarks = Text("???")
    qmarks.move_to(rect)
    return Group(rect, qmarks)


def url_to_image(self, url):
    if url.startswith("https://youtu.be/"):
        name = url.split("/")[-1]  # Get slug
    else:
        name = [p for p in url.split("/") if p][-1].split(".")[0]

    return ImageMobject(os.path.join(DOC_DIR, f"thumbnails/{name}"))


class FourCategories(InteractiveScene):
    frame_scale_factor = 0.75

    def setup(self):
        super().setup()
        df = pd.read_csv(os.path.join(DOC_DIR, "featured_entries.csv"))
        self.titles = df['Title']
        self.authors = df['Author']
        self.urls = df['Link']

    def construct(self):
        # Four categories
        regions = VGroup(*(ScreenRectangle() for x in range(4)))
        regions.set_height(FRAME_HEIGHT / 2)
        regions.arrange_in_grid(2, 2, buff=0)
        regions.set_stroke(width=0)
        regions.set_fill(opacity=0.3)
        regions.set_submobject_colors_by_gradient(
            BLUE_D, BLUE_C, BLUE_E, GREY_BROWN,
        )

        titles = VGroup(*(
            Text(word, font_size=60)
            for word in ["Motivation", "Clarity", "Novelty", "Memorability"]
        ))
        for title, region in zip(titles, regions):
            title.next_to(region.get_top(), DOWN, buff=MED_SMALL_BUFF)

        self.play(
            LaggedStartMap(FadeIn, regions, lag_ratio=0.5),
            LaggedStartMap(Write, titles, lag_ratio=0.8),
            run_time=3
        )
        self.wait()

        # Lesson tiles
        tile = self.get_entry_tile().set_height(0.5)
        regions[0].tiles = tile.get_grid(2, 5)
        regions[1].tiles = tile.get_grid(2, 2)
        regions[2].tiles = tile.get_grid(1, 1)
        regions[3].tiles = tile.get_grid(1, 2)
        # CHANGE: the tiles are Groups (rectangle + Text) and VGroup.add now requires a VMobject; Group is used
        self.tiles = Group()
        for region in regions:
            region.tiles.move_to(region)
            self.tiles.add(*region.tiles)

        self.play(LaggedStart(*(
            FadeIn(tile, scale=0.8)
            for tile in self.tiles
        )), run_time=5, lag_ratio=0.1)
        self.wait()

        # Accentuate titles
        icons = VGroup(*(
            SVGMobject(file)
            for file in ["teaching", "gem", "lightbulb", "memory"]
        ))
        icons.set_stroke(WHITE, width=0)
        icons.set_fill(WHITE, opacity=1)
        icons.set_color_by_gradient(GREY_A, BLUE_B, YELLOW, GREY_B)
        icons[2].set_opacity(0.8)
        icons[1].set_opacity(0.7)
        for title, icon in zip(titles, icons):
            icon.set_height(1.5 * title[0].get_height())
            icon.next_to(title, RIGHT).match_y(title[0])
            title.icon = icon

            self.play(
                FadeIn(icon, lag_ratio=0.25),
                FlashUnder(title),
            )
            title.add(icon)
        self.wait()

        # Relative importance
        self.play(LaggedStart(
            regions[:2].animate.stretch(1.4, 1, about_edge=UP),
            regions[2:].animate.stretch(0.6, 1, about_edge=DOWN),
            titles[:2].animate.shift(MED_SMALL_BUFF * DOWN),
            titles[2:].animate.shift(2 * DOWN),
            regions[0].tiles.animate.shift(DOWN),
            regions[1].tiles.animate.shift(DOWN),
            regions[2].tiles.animate.shift(1.4 * DOWN),
            regions[3].tiles.animate.shift(1.4 * DOWN),
            lag_ratio=0.025,
            run_time=2
        ))
        self.wait()

        # Isolate Motivation
        regions[0].save_state()
        titles[0].save_state()

        self.add(regions[0], regions[0].tiles)
        self.play(
            regions[0].animate.replace(FullScreenRectangle()).set_opacity(0),
            titles[0].animate.set_x(0),
            regions[0].tiles.animate.scale(2).center(),
            FadeOut(regions[1:]),
            FadeOut(titles[1:]),
            *(FadeOut(regions[i].tiles) for i in range(1, 4)),
        )

        # Subregions
        subregions = Rectangle(height=7, width=FRAME_WIDTH / 2).get_grid(1, 2, buff=0)
        subregions.to_edge(DOWN, buff=0)
        subregions.set_stroke(WHITE, 1)
        subregions.set_fill(GREY_E, 1)
        subtitles = VGroup(Text("Macro"), Text("Micro"))
        subtitles.scale(1.2)
        for st, sr in zip(subtitles, subregions):
            st.next_to(sr.get_top(), DOWN)

        descriptions = VGroup(
            Text("Have you generated a\ndesire to learn?"),
            Text("Is each new idea given\na good reason to be there?"),
        )
        descriptions.scale(0.8)
        for desc, st in zip(descriptions, subtitles):
            desc.next_to(st, DOWN, MED_LARGE_BUFF)

        self.play(
            Write(subregions),
            titles[0].animate.to_edge(UP, buff=SMALL_BUFF),
            regions[0].tiles[:7].animate.scale(0.9).arrange_in_grid(3, 3).move_to(subregions[0]).align_to(ORIGIN, UP),
            regions[0].tiles[7:].animate.scale(0.9).arrange_in_grid(2, 2).move_to(subregions[1]).align_to(ORIGIN, UP),
            LaggedStartMap(FadeIn, subtitles, shift=0.5 * DOWN)
        )
        self.wait()
        self.play(Write(descriptions[0]))

        for i in range(7):
            self.highlight_tile(i)

        self.play(Write(descriptions[1]))
        for i in range(7, 10):
            self.highlight_tile(i)

        # Intersection with clarity
        frame = self.camera.frame
        titles[1].save_state()
        c_region = subregions[0].copy()
        c_region.set_fill(regions[1].get_fill_color(), 0.2)
        c_region.set_stroke(BLUE, 3)
        c_region.next_to(subregions, RIGHT, buff=0.1)
        titles[1].match_y(titles[0])
        titles[1].match_x(c_region)

        regions[1].tiles.scale(regions[0].tiles[0].get_height() / regions[1].tiles[0].get_height())
        regions[1].tiles.arrange_in_grid(buff=0.3)
        regions[1].tiles.move_to(c_region)
        regions[1].tiles.align_to(regions[0].tiles[0], UP)

        self.play(
            frame.animate.scale(1.55).move_to(subregions[1]),
            FadeIn(titles[1]),
            FadeIn(c_region),
            FadeIn(regions[1].tiles),
        )
        self.wait()
        c_region.save_state()
        self.play(
            c_region.animate.stretch(2, 0, about_edge=RIGHT)
        )
        self.wait()

        # Attention and focus
        randy = Randolph()
        randy.next_to(subregions[0], UP)
        bucket = VMobject().set_points_as_corners([UL, LEFT, RIGHT, UR])
        bucket.set_stroke(WHITE, 1.5)
        bucket.set_width(1.0).set_height(1.5, stretch=True)
        bucket.next_to(randy.get_corner(UL), UP, buff=0)

        bucket_label = Text("Attention and focus", color=YELLOW)
        bucket_label.next_to(bucket, RIGHT, buff=MED_LARGE_BUFF, aligned_edge=UP)
        bucket_arrow = Arrow(
            bucket_label.get_corner(DL) + 0.7 * RIGHT + 0.1 * DOWN,
            bucket.get_right(),
            color=YELLOW
        )

        focus_dots = Group(*(
            GlowDot([
                interpolate(bucket.get_x(LEFT) + 0.1, bucket.get_x(RIGHT) - 0.1, random.random()),
                interpolate(bucket.get_y(DOWN) + 0.1, bucket.get_y(TOP) - 0.1, random.random()),
                0,
            ])
            for x in range(40)
        ))
        focus_dots.sort(lambda p: p[1])

        self.play(
            frame.animate.move_to(subregions[1], DOWN).shift(MED_SMALL_BUFF * DOWN),
            VFadeIn(randy),
            randy.change("tease"),
            FadeIn(bucket),
        )
        self.play(
            FadeIn(bucket_label),
            ShowCreation(bucket_arrow),
            FadeIn(focus_dots, lag_ratio=0.5),
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()

        # Draining attention and focus
        randy_copy = randy.copy()
        randy_copy.generate_target()
        randy_copy.target.next_to(subregions.get_corner(UR), UR)
        randy_copy.target.change_mode("pondering").look(DOWN)

        bucket_copy = bucket.copy()
        bucket_copy.generate_target()
        bucket_copy.target.next_to(randy_copy.target.get_corner(UL), UP, buff=0)
        bucket_copy.set_opacity(0)

        focus_dots_copy = focus_dots.copy().set_opacity(0)

        self.play(
            MoveToTarget(randy_copy),
            MoveToTarget(bucket_copy),
            focus_dots_copy.animate.move_to(bucket_copy.target).set_opacity(1)
        )
        focus_dots_copy.sort(lambda p: -p[1])
        self.play(
            LaggedStartMap(FadeOut, focus_dots_copy, shift=0.2 * UP, scale=3, lag_ratio=0.4, run_time=6),
            randy_copy.change("erm", regions[1].tiles).set_anim_args(time_span=(4, 5))
        )
        self.wait()
        self.play(Blink(randy_copy))
        self.wait()

        # Transition to clarity
        self.play(
            titles[1].animate.center().to_edge(UP),
            regions[1].tiles.animate.scale(1.5).center(),
            c_region.animate.become(FullScreenRectangle(fill_color=BLACK, fill_opacity=0)),
            frame.animate.set_height(FRAME_HEIGHT).center(),
            *(
                FadeOut(mob, shift=LEFT, time_span=(0.05 * i, 0.05 * i + 1))
                for i, mob in enumerate([
                    randy, bucket, focus_dots, bucket_label,
                    randy_copy, bucket_copy,
                    titles[0], subregions,
                    subtitles, descriptions, *regions[0].tiles,
                ])
            ),
            run_time=2
        )

        for i in range(10, 14):
            self.highlight_tile(i)

        # Novelty
        regions[0].restore()
        regions[0].tiles.scale(0.7)
        regions[0].tiles.arrange_in_grid(4, 3)
        regions[0].tiles.move_to(regions[0]).shift(0.5 * DOWN)

        titles[0].restore()
        self.remove(titles[1])

        self.play(
            FadeIn(regions),
            *map(FadeIn, (titles[0], titles[2], titles[3])),
            *(FadeIn(regions[i].tiles) for i in [0, 2, 3]),
            regions[1].tiles.animate.scale(regions[0].tiles[0].get_height() / regions[1].tiles[0].get_height()).move_to(regions[1]),
            titles[1].animate.restore()
        )
        self.play(FlashAround(regions[2], buff=-0.01, run_time=3, time_width=2))

        # Isolate novelty
        self.og_mobjects = Group(*self.mobjects)
        self.og_mobjects.save_state()
        self.play(
            regions[2].animate.replace(FullScreenRectangle(), stretch=True).set_opacity(0),
            titles[2].animate.center().to_edge(UP),
            *map(FadeOut, [*titles[:2], titles[3], *regions[:2], regions[3], *self.tiles])
        )

        # Components of novelty
        rects = Rectangle().get_grid(1, 2, buff=0)
        rects.set_height(1.5)
        rects.set_width(12, stretch=True)
        rects.next_to(titles[2], DOWN, buff=2.0)
        rects.set_stroke(WHITE, 1)
        rects[0].set_fill(BLUE_E, 1)
        rects[1].set_fill(GREY_BROWN, 1)
        subtitles = VGroup(
            Text("Stylistic\noriginality"),
            Text("Content\noriginality"),
        )
        for st, rect in zip(subtitles, rects):
            st.rect = rect
            st.start_width = st.get_width()
            st.add_updater(lambda m: m.set_max_width(min(m.start_width, 0.8 * m.rect.get_width())))
            st.add_updater(lambda m: m.move_to(m.rect))

        lines = VGroup(*(Line(titles[2].get_bottom(), st.get_top(), buff=0.25) for st in subtitles))
        lines.set_stroke(WHITE, 2)

        subtitles.suspend_updating()
        self.play(
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.5),
            LaggedStartMap(FadeInFromPoint, subtitles, point=titles[2].get_bottom(), lag_ratio=0.5),
        )
        subtitles.resume_updating()
        self.wait()
        self.add(*rects, *subtitles)
        self.play(*map(FadeIn, rects), FadeOut(lines))
        self.play(
            rects[0].animate.set_width(rects[0].get_width() - 5, stretch=True, about_edge=LEFT),
            rects[1].animate.set_width(rects[1].get_width() + 5, stretch=True, about_edge=RIGHT),
        )
        self.wait()

        self.og_mobjects.restore()
        self.clear()
        self.add(*self.og_mobjects)

        # Last couple
        for i in range(14, 17):
            self.highlight_tile(i)

    def get_entry_tile(self):
        return get_entry_tile()

    def highlight_tile(self, index):
        bg = FullScreenFadeRectangle(fill_color=GREY_E, fill_opacity=1)
        tile = self.tiles[index]
        title = Text(self.titles[index], font_size=60)
        author = Text("by " + self.authors[index], font_size=48, color=GREY_A)
        image = self.url_to_image(self.urls[index])

        image.set_width(0.97 * tile.get_width())
        image.move_to(tile)
        image.set_opacity(0.0)

        original_tile = tile.copy()
        tile.generate_target()
        tile.target[1].set_opacity(0)
        tile.target[0].set_fill(BLACK, 1)
        tile.target.set_height(self.frame_scale_factor * FRAME_HEIGHT)
        tile.target.center().to_edge(DOWN, buff=MED_SMALL_BUFF)

        title.set_max_width(FRAME_WIDTH - 1)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        author.move_to(midpoint(title.get_bottom(), tile.target.get_top()))

        bg.save_state()
        bg.replace(tile)
        bg.set_opacity(0)

        self.add(bg, tile, image, title)
        self.play(
            bg.animate.restore(),
            MoveToTarget(tile),
            image.animate.replace(tile.target).set_opacity(1.0),
            Write(title, time_span=(0.5, 2.0)),
        )
        # self.play()
        self.play(FadeIn(author, 0.5 * DOWN))
        self.wait()

        tile.replace_submobject(1, image)
        self.play(
            tile.animate.replace(original_tile),
            *map(FadeOut, (bg, title, author)),
        )

    def url_to_image(self, url):
        # CHANGE: the module's url_to_image function receives (self, url); the original called it with just url (TypeError)
        return url_to_image(self, url)
