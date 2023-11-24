from hep_pheno_tools.abstract_particle import Particle


class TauParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.tlv.SetPtEtaPhiE(
            event.tau_pt[j] / 1000,
            event.tau_eta[j],
            event.tau_phi[j],
            event.tau_E[j] / 1000,
        )
        self.charge = event.tau_charge[j]
        self.is_tight_id = event.tau_isTightID[j]
        self.n_tracks = event.tau_nTracks[j]
        self.trig_match = event.tau_trigMatched[j]
        self.bdt_id = event.tau_BDTid[j]
        self.kind = "tau_jet"
        self.name = f"{self.kind}_{{{j}}}"
