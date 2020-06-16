"""
Functions that calculate corporate income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle corpfunctions.py
# pylint --disable=locally-disabled corpfunctions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

"""
Compute total exemptions.
"""  

@iterate_jit(nopython=True)
def corp_tax_free_income_total(percent_exempt_rate_tax_free_income_statistic_purpose_art_17_1_4d_etc, 
                               percent_exempt_rate_tax_free_income_art_17_1_4, 
                               percent_exempt_rate_tax_free_income_non_agriculture_art_17_1_4e,
                               percent_exempt_rate_tax_free_income_subsidies_art_17_1_21, 
                               percent_exempt_rate_tax_free_income_art_17_1_23_24, percent_exempt_rate_tax_free_income_art_17_1_34, 
                               percent_exempt_rate_tax_free_income_art_17_1_39,
                               percent_exempt_rate_tax_free_income_housing_coops_art_17_1_44,
                               percent_exempt_rate_tax_free_income_subsidies_state_local_art_17_1_47,
                               percent_exempt_rate_tax_free_income_amounts_government_agencies_art_17_1_48,
                               percent_exempt_rate_tax_free_income_agriculture_producer_groups_art_17_1_49,
                               percent_exempt_rate_tax_free_income_financial_programs_central_europe_art_17_1_52,
                               percent_exempt_rate_tax_free_income_other, 
                               percent_exempt_rate_tax_free_income_environmental_finances_art_17_1_53,
                               percent_exempt_rate_tax_free_income_other_art_17_1,
                               tax_free_income_other_art_17_1,
                               tax_free_income_environmental_finances_art_17_1_53,
                               tax_free_income_other,
                               tax_free_income_financial_programs_central_europe_art_17_1_52,
                               tax_free_income_agriculture_producer_groups_art_17_1_49,
                               tax_free_income_amounts_government_agencies_art_17_1_48,
                               tax_free_income_subsidies_state_local_art_17_1_47,
                               tax_free_income_housing_coops_art_17_1_44, 
                               tax_free_income_art_17_1_39,
                               tax_free_income_art_17_1_34,
                               tax_free_income_art_17_1_23_24, tax_free_income_subsidies_art_17_1_21, 
                               tax_free_income_non_agriculture_art_17_1_4e, 
                               tax_free_income_art_17_1_4, tax_free_income_statistic_purpose_art_17_1_4d_etc, 
                               tax_free_income_total):
    tax_free_income_total = (tax_free_income_statistic_purpose_art_17_1_4d_etc*percent_exempt_rate_tax_free_income_statistic_purpose_art_17_1_4d_etc + 
                             tax_free_income_art_17_1_4*percent_exempt_rate_tax_free_income_art_17_1_4 +
                             tax_free_income_non_agriculture_art_17_1_4e*percent_exempt_rate_tax_free_income_non_agriculture_art_17_1_4e + 
                             tax_free_income_subsidies_art_17_1_21*percent_exempt_rate_tax_free_income_subsidies_art_17_1_21 + 
                             tax_free_income_art_17_1_23_24*percent_exempt_rate_tax_free_income_art_17_1_23_24 + 
                             tax_free_income_art_17_1_34*percent_exempt_rate_tax_free_income_art_17_1_34 +
                             tax_free_income_art_17_1_39*percent_exempt_rate_tax_free_income_art_17_1_39 + 
                             tax_free_income_housing_coops_art_17_1_44*percent_exempt_rate_tax_free_income_housing_coops_art_17_1_44 +
                             tax_free_income_subsidies_state_local_art_17_1_47*percent_exempt_rate_tax_free_income_subsidies_state_local_art_17_1_47 + 
                             tax_free_income_amounts_government_agencies_art_17_1_48*percent_exempt_rate_tax_free_income_amounts_government_agencies_art_17_1_48 +
                             tax_free_income_agriculture_producer_groups_art_17_1_49*percent_exempt_rate_tax_free_income_agriculture_producer_groups_art_17_1_49 + 
                             tax_free_income_financial_programs_central_europe_art_17_1_52*percent_exempt_rate_tax_free_income_financial_programs_central_europe_art_17_1_52 +
                             tax_free_income_environmental_finances_art_17_1_53*percent_exempt_rate_tax_free_income_environmental_finances_art_17_1_53 + 
                             tax_free_income_other_art_17_1*percent_exempt_rate_tax_free_income_other_art_17_1 +
                             tax_free_income_other*percent_exempt_rate_tax_free_income_other)

    return (tax_free_income_total)


@iterate_jit(nopython=True)
def corp_deductions_from_income_total(percent_deductions_from_income_art_18_1_1,
                                      percent_deductions_from_income_art_18_1_7,
                                      loss_from_previous_years, 
                                      deductions_from_income_art_18_1_1, 
                                      deductions_from_income_art_18_1_7, 
                                      deductions_from_income_total):
    """
    Compute total current expenditure.
    """
    deductions_from_income_total = (loss_from_previous_years + deductions_from_income_art_18_1_1*percent_deductions_from_income_art_18_1_1 +
                            deductions_from_income_art_18_1_7*percent_deductions_from_income_art_18_1_7)

    return (deductions_from_income_total)


@iterate_jit(nopython=True)
def corp_expenditure(expenditure, tax_deductible_expenditure_poland, tax_deductible_expenditure_outside_poland,
                            tax_deductible_expenditure_outside_poland_other):
    """
    Compute total current expenditure.
    """
    expenditure = (tax_deductible_expenditure_poland + tax_deductible_expenditure_outside_poland +
                            tax_deductible_expenditure_outside_poland_other)

    return (expenditure)


@iterate_jit(nopython=True)
def is_small_business(small_business_threshold, revenue, small_business):
    
    """
    Compute Income = Revenue - Expenditure
    """
    if (revenue <= small_business_threshold):
        small_business = 1
    else:    
        small_business = 0
    
    return (small_business)


@iterate_jit(nopython=True)
def corp_income(revenue, expenditure, income, loss):
    
    """
    Compute Income = Revenue - Expenditure
    """
    if (revenue >= expenditure):
        income = revenue - expenditure
        loss = 0
    else:
        loss = -(revenue - expenditure)
        income = 0
    
    return (income, loss)


@iterate_jit(nopython=True)
def corp_tax_base_before_deductions(income, tax_free_income_total,
                                    deductions_from_income_total,
                                    tax_base_before_deductions):
    """
    Compute corp tax base after taking out the deductions.
    """
    tax_base_before_deductions = (income - tax_free_income_total -
                                  deductions_from_income_total)
    tax_base_before_deductions = np.maximum(0, tax_base_before_deductions)
    
    return (tax_base_before_deductions)


@iterate_jit(nopython=True)
def corp_tax_base_after_deductions(percent_deductions_from_tax_base, 
                                   tax_base_before_deductions,
                                   deductions_from_tax_base,
                                   income_tax_base_after_deductions):
    """
    Compute corp tax base after taking out the deductions.
    """
    income_tax_base_after_deductions = (tax_base_before_deductions -
                                        deductions_from_tax_base*percent_deductions_from_tax_base)
    income_tax_base_after_deductions = np.maximum(0, income_tax_base_after_deductions)

    return (income_tax_base_after_deductions)


@iterate_jit(nopython=True)
def cit_liability(small_business_threshold, cit_rate_small_business,
                  cit_rate_regular, revenue, income_tax_base_after_deductions,
                  citax):
    """
    Compute tax liability given the tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # compute citax amount
    if (revenue <= small_business_threshold):
        citax = cit_rate_small_business * income_tax_base_after_deductions
    else:    
        citax = cit_rate_regular * income_tax_base_after_deductions

    return (citax)
