End-to-End Azure Data Platform – Final Report

Course: CST89xx  • Project Length: 14 weeks  • Group: <Group # / Members>

Title: 

Author(s): 
Date: <Month DD, 2025>

⸻

0. Executive Summary (½–1 page)

A concise overview of the business problem, data sources, target users, and the solution you built on Azure. Summarize outcomes (e.g., latency achieved, data freshness, analytics delivered, cost tier).
	•	Business objective: <What decision/outcome are we enabling?>
	•	Data sources: <Kaggle dataset(s), streaming source(s)>
	•	Core platform: Azure (ADF, ADLS Gen2, Databricks/Synapse, Event Hubs, Stream Analytics, Cognitive Services, Warehouse)
	•	Key results: <SLAs, dashboard KPIs, model accuracy, cost/month>

⸻

1. Use Case (1–2 pages)

1.1 Problem Statement

Describe the domain and pain points. Why is a data platform required now? What decisions depend on this platform?

1.2 Stakeholders & Users
	•	Business stakeholders: <e.g., Operations, Marketing>
	•	Data consumers: <Analysts, Data Scientists, Apps>
	•	Operational owners: <Data Engineering, Cloud Ops>

1.3 Success Criteria & KPIs

List measurable targets (e.g., daily ingestion volume, time-to-dashboard < 15 min, query latency < 5 sec, model F1 ≥ 0.80).

1.4 Datasets (Kaggle)
	•	Dataset name & link: <Kaggle dataset(s)>
	•	Schema summary: <tables, columns, granularity>
	•	Data volume: <rows/GB>
	•	Data freshness: <batch cadence / streaming>
	•	Data sensitivity: <PII? compliance needs?>

Note: Visualizations don’t count toward page length. Include a table or small ERD of the core dataset.

⸻

2. Reference Architecture & Services (2–3 pages)

2.1 Reference Architecture Narrative

Explain the end‑to‑end flow from ingestion to consumption. Include batch + streaming paths, medallion layers, and security boundaries.

flowchart LR
  subgraph Source[Sources]
    K[Kaggle Batch Files]
    API[External API (optional)]
    IOT[Event Producers]
  end

  K -->|Batch copy| ADF((Azure Data Factory))
  API --> ADF
  IOT --> EH[(Event Hubs)] --> ASA((Stream Analytics))

  ADF --> ADLS[(ADLS Gen2 Bronze)]
  ASA --> ADLS

  ADLS --> DBX((Databricks / Synapse Spark))
  DBX --> ADLS_Silver[(ADLS Gen2 Silver)]
  DBX --> ADLS_Gold[(ADLS Gen2 Gold)]

  ADLS_Gold --> WH[(Synapse Dedicated SQL Pool / Fabric Warehouse)]
  ADLS_Gold --> PBI[(Power BI / Fabric Lakehouse)]

  ADLS_Silver --> AI[(Azure Cognitive Services / Azure ML)]
  AI --> WH

  WH --> BI[Dashboards & Reports]

2.2 Azure Services Map & Rationale

Capability	Service	Why this service	Alternatives
Object storage, data lake	Azure Data Lake Storage Gen2	Hierarchical namespaces, ACLs, low-cost at scale	Blob Storage (basic), Fabric OneLake
Batch orchestration	Azure Data Factory	GUI pipelines, Mapping Data Flows, triggers, integration runtime	Synapse Pipelines, Databricks Jobs
Streaming ingestion	Azure Event Hubs	High-throughput event ingestion	Kafka on HDInsight / Confluent
Stream processing	Azure Stream Analytics	SQL-like streaming queries, easy BI output	Spark Structured Streaming
Transform/ML (big data)	Databricks or Synapse Spark	Distributed compute, notebooks, Delta Lake	Fabric Lakehouse
Warehouse (SQL)	Synapse Dedicated SQL Pool / Fabric Warehouse	MPP analytics, T‑SQL access	Azure SQL DB Hyperscale
AI add‑on	Azure AI Language / Vision	No-ML ops, prebuilt models for text/image	Azure ML custom models
Monitoring	Log Analytics + Azure Monitor	Central logs/metrics, KQL	Datadog, Grafana
Security	Entra ID, Key Vault, Defender for Cloud	Identity, secrets, posture management	—

2.3 Data Modeling & Zones

Describe Bronze → Silver → Gold layers, partitioning strategy, Delta format, Slowly Changing Dimensions (if any), and semantic models for BI.

⸻

3. Data Warehousing Design (1–2 pages)

3.1 Schema Design
	•	Model type: Star schema / Data Vault / Lakehouse tables
	•	Fact tables: <grain, measures>
	•	Dimensions: <conformed dims, SCD approach>

3.2 Performance & Cost Optimizations
	•	Partitioning & Z‑ordering
	•	Materialized views in Synapse / Fabric
	•	Caching and result set reuse
	•	Autoscale settings & workload management

⸻

4. Big Data Transformations & Advanced Analytics (2–3 pages)

4.1 Mapping Data Flows (ADF)
	•	Source/sink datasets, schema drift handling
	•	Derived columns, joins, aggregates, window functions
	•	Data quality (null checks, type enforcement)

4.2 Notebooks (Spark / Python)
	•	Sample transformations (cleaning, normalization, feature engineering)
	•	Persist as Delta in Silver/Gold
	•	Advanced analytics:
	•	Forecasting / anomaly detection
	•	Classification/regression example
	•	Model tracking (MLflow if using Databricks)

Include snippets or pseudocode; full code can be in an appendix or repo.

⸻

5. Real‑time Ingestion & Analytics (1–2 pages)

5.1 Event Hubs Producers

Simulate producers (Python script or Azure Function) and event schema.

5.2 Stream Analytics Job
	•	Query (e.g., windowed aggregations)
	•	Output sinks (ADLS Gold, Power BI)
	•	Latency and throughput measurements

5.3 Integration with Warehouse/BI

Explain how streaming data lands in near real‑time dashboards alongside batch data.

⸻

6. Add AI with Cognitive Services (1–2 pages)

6.1 Scenario & Model

Choose a prebuilt capability aligned to your data:
	•	Language: sentiment, key phrase extraction, PII detection
	•	Vision: OCR for receipts/images (if applicable)

6.2 Architecture Integration

Where inference runs (notebook, ADF custom activity) and how outputs flow into Silver/Gold/BI.

6.3 Results

Accuracy notes, examples before/after enrichment, and business impact.

⸻

7. Security, Governance & Compliance (1–2 pages)
	•	Identity & Access: Entra ID groups, RBAC, ACLs on ADLS
	•	Secrets: Key Vault for keys/connection strings
	•	Network: Private endpoints (if configured), IP restrictions
	•	Data protection: Encryption at rest/in transit
	•	Posture & alerts: Defender for Cloud recommendations
	•	Lineage & catalog: Purview (optional)

⸻

8. Deployment Process (1–2 pages)

8.1 Approach

Portal / IaC (Bicep/Terraform) / CLI. Describe why chosen.

8.2 Environments & Parameters

Dev/Test/Prod, naming conventions, tags, region choice, scaling tiers.

8.3 Steps
	1.	Provision resource group & storage
	2.	Create ADF/Databricks/Synapse/Event Hubs
	3.	Configure Linked Services, datasets, Spark clusters
	4.	Publish pipelines & notebooks
	5.	Configure Stream Analytics input/output
	6.	Set up Cognitive Services + keys in Key Vault
	7.	Create SQL objects / Lakehouse tables
	8.	Publish Power BI report / Fabric item

Include screenshots of key deployments and success states.

⸻

9. Testing & Validation (1–2 pages)

9.1 Functional Tests
	•	Ingestion completeness, schema validation, DQ checks
	•	Transformation logic correctness
	•	AI inference outputs within expected ranges

9.2 Performance & Reliability
	•	Batch runtimes, streaming end‑to‑end latency
	•	Autoscaling behavior under load

9.3 Monitoring & Troubleshooting
	•	Log Analytics KQL queries (include a few)
	•	ADF pipeline run histories, failure alerts

⸻

10. Results, Visualizations & Business Insights (1–2 pages)

Summarize BI visuals/KPIs and how stakeholders use them. Explain insights generated and decisions enabled.

Insert screenshots—note they do not count toward page limit.

⸻

11. Limitations & Future Work (½–1 page)

Be explicit about trade‑offs (cost tiers, feature gaps, data quality, model scope) and propose next‑step roadmap.

⸻

12. Conclusion (½ page)

Short wrap‑up reiterating objectives, architecture, and achieved outcomes.

⸻

13. References (APA)

Use APA for any sources, SDK docs, and diagrams. References do not count toward page limit.

⸻

Appendices (optional)
	•	A. Detailed schemas & data dictionary
	•	B. IaC snippets (Bicep/Terraform), ARM exports
	•	C. Notebook code and ADF pipeline JSON
	•	D. Stream Analytics query listing
	•	E. KQL queries for monitoring

⸻

📸 Evidence & Screenshot Checklist (for Section 10)
	•	Resource group & region
	•	ADLS Gen2 containers (bronze/silver/gold)
	•	ADF pipelines (trigger runs success)
	•	Databricks/Synapse notebook runs
	•	Event Hubs namespace + Stream Analytics job running
	•	Cognitive Services resource + sample inference output
	•	Warehouse tables and successful queries
	•	Power BI / Fabric report with refreshed dataset
	•	Log Analytics workspace with KQL results

⸻

📑 Formatting Checklist (Assignment Requirements)
	•	15–20 pages, double‑spaced, Times New Roman 12 pt
	•	Use subheadings; number all pages
	•	Long quotes/lists are single‑spaced
	•	Clean and professional look
	•	Submit Word file with full name in filename

⸻

🧭 How to Use This Template

Replace angle‑bracket sections with your content, and expand each subsection to meet the page count. Keep visuals separate (not counted). Keep a running list of screenshots as you deploy, and paste them into Section 10 and/or Appendices.