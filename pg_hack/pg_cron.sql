docker run -d --name cron \
  -e POSTGRES_USER=cron \
  -e POSTGRES_PASSWORD=cron \
  -e POSTGRES_DB=cron \
  -v ~/pg_changes:/var/lib/postgresql/pg_changes \
  -p 5433:5433 postgres

docker exec -it cron psql -U cron -d cron


CREATE TABLE IF NOT EXISTS last_sync (
    table_name TEXT PRIMARY KEY,
    last_run TIMESTAMP DEFAULT '1970-01-01 00:00:00'
);


INSERT INTO last_sync (table_name, last_run) 
VALUES ('users', '1970-01-01 00:00:00')
ON CONFLICT (table_name) DO NOTHING;

cron=# CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

INSERT INTO users (name, email, created_at, updated_at) VALUES
    ('Alice Johnson', 'alice@example.com', now(), now()),
    ('Bob Smith', 'bob@example.com', now(), now()),
    ('Charlie Brown', 'charlie@example.com', now(), now()),
    ('David White', 'david@example.com', now(), now()),
    ('Emma Williams', 'emma@example.com', now(), now()),
    ('Frank Miller', 'frank@example.com', now(), now()),
    ('Grace Hall', 'grace@example.com', now(), now()),
    ('Hank Adams', 'hank@example.com', now(), now()),
    ('Ivy Clark', 'ivy@example.com', now(), now()),
    ('Jack Evans', 'jack@example.com', now(), now());




cron=# CREATE OR REPLACE FUNCTION extract_changes()
RETURNS void AS $$
DECLARE
    last_run_time TIMESTAMP;
    new_last_run TIMESTAMP := now();
BEGIN
    -- Get last sync timestamp
    SELECT last_run INTO last_run_time FROM last_sync WHERE table_name = 'users';

    -- If last_run_time is NULL (first run), use a default timestamp
    IF last_run_time IS NULL THEN
        last_run_time := '1970-01-01 00:00:00';
    END IF;

    -- Export new or updated rows to CSV inside the Docker-mounted directory
    EXECUTE format(
        'COPY (SELECT * FROM users WHERE updated_at >= %L) TO ''/var/lib/postgresql/pg_changes/users_changes.csv'' WITH CSV HEADER',
        last_run_time
    );

    -- Update last sync time
    UPDATE last_sync SET last_run = new_last_run WHERE table_name = 'users';

END;
$$ LANGUAGE plpgsql;


SELECT extract_changes();

select * from last_sync;