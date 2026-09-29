# ============================================================
# RED & WHITE SKILL EDUCATION - DATA ANALYSIS SET B
# Customer Support Quality Analysis
#
# Python Module
# ============================================================

# ------------------------------------------------------------
# STEP 1: IMPORT LIBRARIES
# ------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ------------------------------------------------------------
# STEP 2: FIND THE PROJECT ROOT FOLDER
# ------------------------------------------------------------

# __file__ means this analysis.py file.
# parents[1] means go one folder up from "python"
# and reach the main project folder.

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------
# STEP 3: CREATE FILE PATHS
# ------------------------------------------------------------

# Location of input CSV files
tickets_path = ROOT / "data" / "raw" / "tickets.csv"
teams_path = ROOT / "data" / "raw" / "teams.csv"

# Location of output folder
output_path = ROOT / "outputs"

# Create outputs folder if it does not already exist
output_path.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# STEP 4: LOAD THE CSV FILES
# ------------------------------------------------------------

print("\n========================================")
print("STEP 1 - LOADING DATA")
print("========================================")

tickets = pd.read_csv(tickets_path)
teams = pd.read_csv(teams_path)

print("\nTickets data loaded successfully.")
print("Teams data loaded successfully.")


# ------------------------------------------------------------
# STEP 5: DISPLAY ORIGINAL DATA INFORMATION
# ------------------------------------------------------------

print("\n========================================")
print("STEP 2 - ORIGINAL DATA")
print("========================================")

print("\nTickets:")
print(tickets)

print("\nTeams:")
print(teams)

print("\nNumber of ticket rows before cleaning:", len(tickets))
print("Number of team rows:", len(teams))


# ------------------------------------------------------------
# STEP 6: CHECK DATA TYPES
# ------------------------------------------------------------

print("\n========================================")
print("STEP 3 - CHECK DATA TYPES")
print("========================================")

print("\nTickets data types:")
print(tickets.dtypes)

print("\nTeams data types:")
print(teams.dtypes)


# ------------------------------------------------------------
# STEP 7: CONVERT NUMERIC COLUMNS
# ------------------------------------------------------------

# resolution_hours must be numeric
tickets["resolution_hours"] = pd.to_numeric(
    tickets["resolution_hours"],
    errors="coerce"
)

# satisfaction must be numeric
tickets["satisfaction"] = pd.to_numeric(
    tickets["satisfaction"],
    errors="coerce"
)

print("\nNumeric columns confirmed.")


# ------------------------------------------------------------
# STEP 8: CHECK FOR EXACT DUPLICATES
# ------------------------------------------------------------

print("\n========================================")
print("STEP 4 - CHECK DUPLICATES")
print("========================================")

duplicate_count = tickets.duplicated().sum()

print("Number of exact duplicate rows:", duplicate_count)

if duplicate_count > 0:
    print("\nDuplicate rows found:")
    print(tickets[tickets.duplicated(keep=False)])


# ------------------------------------------------------------
# STEP 9: REMOVE EXACT DUPLICATE
# ------------------------------------------------------------

# The exam data contains one exact duplicate.
# drop_duplicates() keeps the first copy.

tickets = tickets.drop_duplicates().copy()

print("\nRows after removing duplicates:", len(tickets))


# ------------------------------------------------------------
# STEP 10: CHECK THAT WE HAVE EXACTLY 12 CLEAN RECORDS
# ------------------------------------------------------------

print("\n========================================")
print("STEP 5 - CLEAN DATA CHECK")
print("========================================")

if len(tickets) == 12:
    print("SUCCESS: Exactly 12 clean ticket records found.")
else:
    print("WARNING: Expected 12 rows, but found", len(tickets))


# ------------------------------------------------------------
# STEP 11: MERGE TICKETS WITH TEAMS
# ------------------------------------------------------------

print("\n========================================")
print("STEP 6 - MERGE DATA")
print("========================================")

# team_id is the common column.
#
# tickets = many records
# teams = one record for each team
#
# Therefore this is a many-to-one merge.
#
# how="left" keeps all ticket records.

merged = tickets.merge(
    teams,
    on="team_id",
    how="left",
    validate="many_to_one"
)


print("\nMerged data:")
print(merged)


# ------------------------------------------------------------
# STEP 12: VERIFY MERGE
# ------------------------------------------------------------

print("\n========================================")
print("STEP 7 - MERGE VALIDATION")
print("========================================")

print("Number of rows after merge:", len(merged))

# There should still be exactly 12 rows
if len(merged) == 12:
    print("SUCCESS: Merge contains exactly 12 rows.")
else:
    print("WARNING: Merge row count is not 12.")


# Check whether any department values are missing
unmatched_departments = merged["department"].isna().sum()

print("Unmatched department values:", unmatched_departments)

if unmatched_departments == 0:
    print("SUCCESS: All team IDs matched with the teams table.")
else:
    print("WARNING: Some team IDs did not match.")


# ------------------------------------------------------------
# STEP 13: CREATE SLA BREACH FLAG
# ------------------------------------------------------------

print("\n========================================")
print("STEP 8 - SLA BREACH FLAG")
print("========================================")

# SLA rule:
#
# resolution_hours > 24  --> breach = 1
# resolution_hours <= 24 --> breach = 0
#
# Exactly 24 hours is NOT a breach.

merged["breach_flag"] = (
    merged["resolution_hours"] > 24
).astype(int)

print("\nData with breach_flag:")
print(
    merged[
        [
            "ticket_id",
            "resolution_hours",
            "breach_flag"
        ]
    ]
)


# ------------------------------------------------------------
# STEP 14: CHECK TOTAL BREACHES
# ------------------------------------------------------------

total_tickets = len(merged)

total_breaches = merged["breach_flag"].sum()

overall_breach_rate = (
    total_breaches / total_tickets
) * 100


print("\n========================================")
print("STEP 9 - OVERALL SLA PERFORMANCE")
print("========================================")

print("Total tickets:", total_tickets)
print("Total breached tickets:", total_breaches)
print("Overall SLA breach rate: {:.2f}%".format(
    overall_breach_rate
))


# ------------------------------------------------------------
# STEP 15: DEPARTMENT SUMMARY
# ------------------------------------------------------------

print("\n========================================")
print("STEP 10 - DEPARTMENT SUMMARY")
print("========================================")

# Group data by department.
#
# total_tickets:
# number of tickets in each department
#
# breached_tickets:
# number of tickets where breach_flag = 1

department_summary = (
    merged
    .groupby("department", as_index=False)
    .agg(
        total_tickets=("ticket_id", "count"),
        breached_tickets=("breach_flag", "sum")
    )
)

# Calculate SLA breach rate
department_summary["sla_breach_rate"] = (
    department_summary["breached_tickets"]
    / department_summary["total_tickets"]
) * 100


# Round the rate to 2 decimal places
department_summary["sla_breach_rate"] = (
    department_summary["sla_breach_rate"].round(2)
)


print("\nDepartment summary:")
print(department_summary)


# ------------------------------------------------------------
# STEP 16: TEAM SUMMARY
# ------------------------------------------------------------

print("\n========================================")
print("STEP 11 - TEAM BREACH ANALYSIS")
print("========================================")

team_summary = (
    merged
    .groupby(
        ["team_id", "team"],
        as_index=False
    )
    .agg(
        total_tickets=("ticket_id", "count"),
        breached_tickets=("breach_flag", "sum")
    )
)

# Calculate breach rate for every team
team_summary["breach_rate"] = (
    team_summary["breached_tickets"]
    / team_summary["total_tickets"]
) * 100

team_summary["breach_rate"] = (
    team_summary["breach_rate"].round(2)
)


print("\nTeam summary:")
print(team_summary)


# ------------------------------------------------------------
# STEP 17: FIND HIGHEST BREACH RATE TEAM
# ------------------------------------------------------------

print("\n========================================")
print("STEP 12 - HIGHEST BREACH RATE")
print("========================================")

# Find the highest breach rate
highest_breach_rate = team_summary["breach_rate"].max()

# Select ALL teams having that rate.
# This is important because the exam says to report all ties.

highest_breach_teams = team_summary[
    team_summary["breach_rate"] == highest_breach_rate
]


print("\nHighest team breach rate: {:.2f}%".format(
    highest_breach_rate
))

print("\nTeam(s) with the highest breach rate:")

print(
    highest_breach_teams[
        [
            "team_id",
            "team",
            "breached_tickets",
            "total_tickets",
            "breach_rate"
        ]
    ]
)


# ------------------------------------------------------------
# STEP 18: PRINT NUMERATOR AND DENOMINATOR
# ------------------------------------------------------------

print("\nNumerator = breached tickets")
print("Denominator = total tickets")

for _, row in highest_breach_teams.iterrows():

    print(
        "{} ({}) = {} / {} = {:.2f}%".format(
            row["team"],
            row["team_id"],
            row["breached_tickets"],
            row["total_tickets"],
            row["breach_rate"]
        )
    )


# ------------------------------------------------------------
# STEP 19: MONTHLY AVERAGE RESOLUTION HOURS
# ------------------------------------------------------------

print("\n========================================")
print("STEP 13 - MONTHLY AVERAGE")
print("========================================")

# Required month order:
# Jan -> Feb -> Mar

month_order = ["Jan", "Feb", "Mar"]


monthly_average = (
    merged
    .groupby("month")["resolution_hours"]
    .mean()
    .reindex(month_order)
)


monthly_average = monthly_average.round(2)


print("\nMonthly average resolution hours:")
print(monthly_average)


# ------------------------------------------------------------
# STEP 20: CREATE MONTHLY CHART
# ------------------------------------------------------------

print("\n========================================")
print("STEP 14 - CREATE CHART")
print("========================================")

plt.figure(figsize=(8, 5))

monthly_average.plot(
    kind="bar"
)

plt.title(
    "Average Resolution Hours by Month"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Average Resolution Hours"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()


# ------------------------------------------------------------
# STEP 21: SAVE CHART
# ------------------------------------------------------------

chart_path = output_path / "python_chart.png"

plt.savefig(
    chart_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("\nChart saved successfully:")
print(chart_path)


# ------------------------------------------------------------
# STEP 22: SAVE CLEAN MERGED DATA
# ------------------------------------------------------------

print("\n========================================")
print("STEP 15 - EXPORT CLEAN DATA")
print("========================================")

clean_data_path = output_path / "clean_data.csv"

merged.to_csv(
    clean_data_path,
    index=False
)

print("Clean data saved to:")
print(clean_data_path)


# ------------------------------------------------------------
# STEP 23: SAVE DEPARTMENT SUMMARY
# ------------------------------------------------------------

print("\n========================================")
print("STEP 16 - EXPORT SUMMARY")
print("========================================")

summary_path = output_path / "python_summary.csv"

department_summary.to_csv(
    summary_path,
    index=False
)

print("Department summary saved to:")
print(summary_path)


# ------------------------------------------------------------
# STEP 24: DISPLAY FINAL SUMMARY
# ------------------------------------------------------------

print("\n========================================")
print("FINAL ANALYSIS SUMMARY")
print("========================================")

print("\nTotal clean tickets:", total_tickets)

print(
    "Total SLA breaches:",
    total_breaches
)

print(
    "Overall SLA breach rate: {:.2f}%".format(
        overall_breach_rate
    )
)

print(
    "Overall average resolution hours: {:.2f}".format(
        merged["resolution_hours"].mean()
    )
)

print(
    "Overall average satisfaction: {:.2f}".format(
        merged["satisfaction"].mean()
    )
)


print("\nDepartment Summary:")
print(department_summary)


print("\nTeam Summary:")
print(team_summary)


print("\nHighest breach-rate team(s):")

print(
    highest_breach_teams[
        [
            "team_id",
            "team",
            "breached_tickets",
            "total_tickets",
            "breach_rate"
        ]
    ]
)


# ------------------------------------------------------------
# STEP 25: FINAL MESSAGE
# ------------------------------------------------------------

print("\n========================================")
print("PYTHON ANALYSIS COMPLETED SUCCESSFULLY")
print("========================================")

print("\nCreated files:")

print("1. outputs/clean_data.csv")
print("2. outputs/python_summary.csv")
print("3. outputs/python_chart.png")

print("\nYou can now use these files for")
print("the Power BI and final GitHub submission.")