import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import numpy as np

DB_NAME = "maintenance_data.db"
MAINTENANCE_COST = 300  
INSPECTION_COST = 150   

def load_data():
    conn = sqlite3.connect(DB_NAME)
    
    query = "SELECT * FROM sensor_data"
    df = pd.read_sql(query, conn)
    
    cost_query = "SELECT * FROM baseline_costs"
    costs_df = pd.read_sql(cost_query, conn)
    
    conn.close()
    
    df = df.merge(costs_df[['UDI', 'Unplanned_Failure_Cost']], on='UDI')
    
    return df

df = load_data()

test_size = 0.2
n_estimators = 100

feature_cols = ['Air_temperature_K', 'Process_temperature_K', 'Rotational_speed_rpm', 'Torque_Nm', 'Tool_wear_min']
target_col = 'Machine_failure'

X = df[feature_cols]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

test_indices = X_test.index
test_data = df.loc[test_indices].copy()
test_data['Prediction'] = y_pred

def calculate_financials(row):
    actual = row['Machine_failure']
    pred = row['Prediction']
    fail_cost = row['Unplanned_Failure_Cost']
    
    if actual == 1 and pred == 1:
        return MAINTENANCE_COST, "Maintenance (TP)"
        
    elif actual == 0 and pred == 1:
        return INSPECTION_COST, "Inspection (FP)"
        
    elif actual == 1 and pred == 0:
        return fail_cost, "Missed Failure (FN)"
        
    else:
        return 0, "Business as Usual (TN)"

test_data[['Strategy_Cost', 'Action']] = test_data.apply(
    lambda x: pd.Series(calculate_financials(x)), axis=1
)

print("Exporting data for Tableau...")
test_data.to_csv('tableau_predictions.csv', index=False)

importances = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)
importances.to_csv('tableau_feature_importance.csv', index=False)

print("Done")