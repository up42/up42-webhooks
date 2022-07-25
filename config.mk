## Configuration for the Makefile.
SRC := $(shell pwd)
NGINX_HOST_PORT := 9888
## nginx configuration file.
NGINX_CONF := $(SRC)/openresty/default.conf
## Lua module directory.
LUA_MODULE := $(SRC)/openresty/lua
## Options for running OpenResty locally. Replace the virtual host.
DOCKER_RUN_OPTIONS := --mount type=bind,src=$(NGINX_CONF),dst=/etc/nginx/conf.d/default.conf \
--mount type=bind,src=$(LUA_MODULE),dst=/usr/local/openresty/nginx/lua \
-p $(NGINX_HOST_PORT):80 -d
