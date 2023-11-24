from hep_pheno_tools.abstract_particle import Particle

JET_TYPES = {
    "BTag0_TauTag0": "l_jet",
    "BTag1_TauTag0": "b_jet",
    "BTag0_TauTag1": "tau_jet",
}


class JetParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.tlv.SetPtEtaPhiE(
            event.jet_pt[j] / 1000,
            event.jet_eta[j],
            event.jet_phi[j],
            event.jet_E[j] / 1000,
        )
        # cut on 0.8244273 is 70% WP for MV2c10
        # may does not match with the delphes card tagger
        # may we need update the delphes card
        if event.jet_MV2c10[j] > 0.8244273:
            self.b_tag = 1
        else:
            self.b_tag = 0

        self.kind = self._jet_type()
        self.name = f"{self.kind}_{{{j}}}"

    def _jet_type(self):
        """Estimates the jet type based on the BTag and TauTag attributes.

        Returns:
            str: particle type.
        """
        tag = f"BTag{self.b_tag}_TauTag{self.tau_tag}"
        return JET_TYPES.get(tag, "other_jet")
