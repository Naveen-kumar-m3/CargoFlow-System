# CargoFlow System 📦

CargoFlow System is a web-based logistics analytics platform designed to track cargo movement, analyze shipment performance, and support data-driven decision-making in supply chain operations.

---

## 🎯 Project Objective
The objective of this project is to build a modular and scalable logistics dashboard that enables operational teams to visualize cargo flow, monitor key metrics, and generate analytical insights from structured logistics data.

---

## 🚀 Key Features
- Upload logistics data (Excel / CSV)
- Dynamic filtering by logistics partner, location, payment mode, and date range
- Cargo quantity and invoice value analysis
- Interactive dashboards and charts
- Export filtered data for reporting

---

## 🛠️ Tech Stack
- **Frontend / UI**: Streamlit
- **Backend Logic**: Python
- **Data Processing**: Pandas
- **Visualization**: Plotly

---

## 📂 Project Structure
CargoFlow-System/
├── app.py
├── data/
│ └── March.xls
├── requirements.txt
├── runtime.txt
├── Dockerfile
└── README.md


---

## ▶️ How to Run the Project
```bash
pip install -r requirements.txt
streamlit run app.py


The dashboard follows a top-down information hierarchy:

Operational Overview (KPIs)
Displays total trips, total cargo (MT), and invoice value.

Transporter Insights
Visualizes cargo quantity and invoice value by logistics partner.

Location & Payment Insights
Shows cargo distribution by loading location and payment mode.

Vehicle Performance
Highlights top vehicles by transported cargo.

Detailed Data (Expandable Section)
Provides access to filtered data tables and downloadable reports.

📌 Use Case

CargoFlow System can be used by:

Logistics operations teams

Supply chain analysts

Transport management teams

to monitor shipment trends, evaluate transporter performance, and support operational decision-making.
