# Design Goals for SaaSy

The initial goal is to take an input CSV containing customer contracts and output the following analyses in the following order of priority:

**1. ARR Snowball**
  - Starting ARR
  - New
  - Upsell + Expansion (future: split into separate categories)
  - Downsell + Contraction (future: split into separate categories)
  - *Future: split out cross-sell*
  - Churn
  - Ending ARR

**2. Retention Analysis**
  - Available to Renew (ATR) ARR
  - Multi-year carry (MY) ARR
  - ATR gross retention
  - ATR net retention
  - Total gross retention (incl. MY)
  - Total net retention (incl. MY)

**3. Bookings Analysis**
  - New
  - Upsell + Expansion
  - *Future: split out cross-sell*
  - Renewal

**4. Cohort Analysis**
  - Parameters:
    - Cohort time bounds (monthly, quarterly, yearly)
    - Output time periods (montly, quarterly, yearly)
  - Generates an analysis that shows how ARR from each cohort has evolved over time as well as details around each cohort (number of customers, ARR, Avg. Customer Value)


&nbsp;

---
## Input Data

The input data would be a CSV list of contracts containing the following columns:

*TODO: assess need to specify date format*

- **customer_id** - The unique identifier of the customer
- **start_date** - The start date of the contract
- **end_date** - The end date of the contract (exclusive - i.e. the date at which the contract is no longer in effect)
- **tcv** - The total contract value for the entire period of the contract
- Optional Columns:
  - **close_date** - The closing date of the contract if distinct from start date for bookings analysis (otherwise start date will be used)
