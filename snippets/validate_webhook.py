# Code snippet to use with pipedream.com to validate an incoming
# request (a webhook) from UP42 for job and order statuses updates. It
# acts based on the statuses we are interested in. All the
# information is available and can be passed on to other steps in a
# workflow.

from pipedream.script_helpers import (steps, export)

import os
import re
import base64
from hmac import digest, compare_digest
from hashlib import sha256
from time import time

# Get the response headers.
response_headers = steps["trigger"]["event"]["headers"]

# Get the signature input.
sig_input = steps["trigger"]["event"]["headers"]["signature-input"]

# Get the signature.
sig_header_value = steps["trigger"]["event"]["headers"]["signature"]
sig_header_value = bytes(sig_header_value.split("=", 1)[1], "UTF-8")

# Extract signature timestamp given as UNIX time.
sig_ts_re = re.compile("created=(?P<sig_ts>\d{10,20})")
sig_ts_val = int(sig_ts_re.search(sig_input).groupdict()["sig_ts"])

# Get current date as UNIX time.
current_ts = int(time())

# Reduce the possibility of replay attacks by dropping any incoming request that
# is older than 5 minutes (300 seconds).
if os.environ.get("is_test") != "yes": 
    assert sig_ts_val <= current_ts and abs(current_ts - sig_ts_val) < 300, f"Request time skew is too large." 

# Extract how the signature is generated.
# 1. Look for the up42-sig element in the header.
field_re = re.compile("up42-sig=\((?P<sig_list>.*)\);.*")
sig_val = field_re.search(sig_input).groupdict()["sig_list"]
# 2. Extract the list of signature input components.
list_re = re.compile("[^\"\s]+")
sig_inputs = re.findall(list_re, sig_val)

# Validate the received request by validating the signature.
# 1. First get each signature component concatenated in a single string.
sig_str = "".join(response_headers[i] for i in sig_inputs)
# 2. Compute the HMAC for this string.
secret = os.environ["up42_webhook_secret_zwei"] # get the secret
computed_sig = base64.b64encode(digest(bytes(secret,  "UTF-8"), bytes(sig_str, "UTF-8"), sha256))

Raise an Assertion error if the signature is invalid.
assert compare_digest(sig_header_value, computed_sig),  "Cannot authenticate incoming HTTP request."

# Filter the response based on the job status we are interested in.
def filter_response_status(current_status: str, interesting_statuses: list[str]) -> bool:
    if os.environ.get("is_test") == "yes":
        return True
    assert current_status in interesting_statuses, f"Ignoring request. Ignored status {current_status}."

# Get the current event type. 
current_event_type = steps["trigger"]["event"]["body"]["event"]

# The list of statuses that we are interested in for bot jobs and orders.
notifiable_statuses = ["ERROR", "FAILED", "CANCELLED", "SUCCEEDED"] + ["FAILED PERMANENTLY", "FULFILLED"]

# Filter the response based on the statuses we are interested in.
filter_response_status(steps["trigger"]["event"]["body"]["body"]["status"], notifiable_statuses)
