#!/bin/bash

aws put -v "Content-type: text/html; charset=utf-8" "x-amz-acl:public-read" \
    s3.boskent.com/mazes/race.html race.html

# aws put -v "Content-type: text/html; charset=utf-8" "x-amz-acl:public-read" \
#     s3.boskent.com/mazes/flipper.html flipper.html
