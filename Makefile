SRCDIR = srcs

OUTDIR = output

SCREENDIR = screenshots

MAIN = main.py

SOURCES = $(wildcard $(SRCDIR)/*.py)

run:
	@echo "Data scraping loading..."
	@python3 $(SRCDIR)/$(MAIN)

show:
	@echo "Data scraping loading..."
	@python3 $(SRCDIR)/$(MAIN) noheadless

clean:
	@find $(SRCDIR) -name '*.pyc' -delete
	@find $(SRCDIR) -name '__pycache__' -type d -exec rm -rf {} +
	@echo "Compiled files deleted"
	@rm -rf $(OUTDIR)
	@echo "Output folder deleted"
	@rm -rf $(SCREENDIR)
	@echo "Screenshots folder deleted"

re: clean run
