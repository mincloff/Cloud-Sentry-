# 🛡️ Cloud Guardian | AWS FinOps Auditor

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![AWS Boto3](https://img.shields.io/badge/AWS_Boto3-SDK-orange.svg)

## 📌 The Problem
Developers demand autonomy to spin up cloud resources quickly, but this often leads to "Cloud Sprawl"—abandoned databases, unattached storage, and idle load balancers that waste thousands of dollars. Organizations track spend, but often fail to remediate it effectively.

## 💡 The Solution
**Cloud Guardian** is a FinOps (Cloud Financial Management) tool that acts as an automated janitor for your AWS environment. It scans for structural waste and provides a Django-powered dashboard highlighting exact resources and their estimated monthly financial drain.

## ⚙️ Features (The 80/20 Waste Scan)
Currently, the tool scans for the most common sources of AWS waste:
- **Storage:** Unattached EBS Volumes (`available` state) & S3 Buckets missing Lifecycle Policies.
- **Databases:** Idle RDS Instances & Orphaned Manual RDS Snapshots.
- **Networking:** Unassociated Elastic IPs, Idle Load Balancers (ELBv2), and active NAT Gateways.
- **Compute:** "Stopped" EC2 instances that are still incurring hidden EBS storage costs.

## 🚀 Quick Start / Local Setup

### 1. Clone & Environment setup
```bash
git clone [https://github.com/YOUR_USERNAME/cloud-guardian.git](https://github.com/YOUR_USERNAME/cloud-guardian.git)
cd cloud-guardian
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt