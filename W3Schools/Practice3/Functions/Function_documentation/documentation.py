def calculate_average(numbers):
    """
    Calculates the average of a list of numbers.

    This function iterates through the provided list and computes the mean value.

    Parameters
    ----------
    numbers : list of int or float
        The list of numbers to calculate the average.

    Returns
    -------
    float
        The average of the numbers in the list.

    Raises
    ------
    ValueError
        If the input list is empty.
    """
    if not numbers:
        raise ValueError("The input list cannot be empty.")
    total = sum(numbers)
    average = total / len(numbers)
    return average