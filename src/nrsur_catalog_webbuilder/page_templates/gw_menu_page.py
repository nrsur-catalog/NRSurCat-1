# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [markdown] tags=["full-width"]
# # NRSurrogate Events
#
# Table of the NRSurrogate Catalog events with some posterior median and 90% credible interval values.
# Click on the event name to see more info.
#
#
# {{SUMMARY_TABLE}}
#
#
#
# Look at the [Catalog plots](../catalog_plots.ipynb) to see how to make a larger summary table of the catalog.
# Some of the parameters included are shown below.
#
# | Parameter                  | LaTeX Label              |
# |----------------------------|--------------------------|
# | a_1                        | $a_1$                    |
# | a_2                        | $a_2$                    |
# | azimuth                    | $\epsilon \ [{\rm rad}]$ |
# | chi_1                      | $\chi_1$                 |
# | chi_1_in_plane             | $\chi_1^{\perp}$         |
# | chi_2                      | $\chi_2$                 |
# | chi_2_in_plane             | $\chi_2^{\perp}$         |
# | chi_eff                    | $\chi_{\rm eff}$         |
# | chi_p                      | $\chi_{\rm p}$           |
# | chirp_mass                 | $\mathcal{M} \ [M_{\odot}]$ |
# | comoving_distance          | $d_{\rm C} \ [{\rm Mpc}]$ |
# | cos_iota                   | $\cos{\iota}$            |
# | cos_theta_jn               | $\cos{\theta_{JN}}$      |
# | cos_tilt_1                 | $\cos{\theta_1}$         |
# | cos_tilt_2                 | $\cos{\theta_2}$         |
# | dec                        | ${\rm DEC} \ [{\rm rad}]$ |
# | delta_lambda_tilde         | $\delta \tilde{\Lambda}$ |
# | geocent_time               | $t_c \ [{\rm s}]$         |
# | H1_time                    | $t_H \ [{\rm s}]$         |
# | iota                       | $\iota \ [{\rm rad}]$    ||
# | luminosity_distance        | $d_{\rm L} \ [{\rm Mpc}]$ |
# | mass_1                     | $m_1^{\rm det} \ [M_{\odot}]$       |
# | mass_1_source              | $m_1^{\rm src} \ [M_{\odot}]$ |
# | mass_2                     | $m_2^{\rm det} \ [M_{\odot}]$       |
# | mass_2_source              | $m_2^{\rm src} \ [M_{\odot}]$ |
# | mass_ratio                 | $q$                      |
# | phase                      | $\phi \ [{\rm rad}]$     |
# | phi_1                      | $\phi_1$                 |
# | phi_12                     | $\phi_{12} \ [{\rm rad}]$ |
# | phi_2                      | $\phi_1$                 |
# | phi_jl                     | $\phi_{\rm JL} \ [{\rm rad}]$ |
# | psi                        | $\psi \ [{\rm rad}]$     |
# | ra                         | ${\rm RA} \ [{\rm rad}]$ |
# | redshift                   | $z$                      |
# | spin_1x                    | $S_{1,x}$                |
# | spin_1y                    | $S_{1,y}$                |
# | spin_1z                    | $S_{1,z}$                |
# | spin_2x                    | $S_{2,x}$                |
# | spin_2y                    | $S_{2,y}$                |
# | spin_2z                    | $S_{2,z}$                |
# | symmetric_mass_ratio       | $\eta$                   |
# | theta_jn                   | $\theta_{JN} \ [{\rm rad}]$ |
# | tilt_1                     | $\theta_1 \ [{\rm rad}]$ |
# | tilt_2                     | $\theta_2 \ [{\rm rad}]$ |
# | time_jitter                | $\delta t \ [{\rm s}]$   |
# | total_mass                 | $M\ [M_{\odot}]$         |
# | total_mass_source          | $M^{\rm Source} \ [M_{\odot}]$ |
# | zenith                     | $\kappa \ [{\rm rad}]$   |
# | final_mass                 | $m_f \  [M_{\odot}]$      |
# | final_spin                 | $\chi_f$                 |
# | final_kick                 | $v_f \ [{\rm km/s}]$     |
#

# + tags=["remove-cell"]
# from nrsur_catalog_webbuilder.utils import get_catalog_summary

# POSTERIORS = [
#     "chirp_mass",
#     "mass_ratio",
#     "chi_eff",
#     "final_mass",
#     "final_spin",
#     "final_kick",
# ]

# summary_df = get_catalog_summary("{{EVENTS_DIR}}", "{{CACHE_DIR}}", columns=POSTERIORS)

# import itables.options as opt

# + tags=["remove-input", "full-width"]
# from itables import JavascriptFunction, init_notebook_mode, show

# opt.drawCallback = JavascriptFunction(
#     "function(settings) " '{MathJax.Hub.Queue(["Typeset",MathJax.Hub]);}'
# )

# init_notebook_mode(all_interactive=True)
# summary_df.rename(columns={"Waveform": "   "})

# summary_df = summary_df.reset_index(drop=True)
# show(
#     summary_df,
#     style="width:3500px",
#     scrollX=True,
#     autoWidth=True,
#     lengthMenu=[10, 25, 50],
#     classes="cell-border nowrap display compact",
#     caption='',
# )
