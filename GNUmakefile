images := $(patsubst %,board-%.svg,blank numbers)

all: slides.html

images: $(images)

clean:
	rm -f slides.html
	rm -f board-*.svg
	rm -f board-*.png

slides.html: slides.asc custom.css $(images)
	cdk --theme=twitter --custom-css=custom.css slides.asc

board-%.svg: svg.py
	python3 svg.py $* > $@
