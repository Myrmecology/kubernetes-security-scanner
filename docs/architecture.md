# Kubernetes Security Scanner - Architecture

## System Overview

The Kubernetes Security Scanner is a modular Python application that connects to Kubernetes clusters via the official Kubernetes Python client and performs automated security audits.

## High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                            │
│  (CLI / Shell Script / Docker Container)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Main Scanner (scanner.py)                    │
│  - Orchestrates security checks                             │
│  - Manages workflow and error handling                       │
│  - Coordinates result aggregation                            │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐
│Pod Security │ │  RBAC   │ │ Network  │ │  Resource  │
│   Checker   │ │ Checker │ │ Policy   │ │   Limits   │
│             │ │         │ │ Checker  │ │  Checker   │
└─────────────┘ └─────────┘ └──────────┘ └────────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Kubernetes API Client │
        │    (k8s_client.py)     │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Kubernetes Cluster   │
        │  (Minikube/EKS/AKS/GKE)│
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │    Report Generator    │
        │     (reporter.py)      │
        │  - Console output      │
        │  - JSON export         │
        └────────────────────────┘
```

## Component Details

### 1. Main Scanner (`src/scanner.py`)

**Responsibility:** Entry point and orchestration

**Key Functions:**
- Parses command-line arguments
- Establishes cluster connection
- Coordinates execution of all security checks
- Aggregates findings
- Triggers report generation

**Flow:**
```python
1. Initialize scanner with configuration
2. Connect to Kubernetes cluster via k8s_client
3. Get list of namespaces to scan
4. For each checker:
   - Initialize with k8s_client
   - Run check() method
   - Collect findings
5. Pass findings to Reporter
6. Display/save results
```

### 2. Security Checkers (`src/checks/`)

Each checker is independent and focuses on a specific security domain:

#### Pod Security Checker (`pod_security.py`)
- **Checks for:**
  - Containers running as root (UID 0)
  - Privileged containers
  - Dangerous Linux capabilities
  - Missing security contexts
  - Privilege escalation settings
  - Read-only root filesystem

- **Severity Levels:**
  - CRITICAL: Root user, privileged mode
  - HIGH: Dangerous capabilities, privilege escalation allowed
  - MEDIUM: Missing security context
  - LOW: Writable root filesystem

#### RBAC Checker (`rbac_checker.py`)
- **Checks for:**
  - cluster-admin bindings
  - Overly permissive roles (admin, edit)
  - Default service account with elevated permissions
  - Wildcard permissions

- **Severity Levels:**
  - CRITICAL: cluster-admin to default SA
  - HIGH: cluster-admin to any SA, admin roles
  - MEDIUM: Elevated bindings to named SAs
  - LOW: Default SA usage

#### Network Policy Checker (`network_policy.py`)
- **Checks for:**
  - Missing network policies
  - Overly permissive ingress/egress rules
  - Missing default-deny policies
  - Unrestricted traffic

- **Severity Levels:**
  - HIGH: No network policies in namespace with pods
  - MEDIUM: Missing default-deny, overly permissive rules
  - LOW: Minor policy issues

#### Resource Limit Checker (`resource_limits.py`)
- **Checks for:**
  - Missing CPU limits
  - Missing memory limits
  - Missing resource requests
  - Unbounded resource usage

- **Severity Levels:**
  - MEDIUM: Missing memory limits (OOM risk)
  - LOW: Missing CPU limits/requests

### 3. Kubernetes API Client (`src/utils/k8s_client.py`)

**Responsibility:** Abstraction layer for Kubernetes API

**Key Features:**
- Handles kubeconfig loading (local and in-cluster)
- Provides simplified methods for common operations
- Manages API client instances (CoreV1, RBAC, Networking, Apps)
- Error handling and retries

**API Methods:**
```python
get_cluster_info()          # Cluster metadata
get_namespaces()            # List all namespaces
get_pods(namespace)         # Get pods
get_service_accounts()      # Get service accounts
get_roles()                 # Get roles
get_cluster_roles()         # Get cluster roles
get_role_bindings()         # Get role bindings
get_cluster_role_bindings() # Get cluster role bindings
get_network_policies()      # Get network policies
get_deployments()           # Get deployments
```

### 4. Reporter (`src/utils/reporter.py`)

**Responsibility:** Format and output scan results

**Output Formats:**
- **Console (text):** Colored, formatted output with icons
- **JSON:** Machine-readable format for integration

**Features:**
- Severity-based grouping
- Color-coded output
- Summary statistics
- Recommendations and remediation steps
- Security posture assessment

## Data Flow
```
User Command
    ↓
Scanner.main()
    ↓
Connect to K8s cluster
    ↓
Get namespaces list
    ↓
For each namespace:
    ↓
    Run Pod Security Check
        ↓ (findings)
    Run RBAC Check
        ↓ (findings)
    Run Network Policy Check
        ↓ (findings)
    Run Resource Limits Check
        ↓ (findings)
    ↓
Aggregate all findings
    ↓
Reporter.generate_report()
    ↓
Display results
    ↓
(Optional) Save to file
```

## Security Finding Structure

Each finding is a dictionary with standardized fields:
```python
{
    'severity': 'CRITICAL|HIGH|MEDIUM|LOW|INFO',
    'category': 'Pod Security|RBAC|Network Policy|Resource Limits',
    'title': 'Brief description of issue',
    'resource_name': 'pod-name/container-name or resource name',
    'namespace': 'namespace-name',
    'description': 'Detailed explanation',
    'recommendation': 'What to do about it',
    'remediation': 'How to fix it (specific steps/code)'
}
```

## Extension Points

The architecture is designed for easy extension:

### Adding New Checks

1. Create new checker in `src/checks/`
2. Inherit from base pattern (or create standalone)
3. Implement `check(namespaces)` method
4. Return list of findings
5. Import and add to `scanner.py` checkers list

Example:
```python
# src/checks/my_new_checker.py
class MyNewChecker:
    def __init__(self, k8s_client):
        self.k8s_client = k8s_client
        
    def check(self, namespaces):
        findings = []
        # Your logic here
        return findings
```

### Adding New Output Formats

1. Add format to `Reporter` class
2. Implement generation method
3. Add to CLI options

## Dependencies

### Core Dependencies
- **kubernetes (29.0.0):** Official Kubernetes Python client
- **PyYAML (6.0.1):** YAML parsing
- **click (8.1.7):** CLI framework
- **colorama (0.4.6):** Cross-platform colored output
- **tabulate (0.9.0):** Table formatting

### Development Dependencies
- **pytest:** Testing framework
- **pytest-cov:** Coverage reporting
- **flake8:** Linting
- **black:** Code formatting
- **bandit:** Security scanning

## Configuration

The scanner uses:
- **kubeconfig:** Standard Kubernetes configuration (~/.kube/config)
- **Command-line arguments:** Runtime configuration
- **Environment variables:** (future feature)

## Performance Considerations

- **Parallel execution:** Currently sequential (could be parallelized)
- **Caching:** No caching (each run is fresh)
- **Rate limiting:** Respects Kubernetes API rate limits
- **Memory:** Minimal - processes resources iteratively

## Security Considerations

The scanner itself follows security best practices:
- Non-root execution in Docker
- Read-only kubeconfig mount
- Minimal permissions required
- No secrets stored
- Secure dependencies

## Future Enhancements

1. **Web Dashboard:** Real-time visualization
2. **Historical Tracking:** Compare scans over time
3. **Custom Policies:** User-defined security rules
4. **Automated Remediation:** Fix issues automatically
5. **CI/CD Integration:** Pre-deployment checks
6. **Notifications:** Slack, email, webhooks
7. **Multi-cluster Support:** Scan multiple clusters
8. **Compliance Frameworks:** CIS, PCI-DSS, SOC2 alignment

## Testing Strategy

- **Unit tests:** Mock Kubernetes API responses
- **Integration tests:** Test against real/kind cluster
- **Security tests:** Bandit static analysis
- **CI/CD:** Automated testing on every commit

---

**For implementation details, see the source code and inline comments.**