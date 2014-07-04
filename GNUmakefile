all: slides.html

clean:
	rm slides.html

slides.html: slides.asc custom.css
	/usr/local/bin/cdk --theme=twitter --custom-css=custom.css slides.asc
