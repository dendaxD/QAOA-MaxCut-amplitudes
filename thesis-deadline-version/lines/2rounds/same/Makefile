all: amplitudes-probabilities.pdf

amplitudes-probabilities.pdf: amplitudes-probabilities.tex *.tex
	pdflatex amplitudes-probabilities
	pdflatex amplitudes-probabilities

clean:
	@rm -f *.{log,aux,pdf,toc,bbl,lof,blg,out}

cleanaux:
	@rm -f *.{log,aux,toc,bbl,lof,blg,out}