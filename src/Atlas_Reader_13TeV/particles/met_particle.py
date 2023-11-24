from ROOT import TLorentzVector

from hep_pheno_tools.abstract_particle import Particle


class MetParticle(Particle):
    def __init__(self, event):
        super().__init__()
        self.tlv.SetPtEtaPhiE(
            event.met_et / 1000,
            0,
            event.met_phi,
            event.met_et / 1000,
        )
        self.charge = 0.0
        self.name = "MET"
        self.kind = "MET"
