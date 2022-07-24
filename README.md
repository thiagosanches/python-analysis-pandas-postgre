# python-analysis-pandas-postgre

# The main data
The `filtered-data.csv` was a file with 3 columns:
`date`, `time`, `request_ip`.

I wanted to see the requests from every user on an interval of 5 minutes.

# Pandas

Attempt to run some analysis using pandas. 

Take a look on [main.py](./main.py) file.

I tested with small sample of data from the file `filtered-data.csv` with 1000 rows and worked perfectly. However, with the real file (4.5GB) on my machine it took forever and I was not able to get any data that I wanted, so I decided to perform the analysis on a database.

# PostgreSQL

Attempt to run some analysis using PostgreSQL.

I used the version: `14.4`.

First you have to create the container:

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

All the sub-sequent commands are assuming that you are running the queries inside the container. 

To run inside the container: 

- Enter in the container: `docker exec -it <container_id> bash`.
- Connect into the postgresql server: `psql -U postgres`.
- Create a database: `postgres=# CREATE DATABASE dbname;`.
- Connect to the database: `postgres=# \c dbname;`

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

### Import the CSV into the previous created table
This file can be huge!

You have to copy the `filtered-data.csv` into the mapped volume (`/custom/mount/pgdata/`).

It took less than 30 minutes to import a 4.5GB files with 86 million rows.

```sql
COPY data(date, time, request_ip)
FROM 'filtered-data.csv'
DELIMITER ','
CSV HEADER;
```
You can follow the operation using: `select * from pg_stat_progress_copy \watch 1`.

### Concatenate (if needed) date + time to create a timestamp column

```sql
SELECT request_ip, COUNT(request_ip) request_ip, 
to_timestamp(floor((extract('epoch' from TO_TIMESTAMP(concat(date, concat(' ', time)), 'YYYY/MM/DD/HH24:MI:ss')) / 300 )) * 300) AT TIME ZONE 'UTC' as interval_alias
FROM data GROUP BY request_ip, interval_alias
ORDER BY interval_alias ASC
LIMIT 5
```
You can use the `LIMIT 5` just to see if your data is fine, before going with the heavy query.


### Export the previous query into a csv file

```sql
COPY (
    SELECT request_ip, COUNT(request_ip) request_ip, 
    to_timestamp(floor((extract('epoch' from TO_TIMESTAMP(concat(date, concat(' ', time)), 'YYYY/MM/DD/HH24:MI:ss')) / 300 )) * 300) AT TIME ZONE 'UTC' as interval_alias
    FROM data GROUP BY request_ip, interval_alias
    ORDER BY interval_alias ASC
) TO '/tmp/resampled-data-2.csv' (format csv, delimiter ';');
```

The file will be saved on `/tmp/resampled-data-2.csv`, you have to move to `/var/lib/postgresql/data/pgdata`, to be able to copy outside of the container.

# Results

I'm not a data science specialist, but I got a better performance on PostgreSQL, I didn't create any index or so, but for the heavy query described above it tooks around 10 minutes to finish and save the file, way better than pandas. However, the effort was huge, probably there is something on pandas that can be tunned to speed up the things that I don't know.
