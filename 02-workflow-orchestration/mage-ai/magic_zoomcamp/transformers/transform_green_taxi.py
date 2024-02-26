import re

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def camel_to_snake(name):
    first_pattern = re.compile("(.)([A-Z][a-z]+)")
    second_pattern = re.compile("__([A-Z])")
    third_pattern = re.compile("([a-z0-9])([A-Z])")
    name = first_pattern.sub(r"\1_\2", name)
    name = second_pattern.sub(r"\_1", name)
    name = third_pattern.sub(r"\1_\2", name)
    return name.lower()


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero
    or any of them missing.
    Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    data = data[(data["passenger_count"] > 0) & (data["trip_distance"] > 0)]
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date
    data.columns = map(camel_to_snake, data.columns)

    return data


@test
def test_vendor_id(output, *args) -> None:
    """
    Assert vendor_id is one of the existing values in the column
    """
    assert "vendor_id" in output.columns


@test
def test_passenger_count(output, *args) -> None:
    """
    Assert passenger_count is greater than 0
    """
    # assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert (output["passenger_count"] > 0).all()


@test
def test_trip_distance(output, *args) -> None:
    """
    Assert trip_distance is greater than 0
    """
    assert (output["trip_distance"] > 0).all()
