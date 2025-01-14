from prefixes import *

# these are predicates from DGIDB as well as drug and chemical activity types from drug central
DGIDB_PREDICATE_MAPPING = {
    "ac50": f"{DGIDB}:activator",
    "activator": f"{DGIDB}:activator",
    "agonist": f"{DGIDB}:agonist",
    "allosteric_antagonist": f"{DGIDB}:antagonist",
    "allosteric_modulator": f"{DGIDB}:modulator",
    "antagonist": f"{DGIDB}:antagonist",
    "antibody": f"{DGIDB}:binder",
    "antibody_binding": f"{DGIDB}:binder",
    "antisense_inhibitor": f"{DGIDB}:inhibitor",
    "app_ki": f"RO:0002434",
    "app_km": f"RO:0002434",
    "binding_agent": f"{DGIDB}:binder",
    "blocker": f"{DGIDB}:blocker",
    "channel_blocker": f"{DGIDB}:channel_blocker",
    "ec50": f"{DGIDB}:agonist",
    "ed50": f"RO:0002434",
    "gating_inhibitor": f"{DGIDB}:gating_inhibitor",
    "gi50": f"RO:0002434",
    "ic50": f"{DGIDB}:inhibitor",
    "inhibitor": f"{DGIDB}:inhibitor",
    "interacts_with": f"RO:0002434",
    "inverse_agonist": f"{DGIDB}:inverse_agonist",
    "ka": f"RO:0002434",
    "kact": f"RO:0002434",
    "kb": f"{DGIDB}:binder",
    "kd": f"{DGIDB}:binder",
    "kd1": f"RO:0002434",
    "ki": f"{DGIDB}:inhibitor",
    "km": f"RO:0002434",
    "ks": f"RO:0002434",
    "modulator": f"{DGIDB}:modulator",
    "mic": f"RO:0002434",
    "mpc": f"RO:0002434",
    "negative_modulator": f"{CHEMBL_MECHANISM}:negative_modulator",
    "negative_allosteric_modulator": f"{CHEMBL_MECHANISM}:negative_modulator",
    "opener": f"{CHEMBL_MECHANISM}:opener",
    "other": f"{DGIDB}:other",
    "partial_agonist": f"{DGIDB}:partial_agonist",
    "pa2": f"RO:0002434",
    "pharmacological_chaperone": f"{DGIDB}:chaperone",
    "positive_allosteric_modulator": f"{CHEMBL_MECHANISM}:positive_modulator",
    "positive_modulator": f"{CHEMBL_MECHANISM}:positive_modulator",
    "releasing_agent": f"{CHEMBL_MECHANISM}:releasing_agent",
    "substrate": f"{CHEMBL_MECHANISM}:substrate",
    "xc50": f"RO:0002434"
}
