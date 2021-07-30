import streamlit as st

sidebar_expander = st.sidebar.beta_expander("Parameter Akuisisi!")
with sidebar_expander:
    st.slider("Bad layout slider 1", 0, 100, value=0)
    st.slider("Bad layout slider 2", 0, 100, value=(0,100))

st.sidebar.slider("Good layout slider")