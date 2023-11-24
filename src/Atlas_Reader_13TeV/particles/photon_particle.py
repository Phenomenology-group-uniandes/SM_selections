from hep_pheno_tools.abstract_particle import Particle


class PhotonParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.tlv.SetPtEtaPhiE(
            event.photon_pt[j] / 1000,
            event.photon_eta[j],
            event.photon_phi[j],
            event.photon_E[j] / 1000,
        )
        self.conv_type = event.photon_convType[j]
        # this variables recover the particles near the photon
        # in a cone of DeltaRMax 0.3 for cone30 and 0.2 for cone20
        self.etcone20 = event.photon_etcone20[j] / 1000
        self.ptcone30 = event.photon_ptcone30[j] / 1000
        self.is_tight_id = event.photon_isTightID[j]
        self.trig_match = event.photon_trigMatched[j]
        self.charge = 0
        self.kind = "photon"
        self.name = f"{self.kind}_{{{j}}}"
        # you must ensure that your delphes card have a DeltaRMax 0.3
        self.isolation = self.ptcone30 / self.pt
