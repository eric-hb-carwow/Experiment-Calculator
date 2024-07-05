import streamlit as st
import numpy as np
from scipy.stats import norm
import math

def get_sample_size_with_power(mu_1, std_1, mde, is_absolute_mde=False, alpha=0.05, beta = 0.2):
    # from https://towardsdatascience.com/probing-into-minimum-sample-size-formula-derivation-and-usage-8db9a556280b
    if is_absolute_mde:
        # Absolute MDE
        dmin = mde
    else: # we always use relative at carwow
        # Relative MDE
        dmin = mu_1*mde

    stat_power = 1-beta

    # Calculate the minimum required sample size 
    n = np.ceil(
            2*(pow(norm.ppf(1-alpha/2)+norm.ppf(stat_power),2))*pow(std_1,2) # Numerator        
        / pow(dmin,2) # Denominator
        )
    
    return n


def show_sample_size():
    st.title("Sample Size Calculator")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        base_conversion_rate = st.number_input("Base conversion rate (%)", min_value=0.0, max_value=100.0, value=10.0)
    with col2:
        daily_entrants = st.number_input("Daily entrants", min_value=0, step=1, value=1000)
    with col3:
        num_variants = st.number_input("Number of test groups", min_value=2, step=1, value=2)
    with col4:
        mde = st.number_input("MDE (%)", min_value=0, step=1, value=5)
    
    std_1 = math.sqrt((base_conversion_rate/100)*(1-base_conversion_rate/100))

    if st.button("Calculate sample size"):
        sample_size = get_sample_size_with_power(base_conversion_rate / 100, std_1, mde / 100)
        days_to_run = math.ceil(sample_size/(daily_entrants/num_variants))
        st.success(f"The required number of days for the test to be powered is: {days_to_run}")


def main():
    show_sample_size()


if __name__ == "__main__":
    # remove the + and - buttons from number inputs
    st.markdown("""
        <style>
            button.step-up {display: none;}
            button.step-down {display: none;}
            div[data-baseweb] {border-radius: 4px;}
        </style>""",
        unsafe_allow_html=True)
    main()
