from policyengine_us.model_api import *
from policyengine_core.periods import period as period_
from policyengine_core.periods import instant


def create_repeal_ut_medicaid_expansion() -> Reform:
    """
    Utah HB 15 (2026) - Repeals Medicaid expansion if federal matching
    falls below 85%. This reform sets the income limit to -inf, effectively
    removing expansion Medicaid eligibility.
    """

    def modify_parameters(parameters):
        parameters.gov.hhs.medicaid.eligibility.categories.adult.income_limit.UT.update(
            start=instant("2027-01-01"),
            stop=instant("2100-12-31"),
            value=float("-inf"),
        )
        return parameters

    class reform(Reform):
        def apply(self):
            self.modify_parameters(modify_parameters)

    return reform


def create_repeal_ut_medicaid_expansion_reform(
    parameters, period, bypass: bool = False
):
    if bypass:
        return create_repeal_ut_medicaid_expansion()

    p = parameters.gov.contrib.states.ut.medicaid

    reform_active = False
    current_period = period_(period)

    for _ in range(5):
        if p(current_period).repeal_expansion_in_effect:
            reform_active = True
            break
        current_period = current_period.offset(1, "year")

    if reform_active:
        return create_repeal_ut_medicaid_expansion()
    else:
        return None


repeal_ut_medicaid_expansion = create_repeal_ut_medicaid_expansion_reform(
    None, None, bypass=True
)
