
import numpy as np
import pandas as pd

# ==========================================
# MEDICAL COST ANALYSIS SYSTEM
# ==========================================

# Load cleaned dataset
df = pd.read_csv("Medical_Cost_Prediction_Cleaned.csv")

# Convert numerical columns
numeric_cols = ["Age", "BMI", "Charges"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Clean missing values
df["Name"] = df["Name"].fillna("Unknown")
df["Sex"] = df["Sex"].fillna("Unknown")
df["Smoke"] = df["Smoke"].fillna("Unknown")

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def line():
    print("=" * 55)


def heading(title):
    print("\n")
    line()
    print(title.center(55))
    line()


def display_table(data):
    if data.empty:
        print("No data found!")
    else:
        print(data.to_string(index=False))


# ==========================================
# 1. TOTAL MEDICAL CHARGES
# ==========================================

def total_charges():

    heading("TOTAL MEDICAL CHARGES")

    total = df["Charges"].sum()

    print("Total Medical Charges: Rs.", round(total, 2))


# ==========================================
# 2. AVERAGE MEDICAL CHARGES
# ==========================================

def average_charges():

    heading("AVERAGE MEDICAL CHARGES")

    average = df["Charges"].mean()
    median = df["Charges"].median()

    print("Average Charges : Rs.", round(average, 2))
    print("Median Charges  : Rs.", round(median, 2))


# ==========================================
# 3. GENDER-WISE CHARGES
# ==========================================

def gender_analysis():

    heading("GENDER-WISE MEDICAL CHARGES")

    result = df.groupby("Sex").agg(
        Total_Patients=("Patient_ID", "count"),
        Total_Charges=("Charges", "sum"),
        Average_Charges=("Charges", "mean")
    ).reset_index()

    result = result.sort_values(
        by="Average_Charges", ascending=False
    )

    display_table(result.round(2))


# ==========================================
# 4. SMOKER VS NON-SMOKER ANALYSIS
# ==========================================

def smoking_analysis():

    heading("SMOKING-WISE MEDICAL CHARGES")

    result = df.groupby("Smoke").agg(
        Total_Patients=("Patient_ID", "count"),
        Total_Charges=("Charges", "sum"),
        Average_Charges=("Charges", "mean")
    ).reset_index()

    result = result.sort_values(
        by="Average_Charges", ascending=False
    )

    display_table(result.round(2))


# ==========================================
# 5. AGE-WISE MEDICAL CHARGES
# ==========================================

def age_analysis():

    heading("AGE-WISE MEDICAL CHARGES")

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[0, 18, 30, 45, 60, 100],
        labels=["0-18", "19-30", "31-45", "46-60", "60+"]
    )

    result = df.groupby(
        "Age_Group", observed=False
    ).agg(
        Total_Patients=("Patient_ID", "count"),
        Average_Charges=("Charges", "mean"),
        Total_Charges=("Charges", "sum")
    ).reset_index()

    display_table(result.round(2))


# ==========================================
# 6. HIGHEST MEDICAL CHARGES
# ==========================================

def highest_charges():

    heading("TOP 5 PATIENTS WITH HIGHEST CHARGES")

    result = df.nlargest(5, "Charges")

    display_table(
        result[["Patient_ID", "Name", "Age",
                "Sex", "Smoke", "Charges"]]
    )


# ==========================================
# 7. LOWEST MEDICAL CHARGES
# ==========================================

def lowest_charges():

    heading("TOP 5 PATIENTS WITH LOWEST CHARGES")

    result = df.nsmallest(5, "Charges")

    display_table(
        result[["Patient_ID", "Name", "Age",
                "Sex", "Smoke", "Charges"]]
    )


# ==========================================
# 8. BMI ANALYSIS
# ==========================================

def bmi_analysis():

    heading("BMI ANALYSIS")

    print("Average BMI:", round(df["BMI"].mean(), 2))
    print("Minimum BMI:", df["BMI"].min())
    print("Maximum BMI:", df["BMI"].max())

    print("\nBMI values above 100:")

    result = df[df["BMI"] > 100]

    if result.empty:
        print("No unusual BMI values found.")
    else:
        display_table(
            result[["Patient_ID", "Name", "BMI"]]
        )


# ==========================================
# 9. TOTAL PATIENTS
# ==========================================

def patient_count():

    heading("TOTAL PATIENT RECORDS")

    print("Total Patients:", len(df))
    print("Male Patients:", (df["Sex"] == "Male").sum())
    print("Female Patients:", (df["Sex"] == "Female").sum())
    print("Smokers:", (df["Smoke"] == "Yes").sum())
    print("Non-Smokers:", (df["Smoke"] == "No").sum())


# ==========================================
# 10. SEARCH PATIENT
# ==========================================

def search_patient():

    heading("SEARCH PATIENT DETAILS")

    patient_id = input("Enter Patient ID: ").strip()

    result = df[
        df["Patient_ID"].astype(str).str.upper()
        == patient_id.upper()
    ]

    if result.empty:
        print("Patient not found!")
    else:
        display_table(result)


# ==========================================
# 11. COMPARE TWO PATIENTS
# ==========================================

def compare_patients():

    heading("PATIENT COMPARISON")

    first = input("Enter First Patient ID: ").strip()
    second = input("Enter Second Patient ID: ").strip()

    ids = [first.upper(), second.upper()]

    result = df[
        df["Patient_ID"].astype(str).str.upper().isin(ids)
    ]

    if result["Patient_ID"].nunique() != 2:
        print("Please enter two valid Patient IDs.")
        return

    display_table(
        result[["Patient_ID", "Name", "Age",
                "Sex", "BMI", "Smoke", "Charges"]]
    )


# ==========================================
# MAIN MENU
# ==========================================

def main_menu():

    while True:

        heading("MEDICAL COST ANALYSIS SYSTEM")

        print("1.  Total Medical Charges")
        print("2.  Average Medical Charges")
        print("3.  Gender-wise Charges Analysis")
        print("4.  Smoker vs Non-Smoker Analysis")
        print("5.  Age-wise Medical Charges")
        print("6.  Highest Medical Charges")
        print("7.  Lowest Medical Charges")
        print("8.  BMI Analysis")
        print("9.  Total Patients Count")
        print("10. Search Patient Details")
        print("11. Compare Two Patients")
        print("12. Exit")

        line()

        choice = input("Enter your choice (1-12): ").strip()

        if choice == "1":
            total_charges()

        elif choice == "2":
            average_charges()

        elif choice == "3":
            gender_analysis()

        elif choice == "4":
            smoking_analysis()

        elif choice == "5":
            age_analysis()

        elif choice == "6":
            highest_charges()

        elif choice == "7":
            lowest_charges()

        elif choice == "8":
            bmi_analysis()

        elif choice == "9":
            patient_count()

        elif choice == "10":
            search_patient()

        elif choice == "11":
            compare_patients()

        elif choice == "12":
            heading("THANK YOU")
            print("Exiting Medical Cost Analysis System...")
            break

        else:
            print("Invalid choice! Enter 1 to 12.")

        input("\nPress Enter to return to Main Menu...")


# ==========================================
# PROGRAM EXECUTION
# ==========================================

if __name__ == "__main__":

    print("\nLoading Medical Cost Analysis System...")

    if df.empty:
        print("No patient records found!")

    else:
        print("Cleaned Dataset Loaded Successfully!")
        print("Total Records:", len(df))

        main_menu()
