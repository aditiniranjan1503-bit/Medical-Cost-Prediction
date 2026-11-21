import numpy as np
import pandas as pd

# Load the messy Medical Cost Prediction dataset
df = pd.read_csv("Medical_Cost_Prediction_Messy.csv")
print("Original data:")
print(df.head(10))
print("Original shape:", df.shape)

# Work on a separate copy
df = df.copy()

# 1. Remove duplicate Patient_ID values
df = df.drop_duplicates(subset=["Patient_ID"], keep="first")

# 2. Clean Name (remove extra spaces and use Title Case)
df["Name"] = df["Name"].astype("string").str.strip().str.title()

# 3. Clean and standardize Sex
df["Sex"] = df["Sex"].astype("string").str.strip().str.upper()
sex_map = {
    "MALE": "Male",
    "M": "Male",
    "FEMALE": "Female",
    "F": "Female"
}
df["Sex"] = df["Sex"].map(sex_map).fillna("Unknown")

# 4. Clean Smoke values (Yes/No in a consistent format)
df["Smoke"] = df["Smoke"].astype("string").str.strip().str.upper()
smoke_map = {"YES": "Yes", "NO": "No"}
df["Smoke"] = df["Smoke"].map(smoke_map).fillna("Unknown")

# 5. Clean Age and convert it into numeric values
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
median_age = df["Age"].median()
df["Age"] = df["Age"].fillna(median_age).astype(int)

# 6. Clean BMI and fill missing values with median
df["BMI"] = pd.to_numeric(df["BMI"], errors="coerce")
median_bmi = df["BMI"].median()
df["BMI"] = df["BMI"].fillna(median_bmi)

# Show unusual BMI values for manual checking; do not change them automatically
print("BMI values above 100:")
print(df.loc[df["BMI"] > 100, ["Patient_ID", "BMI"]])

# 7. Clean Charges (remove commas/spaces and convert to numeric)
df["Charges"] = (
    df["Charges"]
    .astype("string")
    .str.strip()
    .str.replace(",", "", regex=False)
)
df["Charges"] = pd.to_numeric(df["Charges"], errors="coerce")

# Charges is the target column. Remove rows where it is missing/invalid.
df = df.dropna(subset=["Charges"])

# 8. Display final cleaned data and save it
print("\\nCleaned data:")
print(df.head(10))
print("\\nMissing values:")
print(df.isnull().sum())
print("Final shape:", df.shape)

df.to_csv("Medical_Cost_Prediction_Cleaned.csv", index=False)
print("Cleaned file saved successfully!")
