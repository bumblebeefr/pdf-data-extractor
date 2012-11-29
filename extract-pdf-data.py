# -*- coding: utf-8 -*-
#!/usr/bin/env python

import lib.pdftoc as pdf
import subprocess,os
import Image
import json,sys,argparse



def main():
	parser = argparse.ArgumentParser(description='Extract Table of Content and pages (as jpg and svg files) from a PDF file.')
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), help='PDF file')
	try :
		args = parser.parse_args()
	except IOError :
		sys.exit(0)

	pdfDescription = pdf.extractToc(args.infile.name)
	pdfExtractionDir = args.infile.name.replace(".pdf","/").replace(".PDF","/")

	print("Creating output directory %s" % pdfExtractionDir)
	try :
		os.makedirs(pdfExtractionDir)
		os.makedirs(pdfExtractionDir+"/thumb/")
		os.makedirs(pdfExtractionDir+"/full/")
		os.makedirs(pdfExtractionDir+"/svg/")
	except OSError :
		print("/!\ existe deja")

	print("Extracting JPG files")
	subprocess.Popen(["pdftoppm", "-jpeg", "-aa", "yes", "-aaVector", "yes", "-freetype", "yes", args.infile.name, pdfExtractionDir+"/full/page"]).wait()
	
	print("Extracting SVG files")
	subprocess.Popen(["pdf2svg", args.infile.name, pdfExtractionDir+"/svg/page-%03d.svg", "all"])

	nbPages = pdfDescription['totalPageNumber']

	pdfDescription['sizes'] = []
	print("Extracting thumbs files")
	for i in range(1,nbPages+1):
		img = Image.open("%sfull/page-%03d.jpg" % (pdfExtractionDir,i))
		pdfDescription['sizes'].append(img.size)
		subprocess.Popen(["convert","-resize","100x150","%sfull/page-%03d.jpg" % (pdfExtractionDir,i),"%sthumb/page-%03d.jpg" % (pdfExtractionDir,i)])


	print("Writing toc (json) file")
	json.dump(pdfDescription,file(pdfExtractionDir+"description.json","w"))



if __name__ == "__main__":
	sys.exit(main())
