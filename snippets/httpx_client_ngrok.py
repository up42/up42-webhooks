# Simple HTTP client to forward a webhook to our development server
# running locally.  It receives the webhook body from the previous
# step that validates the webhook.

# pipedream serialized objects.
from pipedream.script_helpers import (steps, export)

import os

from contextlib import suppress
# httpx and friends.
import httpx
from httpx_auth import Basic

def get_url(u):
    """Return the local development url.

    """
    return f"{os.environ['local_dev_host']}{u}"

# The user and password for the ngrok basic authentication
# are set as pipedream environment variables.
ngrok_basic_auth = Basic(os.environ["ngrok_basic_auth_user"], os.environ["ngrok_basic_auth_pass"])

# Test that the local server is up and running.
r = httpx.get(get_url("/ping"), auth=ngrok_basic_auth)
# If we get the proper response proceed.
assert r.status_code == 200 and r.text == "PONG", f"{os.environ['local_dev_host']} is not reachable."

# Issue the POST request in the given context.
with httpx.Client() as client:
    try:
        r = client.post(get_url("/receive-webhooks"), auth=ngrok_basic_auth, json=steps["trigger"]["event"]["body"])
        # Raise an exception for any non 2XX status code.
        r.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error {exc.response.status_code} while requesting {exc.request.url!r}.")
    except httpx.HTTPError as exc:
        print(f"Error while requesting {exc.request.url!r}.")

    # Return the response body. Continue to returning None even is
    # there is a value error, e..g, response is not JSON.
    with suppress(ValueError):
        export("ngrok_response", r.json())
