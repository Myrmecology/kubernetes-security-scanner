# Kubernetes Security Scanner

A comprehensive security auditing tool for Kubernetes clusters that identifies misconfigurations, security vulnerabilities, and compliance violations. This project demonstrates expertise in cloud security, DevOps practices, and Kubernetes cluster management.

## Table of Contents

- [What This Project Does](#what-this-project-does)
- [What is Kubernetes?](#what-is-kubernetes)
- [What is Docker?](#what-is-docker)
- [Why This Project Matters](#why-this-project-matters)
- [Technical Architecture](#technical-architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Understanding the Results](#understanding-the-results)
- [Demo Scenarios](#demo-scenarios)
- [Project Structure](#project-structure)
- [Security Checks Performed](#security-checks-performed)
- [Technologies Used](#technologies-used)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## What This Project Does

The Kubernetes Security Scanner is a Python-based tool that connects to Kubernetes clusters and performs automated security audits. It examines your cluster configuration and identifies common security misconfigurations that could lead to:

- Container breakouts and host compromise
- Unauthorized access to cluster resources
- Lateral movement between pods
- Resource exhaustion attacks
- Data exfiltration

The scanner generates detailed reports with:
- Severity-rated findings (CRITICAL, HIGH, MEDIUM, LOW)
- Specific affected resources
- Clear explanations of each security issue
- Actionable remediation steps
- Export capabilities for integration with CI/CD pipelines

This tool is designed for DevOps engineers, security professionals, and developers who want to ensure their Kubernetes deployments follow security best practices.

---

## What is Kubernetes?

### Overview

Kubernetes (often abbreviated as K8s - "K" + 8 letters + "s") is an open-source container orchestration platform originally developed by Google and now maintained by the Cloud Native Computing Foundation (CNCF). As of December 2025, Kubernetes is the de facto standard for deploying, scaling, and managing containerized applications in production environments.

### What Problem Does Kubernetes Solve?

In modern application development, applications are broken down into smaller, independent services (microservices) that run in containers. While containers solve many deployment problems, managing hundreds or thousands of containers manually becomes impossible. Kubernetes automates:

- **Deployment:** Rolling out new versions of applications without downtime
- **Scaling:** Automatically adding or removing container instances based on load
- **Self-healing:** Restarting failed containers and replacing unhealthy nodes
- **Load balancing:** Distributing network traffic across multiple container instances
- **Service discovery:** Allowing services to find and communicate with each other
- **Storage orchestration:** Managing persistent data for stateful applications
- **Secret management:** Securely distributing credentials and sensitive configuration

### Key Kubernetes Concepts

**Cluster:** A set of machines (nodes) that run containerized applications managed by Kubernetes.

**Node:** A physical or virtual machine in the cluster. Nodes can be worker nodes (running applications) or control plane nodes (managing the cluster).

**Pod:** The smallest deployable unit in Kubernetes. A pod contains one or more containers that share storage and network resources. Containers in a pod are always scheduled together on the same node.

**Container:** A lightweight, standalone package that contains everything needed to run an application (code, runtime, libraries, dependencies). Containers run inside pods.

**Service:** A stable network endpoint that provides access to a set of pods, enabling communication between different parts of an application.

**Namespace:** A way to divide cluster resources between multiple users or teams, providing logical isolation.

**Deployment:** Describes the desired state for pods and handles rolling updates and rollbacks.

**ConfigMap and Secret:** Objects that store configuration data and sensitive information (like passwords) separately from application code.

### Why Kubernetes Security Matters

Kubernetes clusters are complex distributed systems with many moving parts. A single misconfiguration can expose an entire cluster to compromise. Common security risks include:

- Containers running with root privileges
- Overly permissive access controls (RBAC)
- Missing network segmentation between services
- Exposed sensitive data in configuration
- Unpatched vulnerabilities in container images
- Unrestricted communication with external networks

This is where the Kubernetes Security Scanner comes in - it automatically identifies these misconfigurations before they can be exploited.

### Real-World Usage

As of December 2025, Kubernetes is used by:

- Major cloud providers (AWS EKS, Azure AKS, Google GKE)
- Fortune 500 companies for production workloads
- Startups building cloud-native applications
- Government agencies for secure application deployment
- Financial institutions for high-availability systems

---

## What is Docker?

### Overview

Docker is an open-source platform for developing, shipping, and running applications in containers. Released in 2013, Docker revolutionized software deployment by making containers accessible and practical for everyday use. As of December 2025, Docker remains the most popular container runtime and is used by millions of developers worldwide.

### Containers vs. Virtual Machines

**Traditional Approach (Virtual Machines):**
A virtual machine runs a complete operating system on top of a hypervisor, including its own kernel, libraries, and applications. Each VM requires significant resources (memory, CPU, storage) and takes minutes to start.

**Container Approach (Docker):**
Containers share the host operating system's kernel but run in isolated user spaces. Each container includes only the application code and its dependencies. Containers are:
- Lightweight (megabytes instead of gigabytes)
- Fast to start (seconds instead of minutes)
- Resource-efficient (can run many more containers than VMs on the same hardware)
- Portable (runs consistently across development, testing, and production)

### How Docker Works

Docker uses several Linux kernel features to create isolated environments:

**Namespaces:** Isolate processes so containers can't see or affect each other
**Control groups (cgroups):** Limit CPU, memory, and I/O resources
**Union file systems:** Layer file system changes efficiently
**Container runtime:** Manages the container lifecycle (create, start, stop, delete)

### Docker Components

**Docker Engine:** The core software that runs and manages containers on a host machine.

**Docker Image:** A read-only template containing the application code, runtime, libraries, and dependencies. Images are built from a Dockerfile (a text file with build instructions).

**Docker Container:** A running instance of a Docker image. You can run multiple containers from the same image.

**Docker Hub:** A public registry where developers share container images. You can pull official images (like nginx, python, ubuntu) or publish your own.

**Dockerfile:** A text file that contains instructions for building a Docker image. Example:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Docker in This Project

In the Kubernetes Security Scanner project, Docker serves two purposes:

1. **As a container runtime for Minikube:** Minikube uses Docker to create a local Kubernetes cluster. Instead of needing separate virtual machines, Minikube runs Kubernetes components in Docker containers.

2. **For packaging the scanner itself:** The project includes a Dockerfile that packages the security scanner as a container, making it easy to run anywhere without installing Python dependencies.

### Why Docker Matters for Kubernetes

Kubernetes orchestrates containers, but it doesn't create them - that's Docker's job (or other container runtimes like containerd or CRI-O). Understanding Docker is fundamental to working with Kubernetes because:

- Container images define what runs in your pods
- Dockerfile best practices directly impact Kubernetes security
- Container security issues become Kubernetes security issues
- Debugging Kubernetes often requires understanding container internals

---

## Why This Project Matters

### Industry Relevance

As of December 2025, Kubernetes security is a critical concern across the technology industry:

- **Cloud adoption:** Over 90% of enterprises use containers in production
- **Security breaches:** Misconfigured Kubernetes clusters are a leading cause of cloud security incidents
- **Compliance requirements:** Industries like finance and healthcare require documented security controls
- **DevSecOps movement:** Security is shifting left into the development process

### Skills Demonstrated

This project showcases proficiency in:

**Cloud & DevOps:**
- Kubernetes architecture and API
- Container security principles
- Infrastructure as Code (IaC)
- CI/CD pipeline integration

**Programming & Software Engineering:**
- Python development
- API client design
- Modular architecture
- Unit testing with mocks
- Error handling and logging

**Security:**
- RBAC (Role-Based Access Control) analysis
- Pod Security Standards
- Network policy validation
- Least privilege principles
- Threat modeling

**Professional Practices:**
- Git version control
- Documentation
- Code quality tools (linting, formatting)
- Dependency management
- Security-first development

### Career Applications

This project is valuable for roles in:
- Cloud Security Engineer
- DevOps Engineer
- Site Reliability Engineer (SRE)
- Kubernetes Administrator
- Security Analyst
- Platform Engineer

---

## Technical Architecture

### High-Level Design

The scanner follows a modular architecture with clear separation of concerns:
```
User → Scanner (Orchestrator) → Security Checkers → Kubernetes API
                ↓
         Report Generator → Output (Console/JSON)
```

### Components

**Main Scanner (scanner.py):**
Entry point and orchestration. Handles command-line arguments, establishes cluster connection, coordinates security checks, and triggers report generation.

**Kubernetes Client (k8s_client.py):**
Abstraction layer over the Kubernetes Python client. Provides simplified methods for querying cluster resources and handles authentication/configuration.

**Security Checkers (checks/):**
Independent modules that each focus on a specific security domain:
- Pod Security: Container configurations, privileges, capabilities
- RBAC: Role bindings, service accounts, permissions
- Network Policy: Traffic controls and segmentation
- Resource Limits: CPU/memory constraints

**Reporter (reporter.py):**
Formats findings into human-readable console output or machine-readable JSON for integration with other tools.

### Data Flow

1. User executes scanner with optional parameters (namespace, output format)
2. Scanner connects to Kubernetes cluster using kubeconfig credentials
3. Scanner retrieves list of namespaces to audit
4. For each namespace, scanner executes all security checkers in sequence
5. Each checker queries relevant Kubernetes resources via the API
6. Checkers analyze configurations against security best practices
7. Checkers return lists of findings (issues discovered)
8. Scanner aggregates all findings from all checkers
9. Reporter processes findings and generates formatted output
10. Results displayed to user or saved to file

### Security Model

The scanner itself follows security best practices:
- Read-only access to cluster (never modifies resources)
- Minimal required RBAC permissions
- No secrets stored or logged
- Runs as non-root user in containerized deployments
- Validates all API responses
- Secure dependency management

---

## Prerequisites

Before installing and running the Kubernetes Security Scanner, ensure you have the following installed on your system:

### Required Software

**Python 3.8 or higher**
- Check version: `python --version` or `python3 --version`
- Download: https://www.python.org/downloads/
- The scanner is tested on Python 3.8, 3.9, 3.10, 3.11, and 3.12

**pip (Python package installer)**
- Usually comes with Python
- Check version: `pip --version` or `pip3 --version`
- Upgrade: `python -m pip install --upgrade pip`

**kubectl (Kubernetes command-line tool)**
- Kubernetes CLI for interacting with clusters
- Check version: `kubectl version --client`
- Installation:
  - Windows: `choco install kubernetes-cli`
  - macOS: `brew install kubectl`
  - Linux: Follow official docs at https://kubernetes.io/docs/tasks/tools/

**A Kubernetes Cluster**

You need access to a Kubernetes cluster. Options include:

**Option 1: Minikube (Recommended for learning/demo)**
- Local single-node cluster for development
- Check version: `minikube version`
- Installation:
  - Windows: `choco install minikube`
  - macOS: `brew install minikube`
  - Linux: Follow official docs at https://minikube.sigs.k8s.io/

**Option 2: Docker Desktop with Kubernetes**
- Includes built-in Kubernetes support
- Enable in Settings → Kubernetes → Enable Kubernetes
- Download: https://www.docker.com/products/docker-desktop

**Option 3: Cloud Kubernetes Services**
- AWS EKS (Elastic Kubernetes Service)
- Azure AKS (Azure Kubernetes Service)
- Google GKE (Google Kubernetes Engine)
- Requires cloud provider account and credentials

**Container Runtime (for Minikube)**

If using Minikube, you need a container runtime:

**Docker Desktop (Recommended)**
- Easiest option for Windows and macOS
- Download: https://www.docker.com/products/docker-desktop
- Minikube command: `minikube start --driver=docker`

**Alternative: Hyper-V (Windows only)**
- Built into Windows Pro/Enterprise
- Enable in PowerShell (admin): `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`
- Minikube command: `minikube start --driver=hyperv`

**Alternative: VirtualBox**
- Cross-platform virtualization
- Download: https://www.virtualbox.org/
- Minikube command: `minikube start --driver=virtualbox`

### Optional Software

**Git**
- For cloning the repository
- Check version: `git --version`
- Download: https://git-scm.com/downloads

**VS Code or your preferred code editor**
- For viewing and editing code
- Download: https://code.visualstudio.com/

---

## Installation & Setup

### Step 1: Clone the Repository
```bash
# Using HTTPS
git clone https://github.com/YOUR-USERNAME/kubernetes-security-scanner.git

# Or using SSH
git clone git@github.com:YOUR-USERNAME/kubernetes-security-scanner.git

# Navigate into the project directory
cd kubernetes-security-scanner
```

### Step 2: Set Up Python Virtual Environment (Recommended)

Using a virtual environment isolates project dependencies from your system Python installation.
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (Command Prompt)
venv\Scripts\activate.bat

# On Windows (PowerShell)
venv\Scripts\Activate.ps1

# On Windows (Git Bash)
source venv/Scripts/activate

# On macOS/Linux
source venv/bin/activate

# Your prompt should now show (venv) prefix
```

### Step 3: Install Python Dependencies
```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages include:
- kubernetes (Kubernetes Python client)
- PyYAML (YAML parsing)
- click (CLI framework)
- colorama (colored terminal output)
- tabulate (table formatting)
- pytest (testing framework)
- And several others

### Step 4: Set Up Kubernetes Cluster

#### Option A: Using Minikube (Recommended for Demo)
```bash
# Start Minikube cluster with Docker driver
minikube start --driver=docker

# This will:
# - Download Kubernetes components (~500MB first time)
# - Create a virtual machine or container
# - Configure kubectl automatically
# - Take 2-3 minutes

# Verify cluster is running
minikube status

# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured

# Check cluster info
kubectl cluster-info

# View nodes
kubectl get nodes

# You should see one node named "minikube" in Ready status
```

#### Option B: Using Docker Desktop Kubernetes
```bash
# 1. Open Docker Desktop
# 2. Go to Settings → Kubernetes
# 3. Check "Enable Kubernetes"
# 4. Click "Apply & Restart"
# 5. Wait for Kubernetes to start (green indicator)

# Verify
kubectl cluster-info
kubectl get nodes

# You should see one node named "docker-desktop"
```

#### Option C: Using Cloud Provider
```bash
# Configure kubectl with your cloud cluster credentials
# AWS EKS example:
aws eks update-kubeconfig --name your-cluster-name --region us-east-1

# Azure AKS example:
az aks get-credentials --resource-group your-rg --name your-cluster

# Google GKE example:
gcloud container clusters get-credentials your-cluster --zone us-central1-a

# Verify connection
kubectl cluster-info
kubectl get nodes
```

### Step 5: Verify Installation
```bash
# Test that the scanner can access the cluster
python -m src.scanner --version

# Expected output:
# Kubernetes Security Scanner v1.0.0

# Run scanner help
python -m src.scanner --help

# You should see the full help message with usage examples
```

### Step 6: Test with Demo Resources (Optional)

Deploy intentionally insecure resources to verify the scanner works:
```bash
# Deploy insecure demo resources
kubectl apply -f demo/insecure/

# Verify they're running
kubectl get pods

# Run the scanner
python -m src.scanner

# You should see multiple security findings

# Clean up demo resources
kubectl delete -f demo/insecure/
```

---

## How to Run

### Basic Usage

**Scan entire cluster:**
```bash
python -m src.scanner
```

This will:
- Connect to your current kubectl context
- Scan all namespaces (except kube-system by default)
- Display findings in colored console output
- Show summary statistics

**Scan specific namespace:**
```bash
python -m src.scanner --namespace default
```

Only scans the specified namespace (faster for large clusters).

**Generate JSON report:**
```bash
python -m src.scanner --output json
```

Outputs machine-readable JSON to console instead of formatted text.

**Save results to file:**
```bash
python -m src.scanner --output json --file scan-results.json
```

Saves JSON report to specified file for later analysis or integration.

**Combine options:**
```bash
python -m src.scanner --namespace production --output json --file prod-scan.json
```

### Using the Shell Script (Linux/macOS/Git Bash)
```bash
# Make script executable (first time only)
chmod +x run_scan.sh

# Run the scanner
./run_scan.sh

# Pass arguments
./run_scan.sh --namespace default
```

The shell script:
- Checks prerequisites (Python, kubectl)
- Verifies cluster connection
- Runs the scanner with passed arguments
- Provides helpful error messages

### Running in Docker
```bash
# Build the Docker image
docker build -t k8s-security-scanner .

# Run scanner (mount kubeconfig)
docker run --rm -v ~/.kube:/root/.kube:ro k8s-security-scanner

# With arguments
docker run --rm -v ~/.kube:/root/.kube:ro k8s-security-scanner --namespace default

# Save output to file
docker run --rm -v ~/.kube:/root/.kube:ro -v $(pwd):/output k8s-security-scanner --output json --file /output/scan.json
```

### Command-Line Options
```
-h, --help
    Show help message and exit

-n NAMESPACE, --namespace NAMESPACE
    Scan only the specified namespace
    Default: all namespaces
    Example: --namespace production

-o {text,json}, --output {text,json}
    Output format
    text: Colored console output (default)
    json: Machine-readable JSON
    Example: --output json

-f FILE, --file FILE
    Save output to specified file
    Only works with JSON output format
    Example: --file results.json

-v, --version
    Show scanner version and exit
```

### Exit Codes

- 0: Scan completed successfully
- 1: Error occurred (cluster connection failed, invalid arguments, etc.)

---

## Understanding the Results

### Console Output Format

When you run the scanner with default text output, you'll see:

**Header:**
```
==============================================================
  Kubernetes Security Scanner v1.0.0
  Scanning for misconfigurations and vulnerabilities
==============================================================

🔌 Connecting to Kubernetes cluster...
✅ Connected to cluster: minikube
   Server: https://127.0.0.1:xxxxx

==============================================================
🔍 Starting Kubernetes Security Scan
==============================================================

📦 Scanning all namespaces (X found)

⚡ Running PodSecurityChecker...
   ✓ Found 5 issues
⚡ Running RBACChecker...
   ✓ Found 3 issues
⚡ Running NetworkPolicyChecker...
   ✓ Found 2 issues
⚡ Running ResourceLimitChecker...
   ✓ Found 4 issues
```

**Findings by Severity:**
```
────────────────────────────────────────────────────────────
🔴 CRITICAL Issues (3)
────────────────────────────────────────────────────────────

[CRITICAL] Container running as root (UID 0)
  Resource: insecure-nginx-root/nginx
  Namespace: default
  Category: Pod Security
  Description: Container "nginx" in pod "insecure-nginx-root" is running as root user (UID 0)
  💡 Recommendation: Set runAsUser to a non-zero value in securityContext
  🔧 Remediation: Add securityContext with runAsUser: 1000 (or any non-zero UID)
```

Each finding includes:
- **Severity level:** CRITICAL, HIGH, MEDIUM, or LOW
- **Title:** Brief description of the issue
- **Resource:** Affected Kubernetes resource
- **Namespace:** Where the resource exists
- **Category:** Type of security check
- **Description:** Detailed explanation
- **Recommendation:** What should be done
- **Remediation:** Specific steps to fix

**Summary:**
```
==============================================================
📊 Summary
==============================================================

Severity     Count
-----------  -----
🔴 CRITICAL  3
🟠 HIGH      4
🟡 MEDIUM    3
🟢 LOW       2
-----------  -----
TOTAL ISSUES 12

🚨 Security Posture: CRITICAL - Immediate action required!

✅ Scan complete!
```

### Severity Levels Explained

**CRITICAL (🔴):**
Issues that could lead to immediate cluster compromise or data breach:
- Containers running as root
- Privileged containers
- cluster-admin granted to default service account
- Exposed Kubernetes API without authentication

**HIGH (🟠):**
Serious security issues that significantly increase attack surface:
- Dangerous Linux capabilities granted
- Privilege escalation allowed
- No network policies (unrestricted pod communication)
- Overly permissive RBAC roles

**MEDIUM (🟡):**
Important security concerns that should be addressed:
- Missing security contexts
- Missing default-deny network policies
- Missing memory limits (DoS risk)
- Overly broad role bindings

**LOW (🟢):**
Best practice violations or minor concerns:
- Writable root filesystem
- Missing CPU limits
- Missing resource requests
- Default service account usage

### JSON Output Format

When using `--output json`, the scanner produces structured data:
```json
{
  "scan_metadata": {
    "timestamp": "2025-12-27T14:30:00.000000",
    "total_findings": 12,
    "scanner_version": "1.0.0"
  },
  "summary": {
    "severity_breakdown": {
      "CRITICAL": 3,
      "HIGH": 4,
      "MEDIUM": 3,
      "LOW": 2
    },
    "category_breakdown": {
      "Pod Security": 7,
      "RBAC": 3,
      "Network Policy": 1,
      "Resource Limits": 1
    },
    "total_issues": 12
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "category": "Pod Security",
      "title": "Container running as root (UID 0)",
      "resource_name": "insecure-nginx-root/nginx",
      "namespace": "default",
      "description": "Container \"nginx\" in pod \"insecure-nginx-root\" is running as root user (UID 0)",
      "recommendation": "Set runAsUser to a non-zero value in securityContext",
      "remediation": "Add securityContext with runAsUser: 1000 (or any non-zero UID)"
    }
  ]
}
```

This format is ideal for:
- Feeding into security dashboards
- Integration with CI/CD pipelines
- Automated alerting systems
- Trend analysis over time
- Compliance reporting

---

## Demo Scenarios

### Scenario 1: Finding Critical Security Issues

**Goal:** Demonstrate the scanner detecting severe misconfigurations.
```bash
# Deploy intentionally vulnerable resources
kubectl apply -f demo/insecure/

# Run the scanner
python -m src.scanner

# Observe CRITICAL and HIGH findings
# Point out specific issues like:
# - Pods running as root
# - Privileged containers
# - cluster-admin permissions
```

**Key talking points:**
- "This pod is running as root, meaning if an attacker compromises it, they have full container privileges"
- "Privileged mode gives the container almost unlimited access to the host system"
- "The default service account has cluster-admin - this is extremely dangerous"

### Scenario 2: Fixing Security Issues

**Goal:** Show before-and-after comparison.
```bash
# Show insecure configuration
cat demo/insecure/pod-root.yaml

# Explain the issues:
# - runAsUser: 0 (root)
# - No security context restrictions

# Show secure configuration
cat demo/secure/pod-secure.yaml

# Explain the improvements:
# - runAsUser: 1000 (non-root)
# - runAsNonRoot: true
# - allowPrivilegeEscalation: false
# - readOnlyRootFilesystem: true
# - Capabilities dropped

# Clean up insecure resources
kubectl delete -f demo/insecure/

# Deploy secure resources
kubectl apply -f demo/secure/

# Re-run scanner
python -m src.scanner

# Show reduced findings
```

**Key talking points:**
- "By adding proper security contexts, we've eliminated the critical vulnerabilities"
- "The scanner now shows zero critical issues"
- "These configurations follow Kubernetes Pod Security Standards"

### Scenario 3: CI/CD Integration

**Goal:** Demonstrate automated security scanning in pipelines.
```bash
# Show the GitHub Actions workflow
cat .github/workflows/ci.yml

# Explain how it runs automatically on every commit
# Point out the security-scan job
```

**Simulated pipeline usage:**
```bash
# Example script for CI/CD
#!/bin/bash

# Run scanner and save results
python -m src.scanner --output json --file scan-results.json

# Check for critical issues
if grep -q '"severity": "CRITICAL"' scan-results.json; then
    echo "CRITICAL security issues found! Blocking deployment."
    exit 1
fi

echo "Security scan passed. Proceeding with deployment."
exit 0
```

**Key talking points:**
- "The scanner integrates into CI/CD to catch security issues before production"
- "We can fail deployments if critical vulnerabilities are detected"
- "This implements security shift-left principles"

### Scenario 4: Namespace-Specific Scanning

**Goal:** Show how to audit specific parts of a cluster.
```bash
# Create multiple namespaces
kubectl create namespace production
kubectl create namespace development

# Deploy different resources to each
kubectl apply -f demo/insecure/ -n development
kubectl apply -f demo/secure/ -n production

# Scan only development
python -m src.scanner --namespace development

# Show findings

# Scan only production
python -m src.scanner --namespace production

# Show fewer/no findings

# Clean up
kubectl delete namespace development production
```

**Key talking points:**
- "In large clusters, you can focus scans on specific namespaces"
- "Different teams or environments can have different security postures"
- "This makes the scanner practical for enterprise use"

---

## Project Structure
```
kubernetes-security-scanner/
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD pipeline
├── demo/
│   ├── insecure/                   # Intentionally vulnerable Kubernetes manifests
│   │   ├── pod-root.yaml          # Pod running as root
│   │   ├── privileged-pod.yaml    # Privileged container
│   │   ├── bad-rbac.yaml          # Overly permissive RBAC
│   │   └── no-network-policy.yaml # Missing network policies
│   └── secure/                     # Hardened Kubernetes manifests
│       ├── pod-secure.yaml        # Properly secured pod
│       ├── proper-rbac.yaml       # Least-privilege RBAC
│       └── network-policy.yaml    # Network segmentation
├── docs/
│   ├── architecture.md             # Technical architecture documentation
│   └── demo-guide.md              # Step-by-step demo instructions
├── src/
│   ├── __init__.py                # Package initialization
│   ├── scanner.py                 # Main entry point and orchestration
│   ├── checks/                    # Security checker modules
│   │   ├── __init__.py
│   │   ├── pod_security.py       # Pod security checks
│   │   ├── rbac_checker.py       # RBAC permission analysis
│   │   ├── network_policy.py     # Network policy validation
│   │   └── resource_limits.py    # Resource quota checks
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       ├── k8s_client.py         # Kubernetes API client wrapper
│       └── reporter.py           # Report generation
├── tests/
│   ├── __init__.py
│   ├── test_pod_security.py      # Unit tests for pod checker
│   └── test_rbac.py              # Unit tests for RBAC checker
├── .gitignore                     # Git ignore rules
├── Dockerfile                     # Container image definition
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── run_scan.sh                    # Convenience script for running scanner
└── setup.py                       # Package installation configuration
```

### Key Files Explained

**scanner.py:**
Main application logic. Parses command-line arguments, establishes cluster connection, executes all security checks, and generates reports.

**k8s_client.py:**
Kubernetes API wrapper. Handles authentication, provides simplified methods for querying resources, manages API client lifecycle.

**pod_security.py:**
Checks pod and container configurations for security issues like root users, privileged mode, dangerous capabilities, and missing security contexts.

**rbac_checker.py:**
Analyzes Role-Based Access Control configurations to identify overly permissive role bindings and service accounts.

**network_policy.py:**
Validates network policies to ensure proper traffic segmentation and identify namespaces without network controls.

**resource_limits.py:**
Checks for missing CPU and memory limits that could enable resource exhaustion attacks.

**reporter.py:**
Formats findings into human-readable console output with colors and icons, or generates JSON for programmatic consumption.

**ci.yml:**
GitHub Actions workflow that automatically runs tests, linting, security scans, and Docker builds on every commit.

**Dockerfile:**
Defines a containerized version of the scanner for portable deployment.

---

## Security Checks Performed

### Pod Security Checks

**Running as Root (CRITICAL):**
- Detects: `runAsUser: 0` or missing `runAsNonRoot`
- Risk: Root access in container enables privilege escalation
- Fix: Set `runAsUser` to non-zero value (e.g., 1000)

**Privileged Containers (CRITICAL):**
- Detects: `privileged: true`
- Risk: Nearly unlimited host access, bypasses security features
- Fix: Remove privileged mode unless absolutely necessary

**Dangerous Capabilities (HIGH):**
- Detects: Capabilities like `SYS_ADMIN`, `NET_ADMIN`
- Risk: Excessive kernel-level permissions
- Fix: Drop all capabilities, add only required ones

**Privilege Escalation Allowed (HIGH):**
- Detects: `allowPrivilegeEscalation: true` or not set
- Risk: Processes can gain more privileges than parent
- Fix: Set `allowPrivilegeEscalation: false`

**Missing Security Context (MEDIUM):**
- Detects: No `securityContext` defined
- Risk: Defaults may be insecure
- Fix: Explicitly define security context

**Writable Root Filesystem (LOW):**
- Detects: `readOnlyRootFilesystem: false` or not set
- Risk: Malware can persist changes
- Fix: Set `readOnlyRootFilesystem: true`, use volumes for writable data

### RBAC Checks

**cluster-admin to Default SA (CRITICAL):**
- Detects: Default service account with cluster-admin role
- Risk: All pods in namespace have full cluster control
- Fix: Create dedicated service accounts with minimal permissions

**cluster-admin to Any SA (HIGH):**
- Detects: Any service account with cluster-admin
- Risk: Potential for widespread compromise
- Fix: Use least-privilege roles instead

**Elevated Role Bindings (MEDIUM/HIGH):**
- Detects: `admin` or `edit` cluster roles
- Risk: Overly broad permissions
- Fix: Create custom roles with specific permissions

**Default Service Account Usage (LOW):**
- Detects: Pods using default service account
- Risk: Shared credentials, harder to audit
- Fix: Create application-specific service accounts

### Network Policy Checks

**No Network Policies (HIGH):**
- Detects: Namespaces with pods but no NetworkPolicies
- Risk: Unrestricted pod-to-pod communication
- Fix: Implement default-deny policies

**Missing Default-Deny (MEDIUM):**
- Detects: No policy that denies all traffic by default
- Risk: Permissive by default
- Fix: Create policy selecting all pods with empty rules

**Overly Permissive Rules (MEDIUM/LOW):**
- Detects: Rules allowing traffic from any source/to any destination
- Risk: Ineffective network segmentation
- Fix: Specify exact pod/namespace selectors

### Resource Limit Checks

**Missing Memory Limits (MEDIUM):**
- Detects: No `resources.limits.memory`
- Risk: Pod can exhaust node memory (OOM)
- Fix: Set appropriate memory limits based on application needs

**Missing CPU Limits (LOW):**
- Detects: No `resources.limits.cpu`
- Risk: CPU starvation for other pods
- Fix: Set CPU limits (e.g., "500m" or "1")

**Missing Resource Requests (LOW):**
- Detects: No `resources.requests`
- Risk: Poor scheduling decisions
- Fix: Set requests for proper resource allocation

---

## Technologies Used

### Core Technologies

**Python 3.8+**
Primary programming language for the scanner. Chosen for:
- Excellent Kubernetes client library
- Rich ecosystem for CLI tools
- Easy to read and maintain
- Cross-platform compatibility

**Kubernetes Python Client (kubernetes)**
Official Python client for Kubernetes API. Provides:
- Auto-generated API methods
- Authentication handling
- Type hints and documentation
- Active maintenance

**kubectl**
Kubernetes command-line tool. Used for:
- Cluster authentication
- Manual resource inspection
- Troubleshooting

### Development Tools

**pytest**
Testing framework for unit and integration tests. Features:
- Fixtures for test setup
- Parametrized tests
- Coverage reporting
- Mock support

**flake8**
Python linting tool for code quality. Checks for:
- Syntax errors
- Style violations (PEP 8)
- Unused imports
- Code complexity

**black**
Opinionated code formatter. Ensures:
- Consistent style
- Automatic formatting
- No manual decisions

**bandit**
Security linting tool for Python. Detects:
- Common security issues
- Vulnerable code patterns
- Insecure dependencies

### Infrastructure Tools

**Docker**
Container platform for:
- Packaging the scanner
- Running Minikube
- Portable deployments

**Minikube**
Local Kubernetes cluster for:
- Development
- Testing
- Demonstrations

**GitHub Actions**
CI/CD platform for:
- Automated testing
- Code quality checks
- Security scanning
- Docker builds

### Python Libraries

**PyYAML**
YAML parsing for reading Kubernetes manifests

**click**
CLI framework for command-line interface

**colorama**
Cross-platform colored terminal output

**tabulate**
Table formatting for summary statistics

**python-dateutil**
Date and time utilities

---

## Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term --cov-report=html

# Run specific test file
python -m pytest tests/test_pod_security.py -v

# Run specific test
python -m pytest tests/test_pod_security.py::TestPodSecurityChecker::test_detects_root_user -v
```

### Code Quality
```bash
# Format code with black
python -m black src/ tests/

# Lint with flake8
python -m flake8 src/ --max-line-length=127

# Type checking with mypy
python -m mypy src/

# Security scan with bandit
python -m bandit -r src/
```

### Adding New Security Checks

To add a new security checker:

1. Create a new file in `src/checks/` (e.g., `my_checker.py`)

2. Implement the checker class:
```python
class MyChecker:
    def __init__(self, k8s_client):
        self.k8s_client = k8s_client
        self.findings = []
    
    def check(self, namespaces):
        """Run checks and return findings"""
        self.findings = []
        for namespace in namespaces:
            # Your check logic here
            pass
        return self.findings
```

3. Import and add to `src/scanner.py`:
```python
from src.checks.my_checker import MyChecker

# In run_checks method:
checkers = [
    PodSecurityChecker(self.k8s_client),
    RBACChecker(self.k8s_client),
    NetworkPolicyChecker(self.k8s_client),
    ResourceLimitChecker(self.k8s_client),
    MyChecker(self.k8s_client)  # Add your checker
]
```

4. Write tests in `tests/test_my_checker.py`

5. Update documentation

### Building Docker Image
```bash
# Build image
docker build -t k8s-security-scanner:latest .

# Tag for Docker Hub (replace username)
docker tag k8s-security-scanner:latest username/k8s-security-scanner:latest

# Push to Docker Hub
docker login
docker push username/k8s-security-scanner:latest
```

---

## Troubleshooting

### Connection Issues

**Problem:** "Failed to connect to cluster"

**Solutions:**
```bash
# Check kubectl is configured
kubectl cluster-info

# Check current context
kubectl config current-context

# List available contexts
kubectl config get-contexts

# Switch context
kubectl config use-context minikube

# For Minikube specifically
minikube status
minikube start
```

**Problem:** "The connection to the server localhost:8080 was refused"

**Solutions:**
```bash
# Minikube: Ensure it's running
minikube start

# Docker Desktop: Check Kubernetes is enabled in settings

# Cloud: Verify kubeconfig credentials
kubectl get nodes
```

### Permission Issues

**Problem:** "Forbidden: User cannot list resource"

**Solutions:**
The scanner needs read permissions for:
- pods
- services
- serviceaccounts
- roles
- rolebindings
- clusterroles
- clusterrolebindings
- networkpolicies
- deployments

Create a custom role if needed:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: security-scanner
rules:
- apiGroups: ["", "rbac.authorization.k8s.io", "networking.k8s.io", "apps"]
  resources: ["*"]
  verbs: ["get", "list"]
```

### Python Environment Issues

**Problem:** "ModuleNotFoundError: No module named 'kubernetes'"

**Solutions:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep kubernetes
```

**Problem:** "RuntimeWarning: 'src.scanner' found in sys.modules"

**Solution:**
This warning is harmless and can be ignored. It's a Python module loading quirk when using `-m` flag.

### Minikube Issues

**Problem:** "Exiting due to PROVIDER_DOCKER_NOT_FOUND"

**Solutions:**
```bash
# Install Docker Desktop
# OR use alternative driver:
minikube start --driver=virtualbox
minikube start --driver=hyperv  # Windows only
```

**Problem:** "Minikube cluster is not running"

**Solutions:**
```bash
minikube status
minikube start

# If start fails, try deleting and recreating
minikube delete
minikube start
```

### Scanner Output Issues

**Problem:** "No security issues found" when there should be findings

**Solutions:**
```bash
# Verify demo resources are deployed
kubectl get pods -A

# Deploy insecure examples
kubectl apply -f demo/insecure/

# Re-run scanner
python -m src.scanner
```

**Problem:** Colors not showing in terminal

**Solutions:**
- Use a terminal that supports ANSI colors
- Windows: Use Windows Terminal, PowerShell, or Git Bash
- Enable color support if using older terminal

### Common Errors

**Error:** "exec format error" (Docker on Windows)

**Solution:**
Ensure Docker Desktop is using Linux containers, not Windows containers.

**Error:** "No module named 'src'"

**Solution:**
Run from project root directory where `src/` folder is located.

**Error:** "Permission denied: './run_scan.sh'"

**Solution:**
```bash
chmod +x run_scan.sh
```

---

## Future Enhancements

### Planned Features

**Web Dashboard:**
- Real-time visualization of findings
- Historical trend analysis
- Interactive resource exploration
- Export to PDF reports

**Custom Policy Definitions:**
- User-defined security rules
- Organization-specific compliance checks
- Policy-as-Code (OPA/Rego integration)

**Automated Remediation:**
- Generate Kubernetes manifests with fixes
- Optional auto-apply of fixes
- Pull request creation for IaC repositories

**Advanced Reporting:**
- HTML reports with graphs
- PDF exports for compliance
- Comparison between scans
- Severity trend tracking

**Multi-Cluster Support:**
- Scan multiple clusters in one run
- Aggregate findings across fleet
- Cluster-to-cluster comparison

**Notification Integrations:**
- Slack webhooks
- Email alerts
- PagerDuty integration
- Microsoft Teams

**Extended Security Checks:**
- Image vulnerability scanning (integration with Trivy)
- Secrets detection in manifests
- Pod Security Standards (PSS) validation
- CIS Kubernetes Benchmark alignment
- Admission controller integration

**CI/CD Enhancements:**
- Pre-commit hooks
- GitLab CI templates
- Jenkins plugin
- Azure DevOps integration

---

## Contributing

Contributions are welcome! Here's how to contribute:

### Reporting Issues

Found a bug or have a feature request?

1. Check existing issues on GitHub
2. Create a new issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, Kubernetes version)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/`
6. Format code: `black src/ tests/`
7. Lint code: `flake8 src/`
8. Commit with clear message: `git commit -m 'Add amazing feature'`
9. Push to your fork: `git push origin feature/amazing-feature`
10. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write descriptive docstrings
- Add unit tests for new code
- Keep functions focused and small
- Update documentation for new features
- Use type hints where appropriate

---

## License

This project is licensed under the MIT License.

Copyright (c) 2025 Justin D.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Author

**Your Name**

- GitHub: Myrmecology (https://github.com/Myrmecology/kubernetes-security-scanner)


---

## Acknowledgments

This project was built to demonstrate expertise in:
- Kubernetes security and administration
- Python development
- DevSecOps practices
- Cloud-native technologies

Special thanks to:
- The Kubernetes community for excellent documentation
- CNCF for maintaining critical cloud-native projects
- Security researchers who identified these common misconfigurations
- Open-source contributors who inspire and enable projects like this

---

## Additional Resources

**Kubernetes Security:**
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/security-checklist/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [NSA/CISA Kubernetes Hardening Guide](https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/2716980/nsa-cisa-release-kubernetes-hardening-guidance/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)

**Learning Resources:**
- [Official Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Docker Documentation](https://docs.docker.com/)

**Security Tools:**
- [kube-bench](https://github.com/aquasecurity/kube-bench) - CIS Benchmark checker
- [kubesec](https://github.com/controlplaneio/kubesec) - Security risk analysis
- [Trivy](https://github.com/aquasecurity/trivy) - Vulnerability scanner

---

**⭐ If you found this project helpful, please consider giving it a star on GitHub!**

For questions or support, please open an issue on GitHub.
Happy Coding 