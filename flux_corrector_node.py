"""FLUX Corrector custom node for ComfyUI (compatible with 0.3.28+).

Drop this file into either:
  - ComfyUI/custom_nodes/flux_corrector_node.py
    (and keep __init__.py minimal importing below), or
  - ComfyUI/custom_nodes/comfyui_flux_corrector/flux_corrector_node.py

It auto‑detects the correct sampler list attribute for
both old (SAMPLER_NAMES) and new (SAMPLERS) ComfyUI versions.
"""

import comfy.samplers as samplers

class FLUXCorrector:
    """Second‑stage UNet corrector for FLUX – do low‑noise refinement."""

    CATEGORY      = "Flux"
    RETURN_TYPES  = ("LATENT",)
    RETURN_NAMES  = ("latent",)
    FUNCTION      = "run"

    @classmethod
    def INPUT_TYPES(cls):
        # ComfyUI ≥0.3.29 renamed SAMPLER_NAMES → SAMPLERS
        if hasattr(samplers.KSampler, "SAMPLER_NAMES"):
            sampler_choices = samplers.KSampler.SAMPLER_NAMES
        else:
            sampler_choices = samplers.KSampler.SAMPLERS

        return {
            "required": {
                "latent_in"      : ("LATENT",),
                "positive"       : ("CONDITIONING",),
                "negative"       : ("CONDITIONING",),
                "corrector_model": ("MODEL",),
                "steps"          : ("INT",   {"default": 10, "min": 1,  "max": 50}),
                "denoise_end"    : ("FLOAT", {"default": 0.25, "min": 0, "max": 1, "step": 0.01}),
                "cfg"            : ("FLOAT", {"default": 7.0,  "min": 1,  "max": 15,"step": 0.1}),
                "sampler_name"   : (sampler_choices,)
            }
        }

    def run(self, latent_in, positive, negative,
            corrector_model, steps, denoise_end, cfg, sampler_name):

        sampler = samplers.create_sampler(sampler_name, corrector_model)
        latent_out = sampler.sample(
            steps        = steps,
            latent_image = latent_in,
            cfg          = cfg,
            positive     = positive,
            negative     = negative,
            start_step   = 0,
            end_step     = int(steps * denoise_end)
        )
        return (latent_out,)

NODE_CLASS_MAPPINGS = {"FLUXCorrector": FLUXCorrector}

# Optional pretty display name to allow searching with space
NODE_DISPLAY_NAME_MAPPINGS = {"FLUXCorrector": "FLUX Corrector"}
