from policyengine_us.model_api import *


class meets_snap_work_requirements_person(Variable):
    value_type = bool
    entity = Person
    label = "Person is eligible for SNAP benefits via work requirements"
    documentation = (
        "Whether the person meets the SNAP work requirements. Work "
        "requirement ineligibility attaches to the individual, not the "
        "household - 7 U.S.C. 2015(d)(1)(A) and (o)(2); 7 CFR 273.24(b)(1). "
        "A person failing this requirement is removed from the SNAP unit "
        "per 7 CFR 273.11(c) while the rest of the household remains "
        "eligible. A person fails only if they are subject to the ABAWD "
        "time limit (no exempting child in the unit) and do not meet the "
        "ABAWD work requirements, or if they are affirmatively sanctioned "
        "under the general work requirements (assumed compliant in "
        "baseline)."
    )
    definition_period = MONTH
    reference = (
        "https://www.fns.usda.gov/snap/work-requirements",
        "https://www.law.cornell.edu/cfr/text/7/273.7#f_1",
        "https://www.law.cornell.edu/cfr/text/7/273.24#b",
    )

    def formula(person, period, parameters):
        # General work requirement (7 CFR 273.7): registration compliance
        # is assumed in baseline; this is a hook for sanction modeling.
        general_work_requirements = person(
            "meets_snap_general_work_requirements", period
        )
        # ABAWD time limit (7 U.S.C. 2015(o); 7 CFR 273.24): only binds
        # when the unit has no exempting child.
        abawd_work_requirements = person("meets_snap_abawd_work_requirements", period)
        exempt_child_present = person.spm_unit(
            "snap_abawd_exempt_child_present", period
        )
        return general_work_requirements & (
            abawd_work_requirements | exempt_child_present
        )
