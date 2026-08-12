# pancheck

A Splunk Custom Streaming Search Command for detecting and validating
Potential Account Numbers (PANs) using length validation and the
Luhn (Modulus 10) algorithm.
---
## Overview

`pancheck` is designed to help identify payment card number candidates
inside Splunk searches.

The command does not modify, mask, or replace PAN values.

It only validates the supplied value and returns metadata indicating
whether the value should be considered a PAN candidate.
---
## Features

- PAN length validation
- Luhn (Modulus 10) validation
- Supports PAN lengths from 8 to 19 digits
- Optional explicit PAN length validation
- Does not modify the original PAN
- Does not perform masking
- Designed as a Splunk streaming search command
- Python 3 compatible
- No external Python packages required
---
## Requirements

- Splunk Enterprise 10.x
- Python 3
- Splunk Custom Search Command support
---
## Installation

Copy the `TA_pancheck` directory into:

```text
$SPLUNK_HOME/etc/apps/

Example:
cp -r TA_pancheck /opt/splunk/etc/apps/

Set permissions:
chown -R splunk:splunk /opt/splunk/etc/apps/TA_pancheck
chmod 755 /opt/splunk/etc/apps/TA_pancheck/bin/pancheck.py

Restart Splunk:
/opt/splunk/bin/splunk restart

```
---
## Usage

Validate a PAN field
```
| makeresults
| eval pan="4111111111111111"
| pancheck
| table pan pan_is_valid pan_length pan_luhn_valid pan_should_mask
```
Example output:
```
pan                 pan_is_valid  pan_length  pan_luhn_valid  pan_should_mask
4111111111111111    true          16          true            true
```

Invalid PAN
```
| makeresults
| eval pan="4111111111111112"
| pancheck
| table pan pan_is_valid pan_length pan_luhn_valid pan_should_mask
```
Example output:
```
pan                 pan_is_valid  pan_length  pan_luhn_valid  pan_should_mask
4111111111111112    false         16          false           false
Explicit PAN value
```

The command also supports an explicit PAN argument:
```
| makeresults
| pancheck pan=4111111111111111
| table pan_is_valid pan_length pan_luhn_valid pan_should_mask
```

Explicit length
```
| makeresults
| pancheck pan=4111111111111111 length=16
```
Output Fields
```
Field				Description
pan_is_valid		Indicates whether the value passes PAN length and Luhn validation
pan_length			Number of digits detected
pan_luhn_valid		Result of the Luhn validation
pan_should_mask		Indicates whether the value should be passed to a separate masking mechanism
```
---
# Important
`pancheck` does not prove that a payment card exists, has been issued, or is active.

The Luhn algorithm only validates the mathematical checksum of the number.

# Therefore:
```
Luhn valid != Real issued card
```
The command should be considered a PAN candidate detector/validator.

---
# Masking

pancheck does not perform masking.
It only returns:
```
pan_should_mask=true
```
A separate masking mechanism can use this result to perform the actual redaction or masking.
This separation keeps PAN detection and data protection logic independent.
---
## PCI DSS

PAN (Primary Account Number) is a key data element within the PCI DSS scope when payment card data is involved.
This project focuses specifically on detecting potential PAN values.
National ID numbers, government IDs, and other identity numbers are outside the scope of this project.

---
## Architecture
```
Splunk Search
     |
     v
  pancheck
     |
     +-- Length Validation
     |
     +-- Luhn Validation
     |
     v
PAN Candidate
     |
     +-- pan_is_valid
     +-- pan_length
     +-- pan_luhn_valid
     +-- pan_should_mask
     |
     v
Separate Masking Mechanism
```
---
## License

MIT License

---

## Author

Navid Alizadeh

https://www.linkedin.com/in/navid-alizadeh-vaghaslo

Security Operations Center (SOC)

Detection Engineering | Splunk | Threat Detection | Automation



