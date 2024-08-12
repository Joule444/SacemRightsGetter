SRCDIR = srcs

MAIN = main.py

SOURCES = $(wildcard $(SRCDIR)/*.py)

run:
	python3 $(SRCDIR)/$(MAIN)

clean:
	find $(SRCDIR) -name '*.pyc' -delete
	find $(SRCDIR) -name '__pycache__' -type d -exec rm -rf {} +

re: clean run
