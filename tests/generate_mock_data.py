import bilby
from bilby.gw.result import CompactBinaryCoalescenceResult
from bilby.gw.conversion import generate_all_bbh_parameters
import pandas as pd
import os
import shutil
import numpy as np

END_LABEL = "_NRSur7dq4_merged_result"
TEST_DIR = os.path.join(os.path.dirname(__file__), "test_cache_dir")


def generate_fake_result(n=100, outdir="outdir", event_name="test"):
    bilby.utils.command_line_args.bilby_test_mode = False
    priors = bilby.gw.prior.BBHPriorDict()
    priors["geocent_time"] = 2
    posterior = pd.DataFrame(priors.sample(n))
    posterior = generate_all_bbh_parameters(posterior)

    result = CompactBinaryCoalescenceResult(
        label=event_name,
        outdir=outdir,
        sampler="nestle",
        search_parameter_keys=list(priors.keys()),
        fixed_parameter_keys=list(),
        priors=priors,
        sampler_kwargs=dict(test="test", func=lambda x: x),
        meta_data=dict(
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
    print(f"Generated mock event {event_name} in {filename}")
    return filename


def get_mock_cache_dir(test_dir=TEST_DIR, num_events=3):
    assert num_events > 0
    events = [f"GW{n}" for n in np.random.randint(159999, 209999, num_events)]
    events[0] = "GW170729"
    os.makedirs(test_dir, exist_ok=True)
    test_filename = generate_fake_result(outdir=test_dir)
    for i, event_names in enumerate(events):
        new_fname = os.path.join(test_dir, f"{event_names}{END_LABEL}.json")
        if not os.path.exists(new_fname):
            if i == 0:
                shutil.move(test_filename, new_fname)
                test_filename = new_fname
            else:
                os.symlink(test_filename, new_fname)
    print(f"Generated {len(events)} mock events in {test_dir}")
    return test_dir


def cleanup_mock_data(test_dir=TEST_DIR):
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    get_mock_cache_dir(num_events=10)
