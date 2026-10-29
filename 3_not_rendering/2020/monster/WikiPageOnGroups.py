# ==============================================================================
# Scene:      WikiPageOnGroups
# Source:     videos/_2020/monster.py (lines 2377-2378)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl WikiPageOnGroups.py WikiPageOnGroups -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class WikiPageOnGroups(ExternallyAnimatedScene): pass`, Grant's marker for a clip animated outside manim (screen capture or recording). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo.
# ==============================================================================

from manim_imports_ext import *

class WikiPageOnGroups(ExternallyAnimatedScene):
    pass
