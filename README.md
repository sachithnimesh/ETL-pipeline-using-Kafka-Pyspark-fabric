
# ETL Pipeline using Kafka, PySpark, and Microsoft Fabric

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline that streams data using **Apache Kafka**, processes it with **PySpark**, and uploads the final transformed data into **Microsoft Fabric Lakehouse** for visualization and analytics (e.g., with Power BI).

---

## 📁 Project Structure

```bash
Fabric task/
│
├── Power BI/
│   └── Transform.ipynb          # Power BI-related data transformation logic
│
├── json/                        # Contains raw JSON files (sample or streamed)
│
├── producer/                    # Kafka producer scripts to send JSON data
│
├── .env                         # Environment variables (API keys, Fabric config, etc.)
├── .gitignore                   # Git ignored files
├── docker-compose.yml          # Kafka and Zookeeper orchestration
├── requirements.txt            # Python dependencies
├── run method.txt              # Manual run instructions or steps
├── test.ipynb                  # Notebook for initial testing/debugging
├── upload_jsons_to_fabric.py   # Script to upload JSON data to Microsoft Fabric Lakehouse
├── Ingest_data_from_Kafka_to_Local.py #ingest data from Kafka to Local
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sachithnimesh/ETL-pipeline-using-Kafka-Pyspark-fabric.git
cd ETL-pipeline-using-Kafka-Pyspark-fabric
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows

pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file with the required credentials:

```env
FABRIC_WORKSPACE_ID=your_workspace_id
FABRIC_LAKEHOUSE_NAME=your_lakehouse_name
FABRIC_API_KEY=your_api_key
```

---

## ▶️ Run the Pipeline

### Step 1: Start Kafka Services

```bash
docker-compose up -d
```

### Step 2: Start Kafka Producer

Run the script(s) under the `producer/` folder to send JSON messages to a Kafka topic.

### Step 3: Process Data with PySpark

Use the `test.ipynb` or your own Spark job to consume the Kafka stream and transform the data.

### Step 4: Upload to Microsoft Fabric

```bash
python upload_jsons_to_fabric.py
```

This will push the transformed JSON files in the `json/` folder to your Fabric Lakehouse.

---

## 📊 Power BI Integration

Use the transformations in `Power BI/Transform.ipynb` and connect Power BI to your Microsoft Fabric workspace to visualize and analyze the uploaded data.

---

## 📄 Additional Notes

* Ensure your Microsoft Fabric environment is properly set up and API access is enabled.
* Check `run method.txt` for detailed manual steps or troubleshooting.
* Sample/test data should be placed in the `json/` directory if not streamed in real-time.

---

## 🚀 Technologies Used

* Apache Kafka
* PySpark
* Microsoft Fabric
* Power BI
* Docker
* Python

---
