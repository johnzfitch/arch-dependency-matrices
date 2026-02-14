TEX = latexmk
TEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error

SRC = vectorhit_hybrid_metric_paper.tex
OUT = vectorhit_hybrid_metric_paper.pdf

.PHONY: all clean distclean watch

all: $(OUT)

$(OUT): $(SRC)
	$(TEX) $(TEXFLAGS) $(SRC)

watch:
	$(TEX) $(TEXFLAGS) -pvc $(SRC)

clean:
	rm -f *.aux *.fdb_latexmk *.fls *.log *.out *.toc *.synctex.gz *.bbl *.blg

distclean: clean
	rm -f $(OUT)
