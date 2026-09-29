# Customer Support Quality Analysis — Data Analysis Set B

**Student Name:** Parth Patel
**Student ID:** 12787
**Assigned Set:** Set B

## 1. Business Objective

The objective of this project is to analyze customer support quality and identify differences in resolution performance and service quality across support teams and channels.

The analysis was completed using Excel, SQL, Python, and Power BI.

## 2. Business Questions

1. Which support team should improve resolution performance?
2. How does service quality vary by channel?

## 3. Dataset

The project uses two CSV files:

* `data/raw/tickets.csv` — customer support ticket data
* `data/raw/teams.csv` — team and department lookup data

The tickets file originally contains 13 rows, including one exact duplicate. After removing the duplicate, 12 unique ticket records remain.

## 4. Data Dictionary

### tickets.csv

| Column           | Type    | Meaning                                 |
| ---------------- | ------- | --------------------------------------- |
| ticket_id        | Integer | Unique ticket identifier                |
| month            | Text    | Ticket month                            |
| team_id          | Text    | Support team identifier                 |
| channel          | Text    | Support channel                         |
| resolution_hours | Numeric | Time taken to resolve the ticket        |
| satisfaction     | Numeric | Customer satisfaction score from 1 to 5 |

### teams.csv

| Column     | Type | Meaning                 |
| ---------- | ---- | ----------------------- |
| team_id    | Text | Support team identifier |
| team       | Text | Support team name       |
| department | Text | Support department      |

## 5. Data Cleaning

The following cleaning steps were applied:

1. Loaded the supplied raw CSV files.
2. Preserved the original raw ticket data.
3. Identified and removed the exact duplicate ticket row.
4. Confirmed that 12 unique ticket records remain.
5. Used `team_id` to connect tickets with the teams lookup table.
6. Applied appropriate data types to numeric and text columns.
7. Created the required `breach_flag` field.

## 6. Metric Definitions

### Breach Flag

A ticket is considered an SLA breach when:

`resolution_hours > 24`

A resolution time of exactly 24 hours is not a breach.

### SLA Breach Rate

SLA Breach Rate is calculated as:

`Tickets resolved in more than 24 hours / Total tickets`

The result is displayed as a percentage.

## 7. Tools Used

* Microsoft Excel
* Power BI Desktop
* MySQL
* Python
* pandas
* matplotlib
* Git / GitHub

**SQL Engine and Version:** MySQL 8.0

## 8. Project Structure

```text
data-analysis-set-e-YOUR-STUDENT-ID/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── raw/
│       ├── tickets.csv
│       └── teams.csv
│
├── excel/
│   └── analysis.xlsx
│
├── sql/
│   ├── setup.sql
│   └── queries.sql
│
├── python/
│   └── analysis.py
│
├── powerbi/
│   └── dashboard.pbix
│
└── outputs/
    ├── clean_data.csv
    ├── python_summary.csv
    ├── python_chart.png
    ├── powerbi_dashboard.png
    └── sql/
        ├── s2a_avg_resolution_by_department.csv
        ├── s2b_teams_breaching_sla.csv
        └── s2c_top_channels_by_breach_count.csv
```

## 9. Excel Instructions

The Excel workbook contains four sheets:

* `Raw` — original 13-row ticket data
* `Lookup` — teams lookup data
* `Clean` — cleaned 12-row data with department and breach flag
* `Summary` — channel breach counts, PivotTable, and chart

The duplicate ticket row was removed from the Clean sheet.

## 10. SQL Instructions

Run the SQL files in this order:

1. `sql/setup.sql`
2. `sql/queries.sql`

The setup file creates the required tables and loads the cleaned 12 ticket records and 4 team records.

The queries file contains the three required analytical queries.

## 11. Python Instructions

Install the required packages:

```text
pip install -r requirements.txt
```

Run the Python analysis from the repository root:

```text
python python/analysis.py
```

The Python script loads the raw CSV files, removes the duplicate, merges the datasets, calculates the breach flag, creates the department summary, generates the monthly chart, and exports the required output files.

## 12. Power BI Instructions

The Power BI report is located at:

`powerbi/dashboard.pbix`

The report uses:

* `data/raw/tickets.csv`
* `data/raw/teams.csv`

The tickets query removes the exact duplicate so that 12 records remain.

The Power BI model contains a one-to-many relationship from `teams[team_id]` to `tickets[team_id]`.

The report contains:

* Ticket Count KPI
* Average Satisfaction KPI
* SLA Breach Rate KPI
* Department comparison chart
* Monthly average resolution-time chart
* Channel slicer

### Power BI Refresh

After cloning the repository on another computer:

1. Open `powerbi/dashboard.pbix`.
2. Open Power Query or Data source settings.
3. Update the CSV file paths if required.
4. Confirm that the files point to the local repository's `data/raw/` folder.
5. Click Refresh.

## 13. Video

**Video URL:** []

The video demonstrates the dataset, cleaning process, Excel analysis, SQL query, Python analysis, and Power BI report.

## 16. References

[Write `None` if no external code or resources were used.]

## 17. Authorship Declaration

All work in this repository is my own except where cited.
