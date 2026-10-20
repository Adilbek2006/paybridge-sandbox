PLANTUML ?= java -jar tools/plantuml.jar
.PHONY: test run diagrams report
test:
	pytest --cov=paybridge
run:
	uvicorn paybridge.main:app --app-dir src --reload
diagrams:
	$(PLANTUML) -tpng -o ../export diagrams/src/*.puml
	$(PLANTUML) -tsvg -o ../export diagrams/src/*.puml
report:
	python report/build_report.py
