def raise_error_on_wrong_indentation(
    line_indentation, current_indentation, indentation, line
):
    if line_indentation > current_indentation + indentation:
        raise Exception(f"Expected an indentation of {indentation} in line '{line}'")
