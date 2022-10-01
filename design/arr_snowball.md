# ARR Snowball Implementation

## Output & Definitions
---
### Definitions
- `per_start` - the start date of the period over which the snowball is calculated
- `per_end` - the end date of the period over which the snowball is calculated
- `contract_ARR` - $$ARR =\frac{TCV}{years(end\_date - start\_date)} $$
- `customer_ARR` - The sum of all `contract_ARR` for a particular customer on a particular date `d` calculated as:
$$\sum_{start\_date <= d < end\_date} contract\_ARR$$
- `contract_buffer` - A parameter that dictates how much buffer (in days) should be applied to the start and end dates of a contract for the purposes of analyzing customer continuity (i.e. renewal rates, churn, new, etc.)
- `contract_df` - The [input contract data](goals.md#input-data) read from the CSV into a dataframe


### Outputs
- **Starting ARR**
  - The sum of all `contract_ARR` for which `start_date` <= `per_start` < `end_date`
- **New**
  - The sum of all `contract_ARR` for which associated `customer_ARR` during the period of `start_date - contract_buffer` is 0
  - *i.e. contracts that are not in some way a continuation of a previous contract*
- **Upsell + Expansion** (future: split into separate categories)
  $$\sum \big(\text{contract\_ARR } - \text{customer\_ARR}_\text{start\_date - contract\_buffer}\big) \newline \text{ where } > 0  \newline \text{and} \newline \text{customer\_ARR}_\text{start\_date - contract\_buffer} > 0$$
- **Downsell + Contraction** (future: split into separate categories)
  $$\sum \big(\text{contract\_ARR } - \text{customer\_ARR}_\text{start\_date - contract\_buffer}\big) \newline \text{ where } < 0  \newline \text{and} \newline \text{customer\_ARR}_\text{start\_date - contract\_buffer} > 0$$
  - This doesn't work for the following edge case:
    - Assume three contracts for the same customer:
      - A - ARR: 200, start_date: 1/1/2020, end_date: 1/1/2021
      - B - ARR: 100, start_date: 7/1/2020, end_date: 7/1/2021
      - C - ARR: 100, start_date: 7/1/2021, end_date: 7/1/2022
    - There should be a downsell event on 1/1/2021 as contract A wasn't renewed, but this wouldn't be captured in the above formula
    - Similar dynamics exist for Churn as there may be recovered churn during the period
- *Future: split out cross-sell*
- **Churn**
  - The sum of all `customer_ARR` at time `per_start` for which `customer_ARR` is 0 for all dates in the range of \[`per_end`, `per_end` + `contract_buffer`\]
- **Ending ARR**
  - The sum of all `contract_ARR` for which `start_date` <= `per_end` < `end_date`

## Implementation
1. Augment & normalize the `contract_df`
    - Calculate ARR for each contract and add as a column (`ARR`)

2. **Starting ARR** and **Ending ARR** are trivial to calculate using a sum over the `contract_df` with date contraints for the various `per_start` and `per_end`

3. The other values require the ability to interrogate `customer_ARR` at a particular date, so construct a data structure that would allow efficient calculation of `customer_ARR` at a particular date, ideally taking into account the `contract_buffer` parameter

