# Docker, SQL, and Terraform — Answers & Explanations

## Question 1. Understanding Docker Images

Run Docker with the `python:3.13` image. Use an entrypoint bash to interact with the container.

**What's the version of pip in the image?**

- 25.3  
- 24.3.1  
- 24.2.1  
- 23.3.1  

**ANSWER:** 25.3  

I ran:

```bash
docker run -it --entrypoint bash python:3.13
```

After the prompt changed to:

```text
root@370bc7a8c44a:/#
```

I confirmed the pip version with:

```bash
pip --version
```

---

## Question 2. Understanding Docker Networking and docker-compose

Given the following `docker-compose.yaml`, what is the hostname and port that **pgAdmin** should use to connect to the **Postgres** database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

**ANSWER:** postgres:5432 and db:5432  

Explanation: Port 5432 is the internal Postgres port. Containers can communicate using service or container names inside the Docker network.

---

## Question 3. Counting Short Trips

Trips in November 2025 with trip_distance ≤ 1 mile.

**ANSWER:** 8,007  

```sql
SELECT COUNT(*)
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1.0;
```

---

## Question 4. Longest Trip for Each Day

**ANSWER:** 2025-11-14  

```sql
SELECT 
    CAST(lpep_pickup_datetime AS DATE) AS pickup_day,
    MAX(trip_distance) AS max_dist
FROM green_taxi_data
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_dist DESC
LIMIT 1;
```

---

## Question 5. Biggest Pickup Zone

**ANSWER:** East Harlem North  

```sql
SELECT 
    zones."Zone",
    SUM(green_taxi_data.total_amount) AS total_money
FROM green_taxi_data
JOIN zones 
  ON green_taxi_data."PULocationID" = zones."LocationID"
WHERE CAST(lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY zones."Zone"
ORDER BY total_money DESC;
```

---

## Question 6. Largest Tip

**ANSWER:** Yorkville West  

```sql
SELECT 
    do_zones."Zone" AS dropoff_zone_name,
    MAX(g.tip_amount) AS largest_tip
FROM green_taxi_data g
JOIN zones pu_zones 
  ON g."PULocationID" = pu_zones."LocationID"
JOIN zones do_zones 
  ON g."DOLocationID" = do_zones."LocationID"
WHERE pu_zones."Zone" = 'East Harlem North'
  AND g.lpep_pickup_datetime >= '2025-11-01'
  AND g.lpep_pickup_datetime < '2025-12-01'
GROUP BY dropoff_zone_name
ORDER BY largest_tip DESC
LIMIT 1;
```

---

## Question 7. Terraform Workflow

**ANSWER:**  
terraform init → terraform apply -auto-approve → terraform destroy
