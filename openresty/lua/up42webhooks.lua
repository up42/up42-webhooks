--- Module for working with UP42 webhooks in OpenResty.
-- @module up42webhooks.lua
-- @author António Almeida <antonio.almeida@up42.com>
-- @copyright UP42 GmbH
-- @license MIT
-- @alias M

--- Some local definitions.
local ipairs = ipairs
-- String functions.
local format = string.format
-- Math functions.
local max = math.max
-- nginx Lua functions and constants.
local ngx = ngx
local rcvd = ngx.shared.received_webhooks

-- Avoid polluting the global environment.
-- No globals beyond this point.
-- If we are in Lua 5.1 this function exists.
if _G.setfenv then
   setfenv(1, {})
else -- Lua >= 5.2.
   _ENV = nil
end

--- Module table.
local M = { _VERSION = '1.0',
            _NAME = 'up42webhooks',
            _DESCRIPTION = 'Handling webhooks for UP42 in OpenResty' }

-- Define a variable to be used in a closure below.
local counter = 0

-- Increment the counter and return it.
function M.inc()
   counter = counter + 1
   return counter
end

-- Decrement the counter and return it.
function M.dec()
   counter = max(counter - 1, 0)
   return counter
end

-- Return a string stating the success or failure of storing the data.
function M.set_key_value_webhook()
   -- Read the request body.
   ngx.req.read_body()
   local data = ngx.req.get_body_data()

   local ok, err, forced
   -- If nginx read data from the request body, then return it and add
   -- the value of counter to be used as a key.
   if data then
      M.inc()
      ok, err, forced = rcvd:set(counter, data)
   end

   if ok then
      return format('{"msg": "value with key %d stored"}', counter)
   else
      -- Decrement the counter if there is an issue with the dict so
      -- that we always have consecutive keys.
      M.dec()
      return format('{"msg": "%s"}', err)
   end
end

-- Represents the total number of webhooks.
local total_number_webhooks = 0

-- Dumps all the webhooks that have been stored.
-- Side effects only. No return.
function M.dump_webhooks()
   -- Get all the keys for the shared dict.
   local keys = rcvd:get_keys()
   -- Iterate over them. Assuming no key is nil.
   for _, k in ipairs(keys) do
      ngx.say(rcvd:get(k))
   end
   -- Set the total number of webhooks. It needs to be retrieved from
   -- the keys available in the dict to persist.
   total_number_webhooks = #keys
end

-- Prints the total number of items in the shared dict.
function M.dump_cardinality()
   return ngx.say(format('{"number_webhooks_received": %d}', total_number_webhooks))
end

-- Return the module table.
return M
