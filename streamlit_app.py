import streamlit as st
import pandas as pd
from optimizer import *

# Streamlit App Title
st.title('Optimize Drug Cart Allocation')

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())

    # User Input for Unit Constraints
    st.write("Adjust Unit Constraints:")
    unit_constraints_input = st.text_area(
        "Enter unit constraints in the format {'C+G': ['C', 'G'], 'B+F': ['B', 'F'], ...}",
        value="{'C+G': ['C', 'G'], 'B+F': ['B', 'F'], '1B+1C': ['1B', '1C'], '1A+J+K+N+Z': ['1A', 'J', 'K', 'N', 'Z']}"
    )
    unit_constraints = eval(unit_constraints_input)

    # User Input for Number of Carts
    num_carts = st.number_input("Number of Carts", min_value=1, max_value=9999, value=6, step=1)

    # Call the function to optimize cart allocation
    carts, cart_weights = optimize_cart_allocation(
        df,
        drug_unit_col='Drug Unit',
        drug_count_col='Medication_Count',
        unit_constraint_dict=unit_constraints,
        number_of_carts=num_carts
    )

    # Display the Results
    st.write("Optimized Cart Allocation:")
    for i, cart in enumerate(carts):
        st.write(f"Cart {i + 1}: {cart}")
    st.write("Cart Weights:", cart_weights)