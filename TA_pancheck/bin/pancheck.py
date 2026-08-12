
#!/usr/bin/env python3

# navid alizadeh vaghasloo 2026
import sys
import csv
import re


def normalize(value):
    if value is None:
        return ""

    return re.sub(r"[\s-]", "", str(value).strip())


def luhn_check(number):
    total = 0

    for index, digit in enumerate(reversed(number)):
        value = int(digit)

        if index % 2 == 1:
            value *= 2

            if value > 9:
                value -= 9

        total += value

    return total % 10 == 0


def validate_pan(value, expected_length=None):

    pan = normalize(value)

    pan_length = len(pan)

    if not pan:
        return False, pan_length, False, False

    if not pan.isdigit():
        return False, pan_length, False, False

    length_valid = 8 <= pan_length <= 19

    if expected_length:
        length_valid = pan_length == int(expected_length)

    if not length_valid:
        return False, pan_length, False, False

    luhn_valid = luhn_check(pan)

    is_pan = luhn_valid

    return (
        is_pan,
        pan_length,
        luhn_valid,
        is_pan
    )


def main():

    pan_argument = None
    expected_length = None

    for argument in sys.argv[1:]:

        if argument.startswith("pan="):
            pan_argument = argument.split("=", 1)[1]

        elif argument.startswith("length="):
            expected_length = argument.split("=", 1)[1]

    reader = csv.DictReader(sys.stdin)

    input_fields = reader.fieldnames or []

    output_fields = list(input_fields)

    fields_to_add = [
        "pan_is_valid",
        "pan_length",
        "pan_luhn_valid",
        "pan_should_mask"
    ]

    for field in fields_to_add:

        if field not in output_fields:
            output_fields.append(field)

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=output_fields,
        extrasaction="ignore"
    )

    writer.writeheader()

    for record in reader:

        if pan_argument is not None:
            value = pan_argument
        else:
            value = record.get("pan", "")

        (
            is_pan,
            pan_length,
            luhn_valid,
            should_mask
        ) = validate_pan(
            value,
            expected_length
        )

        record["pan_is_valid"] = str(is_pan).lower()
        record["pan_length"] = str(pan_length)
        record["pan_luhn_valid"] = str(luhn_valid).lower()
        record["pan_should_mask"] = str(should_mask).lower()

        writer.writerow(record)


if __name__ == "__main__":
    main()
