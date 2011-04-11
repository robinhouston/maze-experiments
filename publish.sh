#!/bin/bash

while [ $# -gt 0 ]; do
   case "$1" in
       *.html)
          aws put -v "Content-type: text/html; charset=utf-8" "x-amz-acl:public-read" \
              s3.boskent.com/mazes/"$1" "$1"
          ;;
       *.js)
          aws put -v "Content-type: text/javascript; charset=utf-8" "x-amz-acl:public-read" \
              s3.boskent.com/mazes/"$1" "$1"
          ;;
       *.css)
          aws put -v "Content-type: text/css; charset=utf-8" "x-amz-acl:public-read" \
              s3.boskent.com/mazes/"$1" "$1"
          ;;
       *.pdf)
          aws put -v "Content-type: application/pdf" "x-amz-acl:public-read" \
              s3.boskent.com/mazes/"$1" "$1"
          ;;
       *)
         echo >&2 "Filename '$1' has an unknown extension; not published."
         ;;
   esac
   shift
done
