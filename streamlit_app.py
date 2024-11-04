import streamlit as st
import pandas as pd
import ast
import re
from optimizer import *

# Streamlit App Title
st.title('Optimize Drug Cart Allocation')

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())

    # Select the column for drug unit
    drug_unit_col = st.selectbox("Select Drug Unit Column", df.columns)
    # Display all unique drug units
    unique_drug_units = sorted(df[drug_unit_col].unique())
    st.write(f"Unique Drug Units in {drug_unit_col}:")
    st.write(unique_drug_units)

    # Select the column for drug count
    drug_count_col = st.selectbox("Select Drug Count Column", df.columns)

    # Ensure the drug count column is of type float
    try:
        df[drug_count_col] = df[drug_count_col].astype(float)
    except ValueError:
        st.error(f"Cannot convert {drug_count_col} to float. Please check your data.")

    # Display the sum of all values in the drug count column
    total_drug_count = df[drug_count_col].sum()
    st.write(f"Total Sum of {drug_count_col}: {total_drug_count}")

    # User Input for Unit Constraints
    st.write("Adjust Unit Constraints:")
    unit_constraints_input = st.text_area(
        "Enter unit constraints in the format [A,B], [1C,1D,1E],...",
        value = "[A,B], [1C,1D,1E]"
    )

    unit_constraints_input_clean = unit_constraints_input.replace(' ','')
    unit_constraints_input_clean = re.sub(r'(\b[^,\[\]]+\b)', r"'\1'", unit_constraints_input_clean)
    unit_constraints = {' & '.join(x):x for x in ast.literal_eval(unit_constraints_input_clean)}

    # User Input for Number of Carts
    num_carts = st.number_input("Number of Carts", min_value=1, max_value=99999, value=1, step=1)

    # User Selection for the Optimization Algorithm
    algorithm = st.selectbox("Select Algorithm", ["greedy", "best-fit decreasing"])

    # Call the function to optimize cart allocation
    df_optimized_cart = optimize_cart_allocation(
        df,
        drug_unit_col=drug_unit_col,
        drug_count_col=drug_count_col,
        unit_constraint_dict=unit_constraints,
        number_of_carts=num_carts,
        algorithm=algorithm
    )

    # Display the Results
    st.write("Optimized Cart Allocation:")
    st.write(df_optimized_cart)

    # for i, cart in enumerate(carts):
    #     st.write(f"Cart {i + 1}: {cart}")
    # st.write("Cart Weights:", cart_weights)