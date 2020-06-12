all: amplitudes.pdf

amplitudes.pdf: amplitudes.tex *.tex
	pdflatex amplitudes
	pdflatex amplitudes

clean:
	@rm -f *.{log,aux,pdf,toc,bbl,lof,blg,out}

cleanaux:
	@rm -f *.{log,aux,toc,bbl,lof,blg,out}