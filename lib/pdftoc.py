# -*- coding: utf-8 -*-
#
# Inspired by dumppdf.py 
#
import sys, re
from pdfminer.psparser import PSKeyword, PSLiteral
from pdfminer.pdfparser import PDFDocument, PDFParser, PDFNoOutlines, PDFDestinationNotFound
from pdfminer.pdftypes import PDFStream, PDFObjRef, resolve1, stream_value

from pprint import pprint
import json

ESC_PAT = re.compile(r'[\000-\037&<>()"\042\047\134\177-\377]')
def e(s):
	return ESC_PAT.sub(lambda m:'&#%d;' % ord(m.group(0)), s)


def with_pdf (pdf_doc, fn, pdf_pwd, *args):
	"""Open the pdf document, and apply the function, returning the results"""
	result = None
	try:
		# open the pdf file
		fp = open(pdf_doc, 'rb')
		# create a parser object associated with the file object
		parser = PDFParser(fp)
		# create a PDFDocument object that stores the document structure
		doc = PDFDocument()
		# connect the parser and document objects
		parser.set_document(doc)
		doc.set_parser(parser)
		# supply the password for initialization
		doc.initialize(pdf_pwd)

		if doc.is_extractable:
				# apply the function and return the result
				result = fn(doc, *args)

		# close the pdf file
		parser.close()
		fp.close()
	except IOError:
		# the file doesn't exist or similar problem
		pass
	return result



#Ajoute l'element au bon niveau dans la TOC
def addToToc(toc,level,title,page):
	if(level == 1) :
		toc.append({'title':title,'page':page,'subToc':[]})
	else :
		category = toc[-1]
		for i in range(2,level):
			category = category['subToc'][-1]
		category['subToc'].append({'title':title,'page':page,'subToc':[]})

#Fonction interne D'extraction de la TOC sous forme d'une liste
def dumpoutline(doc):
	pages = dict( (page.pageid, pageno) for (pageno,page) in enumerate(doc.get_pages()) )
	totalPageNumber = len(pages)
	def resolve_dest(dest):
		try :
			if isinstance(dest, str):
					dest = resolve1(doc.get_dest(dest))
			elif isinstance(dest, PSLiteral):
					dest = resolve1(doc.get_dest(dest.name))
			if isinstance(dest, dict):
					dest = dest['D']
			return dest
		except PDFDestinationNotFound :
			return None
	try:
		outlines = doc.get_outlines()

		for (level,title,dest,a,se) in outlines:
			pageno = None
			if dest:
					dest = resolve_dest(dest)
					if dest is None :
						continue
					pageno = pages[dest[0].objid]
			elif a:
					action = a.resolve()
					if isinstance(action, dict):
						subtype = action.get('S')
						if subtype and repr(subtype) == '/GoTo' and action.get('D'):
							dest = resolve_dest(action['D'])
							pageno = pages[dest[0].objid]
			s = e(title).encode('utf-8', 'xmlcharrefreplace')
			if pageno is not None:
				yield(level, s,pageno,totalPageNumber)
	except PDFNoOutlines:
		pass
	return


#Fonction interne D'extraction de la TOC sous forme d'u dict
def _extractToc(doc) :
	pdfDoc = {'totalPageNumber':0,'toc':[]};
	for(level,title,page,totalPageNumber) in  dumpoutline(doc):
		addToToc(pdfDoc['toc'],level,title,page)
		pdfDoc['totalPageNumber'] = totalPageNumber;
	return pdfDoc

#extraction de la toc
def extractToc(pdf_doc, pdf_pwd=''):
    """Return the table of contents (toc), if any, for this pdf file"""
    return with_pdf(pdf_doc, _extractToc, pdf_pwd)



	
# main
def main(argv):
	#for(level,titre,page) in dumpoutline("/home/fdellier/Livres Numeriques/La_Corse_pour_les_Nuls.pdf"):
	#	print (level,titre,page)
	obj = {'toc':extractToc("/home/fdellier/Livres Numeriques/La_Corse_pour_les_Nuls.pdf")}
	#pprint(obj)
	print(json.dumps(obj)) 
	#print(extractPageNumber("/home/fdellier/Livres Numeriques/La_Corse_pour_les_Nuls.pdf"))

if __name__ == '__main__': sys.exit(main(sys.argv))
