from policyengine_us.model_api import *


class meets_snap_general_work_requirements(Variable):
    value_type = bool
    entity = Person
    label = "Person is eligible for SNAP benefits via general work requirements"
    documentation = (
        "Whether the person complies with the SNAP general work "
        "requirements of 7 CFR 273.7. The general requirement obligates "
        "non-exempt persons to register for work and accept suitable "
        "employment; working fewer than 30 hours per week is not itself "
        "disqualifying - 30+ hours of work is exemption 273.7(b)(1)(vii) "
        "from registration, not a compliance test. Disqualification "
        "requires an affirmative noncompliance event: refusing suitable "
        "employment or E&T noncompliance (273.7(f)), or voluntarily "
        "quitting or reducing work effort (273.7(j)). These events are "
        "not observable in survey data, so the baseline assumes "
        "registration compliance and this variable defaults to true for "
        "everyone. It is retained as a hook for modeling work-requirement "
        "sanctions: set it to false for a person to disqualify that "
        "individual, which removes them from the SNAP unit per 7 CFR "
        "273.11(c) rather than making the household ineligible."
    )
    default_value = True
    definition_period = MONTH
    reference = (
        "https://www.law.cornell.edu/cfr/text/7/273.7#f",
        "https://www.law.cornell.edu/cfr/text/7/273.7#j",
        "https://www.law.cornell.edu/uscode/text/7/2015#d_1",
    )
