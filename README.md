# Operation Nightfall: Industrial Predictive Maintenance

## 1. The Real-World Problem
In modern manufacturing (e.g., automotive assembly, semiconductor fabs, or chemical plants), **unplanned downtime** is the single biggest destroyer of profit. 

- **The Scenario**: A Critical Cooling Fan ($200 part) fails unexpectedly on a Friday afternoon.
- **The Consequence**: The entire production line halts. 
    - 50 workers are paid to stand idle.
    - Rush shipping for a replacement part costs $5,000.
    - 4 hours of lost production = $250,000 in missed revenue.
- **The Old Solution (Run-to-Failure)**: Wait for things to break, then fix them. **Cost: High.**
- **The "Safe" Solution (Preventive Maintenance)**: Replace *every* fan every 2 months, even if they are fine. **Cost: Medium (Wasteful).**

## 2. The Solution: Predictive Financial Modeling
This project does not just predict *if* a machine will fail. It builds a financial decision engine that tells stakeholders: **"Here is exactly how much money we save by fixing specific machines today."**

It bridges the gap between **Data Science metrics** (Accuracy, Recall) and **Business metrics** (ROI, Net Savings).

## 3. Tech Stack & Architecture
This project simulates a full industrial data pipeline:

### **Step 1: Data Engineering (SQL/SQLite)**
*   **Script**: `db_setup.py`
*   **Action**: Ingests raw sensor data (`ai4i2020.csv`) into a Relational Database.
*   **Business Logic**: Creates a SQL `cost_matrix` table to assign real dollar values to different failure modes (e.g., Power Failure is more expensive than Tool Wear).
*   **Baseline View**: Creates a SQL View to calculate the "Status Quo" cost—the money lost if we did nothing.

### **Step 2: Predictive Modeling (Python & Scikit-Learn)**
*   **Script**: `analysis.py`
*   **Action**: Connects to the SQL DB and trains a **Random Forest Classifier** on sensor readings (Torque, Temperature, RPM).
*   **Financial Engine**: 
    - Calculates the cost of a **False Positive** (Inspection cost: $150).
    - Calculates the cost of a **True Positive** (Maintenance cost: $300).
    - Calculates the cost of a **False Negative** (Failure cost: $1,000 - $5,000).

### **Step 3: Financial Reporting (Tableau)**
*   **Output**: `tableau_predictions.csv`
*   **Action**: A dashboard that visualizes the **Net Savings** and **ROI** of the predictive strategy compared to the run-to-failure baseline.

## 4. How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Database**:
   ```bash
   python db_setup.py
   ```
   *This creates `maintenance_data.db` and populates the SQL tables.*

3. **Run the Analysis Pipeline**:
   ```bash
   python analysis.py
   ```
   *This trains the model, calculates financials, and generates `tableau_predictions.csv`.*

4. **Visualize in Tableau**:
   - Open Tableau and connect to the generated `tableau_predictions.csv`.
   - Use the `Strategy_Cost` and `Unplanned_Failure_Cost` columns to build your ROI dashboard.

## 5. Key Results (Example)
- **Status Quo Cost**: $3.4M (Money lost to failures)
- **Predictive Strategy Cost**: $1.3M (Money spent on inspections/maintenance)
- **Net Savings**: **$2.1M**
- **ROI**: **~155%**