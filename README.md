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
### Concatenate (if needed) date + time to create a timestamp column
You can use the `LIMIT 5` just to see if your data is fine.
```sql
SELECT request_ip, COUNT(request_ip) request_ip, 
to_timestamp(floor((extract('epoch' from TO_TIMESTAMP(concat(date, concat(' ', time)), 'YYYY/MM/DD/HH24:MI:ss')) / 300 )) * 300) AT TIME ZONE 'UTC' as interval_alias
FROM data GROUP BY request_ip, interval_alias
ORDER BY interval_alias ASC
LIMIT 5
```

### Export the previous query into a csv file
The file will be saved on `/tmp/resampled-data-2.csv`, you have to move to `/var/lib/postgresql/data/pgdata`.
```sql
COPY (
    SELECT request_ip, COUNT(request_ip) request_ip, 
    to_timestamp(floor((extract('epoch' from TO_TIMESTAMP(concat(date, concat(' ', time)), 'YYYY/MM/DD/HH24:MI:ss')) / 300 )) * 300) AT TIME ZONE 'UTC' as interval_alias
    FROM data GROUP BY request_ip, interval_alias
    ORDER BY interval_alias ASC
) TO '/tmp/resampled-data-2.csv' (format csv, delimiter ';');
```

