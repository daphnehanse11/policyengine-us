from policyengine_us.model_api import *


class medicaid_community_engagement_pass_through_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Medicaid community engagement pass-through eligibility"
    definition_period = MONTH
    reference = (
        "https://www.congress.gov/bill/119th-congress/house-bill/1/text",
        "https://www.medicaid.gov/federal-policy-guidance/downloads/cib12082025.pdf#page=6",
    )

    def formula(person, period, parameters):
        snap_work = parameters(period).gov.usda.snap.work_requirements
        snap = person.spm_unit("snap", period) > 0
        tanf = person.spm_unit("is_tanf_enrolled", period)

        age = person("monthly_age", period)
        snap_age_exempt = snap_work.general.age_threshold.exempted.calc(age)
        snap_non_age_exempt = person("is_snap_work_registration_exempt_non_age", period)
        # Compliance with SNAP work requirements (general registration
        # plus the ABAWD time limit, including the household-wide
        # exempting-child exception).
        snap_work_compliant = person("meets_snap_work_requirements_person", period)
        snap_pass_through = (
            snap & ~snap_age_exempt & ~snap_non_age_exempt & snap_work_compliant
        )

        tanf_pass_through = tanf & person.spm_unit(
            "meets_tanf_work_requirements", period
        )
        return snap_pass_through | tanf_pass_through
