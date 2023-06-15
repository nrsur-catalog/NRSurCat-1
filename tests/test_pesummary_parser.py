from nrsur_catalog.utils.pesummary_result_to_bilby_result import (
    _parse_prior,
    _parse_posterior,
    pesummary_to_bilby_result,
)

from bilby.gw.prior import BBHPriorDict
from bilby.gw.result import CBCResult
import pandas as pd


def test_prior_parser():
    p = {
        'a_1': ["Uniform(minimum=0, maximum=0.99, name='a_1', latex_label='$a_1$', unit=None, boundary=None)"],
        'a_2': ["Uniform(minimum=0, maximum=0.99, name='a_2', latex_label='$a_2$', unit=None, boundary=None)"],
        'azimuth': [
            "Uniform(minimum=0, maximum=6.283185307179586, name=None, latex_label='$\\\\epsilon$', unit=None, boundary='periodic')"],
        'chirp_mass': [
            "UniformInComponentsChirpMass(minimum=12, maximum=400, name='chirp_mass', latex_label='$\\\\mathcal{M}$', unit=None, boundary=None)"],
        'geocent_time': [
            "Uniform(minimum=1126259462.2910001, maximum=1126259462.491, name='geocent_time', latex_label='$t_c$', unit='$s$', boundary=None)"],
        'luminosity_distance': [
            'UniformSourceFrame(minimum=100.0, maximum=10000.0, cosmology=FlatLambdaCDM(H0=67.7 km / (Mpc s), Om0=0.307, Tcmb0=2.725 K, Neff=3.05, m_nu=[0.   0.   0.06] eV, Ob0=0.0486), name=\'luminosity_distance\', latex_label=\'$d_L$\', unit=Unit("Mpc"), boundary=None)'],
        'mass_ratio': [
            "UniformInComponentsMassRatio(minimum=0.167, maximum=1, name='mass_ratio', latex_label='$q$', unit=None, boundary=None)"],
        'phase': [
            "Uniform(minimum=0, maximum=6.283185307179586, name='phase', latex_label='$\\\\phi$', unit=None, boundary='periodic')"],
        'phi_12': [
            "Uniform(minimum=0, maximum=6.283185307179586, name='phi_12', latex_label='$\\\\Delta\\\\phi$', unit=None, boundary='periodic')"],
        'phi_jl': [
            "Uniform(minimum=0, maximum=6.283185307179586, name='phi_jl', latex_label='$\\\\phi_{JL}$', unit=None, boundary='periodic')"],
        'psi': [
            "Uniform(minimum=0, maximum=3.141592653589793, name='psi', latex_label='$\\\\psi$', unit=None, boundary='periodic')"],
        'theta_jn': [
            "Sine(minimum=0, maximum=3.141592653589793, name='theta_jn', latex_label='$\\\\theta_{JN}$', unit=None, boundary=None)"],
        'tilt_1': [
            "Sine(minimum=0, maximum=3.141592653589793, name='tilt_1', latex_label='$\\\\theta_1$', unit=None, boundary=None)"],
        'tilt_2': [
            "Sine(minimum=0, maximum=3.141592653589793, name='tilt_2', latex_label='$\\\\theta_2$', unit=None, boundary=None)"],
        'total_mass': ["Constraint(minimum=60, maximum=400, name='total_mass', latex_label='$M$', unit=None)"],
        'zenith': [
            "Sine(minimum=0, maximum=3.141592653589793, name=None, latex_label='$\\\\kappa$', unit=None, boundary=None)"]}
    pri = _parse_prior(p)
    assert isinstance(pri, BBHPriorDict)
    assert pri['chirp_mass'].minimum == 12
    assert pri['chirp_mass'].maximum == 400


def test_pesummary_to_bilby(mock_nrsur_result):
    r = pesummary_to_bilby_result(mock_nrsur_result)
    assert isinstance(r, CBCResult)
    assert isinstance(r.posterior, pd.DataFrame)
    assert isinstance(r.priors, BBHPriorDict)
    assert r.meta_data['likelihood']['time_marginalization'] == False