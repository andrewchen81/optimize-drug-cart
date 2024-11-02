# Import Packages
import pandas as pd
import numpy as np
import streamlit as st

def optimize_cart_allocation(
    df, # Input DF with Drug Unit & Drug Count
    drug_unit_col, # drug unit col in df
    drug_count_col, # drug count col in df
    unit_constraint_dict, # drug unit combination constraint
    number_of_carts, # number of carts to distribute drug units
    algorithm = 'greedy' # algorithm of choice
):
    drug_units = [str(x).strip() for x in df[drug_unit_col]]
    medication_count = [float(x) for x in df['Medication_Count'].tolist()]

    clean_unit_constraint_dict = {key: [x for x in value if x in drug_units] for key, value in unit_constraint_dict.items()}

    constrained_drug_items = {key: sum(medication_count[drug_units.index(x)] for x in value) for key, value in clean_unit_constraint_dict.items()}
    unconstrained_drug_items = [(x, medication_count[drug_units.index(x)]) for x in drug_units if all(x not in group for group in clean_unit_constraint_dict.values())]
    updated_drug_items = list(constrained_drug_items.items()) + unconstrained_drug_items

    if algorithm == 'greedy':
        greedy_algorithm(updated_drug_items)

def greedy_algorithm(
    drug_items # Updated drug items (with the unit constraints)
):
    sorted_units = sorted(drug_items, key=lambda x: x[1], reverse=True)
    carts = [[] for _ in range(num_carts)]
    cart_weights = [0] * num_carts

    for unit, weight in sorted_units:
        min_cart_index = cart_weights.index(min(cart_weights))
        carts[min_cart_index].append((unit, weight))
        cart_weights[min_cart_index] += weight
    print(carts,unit,cart_weights)



# df = pd.read_csv('/Users/andrewchen/Documents/optimize_drug_cart_project/daily_files/drug_medication_count_20241018.csv')
# unit_constraints = {
# 	'C+G': ['C', 'G'],
# 	'B+F': ['B', 'F'],
# 	'1B+1C': ['1B', '1C'],
# 	'1A+J+K+N+Z': ['1A', 'J', 'K', 'N', 'Z']
# }
# num_carts = 6
#
# optimize_cart_allocation(
#     df=df,
#     drug_unit_col = 'Drug Unit',
#     drug_count_col = 'Medication_Count',
#     unit_constraint_dict = unit_constraints,
#     number_of_carts = num_carts,
#     algorithm = 'greedy'
# )
#
