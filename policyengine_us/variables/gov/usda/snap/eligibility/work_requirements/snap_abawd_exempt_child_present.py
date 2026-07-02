from policyengine_us.model_api import *


class snap_abawd_exempt_child_present(Variable):
    value_type = bool
    entity = SPMUnit
    label = "SNAP unit contains a child exempting members from ABAWD work requirements"
    documentation = (
        "Whether the SNAP unit contains a child whose presence exempts all "
        "members from the ABAWD time limit. Pre-HR1, 7 CFR 273.24(c)(3)-(c)(4) "
        "exempt a person who is a parent (or other member) of a household with "
        "responsibility for a dependent child under 18, or who resides in a "
        "household where a household member is under age 18, 'even if the "
        "household member who is under 18 is not himself eligible' - so any "
        "member under 18 triggers the exemption, with no tax-dependency "
        "requirement. Post-HR1, 7 U.S.C. 2015(o)(3)(C) excepts a parent or "
        "other member of a household with responsibility for a dependent "
        "child under 14, which FNS has historically implemented "
        "household-wide."
    )
    definition_period = MONTH
    reference = (
        "https://www.law.cornell.edu/cfr/text/7/273.24#c_3",
        "https://www.law.cornell.edu/cfr/text/7/273.24#c_4",
        "https://www.law.cornell.edu/uscode/text/7/2015#o_3_C",
    )

    def formula(spm_unit, period, parameters):
        person = spm_unit.members
        # All members of an SPM unit share a household, so any() returns
        # the household's HR1 status.
        hr1_in_effect = spm_unit.any(person("is_snap_abawd_hr1_in_effect", period))
        p = parameters(period).gov.usda.snap.work_requirements.abawd.age_threshold
        # Snapshot pre-HR1 values (last month before 2025-07-04 effective
        # date) for states that delay HR1 adoption.
        p_pre = parameters(
            "2025-06-01"
        ).gov.usda.snap.work_requirements.abawd.age_threshold
        age = person("monthly_age", period)
        # Pre-HR1: any household member under 18 exempts all members,
        # regardless of tax dependency - 7 CFR 273.24(c)(3)-(c)(4).
        member_under_pre_hr1_threshold = spm_unit.any(age < p_pre.dependent)
        # Post-HR1: dependent child under 14 - 7 U.S.C. 2015(o)(3)(C).
        is_dependent = person("is_tax_unit_dependent", period)
        dependent_under_post_hr1_threshold = spm_unit.any(
            is_dependent & (age < p.dependent)
        )
        return where(
            hr1_in_effect,
            dependent_under_post_hr1_threshold,
            member_under_pre_hr1_threshold,
        )
