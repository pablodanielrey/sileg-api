#!/bin/bash
docker run -ti --rm -v $(pwd):/tmp --env-file ../.env sileg-api bash