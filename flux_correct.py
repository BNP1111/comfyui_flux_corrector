# ComfyUI custom node: FLUX Corrector
# save as ComfyUI/custom_nodes/flux_corrector_node.py
import comfy.samplers as samplers

class FLUXCorrector:
    """
    Second-stage UNet corrector for FLUX.
    Feed it the latent from stage-1, the same conditioning,
    and the FLUX-Corrector UNet model.
    """
    CATEGORY      = "Flux"
    RETURN_TYPES  = ("LATENT",)
    RETURN_NAMES  = ("latent",)
    FUNCTION      = "run"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent_in"      : ("LATENT",),
                "positive"       : ("CONDITIONING",),
                "negative"       : ("CONDITIONING",),
                "corrector_model": ("MODEL",),
                "steps"          : ("INT",   {"default": 10, "min": 1,  "max": 50}),
                "denoise_end"    : ("FLOAT", {"default": 0.25, "min": 0, "max": 1, "step": 0.01}),
                "cfg"            : ("FLOAT", {"default": 7.0,  "min": 1,  "max": 15,"step": 0.1}),
                "sampler_name"   : (samplers.KSampler.SAMPLER_NAMES,)
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
