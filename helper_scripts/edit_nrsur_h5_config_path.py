import h5py
import shutil, os

PATH = "/Users/avaj0001/Documents/projects/NR_DATA/"

LVK = 'IGWN-GWTC2p1-v2-GW190915_235702_PEDataRelease_mixed_cosmo.h5'
NRSUR = 'GW190916_200658_NRSur7dq4.h5'


def get_lvk_config_keys(fname):
    with h5py.File(fname, 'r') as f:
        return list(f['C01:IMRPhenomXPHM/config_file/config'].keys())

def get_NRSUR_config_keys(fname):
    with h5py.File(fname, 'r') as f:
        return list(f['Bilby:NRSur7dq4/config_file/config'].keys())

def copy_h5_file_contents_from_one_group_to_another(fname, src_grp, dst_grp):
    new_fname = fname.replace('.h5', '_EDITED.h5')
    if os.path.exists(new_fname):
        os.remove(new_fname)
    shutil.copy(fname, new_fname)
    with h5py.File(new_fname, 'r+') as f:
        if dst_grp in f:
            del f[dst_grp]
        f.copy(src_grp, dst_grp)
    return new_fname


new_nrsur_path = copy_h5_file_contents_from_one_group_to_another(PATH + NRSUR, 'Bilby:NRSur7dq4/meta_data/other/config_file',
                                                'Bilby:NRSur7dq4/config_file/config')



lvk_config_keys = get_lvk_config_keys(PATH + LVK)
nrsur_config_keys = get_NRSUR_config_keys(new_nrsur_path)

# write the config keys to a file
with open('lvk_config_keys.txt', 'w') as f:
    for key in lvk_config_keys:
        f.write(key + '\n')

with open('nrsur_config_keys.txt', 'w') as f:
    for key in nrsur_config_keys:
        f.write(key + '\n')
