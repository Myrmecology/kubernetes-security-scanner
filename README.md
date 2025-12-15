# Kubernetes Security Scanner 🔐

A comprehensive security auditing tool for Kubernetes clusters that identifies misconfigurations, security vulnerabilities, and compliance violations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-1.20+-326CE5.svg)

## 🎯 Purpose

This tool helps DevOps engineers and security professionals identify and remediate security issues in Kubernetes clusters before they become vulnerabilities. It performs automated security audits across multiple areas:

- **Pod Security**: Detects containers running as root or with elevated privileges
- **RBAC Analysis**: Identifies overly permissive role bindings and service accounts
- **Network Policies**: Validates network segmentation and traffic controls
- **Resource Limits**: Checks for missing CPU/memory limits that could enable DoS attacks
- **Security Context**: Ensures proper security contexts are defined

## 🚀 Features

- ✅ **Automated Security Scanning** - Run comprehensive security checks with a single command
- ✅ **Multi-Check Support** - Covers pods, RBAC, network policies, and resource configurations
- ✅ **Detailed Reporting** - Clear, actionable output with severity levels
- ✅ **CIS Kubernetes Benchmark Alignment** - Checks based on industry best practices
- ✅ **Easy Integration** - Works with any Kubernetes cluster (Minikube, EKS, AKS, GKE)
- ✅ **CI/CD Ready** - Can be integrated into your deployment pipeline

## 📋 Prerequisites

- Python 3.8 or higher
- `kubectl` installed and configured
- Access to a Kubernetes cluster (local or remote)
- Appropriate RBAC permissions to read cluster resources

## 🔧 Installation

### Clone the Repository
```bash
git clone https://github.com/Myrmecology/kubernetes-security-scanner.git
cd kubernetes-security-scanner
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Verify kubectl Access
```bash
kubectl cluster-info
kubectl get nodes
```

## 💻 Usage

### Basic Scan

Run a complete security scan of your cluster:
```bash
python -m src.scanner
```

### Using the Shell Script
```bash
./run_scan.sh
```

### Scan Specific Namespaces
```bash
python -m src.scanner --namespace production
```

### Generate JSON Report
```bash
python -m src.scanner --output json --file report.json
```

## 📊 Sample Output
```
🔍 Kubernetes Security Scanner v1.0
==================================================

Scanning cluster: minikube
Namespaces: default, kube-system

[CRITICAL] Pod 'nginx-insecure' running as root (UID 0)
  Namespace: default
  Recommendation: Set runAsUser to non-zero value

[HIGH] Pod 'app-privileged' has privileged mode enabled
  Namespace: default
  Recommendation: Remove privileged: true from securityContext

[MEDIUM] ServiceAccount 'default' has cluster-admin binding
  Namespace: default
  Recommendation: Use least-privilege RBAC roles

[LOW] Pod 'web-app' missing resource limits
  Namespace: default
  Recommendation: Set CPU and memory limits

==================================================
Summary:
  Total Issues: 12
  Critical: 3
  High: 4
  Medium: 3
  Low: 2
```

## 🧪 Demo Environment

This repository includes sample Kubernetes manifests for testing:

### Deploy Insecure Resources (for testing)
```bash
kubectl apply -f demo/insecure/
```

### Run the Scanner
```bash
python -m src.scanner
```

### Deploy Secure Alternatives
```bash
kubectl apply -f demo/secure/
```

### Verify Improvements
```bash
python -m src.scanner
```

## 🏗️ Architecture
```
kubernetes-security-scanner/
├── src/
│   ├── scanner.py              # Main entry point
│   ├── checks/                 # Security check modules
│   │   ├── pod_security.py     # Pod-level security checks
│   │   ├── rbac_checker.py     # RBAC permission analysis
│   │   ├── network_policy.py   # Network policy validation
│   │   └── resource_limits.py  # Resource quota checks
│   └── utils/
│       ├── k8s_client.py       # Kubernetes API client wrapper
│       └── reporter.py         # Report generation utilities
├── tests/                      # Unit tests
├── demo/                       # Sample K8s manifests
│   ├── insecure/              # Intentionally vulnerable configs
│   └── secure/                # Hardened configs
└── docs/                      # Additional documentation
```

## 🔍 Security Checks Performed

### Pod Security Checks
- Containers running as root (UID 0)
- Privileged containers
- Host network/PID/IPC access
- Dangerous capabilities (CAP_SYS_ADMIN, etc.)
- Host path volume mounts
- Missing security contexts

### RBAC Checks
- Service accounts with cluster-admin privileges
- Wildcard permissions (*, **)
- Overly broad role bindings
- Unused service accounts with elevated permissions

### Network Policy Checks
- Namespaces without network policies
- Policies allowing unrestricted egress
- Missing ingress controls

### Resource Limit Checks
- Missing CPU limits
- Missing memory limits
- Potential for resource exhaustion

## 🛠️ Development

### Run Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest --cov=src tests/
```

### Lint Code
```bash
flake8 src/
black src/
```



## 📝 Roadmap

- [ ] Add support for Pod Security Standards (PSS)
- [ ] Implement custom security policy definitions
- [ ] Add web dashboard for visualization
- [ ] Export reports to PDF/HTML
- [ ] Slack/email notifications for critical findings
- [ ] Integration with admission controllers
- [ ] Support for OPA/Gatekeeper policy validation

## 📚 References

- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA/CISA Kubernetes Hardening Guide](https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/2716980/nsa-cisa-release-kubernetes-hardening-guidance/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/security-checklist/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Justin D.**
- GitHub: Myrmecology (https://github.com/Myrmecology/kubernetes-security-scanner)


## 🙏 Acknowledgments

- Kubernetes community for excellent documentation
- Security researchers who identified these common misconfigurations
- Open-source security tools that inspired this project

---

**⭐ If you find this project helpful, please consider giving it a star!**
Happy coding