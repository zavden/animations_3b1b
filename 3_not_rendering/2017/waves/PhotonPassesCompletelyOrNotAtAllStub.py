# ==============================================================================
# Scene:      PhotonPassesCompletelyOrNotAtAllStub
# Source:     videos/_2017/waves.py (lines 3134-3135)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl PhotonPassesCompletelyOrNotAtAllStub.py PhotonPassesCompletelyOrNotAtAllStub -w -m --fps 15
#
# Why it does not render:
#   Placeholder for an external video inherited from ExternallyAnimatedScene: the class body is only `pass` and its construct raises "Don't actually run this class." on purpose. Grant animated it outside manim (the external clip is not in the repo), so there is nothing to render without inventing its content.
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class PhotonPassesCompletelyOrNotAtAllStub(ExternallyAnimatedScene):
    pass
