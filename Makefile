install:
	cd backend && pip install -r requirements.txt

run:
	cd backend && uvicorn app.main:app --reload

test:
	cd backend && pytest tests/

test-cov:
	cd backend && pytest --cov=app tests/

rm-cache:
	Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force

fe-install:
	cd frontend && npm install

fe-run:
	cd frontend && npm run dev

fe-test:
	cd frontend && npm run test

fe-test-cov:
	cd frontend && npm run coverage

fe-build:
	cd frontend && npm run build