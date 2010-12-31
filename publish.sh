#!/bin/bash

aws put -v "Content-type: text/html; charset=utf-8" "x-amz-acl:public-read" \
    s3.boskent.com/mazes/eller.html eller.html
