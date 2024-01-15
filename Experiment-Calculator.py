import streamlit as st
import numpy as np
from scipy.stats import binom_test

def calculate_power(base_conversion_rate, daily_entrants_per_variant, num_days):
    # Assuming a two-sided test and a significance level of 0.05
    alpha = 0.05

    # Convert base conversion rate to the corresponding success probability
    p_null = base_conversion_rate
    p_alt = base_conversion_rate + (daily_entrants_per_variant / 100)

    # Calculate the number of successes needed in the alternative hypothesis
    n_alt = daily_entrants_per_variant * num_days

    # Calculate the power of the test
    power = 1 - binom_test(n_alt, n=n_alt, p=p_null, alternative='less')

    return power

def main():
    st.title("Power of A/B Test Calculator")

    base_conversion_rate = st.number_input("Base Conversion Rate (%)", min_value=0.0, max_value=100.0, value=10.0)
    daily_entrants_per_variant = st.number_input("Daily Entrants per Variant", min_value=0, step=1, value=100)
    num_days = st.number_input("Number of Days", min_value=1, step=1, value=7)

    if st.button("Calculate Power"):
        power = calculate_power(base_conversion_rate / 100, daily_entrants_per_variant, num_days)
        st.success(f"The power of the test is: {power:.4f}")

if __name__ == "__main__":
    main()
