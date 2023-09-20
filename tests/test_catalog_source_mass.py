from nrsur_catalog import Catalog, NRsurResult

CACHE = "/Users/avaj0001/Documents/projects/NRSUR_PRJ/out_web/.nrsur_catalog_cache"



r = NRsurResult.load("GW200224_222234", cache_dir=CACHE)
fig = r.plot_corner(["mass_1_source", "mass_2_source", "chirp_mass", "mass_ratio"])
fig.savefig("GW200224_222234_corner.png")

# fig = r.plot_signal(n_samples=100)
# fig.savefig("GW200224_222234_signal.png")
#
#
# catalog = Catalog.load(cache_dir=CACHE)
# catalog.violin_plot("mass_1_source")

## NEED TO DOWNLOAD  https://zenodo.org/record/5546663/files/IGWN-GWTC3p0-v1-GW200224_222234_PEDataRelease_mixed_cosmo.h5
