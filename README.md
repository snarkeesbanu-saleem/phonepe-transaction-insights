# PhonePe Pulse Transaction & User Insights Dashboard

An interactive, live geo-visualization and forecasting dashboard for exploring PhonePe Pulse datasets in India (covering 2018–2022). 

**Check out the live website here:**
👉 **[phonepe-transaction-insights.streamlit.app](https://phonepe-transaction-insights-t3i3cass9ukdxqvv9xjftm.streamlit.app/)**

---

## 🚀 Key Features

The dashboard is built entirely in Python and features **over 10 interactive filter options** (Year, Quarter, State, Theme, Time Range, Metric types, and District selectors) to query and visualize transaction and user trends:

1. **🌐 Transaction Analytics & Geographic Maps**
   * **State-level Choropleth Map**: Real-time India choropleth map plotting transaction amounts and volumes across states using custom GeoJSON boundaries.
   * **Category Share**: A dynamic donut chart illustrating transaction distributions (e.g., Peer-to-peer, Merchant payments, Financial services).
   * **Year-over-Year (YoY) Growth**: Automatic calculation and bar chart comparison of annual growth metrics.

2. **👥 User & Device Insights**
   * **User Heatmap**: Dynamic geographic representation of registered users and app opening frequency.
   * **Mobile Brand Market Share**: Detailed market analytics showing device preferences (Xiaomi, Samsung, Vivo, Oppo, Apple, etc.) per state, year, and quarter.

3. **🔮 Machine Learning Trend Forecasting**
   * Integrates a **Scikit-Learn Linear Regression model** trained on historical multi-quarter ranges that predicts and plots projected transaction counts and values for upcoming quarters.

4. **🔍 Regional Pincode & District Deep-Dive**
   * Detailed drill-down tables and rankings showing the **Top 10 Districts** and **Top 10 Pincodes** based on transaction activity and registered user bases.

5. **🎨 Premium Aesthetic Themes**
   * Choose from four customized styling themes in the sidebar:
     * **Default**: Clean slate layout with Light and Dark modes.
     * **Neon**: High-contrast, dark mode interface with vibrant green/cyan metrics.
     * **Cyan**: Sleek deep-sea dark layout with bright cyan highlights.
     * **Sunset**: Warm twilight aesthetic featuring sunset red and purple accents.

---

## 🛠️ Architecture & Technology Stack

The project has been optimized to run **100% database-free** (eliminating MySQL/PostgreSQL dependencies). This allows it to load instantly, run fully offline, and deploy seamlessly to container hosts like Streamlit Cloud or Render.

* **Core Language:** Python
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express (Interactive charts & maps)
* **Frontend Framework:** Streamlit (Layout, custom CSS themes, and components)
* **Machine Learning:** Scikit-Learn (Linear Regression forecasting)

---

## 📂 Data Pipeline & Extraction

The repository includes a data compiler script [extract_data.py](extract_data.py) that automatically crawls, parses, and cleanses the raw JSON files from the official PhonePe Pulse GitHub repository:
* **Source Path:** `data/` directory (parsed locally)
* **Output Path:** Compiles raw data into 7 relation-mapped CSV files loaded by `app.py`.

---

## 💻 Installation & Running Locally

Follow these steps to run the project on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/snarkeesbanu-saleem/phonepe-transaction-insights.git
   cd phonepe-transaction-insights
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the raw data (optional - CSVs are already included for instant use):**
   ```bash
   python extract_data.py
   ```

4. **Launch the Streamlit app:**
   ```bash
   python -m streamlit run app.py
   ```
