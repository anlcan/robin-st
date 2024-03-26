.PHONY: upreq api st

upreq:
	pip install -r requirements.txt

api:
	uvicorn server:app --reload

st:
	streamlit run streamlit_app.py