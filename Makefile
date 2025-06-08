TEST_OUTPUT := tests/repository_analysis.json
DOT_OUTPUT := tests/dependencies.dot
GROUPED_OUTPUT := grouped_diagram.mmd
CLEAN_OUTPUT := clean_diagram.mmd
HTML_OUTPUT := repo_analysis.html


.PHONY: test analyze diagrams clean

test: $(TEST_OUTPUT) $(DOT_OUTPUT)

analyze: $(TEST_OUTPUT) $(GROUPED_OUTPUT) $(CLEAN_OUTPUT) $(HTML_OUTPUT)

diagrams: $(GROUPED_OUTPUT) $(CLEAN_OUTPUT) $(DOT_OUTPUT)

$(TEST_OUTPUT):
	python -m pymoduleanalyzer.cli.main analyze repository --path . --json-output $@

$(DOT_OUTPUT):
	python -m pymoduleanalyzer.cli.main analyze graph --path . --output $@

$(GROUPED_OUTPUT):
	python generate_grouped_mermaid.py

$(CLEAN_OUTPUT):
	python -m pymoduleanalyzer.cli.main analyze graph --path . --output $@ --format mermaid

$(HTML_OUTPUT):
	python generate_interactive_html.py

clean:
	rm -f $(TEST_OUTPUT) $(DOT_OUTPUT) $(GROUPED_OUTPUT) $(CLEAN_OUTPUT) $(HTML_OUTPUT)
	rm -f detailed_analysis.json analysis.json repo_diagram.mmd project_diagram.mmd
