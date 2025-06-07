TEST_OUTPUT := tests/repository_analysis.json
DOT_OUTPUT := tests/dependencies.dot


.PHONY: test

test: $(TEST_OUTPUT) $(DOT_OUTPUT)

$(TEST_OUTPUT):
	python -m pymoduleanalyzer.cli.main analyze repository --path . --json-output $@

$(DOT_OUTPUT):
	python -m pymoduleanalyzer.cli.main analyze graph --path . --output $@
