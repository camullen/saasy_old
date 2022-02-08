# ARR Snowball Implementation

## Output & Definitions
---
### Definitions
- `per_start` - the start date of the period over which the snowball is calculated
- `per_end` - the end date of the period over which the snowball is calculated
- `contract_ARR` - $$ARR =\frac{TCV}{years(end\_date - start\_date)} $$
- `customer_ARR` - The sum of all `contract_ARR` for a particular customer on a particular date
- `contract_buffer` - A parameter that dictates how much buffer (in days) should be applied to the start and end dates of a contract for the purposes of analyzing customer continuity (i.e. renewal rates, churn, new, etc.)


### Outputs
- Starting ARR
  - The sum of all `contract_ARR` for which `start_date` <= `per_start` <= `end_date`
- New
  - The sum of all `contract_ARR` for which associated `customer_ARR` during the period of `start_date - contract_buffer` is 0
  - *i.e. contracts that are not in some way a continuation of a previous contract*
- Upsell + Expansion (future: split into separate categories)
  $$\sum \big(\text{contract\_ARR } - \text{customer\_ARR}_\text{start\_date - contract\_buffer}\big) \newline \text{ where } > 0  \newline \text{and} \newline \text{customer\_ARR}_\text{start\_date - contract\_buffer} > 0$$
- Downsell + Contraction (future: split into separate categories)
  $$\sum \big(\text{contract\_ARR } - \text{customer\_ARR}_\text{start\_date - contract\_buffer}\big) \newline \text{ where } < 0  \newline \text{and} \newline \text{customer\_ARR}_\text{start\_date - contract\_buffer} > 0$$
- *Future: split out cross-sell*
- Churn
  - The sum of all `customer_ARR` at time `per_start` for which `customer_ARR` is 0 for all dates in the range of \[`per_end`, `per_end` + `contract_buffer`\]
- Ending ARR
  - The sum of all `contract_ARR` for which `start_date` <= `per_end` <= `end_date`

