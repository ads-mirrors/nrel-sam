
# Helper functions

def get_inflation_factor(base_yr, inflation_yr):

    # https://toweringskills.com/financial-analysis/cost-indices/
    inflation_dict=(
    {
        2024:800,
        2021:708.8,
        2019:607.5,
        2018:603.1,
        2017:567.5,
        2016:541.7,
        2013:567.3
    })

    return inflation_dict[inflation_yr] / inflation_dict[base_yr]

    # Define PHX costs

def get_bare_erected_cost_factor():
    # Weiland 2019
    frac_installation = 0.02
    frac_labor = 0.03

    f_bare_erected = 1.0 + frac_installation + frac_labor
    return f_bare_erected

# Cost Functions (UA in W/K, U in W/m2 K)


def buck_low_2021(UA, U, inflation_yr):
    
    yr = 2021

    A = UA / U                                      # m2
    unit_cost_equipment = 4158                      # $/m2
    base_cost_equipment = A * unit_cost_equipment   # $
    inflated_cost_equipment = base_cost_equipment * get_inflation_factor(yr, inflation_yr)  # $

    inflated_cost_bare_erected = inflated_cost_equipment * get_bare_erected_cost_factor()   # $

    return inflated_cost_equipment, inflated_cost_bare_erected    # $

def buck_high_2021(UA, U, inflation_yr):
    
    yr = 2021

    A = UA / U 
    unit_cost_equipment = 9031 # $/m2

    base_cost_equipment = A * unit_cost_equipment   # $
    inflated_cost_equipment = base_cost_equipment * get_inflation_factor(yr, inflation_yr)  # $

    inflated_cost_bare_erected = inflated_cost_equipment * get_bare_erected_cost_factor()   # $

    return inflated_cost_equipment, inflated_cost_bare_erected    # $

def buck_highx10_2021(UA, U, inflation_yr):
    
    buck_cost_equipment, buck_cost_bare_erected = buck_high_2021(UA, U, inflation_yr)

    return buck_cost_equipment * 10, buck_cost_bare_erected * 10


def carlson_2021(UA, U, inflation_yr):
    
    yr = 2017

    base_cost_equipment = 3.5 * UA
    inflated_cost_equipment = base_cost_equipment * 1.407577  # $

    inflated_cost_bare_erected = inflated_cost_equipment * get_bare_erected_cost_factor()   # $

    return inflated_cost_equipment, inflated_cost_bare_erected    # $