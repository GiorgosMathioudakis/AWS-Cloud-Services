# AWS-Powered Cloud Services Projects 🚀

This repository contains the implementations for three major assignments of the **HY452 / CS452 - Introduction to the Science and Technology of Services** course at the University of Crete (2024-2025). The focus of these projects is on building, deploying, and integrating **serverless, RESTful, and distributed systems** using **Amazon Web Services (AWS)** and other cloud technologies.

---

## 📁 Project Overview

### 🧩 Assignment 1: Serverless Game Backend on AWS
**Focus**: Serverless architecture for game user management and leaderboard system.

🔧 **Key AWS Components Used**:
- **API Gateway** – RESTful endpoints for registration, login, leaderboard, and asset retrieval.
- **Lambda** – Stateless backend logic for all API operations.
- **DynamoDB** – User and leaderboard data storage.
- **Step Functions** – Orchestrated workflows for user registration and login.
- **S3** – Storage and retrieval of background game assets.
- **SNS / SQS** – Event-driven processing and high-score notifications.

🎮 **Functionalities**:
- Register/login users via `/register` and `/login`.
- Submit and retrieve scores using `/leaderboard`.
- Fetch game backgrounds via S3.
- Notifications sent when high scores are achieved.

📷 **Screenshots & Implementation**: Included in `Assignment1_Report.pdf`.

---

### 🌍 Assignment 2: RESTful Web Services with Spring Boot & Jersey
**Focus**: Development and deployment of RESTful services with Java frameworks and XML/JSON processing.

💡 **Key Highlights**:
- Built REST APIs using **Spring Boot** and **Jersey**.
- Deployed services on **AWS EC2**.
- Developed a Spring Boot service to expose geographic data via endpoints.
- Implemented an interactive client using **DBpedia Spotlight API** for named entity annotation.
- Used **Swagger (OpenAPI 3)** for API documentation.
- Bonus: Developed SOAP-based services using **Apache Axis2**.

🗺️ **Features**:
- Lookup country/rivers data from XML dataset.
- REST endpoints for geographic queries.
- Text annotation client linked to DBpedia.

📷 **Screenshots & Swagger API Doc**: Included in `Assignment2_Report.pdf`.

---

### 🎮 Assignment 3: Game-Theoretic Resource Allocation Simulation
**Focus**: Cloud-based simulation of task allocation using utility-based optimization.

🔧 **AWS Integration**:
- Each simulated user was hosted on a dedicated **EC2 instance**.
- Used **SQS** for task submission queues.
- **Lambda functions** coordinated resource management and triggered evaluation.
- Final results and utility values were stored in **DynamoDB**.

📊 **System Flow**:
- Users compute best resource allocations using brute-force optimization.
- Submit allocation vectors to the cloud provider.
- Provider computes completion time, expenses, and sends back results.
- Optional: Petri Net modeling and reachability graph for task/resource interaction.

📷 **Screenshots & Architecture Diagrams**: Included in `Assignment3_Report.pdf`.

---

## 🌩️ Tech Stack
- **AWS Services**: Lambda, API Gateway, DynamoDB, S3, SNS, SQS, Step Functions, EC2
- **Languages**: Python, Java (Spring Boot, Jersey), JSON, XML
- **Frameworks**: Spring Boot, Jersey, Axis2, Swagger, DBpedia Spotlight
- **Tools**: Postman, AWS Console, Eclipse, GitHub



## ✅ Status
All projects completed, tested, and deployed successfully on AWS. Each includes a PDF report with implementation notes, AWS screenshots, and results.

---

## 📄 License
This project is for educational purposes and part of coursework for HY452 at the University of Crete. All code is original unless otherwise referenced.
