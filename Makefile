start:
	docker compose up --build

migrate:
	docker compose exec web	alembic upgrade head
