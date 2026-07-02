from policyengine_us.model_api import *


class meets_snap_work_requirements(Variable):
    value_type = bool
    entity = SPMUnit
    label = "SPM Unit is eligible for SNAP benefits via work requirements"
    documentation = (
        "Whether at least one SNAP unit member meets the work "
        "requirements. Work requirement ineligibility attaches to the "
        "individual, who is removed from the SNAP unit per 7 CFR "
        "273.11(c); the unit as a whole is ineligible only when no "
        "members remain eligible."
    )
    definition_period = MONTH
    reference = (
        "https://www.fns.usda.gov/snap/work-requirements",
        "https://www.law.cornell.edu/cfr/text/7/273.7#f_1",
        "https://www.law.cornell.edu/cfr/text/7/273.24#b",
    )

    def formula(spm_unit, period, parameters):
        person = spm_unit.members
        return spm_unit.any(person("meets_snap_work_requirements_person", period))
