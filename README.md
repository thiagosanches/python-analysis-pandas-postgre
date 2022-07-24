# python-analysis-pandas

# Pandas

Attempt to run some analysis using pandas.

# PostgreSQL

Attempt to run some analysis using PostgreSQL.

### Create a postgresql container

```bash
docker run -d \
--name some-postgres \
-p 5432:5432 \
-e POSTGRES_PASSWORD=forabozo \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v /custom/mount:/var/lib/postgresql/data \
postgres
```

### Create a table that you want to import the data (csv)

```sql
CREATE TABLE data (
  id SERIAL,
  date DATE,
  time VARCHAR(255),
  request_ip VARCHAR(255),
  PRIMARY KEY (id)
)
```

### Copy the CSV into the previous created table
You have to copy the `filtered-data.csv` into the mapped volume (`/custom/mount/pgdata/`).

```sql
COPY data(date, time, request_ip)
FROM 'filtered-data.csv'
DELIMITER ','
CSV HEADER;
```
