from hep_pheno_tools.delphes_reader.classifier import DEFAULT_CUTS
from hep_pheno_tools.delphes_reader.classifier import (
    get_good_jets as hpt_get_good_jets,
)
from hep_pheno_tools.delphes_reader.classifier import (
    get_good_leptons as hpt_get_good_leptons,
)
from hep_pheno_tools.delphes_reader.classifier import (
    get_unified,
    jets_NAMES_DIC,
    leptons_NAMES_DIC,
)

from .particles import (
    JetParticle,
    LeptonParticle,
    MetParticle,
    PhotonParticle,
    TauParticle,
)


def get_met(event):
    return MetParticle(event)


def get_leptons(event):
    return [LeptonParticle(event, i) for i in range(event.lep_n)]


def get_jets(event):
    jet_dict = {key: [] for key in jets_NAMES_DIC.keys()}
    for entry in range(event.jet_n):
        jet = JetParticle(event, entry)
        jet_dict[jet.kind].append(jet)
    for entry in range(event.tau_n):
        tau = TauParticle(event, entry)
        jet_dict["tau_jet"].append(tau)
    for key in jet_dict.keys():
        jet_dict[key].sort(reverse=True, key=lambda x: x.pt)
    return get_unified(jet_dict)


def get_good_jets(event):
    return hpt_get_good_jets(get_jets(event))


def get_good_leptons(event, kin_cuts=DEFAULT_CUTS):
    if not ("lep" in kin_cuts.keys()):
        kin_cuts["lep"] = (
            kin_cuts["muon"]
            if "muon" in kin_cuts.keys()
            else DEFAULT_CUTS["muon"]
        )
    return hpt_get_good_leptons({"lep": get_leptons(event)})
