import bilby
from bilby.gw.result import CompactBinaryCoalescenceResult
from bilby.gw.conversion import generate_all_bbh_parameters
from bilby.core.prior import TruncatedGaussian as TG
import pandas as pd
import os
import shutil
import numpy as np
import h5py
from bilby.core.utils import recursively_save_dict_contents_to_group
from nrsur_catalog.logger import logger

from nrsur_catalog.cache import LVK_LABEL, LVK_FILE_EXTENSION, NR_LABEL, NR_FILE_EXTENSION

np.random.seed(0)

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
            log_likelihood=bilby.core.prior.Uniform(-10, -5, name="log_likelihood"),
            log_prior=bilby.core.prior.Uniform(-10, -5, name="log_prior"),
            geocent_time=bilby.core.prior.Gaussian(0, 1, name="geocent_time", latex_label="$t_c$"),
            azimuth=bilby.core.prior.Gaussian(0, 1, name="azimuth", latex_label="$\phi$"),
            zenith=bilby.core.prior.Gaussian(0, 1, name="zenith", latex_label="$\\theta$"),
        )
    )
    return prior.sample(npts)


def generate_fake_result(
        n=100, outdir="outdir", event_name="test", fname=None, save=True,
):
    bilby.utils.command_line_args.bilby_test_mode = False
    priors = bilby.gw.prior.BBHPriorDict()
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


def get_mock_cache_dir(test_dir=TEST_DIR, num_events=2, pts=100):
    assert num_events > 0
    events = [f"GW{n}" for n in np.random.randint(159999, 209999, num_events)]
    events[0] = "GW170729"
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=False)
    for i, event_names in enumerate(events):
        nr_fname = os.path.join(test_dir, f"{event_names}{NR_FILE_EXTENSION}")
        write_pesummary_like_result(nr_fname, label=NR_LABEL, n=pts)
        lvk_fname = os.path.join(test_dir, f"{event_names}{LVK_FILE_EXTENSION}")
        write_pesummary_like_result(lvk_fname, label=LVK_LABEL, n=pts)
    logger.info(f"Generated {len(events)} mock events in {test_dir}")
    logger.info(f"{os.listdir(test_dir)}")
    return test_dir


def write_pesummary_like_result(filepath: str, label=LVK_LABEL, n=1000):
    if os.path.dirname(filepath) != '':
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.isfile(filepath):
        r = generate_fake_result(n=n, event_name=label, save=False)
        r.posterior.drop(columns=['waveform_approximant'], inplace=True)
        with h5py.File(filepath, "w") as f:
            grp = f.create_group(label)
            grp.create_dataset("posterior_samples", data=r.posterior.to_records(index=False))

            # create a subgroup for the prior
            prior_grp = grp.create_group("priors")
            pri = prior_grp.create_group("analytic")
            for key, item in r.priors.items():
                pri[key] = [str(item)]

            # create a subgroup for the meta_data
            meta_data_grp = grp.create_group("meta_data")
            meta_data_grp.create_group("other")
            recursively_save_dict_contents_to_group(f, f"{label}/meta_data/other/", r.meta_data)

            f.close()


def cleanup_mock_data(test_dir=TEST_DIR):
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    get_mock_cache_dir(num_events=3)
