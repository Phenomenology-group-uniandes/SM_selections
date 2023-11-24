# This selection function is for the Z->ll channel

from hep_pheno_tools import delphes_reader
from hep_pheno_tools.abstract_particle import get_kinematics_row

# Define constants
PT_MIN_CUT = 25  # GeV
ETA_MIN_CUT = -2.37
ETA_MAX_CUT = 2.37
RECO_Z_MIN = 66  # GeV
RECO_Z_MAX = 116  # GeV

basic_cuts = {
    "pt_min_cut": PT_MIN_CUT,
    "eta_min_cut": ETA_MIN_CUT,
    "eta_max_cut": ETA_MAX_CUT,
}
kin_cuts = {"muon": basic_cuts.copy(), "electron": basic_cuts.copy()}


def lep_lep_selection(event, data_type):
    """
    Function to select leptons from an event based on the data type.

    Parameters:
    event: The event to select leptons from.
    data_type: The type of data. Currently only "MonteCarlo" is supported.

    Returns:
    kin_row: The kinematics row of the selected leptons.
    """
    # Select the method to get good leptons based on the data type
    if data_type == "MonteCarlo":
        get_good_leptons = delphes_reader.classifier.get_good_leptons
    else:
        return "Error: data_type: {} not recognised".format(data_type)

    # Get the good leptons, ie. leptons that pass the kinematic cuts
    leptons = get_good_leptons(event, kin_cuts)

    # Check that there are exactly two leptons
    if len(leptons) != 2:
        return None
    # Check that the leptons have opposite charge
    if leptons[0] * leptons[1].charge >= 0:
        return None
    # Check that the leptons have the same flavour
    if leptons[0].kind != leptons[1].kind:
        return None
    # Check that the reconstructed Z mass is near the Z mass
    reco_z = leptons[0] + leptons[1]
    if not (RECO_Z_MIN <= reco_z.M() <= RECO_Z_MAX):
        return None
    # Calculate the kinematics row
    kin_row = get_kinematics_row(leptons)
    # Calculate the reconstructed Z mass
    kin_row["reco_z_mass"] = reco_z.M()
    return kin_row
