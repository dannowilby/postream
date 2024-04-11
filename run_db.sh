
docker run --name my_postgres -p 5432:5432 -v $(pwd)/data:/var/lib/postgresql/data --env-file ./postgres.env -d postgres
