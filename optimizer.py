# Import Packages
import pandas as pd
import numpy as np
import streamlit as st
import re
import ast

def greedy_algorithm(
    drug_items, # Updated drug items (with the unit constraints)
    number_of_carts
):
    sorted_units = sorted(drug_items, key=lambda x: x[1], reverse=True)
    carts = [[] for _ in range(number_of_carts)]
    cart_weights = [0] * number_of_carts

    for unit, weight in sorted_units:
        min_cart_index = cart_weights.index(min(cart_weights))
        carts[min_cart_index].append((unit, weight))
        cart_weights[min_cart_index] += weight
    return carts,cart_weights

def best_fit_decreasing_algorithm(
  drug_items, # Updated drug items (with the unit constraints)
  number_of_carts
):
    sorted_units = sorted(drug_items, key=lambda x: x[1], reverse=True)
    carts = [[] for _ in range(number_of_carts)]
    cart_weights = [0] * number_of_carts

    for unit, weight in sorted_units:
        best_cart_index = -1
        min_remaining_space = float('inf')

        for i in range(number_of_carts):
            remaining_space = cart_weights[i] + weight
            if remaining_space < min_remaining_space:
                best_cart_index = i
                min_remaining_space = remaining_space

        if best_cart_index != -1:
            carts[best_cart_index].append((unit, weight))
            cart_weights[best_cart_index] += weight

    return carts, cart_weights

def optimize_cart_allocation(
    df, # Input DF with Drug Unit & Drug Count
    drug_unit_col, # drug unit col in df
    drug_count_col, # drug count col in df
    unit_constraint_dict, # drug unit combination constraint
    number_of_carts, # number of carts to distribute drug units
    algorithm # algorithm of choice
):
    drug_units = [str(x).strip() for x in df[drug_unit_col]]
    medication_count = [float(x) for x in df['Medication_Count'].tolist()]

    clean_unit_constraint_dict = {key: [x for x in value if x in drug_units] for key, value in unit_constraint_dict.items()}

    constrained_drug_items = {key: sum(medication_count[drug_units.index(x)] for x in value) for key, value in clean_unit_constraint_dict.items()}
    unconstrained_drug_items = [(x, medication_count[drug_units.index(x)]) for x in drug_units if all(x not in group for group in clean_unit_constraint_dict.values())]
    updated_drug_items = list(constrained_drug_items.items()) + unconstrained_drug_items

    if algorithm == 'greedy':
        carts, cart_weights = greedy_algorithm(updated_drug_items,number_of_carts)

    elif algorithm == 'best-fit decreasing':
        carts, cart_weights = best_fit_decreasing_algorithm(updated_drug_items,number_of_carts)

    cart_data = {}
    for i in range(number_of_carts):
        cart_data[f"Cart{i + 1}"] = [
            ", ".join([sub_item.strip() for item in carts[i] for sub_item in item[0].split('&')]), # Drug units as a comma-separated string
            cart_weights[i]  # Total weight of the cart
        ]

    df_optimized_cart = pd.DataFrame(cart_data, index=["Drug Units", "Cart Total Weight"])
    print(df_optimized_cart.T.reset_index().rename(columns={'index':'Cart Assignment'}))
    return df_optimized_cart

    elif algorithm == 'best-fit decreasing':
        carts, cart_weights = best_fit_decreasing_algorithm(updated_drug_items, number_of_carts)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    if carts is None or cart_weights is None:
        raise RuntimeError("Failed to generate carts and cart weights")

    cart_data = {}
    for i in range(number_of_carts):
        cart_data[f"Cart{i + 1}"] = [
            ", ".join([sub_item.strip() for item in carts[i] for sub_item in item[0].split('&')]), # Drug units as a comma-separated string
            cart_weights[i]  # Total weight of the cart
        ]

    df_optimized_cart = pd.DataFrame(cart_data, index=["Drug Units", "Cart Total Weight"])
    # print(df_optimized_cart.T.reset_index().rename(columns={'index':'Cart Assignment'}))
    return df_optimized_cart.T.reset_index().rename(columns={'index':'Cart Assignment'})





# df = pd.read_csv('/Users/andrewchen/Documents/optimize_drug_cart_project/daily_files/drug_medication_count_20241018.csv')
#
# unit_constraints_input = "[C,G], [B,F], [1B,1C], [1A,J,K,N,Z]"
# unit_constraints_input_clean = unit_constraints_input.replace(' ','')
# unit_constraints_input_clean = re.sub(r'(\b[^,\[\]]+\b)', r"'\1'", unit_constraints_input_clean)
# unit_constraints = {' & '.join(x):x for x in ast.literal_eval(unit_constraints_input_clean)}
#
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

