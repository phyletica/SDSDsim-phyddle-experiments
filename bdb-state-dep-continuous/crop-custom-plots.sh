#! /usr/bin/env bash 

set -e

for pdf_path in custom-plots/*pdf direct/custom-plots/*pdf
do
    if [[ "$pdf_path" != *cropped.pdf ]]
    then
        path_prefix="${pdf_path/\.pdf/}"
        cropped_path="${path_prefix}-cropped.pdf"
        pdfcrop "$pdf_path" "$cropped_path"
    fi
done
