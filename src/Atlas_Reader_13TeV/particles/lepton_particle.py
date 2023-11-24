from hep_pheno_tools.abstract_particle import Particle


class LeptonParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.tlv.SetPtEtaPhiE(
            event.lep_pt[j] / 1000,
            event.lep_eta[j],
            event.lep_phi[j],
            event.lep_E[j] / 1000,
        )
        self.charge = event.lep_charge[j]
        self.is_tight_id = event.lep_isTightID[j]
        self.etcone20 = event.lep_etcone20[j] / 1000
        self.ptcone30 = event.lep_ptcone30[j] / 1000
        self.trig_match = event.lep_trigMatched[j]
        print(event.lep_type[j])
        if event.lep_type[j] == 11:
            self.name = "e"
            self.kind = "electron"
        elif event.lep_type[j] == 13:
            self.name = "mu"
            self.kind = "muon"
