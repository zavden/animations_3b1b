# ==============================================================================
# Scene:      Lean
# Source:     videos/_2026/2025_p6/problem_intro.py (lines 396-483)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Lean.py Lean -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

# Mathlib's formalization of IMO 2024 Q3, whose module docstring states the problem in
# English, and whose source both states it in Lean and proves it
LEAN_FILE = Path(__file__).parent / "Imo2024Q3.lean"


# Consolas, which Code reaches for by default, has none of ℕ ↦ ∀ ∈ ⟨ ⟩; Menlo carries every
# glyph this file uses but ⊔ and ⋃, so the source stays in one font at one width
LEAN_FONT = "Menlo"


def lean_slice(source, start, end=None):
    """
    The stretch of a Lean source from where one snippet of it appears up to where another
    does, or to the end of it where no end is named.
    """
    index = source.index(start)
    return source[index:source.index(end, index) if end else len(source)].strip("\n")


def lean_code(code, **kwargs):
    """
    Lean source, highlighted as the Lean 4 it is: pygments answers to the name "lean" with
    its Lean 3 lexer, which leaves this file's declarations unhighlighted.
    """
    return Code(code, language="lean4", font=LEAN_FONT, alignment="LEFT", **kwargs)


def source_blocks(code):
    """Each paragraph of a source, as the line it begins on and the lines themselves"""
    blocks = []
    lines = []
    for number, line in enumerate(code.split("\n")):
        if line.strip():
            lines.append(line)
        elif lines:
            blocks.append((number - len(lines), "\n".join(lines)))
            lines = []
    if lines:
        blocks.append((number + 1 - len(lines), "\n".join(lines)))
    return blocks


class SourceColumn(VGroup):
    """
    Every glyph of a source, which moves as one whether or not all of it is showing.

    An animation which reveals a group a piece at a time takes whatever it has not reached
    yet out of the group as it goes, see ShowIncreasingSubsets. A group scrolled while that
    runs would move only what is showing and leave the rest where it stood: each glyph would
    start moving as it appeared, and every line would break wherever the reveal had got to,
    its tail a line below its head. So a shift here moves every glyph, showing or not.
    """

    def __init__(self, *glyphs):
        super().__init__(*glyphs)
        self.glyphs = list(glyphs)

    def shift(self, vector):
        for glyph in self.glyphs:
            glyph.shift(vector)
        return self


def lean_column(code, font_size=36):
    """
    Lean source as a column of blocks, a paragraph of it to each, rather than as one mobject
    holding the lot. Text is laid out on a canvas of fixed size, which a thousand lines at a
    readable font size overrun: what does not fit is dropped, and what is left comes back
    folded into the room there was, which reads as a source full of stray line breaks.

    Each block is put where its own line numbers say, so the blank lines between paragraphs
    and the indentation within them come out as the file has them. What fixes where a block
    begins is a bar given a line of its own in front of it, and taken away once it has: the
    box around a block's glyphs reaches as far as its tallest, which differs from paragraph
    to paragraph, so stacking those boxes would leave each one a little out.

    Comes back flat, a glyph to a submobject, as a single Code mobject would, so that
    showing it a piece at a time shows it a glyph at a time.
    """
    glyph = lean_code("x", font_size=font_size)
    line_height = lean_code("x\nx", font_size=font_size).get_height() - glyph.get_height()
    column = VGroup()
    for number, block in source_blocks(code):
        mob = lean_code("|\n" + block, font_size=font_size)
        anchor = mob[0]
        mob.shift((number - 1) * line_height * DOWN - anchor.get_corner(DL))
        mob.remove(anchor)
        column.add(mob)
    return SourceColumn(*column.family_members_with_points())


class Lean(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        source = LEAN_FILE.read_text()
        english = self.get_english_statement(source)
        statement = self.get_lean_statement(source)
        proof = self.get_lean_proof(source)

        titles = VGroup(
            Text("Problem\n(English)"),
            Text("Problem\n(Lean)").set_color(TEAL),
            Text("Proof\n(Lean)").set_color(TEAL),
        )
        pieces = VGroup(english, statement, proof)
        for title, piece, x in zip(titles, pieces, [-1, 0, 1]):
            title.set_x(x * FRAME_WIDTH / 3)
            title.to_edge(UP, buff=MED_LARGE_BUFF)
            piece.set_width(4)
            piece.next_to(title, DOWN, LARGE_BUFF)

        arrow = Arrow(titles[0], titles[1], thickness=6, buff=0.3)
        arrow.set_fill((WHITE, TEAL), gradient_direction=RIGHT)

        # Show initial translation
        frame.reorient(0, 0, 0, (-2.30, 1.76, 0.00), 5.71)
        self.add(titles[0], pieces[0])
        self.play(LaggedStart(
            GrowArrow(arrow),
            TransformMatchingStrings(
                titles[0].copy(), titles[1],
                key_map={"English": "Lean"},
                run_time=1
            ),
            TransformFromCopy(english, statement, lag_ratio=1e-4),
            run_time=2,
            lag_ratio=0.25
        ))
        self.wait(2)

        # Show proof
        arrow2 = Arrow(titles[1], titles[2], thickness=6, buff=0.3)
        arrow2.set_fill(TEAL)

        back_rect = VGroup(
            Rectangle(proof.get_width() + 0.5, 1.5).set_fill(BLACK, 1),
            Rectangle(proof.get_width() + 0.5, 1.5).set_fill(BLACK, opacity=(0, 1), gradient_direction=UP),
        )
        back_rect.arrange(DOWN, buff=0)
        back_rect.move_to(proof).to_edge(UP, buff=0)
        back_rect.set_stroke(width=0)

        proof.set_z_index(-1)
        proof.add_updater(lambda m, dt: m.shift(2 * dt * UP))

        self.add(back_rect)
        self.play(
            GrowArrow(arrow2),
            TransformMatchingStrings(titles[1].copy(), titles[2], run_time=1),
            ShowIncreasingSubsets(proof, run_time=10, rate_func=linear),
            frame.animate.to_default_state(),
        )
        self.wait()

    def get_english_statement(self, source):
        statement = lean_slice(source, "Let $a_1", "We follow Solution 1")
        pre_result = VGroup(*(
            TexText(" ".join(paragraph.split()), alignment="", font_size=36)
            for paragraph in statement.split("\n\n")
        ))
        pre_result.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        return VGroup(*pre_result.family_members_with_points())

    def get_lean_statement(self, source):
        definitions = lean_slice(source, "/-- The condition of the problem.", "/-! ###")
        claim, _ = self.get_theorem(source)
        return lean_code("\n\n".join([definitions, claim]))

    def get_lean_proof(self, source):
        development = lean_slice(source, "/-! ### Definitions", "theorem result")
        _, tactics = self.get_theorem(source)
        return lean_column("\n\n".join([development, tactics]))

    def get_theorem(self, source):
        """The final theorem, as what it claims and how it is proved"""
        theorem = lean_slice(source, "theorem result", "end Imo2024Q3")
        claim, _, tactics = theorem.partition(":= by")
        return claim.strip() + " := by", tactics.strip("\n")
