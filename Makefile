.PHONY: upreq api st


b:
	docker build -t robin-st:render .
d: b
	docker run -p 8080:8000 robin-st:render
reg:
	docker build --platform linux/amd64 -t robin-st:render .
	docker tag robin-st:render  ghcr.io/anlcan/robin-st:render
	docker push ghcr.io/anlcan/robin-st:render
	http https://api.render.com/deploy/srv-co1kmqf79t8c73ceqrig?key=aadyiL-3WA0

upreq:
	pip install -r requirements.txt

api:
	#source evn/bin/activate
	uvicorn server:app --reload

st:
	streamlit run streamlit_app.py