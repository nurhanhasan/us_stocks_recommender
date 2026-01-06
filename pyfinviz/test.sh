#!/bin/bash -e

BASE_URL="http://localhost:8000"
# BASE_URL="http://0.0.0.0:4000"

call_endpoint() {
    set +x

    local method=$1
    local path=$2

    echo "curl -X $method $BASE_URL$path -H 'accept: application/json'"

    curl -X $method $BASE_URL$path -H 'accept: application/json'

    echo -e "\n"

    set -x
}


# Health check
call_endpoint GET "/health"

# Stocks
call_endpoint GET "/stocks"
call_endpoint DELETE "/stocks"

# Scan
call_endpoint GET "/scan"
call_endpoint GET "/scan"

# Stocks again
call_endpoint GET "/stocks"
call_endpoint DELETE "/stocks"
call_endpoint GET "/stocks"