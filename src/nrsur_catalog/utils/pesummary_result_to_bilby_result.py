from bilby.gw.prior import BBHPriorDict
from typing import Dict,List

def parse_prior(p:Dict[str,List[str]])->BBHPriorDict:
    """Parse a prior string into a bilby prior object

    parameters
    ----------
    p: dict
        p = {
        'a_1': ["Uniform(minimum=0,...)"],
        'a_2': ["Uniform(minimum=0,...)"],
        ...
        }

    returns a bilby prior object
    """
    pri = {k:v[0] for k,v in p.items()}
    # convert 'UniformInComponentsChirpMass' to 'bilby.gw.prior.UniformInComponentsChirpMass'
    for k,v in pri.items():
        if 'UniformInComponentsChirpMass' in v:
            v = v.replace('UniformInComponentsChirpMass', 'bilby.gw.prior.UniformInComponentsChirpMass')
            pri[k] = v
        elif 'UniformSourceFrame' in v:
            v = v.replace('UniformSourceFrame', 'bilby.gw.prior.UniformSourceFrame')
            pri[k] = v
        elif 'UniformInComponentsMassRatio' in v:
            v = v.replace('UniformInComponentsMassRatio', 'bilby.gw.prior.UniformInComponentsMassRatio')
            pri[k] = v
    pri = BBHPriorDict(pri)
    return pri