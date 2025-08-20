import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def apply_impeller_trim(head, trim_ratio):
    return head * (trim_ratio ** 2)

def apply_viscosity_correction(head, eff, factor):
    return head * factor, eff * factor

def calculate_power(flow, head, eff, rho=1000, g=9.81):
    return (rho * g * flow * head) / (eff * 1000)

st.set_page_config(page_title="Pump Curve Analyzer", layout="wide")
st.title("💧 Pump Curve Analyzer")
st.markdown("### Upload, Analyze and Adjust Pump Performance")

tab1, tab2, tab3, tab4 = st.tabs(["📂 Upload Data", "📈 Base Curve", "⚙️ Adjustments", "⬇️ Export"])

with tab1:
    st.subheader("Upload Pump Data (CSV)")
    uploaded_file = st.file_uploader("Upload pump curve CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
    else:
        st.info("No file uploaded. Using example dataset.")
        flow = np.linspace(0.01, 0.1, 10)
        head = 50 - 200 * (flow - 0.05) ** 2
        eff = 0.7 - 10 * (flow - 0.05) ** 2
        df = pd.DataFrame({"Flow": flow, "Head": head, "Efficiency": eff})

with tab2:
    st.subheader("Pump Performance Curve (Original)")
    fig, ax = plt.subplots()
    ax.plot(df["Flow"], df["Head"], label="Head Curve", color="b")
    ax.set_xlabel("Flow [m3/s]")
    ax.set_ylabel("Head [m]", color="b")
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.plot(df["Flow"], df["Efficiency"]*100, label="Efficiency", color="g")
    ax2.set_ylabel("Efficiency [%]", color="g")
    st.pyplot(fig)

with tab3:
    st.subheader("Adjust Pump Performance")
    trim_ratio = st.slider("Impeller Trim Ratio", 0.5, 1.0, 1.0, 0.05)
    visc_factor = st.slider("Viscosity Correction Factor", 0.5, 1.0, 1.0, 0.05)
    df_adj = df.copy()
    df_adj["Head"] = apply_impeller_trim(df["Head"], trim_ratio)
    df_adj["Head"], df_adj["Efficiency"] = apply_viscosity_correction(df_adj["Head"], df["Efficiency"], visc_factor)
    df_adj["Power (kW)"] = calculate_power(df["Flow"], df_adj["Head"], df_adj["Efficiency"])
    fig, ax = plt.subplots()
    ax.plot(df["Flow"], df["Head"], label="Original Head", color="b", linestyle="--")
    ax.plot(df_adj["Flow"], df_adj["Head"], label="Adjusted Head", color="r")
    ax.set_xlabel("Flow [m3/s]")
    ax.set_ylabel("Head [m]")
    ax.grid(True)
    ax.legend()
    ax2 = ax.twinx()
    ax2.plot(df_adj["Flow"], df_adj["Efficiency"]*100, label="Adjusted Efficiency", color="g")
    ax2.set_ylabel("Efficiency [%]", color="g")
    st.pyplot(fig)
    st.dataframe(df_adj)

with tab4:
    st.subheader("Download Results")
    csv = df_adj.to_csv(index=False).encode("utf-8")
    st.download_button("Download Adjusted Curve CSV", csv, "adjusted_pump_curve.csv", "text/csv")
