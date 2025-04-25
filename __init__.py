"""Package init for comfyui_flux_corrector.

It tries to import FLUXCorrector whether the node file lives
inside this folder (./flux_corrector_node.py) **or**
directly under the parent custom_nodes directory
(../flux_corrector_node.py).

Place flux_corrector_node.py in either location.
"""

import importlib
import importlib.util
import pathlib
import sys

FLUXCorrector = None

# 1) Try normal relative import (preferred layout)
try:
    from .flux_corrector_node import FLUXCorrector  # type: ignore
except ModuleNotFoundError:
    # 2) Fallback: look in parent custom_nodes directory
    pkg_dir = pathlib.Path(__file__).resolve().parent
    parent_candidate = pkg_dir.parent / "flux_corrector_node.py"
    if parent_candidate.exists():
        spec = importlib.util.spec_from_file_location(
            "flux_corrector_node_fallback", parent_candidate)
        mod  = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules[spec.name] = mod  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        FLUXCorrector = mod.FLUXCorrector  # type: ignore
    else:
        # Reraise original error for visibility
        raise

NODE_CLASS_MAPPINGS = {"FLUXCorrector": FLUXCorrector}
