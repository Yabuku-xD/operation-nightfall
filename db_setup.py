import pandas as pd
import sqlite3
import os

DB_NAME = "maintenance_data.db"
CSV_FILE = "ai4i2020.csv"

def setup_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    print("Loading CSV...")
    df = pd.read_csv(CSV_FILE)
    
    df.columns = [c.replace('[', '').replace(']', '').replace(' ', '_') for c in df.columns]
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Creating 'sensor_data' table...")
    df.to_sql('sensor_data', conn, if_exists='replace', index=False)

    print("Creating 'cost_matrix' table...")
    cost_data = {
        'Failure_Type': ['TWF', 'HDF', 'PWF', 'OSF', 'RNF'],
        'Failure_Cost': [2000, 4000, 5000, 6000, 1000],
        'Description': ['Tool Wear Failure', 'Heat Dissipation Failure', 'Power Failure', 'Overstrain Failure', 'Random Failure']
    }
    cost_df = pd.read_json(pd.DataFrame(cost_data).to_json()) 
    cost_df.to_sql('cost_matrix', conn, if_exists='replace', index=False)

    print("Creating SQL Views...")
    create_view_query = """
    CREATE VIEW baseline_costs AS
    SELECT 
        sd.UDI,
        sd.Product_ID,
        sd.Machine_failure,
        CASE 
            WHEN sd.TWF = 1 THEN (SELECT Failure_Cost FROM cost_matrix WHERE Failure_Type = 'TWF')
            WHEN sd.HDF = 1 THEN (SELECT Failure_Cost FROM cost_matrix WHERE Failure_Type = 'HDF')
            WHEN sd.PWF = 1 THEN (SELECT Failure_Cost FROM cost_matrix WHERE Failure_Type = 'PWF')
            WHEN sd.OSF = 1 THEN (SELECT Failure_Cost FROM cost_matrix WHERE Failure_Type = 'OSF')
            WHEN sd.RNF = 1 THEN (SELECT Failure_Cost FROM cost_matrix WHERE Failure_Type = 'RNF')
            ELSE 0
        END as Unplanned_Failure_Cost
    FROM sensor_data sd;
    """
    cursor.execute(create_view_query)
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
