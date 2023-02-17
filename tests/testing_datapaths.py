import bilby
from bilby.gw.result import CompactBinaryCoalescenceResult
from bilby.gw.conversion import generate_all_bbh_parameters
import pandas as pd
import os

END_LABEL = "_NRSur7dq4_merged_result"


def generate_fake_result(n=100, outdir="outdir", event_name="test"):
    bilby.utils.command_line_args.bilby_test_mode = False
    priors = bilby.gw.prior.BBHPriorDict()
    priors["geocent_time"] = 2
    posterior = pd.DataFrame(priors.sample(n))
    posterior =  generate_all_bbh_parameters(posterior)

    result = CompactBinaryCoalescenceResult(
        label=event_name,
        outdir=outdir,
        sampler="nestle",
        search_parameter_keys=list(priors.keys()),
        fixed_parameter_keys=list(),
        priors=priors,
        sampler_kwargs=dict(test="test", func=lambda x: x),
        meta_data= dict(
            likelihood=dict(
                phase_marginalization=False,
                distance_marginalization=False,
                time_marginalization=False,
                frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
                waveform_arguments=dict(
                    reference_frequency=20.0, waveform_approximant="NRSur7dq4"
                ),
                interferometers=dict(
                    H1=dict(optimal_SNR=1),
                    L1=dict(optimal_SNR=1),
                ),
                sampling_frequency=4096,
                duration=4,
                start_time=0,
                waveform_generator_class=bilby.gw.waveform_generator.WaveformGenerator,
                parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
            )
        ),
        posterior=posterior,
    )
    filename = os.path.join(outdir, f"{event_name}.json")
    result.save_to_file(filename=filename)
    return filename


def get_test_cache_dir():
    test_dir = os.path.join(os.path.dirname(__file__), "test_cache_dir")

    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
        filename = generate_fake_result(outdir=test_dir)
        for event_names in ["GW170729", "GW150914", "GW190521"]:
            os.symlink(
                filename,
                os.path.join(test_dir, f"{event_names}{END_LABEL}.json"),
            )
    return test_dir
