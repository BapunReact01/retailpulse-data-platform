# RetailPulse Troubleshooting Guide

## Common Issues and Solutions

### Docker Issues

#### Issue: Docker compose fails to start

**Symptoms:**
- Error: "service "postgres_dw" refers to undefined network retailpulse_network"

**Solutions:**
1. Check if ports are already in use:
   ```bash
   netstat -ano | findstr :5432
   ```
2. Stop conflicting services or change ports in docker-compose.yml
3. Restart Docker Desktop

#### Issue: Out of memory errors

**Symptoms:**
ERROR: for postgres_ops Cannot start service postgres_ops: driver failed programming external connectivity

**Solutions:**
1. Check if ports are already in use:
   ```bash
   netstat -ano | findstr :5432
   ```
2. Stop conflicting services or change ports in docker-compose.yml
3. Restart Docker Desktop

#### Issue: Out of memory errors

**Symptoms:**
Container exited with code 137
**Solutions:**
1. Increase Docker memory allocation in Docker Desktop settings
2. Reduce Spark executor memory in .env file
3. Limit number of Spark workers

#### Issue: Containers cannot communicate

**Symptoms:**
Connection refused to spark-master:7077

**Solutions:**
1. Check all services are on the same network:
   ```bash
   docker network inspect retailpulse_network
   ```
2. Restart services:
   ```bash
   docker compose down
   docker compose up -d
   ```

### PostgreSQL Issues

#### Issue: Database connection refused

**Symptoms:**
psql: connection refused

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   docker compose ps postgres_ops
   ```
2. Check logs:
   ```bash
   docker compose logs postgres_ops
   ```
3. Verify port mapping in docker-compose.yml

### Spark Issues

#### Issue: Spark worker fails with rsync error

**Symptoms:**
rsync: command not found

**Solutions:**
This is a known issue with Alpine-based Spark images. Either:
1. Use a different Spark image (non-Alpine)
2. Install rsync in the container
3. Use Bitnami Spark images instead

### General Debugging Tips

#### Check Container Logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs postgres_ops

# Follow logs in real-time
docker compose logs -f spark-master