create-venv:
	python3 -m venv .venv;
	source .venv/bin/activate; 

setup:
	pip install -r requirements.txt;

run-local:
	python3 main.py

run-streamlit:
	streamlit run main.py