
docker run --name my_postgres -p 5432:5432 -v $(pwd)/data:/var/lib/postgresql/data --env-file ./.streamlit/secrets.toml -d postgres
