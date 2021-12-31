import pandas as pd

# bookings_to_arr
#
# Accepts a pandas dataframe containing bookings data and returns a pandas
# dataframe containing changes in ARR with the following columns:
#    - date - the date of the change
#    - type - the type of the change (new, upsell, downsell, and churn)
#    - customer_id - the id of the customer
#    - prior_arr - the ARR for the customer prior to the change
#    - next_arr - the ARR for the customer following the change
#    - delta_arr - the change in ARR
#
# The bookings (input) dataframe should contain the following columns:
#    - date - the date of the booking (as pandas Timestamps)
#    - customer_id - the unique id of the customer
#    - arr - the amount of ARR booked
#    - start_date - the start date of the contract (as pandas Timestamps)
#    - end_date - the end date of the contract (as pandas Timestamps)


def bookings_to_arr(bookings):
    intervals = bookings_to_intervals(bookings)
    print(intervals)


def bookings_to_intervals(bookings):

    interval_list = []

    for index, row in bookings.sort_values(by=["customer_id", "start_date"]).iterrows():
        interval_list.append(row)
        if index == 2:
            interval_list.append(row)
        # print(f"Index: {index}")
        # print(bookings.loc[index])
        # print("\n")

    return pd.DataFrame(data=interval_list)


test_bookings = pd.DataFrame.from_records(
    [
        {
            "date": pd.Timestamp(ts_input="9/25/2019", tz="UTC"),
            "customer_id": 1234,
            "arr": 200,
            "start_date": pd.Timestamp(ts_input="10/1/2019", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2020", tz="UTC"),
        },
        {
            "date": pd.Timestamp(ts_input="9/25/2018", tz="UTC"),
            "customer_id": 1234,
            "arr": 125,
            "start_date": pd.Timestamp(ts_input="10/1/2018", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2019", tz="UTC"),
        },
        {
            "date": pd.Timestamp(ts_input="9/25/2020", tz="UTC"),
            "customer_id": 1234,
            "arr": 150,
            "start_date": pd.Timestamp(ts_input="10/1/2020", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2021", tz="UTC"),
        },
        {
            "date": pd.Timestamp(ts_input="9/25/2021", tz="UTC"),
            "customer_id": 1234,
            "arr": 150,
            "start_date": pd.Timestamp(ts_input="10/1/2021", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2022", tz="UTC"),
        },
        {
            "date": pd.Timestamp(ts_input="9/25/2018", tz="UTC"),
            "customer_id": 5000,
            "arr": 100,
            "start_date": pd.Timestamp(ts_input="10/1/2018", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2019", tz="UTC"),
        },
        {
            "date": pd.Timestamp(ts_input="9/25/2019", tz="UTC"),
            "customer_id": 5000,
            "arr": 100,
            "start_date": pd.Timestamp(ts_input="10/1/2019", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2020", tz="UTC"),
        },
        {
            "date": pd.Timestamp(ts_input="9/25/2020", tz="UTC"),
            "customer_id": 5000,
            "arr": 150,
            "start_date": pd.Timestamp(ts_input="10/1/2020", tz="UTC"),
            "end_date": pd.Timestamp(ts_input="9/30/2021", tz="UTC"),
        },
    ]
)


if __name__ == "__main__":
    bookings_to_arr(test_bookings)
