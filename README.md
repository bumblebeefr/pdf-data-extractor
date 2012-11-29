pdf data extractor
==================

A Quick and dirty python script I used to extract some data from a pdf file :
 * All pages as JPG files
 * All pages as SVG files
 * A thumbnail of each page
 * The Table of content of the Document, as a json document.

Usage 
-----
python pdf-data-extractor.py myfile.pdf

*Will generate a folder named myfile and extract data into it*

Dependencies
------------

It depends on some python libraries  :
 * argparse
 * [pdfminer](http://www.unixuser.org/~euske/python/pdfminer/index.html)
 * Python Imaging Library (PIL)

and on some Linux command line tools :
 * pdftoppm
 * pdf2svg
 * convert (image magick)
