#
# "THE BEER-WARE LICENSE" (Revision 42):
# <08gr551@es.aau.dk> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy us a beer in return.
#

# EPS_DIR: Directory where the converted EPS files will be put
# IMG_SRC_DIR: Directory where the images sources are located 
EPS_DIR = eps
IMG_SRC_DIR = images

# All the files to check for changes
SRCS  = $(shell find . -name '*.tex')
SVGS  = $(wildcard images/*.svg)
EPSS  = $(wildcard images/*.eps)
DOTS  = $(wildcard images/*.dot)
PICS  = $(wildcard images/*.pic) 
DIAS  = $(wildcard images/*.dia)
#JPEGS = $(wildcard images/*.jpeg)

# All the SVG files which have a DOT version are found
SVGS_DOTS = $(addsuffix .svg, $(basename $(DOTS)))
EPSS_SVGS = $(addprefix $(EPS_DIR)/, $(notdir $(addsuffix .eps, $(basename $(SVGS_DOTS)))))

# All the SVG files which have a PIC version are found
SVGS_PICS = $(addsuffix .svg, $(basename $(PICS)))
EPSS_SVGS += $(addprefix $(EPS_DIR)/, $(notdir $(addsuffix .eps, $(basename $(SVGS_PICS)))))

# All the EPS files which have a SVG version are found
EPSS_SVGS +=  $(addprefix $(EPS_DIR)/, $(notdir $(addsuffix .eps, $(basename $(SVGS)))))

# All the EPS files which have a DIA version are found and change the directory to save the EPS image
EPSS_DIAS_NODIR = $(notdir $(addsuffix .eps, $(basename $(DIAS))))
EPSS_DIAS =   $(addprefix $(EPS_DIR)/, $(EPSS_DIAS_NODIR))



# The main tex file to compile
MAIN = article
TARGET = article

# The tex compiler 
# -pd option is used to for making dvi->ps->pdf output 
TEX = rubber -pd -W refs -W misc

# Declare PHONY targets
.PHONY: all force clean clean_img clean_eps clean_svg open fixme love

# LaTeX conversion rules

# Default target
all: $(MAIN).pdf
	@echo -e "\033[1m** Done compiling $(MAIN).pdf\033[0m"

$(MAIN).pdf: $(MAIN).tex $(SRCS) $(EPSS) $(EPSS_SVGS) $(EPSS_DIAS) $(SVGS_PICS)
	@echo -e "\033[1m** Compiling LaTeX documents\033[0m"
	@$(TEX) $(MAIN)
	@echo ""
	@echo -e "\033[1m** Removing temporary files\033[0m"
	rm -f */*.aux *.aux
	@echo ""

# Image conversion rules

# Use dia to convert .dia files to .eps files
$(EPS_DIR)/%.eps: $(IMG_SRC_DIR)/%.dia 
	@echo -e "\033[1m** Generating EPS from $<\033[0m"
	dia $< -t eps -e $@
	@echo ""

# Use inkscape to convert .svg files to .eps files
$(EPS_DIR)/%.eps: $(IMG_SRC_DIR)/%.svg 
	@echo -e "\033[1m** Generating EPS from $<\033[0m"
	inkscape -t -T --export-eps=$@ $<
	@echo ""
	
# Use dot to convert .dot files to .svg files
%.svg: %.dot 
	@echo -e "\033[1m** Generating SVG from $<\033[0m"
	dot -Tsvg -o $@ $<
	@echo ""

# Use pic2plot to convert .pic files to .svg files
%.svg: %.pic
	@echo -e "\033[1m** Generating SVG from $<\033[0m"
	pic2plot -Tsvg $< > $@
	cat $@ | egrep -ve "^<rect id=\"background\"" > ./tmp && mv ./tmp $@
	@echo ""



# Clean up rules 

force: clean all

clean:
	@echo -e "\033[1m** Cleaning up\033[0m"
	rm -f *.toc *.aux *.pdf *.ps *.log *.lof *.bbl *.blg *.dvi */*.aux *.glo *.gls *.ilg *.nls *.nlo *.idx *.ind *.out *.ist

clean_img: clean_eps clean_svg

# A rule for removing all EPS files which have a SVG and DIA version
clean_eps: 
	rm -f $(EPSS_SVGS) $(EPSS_DIAS)

# A rule for removing all SVG files which have a DOT version
clean_svg: 
	rm -f $(SVGS_DOTS) $(SVGS_PICS)

# Open the compiled pdf file - remember to set the PDFREADER env var
open: $(MAIN).pdf
	@echo -e "\033[1mOpening $(MAIN).pdf\033[0m"
	@./countfixme
	${PDFREADER} $(MAIN).pdf
	@echo ""
	
# Count fixmes
fixme: all
	@echo ""
	@echo -e "\033[1m** Counting FiXMEs\033[0m"
	@./countfixme

# Well...
love: 
	@echo -e "not war?"
