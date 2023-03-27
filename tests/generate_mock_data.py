import bilby
from bilby.gw.result import CompactBinaryCoalescenceResult
from bilby.gw.conversion import generate_all_bbh_parameters
from bilby.core.prior import TruncatedGaussian as TG
import pandas as pd
import os
import shutil
import numpy as np

from nrsur_catalog.logger import logger

np.random.seed(0)

END_LABEL = "_NRSur7dq4_merged_result"
TEST_DIR = os.path.join(os.path.dirname(__file__), "test_cache_dir")


def generate_fake_posterior(npts=100):
    inj = bilby.gw.prior.BBHPriorDict().sample(1)
    prior = bilby.gw.prior.BBHPriorDict(
        dict(
            mass_ratio=TG(
                name="mass_ratio",
                minimum=0.125,
                maximum=1,
                mu=inj["mass_ratio"],
                sigma=0.1,
            ),
            chirp_mass=TG(
                name="chirp_mass",
                minimum=25,
                maximum=100,
                mu=inj["chirp_mass"],
                sigma=10,
            ),
            luminosity_distance=TG(
                name="luminosity_distance",
                minimum=1e2,
                maximum=5e3,
                mu=inj["luminosity_distance"],
                sigma=1e2,
            ),
            dec=TG(
                name="dec",
                minimum=-np.pi / 2,
                maximum=np.pi / 2,
                mu=inj["dec"],
                sigma=np.pi / 4,
            ),
            ra=TG(
                name="ra",
                minimum=0,
                maximum=2 * np.pi,
                boundary="periodic",
                mu=inj["ra"],
                sigma=np.pi / 4,
            ),
            theta_jn=TG(
                name="theta_jn",
                minimum=0,
                maximum=np.pi,
                mu=inj["theta_jn"],
                sigma=np.pi / 4,
            ),
            psi=TG(
                name="psi",
                minimum=0,
                maximum=np.pi,
                boundary="periodic",
                mu=inj["psi"],
                sigma=np.pi / 4,
            ),
            phase=TG(
                name="phase",
                minimum=0,
                maximum=2 * np.pi,
                boundary="periodic",
                mu=inj["phase"],
                sigma=np.pi / 4,
            ),
            a_1=TG(name="a_1", minimum=0, maximum=0.99, mu=inj["a_1"], sigma=0.1),
            a_2=TG(name="a_2", minimum=0, maximum=0.99, mu=inj["a_2"], sigma=0.1),
            tilt_1=TG(
                name="tilt_1",
                minimum=0,
                maximum=np.pi,
                mu=inj["tilt_1"],
                sigma=np.pi / 4,
            ),
            tilt_2=TG(
                name="tilt_2",
                minimum=0,
                maximum=np.pi,
                mu=inj["tilt_2"],
                sigma=np.pi / 4,
            ),
            phi_12=TG(
                name="phi_12",
                minimum=0,
                maximum=2 * np.pi,
                boundary="periodic",
                mu=inj["phi_12"],
                sigma=np.pi / 4,
            ),
            phi_jl=TG(
                name="phi_jl",
                minimum=0,
                maximum=2 * np.pi,
                boundary="periodic",
                mu=inj["phi_jl"],
                sigma=np.pi / 4,
            ),
        )
    )
    return prior.sample(npts)


def generate_fake_result(
    n=100, outdir="outdir", event_name="test", fname=None, save=True,
):
    bilby.utils.command_line_args.bilby_test_mode = False
    priors = bilby.gw.prior.BBHPriorDict()
    # priors["geocent_time"] = 2
    posterior = pd.DataFrame(generate_fake_posterior(npts=n))
    posterior = generate_all_bbh_parameters(posterior)
    result = CompactBinaryCoalescenceResult(
        label=event_name,
        outdir=outdir,
        sampler="dynesty",
        search_parameter_keys=list(priors.keys()),
        fixed_parameter_keys=list(),
        priors=bilby.gw.prior.BBHPriorDict(),
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
    if fname is None:
        fname = os.path.join(outdir, f"{event_name}.hdf5")
    if save:
        result.save_to_file(filename=fname, extension="hdf5")
        return fname
    else:
        return result


def get_mock_results(num_events=3, pts=1000):
    events = [f"GW{n}" for n in np.random.randint(159999, 209999, num_events)]
    res_dic = {}
    for event_name in events:
        res_dic[event_name] = generate_fake_result(
            n=pts, event_name=event_name, save=False
        )
    return res_dic


def get_mock_cache_dir(test_dir=TEST_DIR, num_events=3, symlinks=True, pts=100, end_label=END_LABEL):
    assert num_events > 0
    events = [f"GW{n}" for n in np.random.randint(159999, 209999, num_events)]
    events[0] = "GW170729"
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=False)
    test_filename = ""
    for i, event_names in enumerate(events):
        new_fname = os.path.join(test_dir, f"{event_names}{end_label}.hdf5")
        if i == 0:
            test_filename = generate_fake_result(fname=new_fname, n=pts)
        else:
            if symlinks:
                os.symlink(test_filename, new_fname)
                logger.debug("simlink {} -> {}".format(new_fname, test_filename))
            else:
                generate_fake_result(fname=new_fname, n=pts)
    logger.info(f"Generated {len(events)} mock events in {test_dir}")
    logger.info(f"{os.listdir(test_dir)}")
    return test_dir


def cleanup_mock_data(test_dir=TEST_DIR):
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    get_mock_cache_dir(num_events=10)
