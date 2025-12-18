import streamlit as st
import plotly.express as px
import pandas as pd
import warnings


def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel("data/March.xls")
    df.columns = df.columns.str.strip()
    return df


def find_quantity_column(df):
    for col in df.columns:
        if "QNT" in col.upper() and "KG" in col.upper():
            return col
    return None


def filter_data(df, transporter, loading_location, inv_location, payment_by, date_col, start_date, end_date):
    return df[
        (df["TRANSPORTER"].isin(transporter) if transporter else True) &
        (df["LOADING LOCATION"].isin(loading_location) if loading_location else True) &
        (df["INV LOCATION"].isin(inv_location) if inv_location else True) &
        (df["PAYMENT BY"].isin(payment_by) if payment_by else True) &
        (df[date_col] >= pd.to_datetime(start_date)) &
        (df[date_col] <= pd.to_datetime(end_date))
    ]


warnings.filterwarnings("ignore")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CargoFlow System",
    page_icon="📦",
    layout="wide"
)

st.title("📦 CargoFlow System")
st.subheader("Logistics & Cargo Analytics Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ---------------- DATA LOADING ----------------
fl = st.file_uploader("📂 Upload Logistics File", type=["csv", "xlsx", "xls"])

df = load_data(fl)
required_columns = [
    "TRANSPORTER",
    "LOADING LOCATION",
    "INV LOCATION",
    "PAYMENT BY",
    "INV -VALUE",
    "VEHICLE NUMBER"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {', '.join(missing_cols)}")
    st.stop()
if fl is not None:
    st.success(f"File '{fl.name}' uploaded successfully")



# ---------------- FIND REQUIRED COLUMNS ----------------
# Quantity column
quantity_col = find_quantity_column(df)

if quantity_col is None:
    st.error("Quantity column (KG) not found in dataset.")
    st.stop()

if quantity_col is None:
    st.error("Quantity column (KG) not found in dataset.")
    st.stop()

# Date column
date_columns = [col for col in df.columns if "DATE" in col.upper()]
if not date_columns:
    st.error("Date column not found in dataset.")
    st.stop()

selected_date_column = date_columns[0]
df[selected_date_column] = pd.to_datetime(df[selected_date_column])

# ---------------- SIDEBAR FILTERS ----------------
with st.sidebar:
    st.subheader("🔍 Filter Selection")
    st.markdown("---")

    transporter = st.multiselect(
        "Logistics Partner",
        df["TRANSPORTER"].unique()
    )

    loading_location = st.multiselect(
        "Loading Location",
        df["LOADING LOCATION"].unique()
    )

    inv_location = st.multiselect(
        "Invoice Location",
        df["INV LOCATION"].unique()
    )

    payment_by = st.multiselect(
        "Payment Mode",
        df["PAYMENT BY"].unique()
    )

# Date range
col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input("Start Date", df[selected_date_column].min())
with col2:
    date2 = st.date_input("End Date", df[selected_date_column].max())

# ---------------- FILTER DATA ----------------
filtered_df = filter_data(
    df,
    transporter,
    loading_location,
    inv_location,
    payment_by,
    selected_date_column,
    date1,
    date2
)


# Derived column
filtered_df = filtered_df.copy()
filtered_df["INV -QNT-MT"] = filtered_df[quantity_col] / 1000
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()


# ---------------- KPI SECTION ----------------
st.markdown("## 📊 Operational Overview")

k1, k2, k3 = st.columns(3)
k1.metric("Total Trips", f"{filtered_df.shape[0]:,}")
k2.metric("Total Cargo", f"{filtered_df['INV -QNT-MT'].sum():,.2f} MT")
k3.metric("Total Invoice Value", f"₹{filtered_df['INV -VALUE'].sum():,.2f}")

st.markdown("---")

# ---------------- TRANSPORTER INSIGHTS ----------------
transporter_summary = (
    filtered_df
    .groupby("TRANSPORTER")
    .agg({
        "INV -QNT-MT": "sum",
        "INV -VALUE": "sum"
    })
    .reset_index()
)

fig_transporter_quantity = px.pie(
    transporter_summary,
    names="TRANSPORTER",
    values="INV -QNT-MT",
    title="Transporter Distribution by Quantity (MT)"
)

fig_transporter_amount = px.pie(
    transporter_summary,
    names="TRANSPORTER",
    values="INV -VALUE",
    title="Transporter Distribution by Invoice Value"
)

st.markdown("## 🚚 Transporter Insights")
c1, c2 = st.columns(2)
c1.plotly_chart(fig_transporter_quantity, use_container_width=True)
c2.plotly_chart(fig_transporter_amount, use_container_width=True)

st.markdown("---")

# ---------------- LOCATION & PAYMENT ----------------
fig_loading_location = px.pie(
    filtered_df,
    names="LOADING LOCATION",
    title="Loading Location Distribution"
)

fig_payment_by = px.pie(
    filtered_df,
    names="PAYMENT BY",
    title="Payment Mode Distribution"
)

st.markdown("## 📍 Location & Payment Insights")
c1, c2 = st.columns(2)
c1.plotly_chart(fig_loading_location, use_container_width=True)
c2.plotly_chart(fig_payment_by, use_container_width=True)

st.markdown("---")

# ---------------- VEHICLE PERFORMANCE ----------------
top_vehicles = (
    filtered_df
    .groupby("VEHICLE NUMBER")["INV -QNT-MT"]
    .sum()
    .reset_index()
    .sort_values(by="INV -QNT-MT", ascending=False)
    .head(5)
)

fig_top_vehicles = px.bar(
    top_vehicles,
    x="VEHICLE NUMBER",
    y="INV -QNT-MT",
    title="Top 5 Vehicles by Cargo Transported (MT)"
)

st.markdown("## 🏆 Vehicle Performance")
c1, c2 = st.columns(2)
c1.plotly_chart(fig_top_vehicles, use_container_width=True)
c2.write(top_vehicles)

# ---------------- EXPANDABLE DETAILS ----------------
with st.expander("📄 View Detailed Data & Reports"):
    st.subheader("Filtered Dataset")
    st.write(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Data",
        data=csv,
        file_name="Filtered_Data.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2025 CargoFlow System | Logistics Analytics Platform")
