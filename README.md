# 📚 ETL Pipeline with Airflow, PostgreSQL, and OpenLibrary API

This project implements an ETL (Extract, Transform, Load) pipeline using **Apache Airflow**, deployed via **Docker Compose**. The pipeline extracts book data from the **OpenLibrary API**, transforms it as needed, and loads it into a **PostgreSQL** database.

---

## 🚀 Project Features

- ✅ **Airflow setup using Docker Compose**
- ✅ **PostgreSQL database integration**
- ✅ **Custom Airflow DAG to extract data from OpenLibrary API**
- ✅ **Data transformation and loading into PostgreSQL**
- ✅ Clean project structure and modular Python code

---

## 🛠️ Tech Stack

- [Apache Airflow](https://airflow.apache.org/)
- [Docker + Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org/)
- [Python 3](https://www.python.org/)
- [OpenLibrary API](https://openlibrary.org/developers/api)

---

## 📁 Project Structure

## Steps to install docker without GUI
Steps: Open PowerShell (Admin) and run:
- Check if WSL is enabled
```bash
wsl --list --verbose
```
Note: If WSL is not installed, proceed to the next step else skip next step.
- Install WSL2 and Ubuntu 22.04 LTS
```bash
   wsl --install -d Ubuntu-22.04
```
- If WSL is already installed, ensure it's set to version 2
```bash
wsl --set-default-version 2
```
- Install Docker Engine inside WSL
```bash
sudo apt update
sudo apt install -y docker.io
```
- Start and enable Docker
```bash
sudo systemctl enable --now docker
```
- Add your user to the Docker group
```bash
sudo usermod -aG docker $USER
```
- Test Docker
```bash
docker run hello-world
```
## Steps to set up Airflow

Follow the steps in [AirFlow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- Download YAML file - For windows use different cmd
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.3/docker-compose.yaml'
```
- Set up folders - For windows use differnt cmd
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
- start docker-compse
```bash
docker compose up airflow-init
docker compose up
```
