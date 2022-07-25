# Using webhooks in UP42

## Introduction

This repository contains code for using webhooks with
[UP42](https://up42.com).

It is divided in several parts:

 1. Low code version with Python snippets to be used together with
    [pipedream](https://pipedream.com).
 2. Server side version with a light Python client to work with
    webhooks and a [OpenResty](https://openresty.org) based minimal
    setup that just does Incoming HTTP request validation and leaves
    it there. Is then up to you to add your custom server side code to
    do something with the incoming webhook. (To be added)

## Pipedream snippets

The pipedream snippets are in the snippets directory. And the
filenames are self explanatory:

 * `pipedream_up42_webhook_job_status_handler.py`: incoming HTTP
   validation and job status filtering.

 * `pipedream_up42_webhook_order_status_handler.py`: incoming HTTP
   validation and order status filtering.

 * `validate_webhook.py`: incoming HTTP validation for **both** job
   and order status filtering.

 * `httpx_client_ngrok.py`: forward the webhook to our local OpenResty
   instance.


## OpenResty configuration and Lua module

The `openresty` directory contains:

 * `default.conf`: server configuration.

 * `lua`: directory containing the `up42webhooks.lua` module that
   implements a webhook record collection system. I.e., all webhook
   requests forwarded by pipedream get collected in a
   [in-memory](https://nginx.org/en/docs/dev/development_guide.html#shared_memory)
   key-value store, that persists across requests and OpenResty
   reloads, so that we can consult them at our leisure.

## Jupyter notebook

In the `notebook` directory there is a Python
[Jupyter](https://jupyter.org) notebook that makes use of the
[SDK webhooks](https://sdk.up42.com/webhooks/) implementation.

 * `sdk_webhooks_testing.ipynb`.

## Makefile

The server side setup runs from a Makefile. The configuration for the
Makefile is in `config.mk`.

## Using this code

For a detailed description of the usage of this code please refer to
the UP42 blog posts.

 * [Blog post on the "low code" version](https://up42.com/blog/tech/first-step-into-webhooks-no-code-required)


## License

MIT License

Copyright (c) 2022 UP42 GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
