# ==============================================================================
# Scene:      Questions
# Source:     videos/_2019/QA_2to21.py (lines 6-63)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Questions.py Questions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TexText.CONFIG.update(alignment="") no longer exists: alignment="" is passed to each OldTexText with a local function
# ==============================================================================

from manim_imports_ext import *

# For Q&A Video
class Questions(Scene):
    def construct(self):
        # CHANGE: TexText.CONFIG.update(...) no longer exists in GL; the default alignment "" is passed in each call with this function
        def text_no_align(*args, **kwargs):
            kwargs.setdefault("alignment", "")
            return OldTexText(*args, **kwargs)

        questions = VGroup(
            text_no_align(
                "Who is your favorite mathematician?"
            ),
            text_no_align(
                "A teenage kid walks up to you and says they\\\\",
                "hate maths. What do you tell/show them?"
            ),
            text_no_align(
                "What advice would you want to give to give a\\\\",
                "math enthusiast suffering from an anxiety\\\\",
                "disorder, clinical depression and ADHD?",
            ),
            text_no_align(
                "Is Ben, Ben and Blue still a thing?"
            ),
            text_no_align(
                "Favorite podcasts?"
            ),
            text_no_align(
                "Hey Grant, if you had, both, the responsibility and\\\\",
                "opportunity to best introduce the world of mathematics\\\\",
                "to curious and intelligent minds before they are shaped\\\\",
                "by the antiquated, disempowering and demotivational\\\\",
                "education system of today, what would you do?  (Asking\\\\",
                "because I will soon be a father).\\\\",
            ),
            text_no_align(
                "What's something you think could've\\\\",
                "been discovered long before it was\\\\",
                "actually discovered?",
            ),
            text_no_align(
                "Can we fix math on Wikipedia? Really serious\\\\",
                "here. I constantly go there after your vids for\\\\",
                "a bit of deeper dive and learn - nothing more, ever.\\\\",
                "Compared to almost any topic in the natural sciences\\\\",
                "or physics where at least I get an outline of where\\\\",
                "to go next. It's such a shame."
            ),
        )

        last_question = VMobject()
        for question in questions:
            question.set_width(FRAME_WIDTH - 1)
            self.play(
                FadeInFromDown(question),
                FadeOut(last_question, UP)
            )
            last_question = question
            self.wait(2)
