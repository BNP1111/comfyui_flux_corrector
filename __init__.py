# __init__.py for comfyui_flux_corrector
# Exposes FLUXCorrector node to ComfyUI

from .flux_corrector_node import FLUXCorrector

NODE_CLASS_MAPPINGS = {
    "FLUXCorrector": FLUXCorrector,
}
