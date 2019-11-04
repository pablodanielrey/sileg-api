#!/bin/bash
docker run -ti --rm --name mongo-express --add-host mongo:163.10.56.55 -p 8081:8081 mongo-express
