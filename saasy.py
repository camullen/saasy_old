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

DEFAULT_TOLERANCE = 3


def bookings_to_arr(bookings):
    intervals = bookings_to_intervals(bookings)
    print(intervals)


def bookings_to_intervals(bookings):

    interval_list = []

    for cust_id, group in bookings.sort_values(by="start_date").groupby("customer_id"):
        # interval_list.append(row)
        # if index == 2:
        #     interval_list.append(row)
        # print(f"customer_id: {cust_id}\ngroup:\n{group}\n")
        booking_group_to_intervals(group)

    return pd.DataFrame(data=interval_list)


# TODO: verify integrity of input data
# Remember that we are receiving a booking group sorted by start_date (ascending)
def booking_group_to_intervals(booking_group, tolerance=DEFAULT_TOLERANCE):
    intervals = []
    for index, curr_booking in booking_group.itercurr_bookings():
        # If this is the first booking, then add to intervals and go to next booking
        if len(intervals) == 0:
            intervals.append(
                {
                    "start_date": curr_booking["start_date"],
                    "end_date": curr_booking["end_date"],
                    "customer_id": curr_booking["customer_id"],
                    "prior_arr": 0,
                    "arr": curr_booking["arr"],
                }
            )
        # If the bookings are contiguious
        elif is_contiguous(intervals[-1], curr_booking, tolerance=tolerance):
            # if bookings are contiguous and have the same ARR, extend previous
            # interval and move to next booking
            if intervals[-1]["arr"] == curr_booking["arr"]:
                intervals[-1]["end_date"] = curr_booking["end_date"]

            # The ARR is different, so we need a new interval
            # TODO: decide how to handle gaps between previous end_date and new start_date
            else:
                intervals.append(
                    {
                        "start_date": curr_booking["start_date"],
                        "end_date": curr_booking["end_date"],
                        "customer_id": curr_booking["customer_id"],
                        "prior_arr": intervals[-1]["arr"],
                        "arr": curr_booking["arr"],
                    }
                )

        # If the next booking starts significantly (we've already checked for
        # (tolerance above) after the last booking ends we need an interval
        # with 0 ARR in between
        elif curr_booking["start_date"] > intervals[-1]["end_date"]:
            # Add churn gap to intervals
            intervals.append(
                {
                    "start_date": intervals[-1]["end_date"],
                    "end_date": curr_booking["start_date"],
                    "customer_id": curr_booking["customer_id"],
                    "prior_arr": intervals[-1]["arr"],
                    "arr": 0,
                }
            )
            # Add current booking to intervals
            intervals.append(
                {
                    "start_date": curr_booking["start_date"],
                    "end_date": curr_booking["end_date"],
                    "customer_id": curr_booking["customer_id"],
                    "prior_arr": intervals[-1]["arr"],
                    "arr": curr_booking["arr"],
                }
            )
        # If not contiguous, or the start date is after the previous end date,
        # there are overlapping bookings and we need to splice something in
        # TODO: Handle edge case where the the start date of the previous interval
        # equals that of the current booking

        # Check if they are completely overlapping and up the ARR and expand the bounds
        elif ts_equal(curr_booking["start_date"], intervals[-1]["start_date"], tolerance=tolerance) and ts_equal(
            curr_booking["end_date"], intervals[-1]["end_date"], tolerance=tolerance
        ):
            intervals[-1]["start_date"] = min(intervals[-1]["start_date"], curr_booking["start_date"])
            intervals[-1]["end_date"] = max(intervals[-1]["end_date"], curr_booking["end_date"])
            intervals[-1]["arr"] += curr_booking["arr"]

        # Check if the start is overlapping and then shorten the existing interval and add the new (non-overlapping) one
        elif ts_equal(curr_booking["start_date"], intervals[-1]["start_date"], tolerance=tolerance):
            intervals[-1]["end_date"] = min(intervals[-1]["end_date"], curr_booking["end_date"])
            intervals[-1]["arr"] += curr_booking["arr"]
            intervals.append(
                {
                    "start_date": intervals[-1]["end_date"],
                    "end_date": max(intervals[-1]["end_date"], curr_booking["end_date"])
                    # Need to figure out which ARR to put into the non-overlapping segment
                }
            )


def is_contiguous(prev_interval, next_interval, tolerance=DEFAULT_TOLERANCE):
    return ts_equal(next_interval["start_date"], prev_interval["end_date"], tolerance=tolerance)


def ts_equal(ts_a, ts_b, tolerance=DEFAULT_TOLERANCE):
    day_gap = (ts_a - ts_b).days
    return abs(day_gap) <= tolerance


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
