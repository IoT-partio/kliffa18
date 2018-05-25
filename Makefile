init:
	cd gateway_raspberry; pip install pipenv && \
	pipenv install --dev
test:
	cd gateway_raspberry/ingest_api; pipenv run py.test