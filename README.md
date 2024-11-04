Optimize Drug Cart

An application for optimizing the allocation of drugs into carts using different algorithms. This project uses Python and Streamlit to provide an interactive interface for optimizing drug distribution based on provided constraints.


Overview

The Optimize Drug Cart project is designed to streamline the allocation of medications into a specified number of carts while considering constraints and different optimization strategies. The application provides an intuitive interface built with Streamlit, allowing users to upload drug data, define constraints, and choose an optimization algorithm.

Features

File Upload: Upload your medication data in CSV format.

Interactive Selection: Choose drug unit and count columns dynamically from the uploaded file.

Custom Constraints: Specify drug unit constraints to group medications.

Optimization Algorithms: Use either a "Greedy" or "Best-Fit Decreasing" algorithm to allocate medications.

Results Visualization: View optimized cart assignments with total weights for each cart.

Installation

Prerequisites
Python 3.8 or higher
pip for package management

Steps

Clone the repository:

git clone https://github.com/andrewchen81/optimize-drug-cart.git
cd optimize-drug-cart

Install the required dependencies:

pip install -r requirements.txt


Run the Streamlit app

streamlit run streamlit_app.py


