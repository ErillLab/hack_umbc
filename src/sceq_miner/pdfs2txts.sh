#!/bin/bash

# Convert the pdfs to txts

pdf_path=../../data/sceq_pdfs
for pdf in `ls $pdf_path`; do
    #http://stackoverflow.com/questions/12152626
    class_name=`echo $pdf | cut -f1 -d'.'`
    full_pdf_path=$pdf_path/$class_name.pdf
    echo "full path is: $full_pdf_path"
    echo "starting on $class_name"
    txt_name=../../data/sceq_txts/$class_name.txt
    # check if txt already exists
    cd ../../data/sceq_txts
    if [ -e $txt_name ] 
    then 
	echo "$txt_name exists, moving on"
    else
	pdftotext -layout $full_pdf_path # creates a txt in same directory, -layout switch turns vomit off.
	mv $pdf_path/$class_name.txt $txt_name
	echo "finished on $pdf"
    fi
done


    