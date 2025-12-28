# Kubernetes Security Scanner - Demo Guide

This guide provides step-by-step instructions for demonstrating the Kubernetes Security Scanner, perfect for YouTube videos, presentations, or interviews.

## Prerequisites

Before starting the demo, ensure you have:

- ✅ Minikube installed
- ✅ kubectl installed and configured
- ✅ Python 3.8+ installed
- ✅ This project cloned and dependencies installed

## Demo Scenario Overview

**The Story:** You'll demonstrate how the scanner identifies security vulnerabilities in a Kubernetes cluster, then show how to fix them.

**Duration:** 10-15 minutes

**Flow:**
1. Setup clean Kubernetes cluster
2. Deploy intentionally insecure resources
3. Run the security scanner
4. Review and explain findings
5. Deploy secure alternatives
6. Re-run scanner to show improvements

---

## Part 1: Environment Setup (2 minutes)

### Step 1: Start Minikube
```bash
# Start a fresh Minikube cluster
minikube start --driver=docker

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

**What to say:**
> "I've set up a local Kubernetes cluster using Minikube. This represents a typical development or staging environment where we need to ensure security best practices."

### Step 2: Verify Scanner Installation
```bash
# Navigate to project directory
cd kubernetes-security-scanner

# Install dependencies (if not already done)
pip install -r requirements.txt

# Verify scanner works
python -m src.scanner --version
```

**What to say:**
> "I've built a security scanner in Python that uses the Kubernetes API to audit our cluster. Let's see what it finds."

---

## Part 2: Deploy Insecure Resources (2 minutes)

### Step 3: Show the Insecure Configuration Files
```bash
# Show insecure pod running as root
cat demo/insecure/pod-root.yaml
```

**What to say (highlight key issues):**
> "Notice this pod is running as UID 0 - the root user. This is a critical security issue because if an attacker compromises this container, they have root privileges."
```bash
# Show privileged container
cat demo/insecure/privileged-pod.yaml
```

**What to say:**
> "This container has privileged mode enabled, which gives it almost unlimited access to the host system. This is extremely dangerous."
```bash
# Show bad RBAC
cat demo/insecure/bad-rbac.yaml
```

**What to say:**
> "Here we're granting cluster-admin privileges to the default service account. This means every pod using this service account has full control over the entire cluster!"

### Step 4: Deploy All Insecure Resources
```bash
# Deploy all insecure examples
kubectl apply -f demo/insecure/

# Verify they're running
kubectl get pods -A
kubectl get clusterrolebindings | grep dangerous
```

**What to say:**
> "I've deployed several resources with common security misconfigurations. On the surface, everything looks normal - all pods are running. But let's see what our scanner finds."

---

## Part 3: Run the Security Scan (3 minutes)

### Step 5: Execute the Scanner
```bash
# Run the scanner
python -m src.scanner

# OR use the shell script
./run_scan.sh
```

**What to say while it runs:**
> "The scanner is now checking our cluster for security issues. It's examining pod configurations, RBAC permissions, network policies, and resource limits."

### Step 6: Explain the Results

**Point out the findings by severity:**

**CRITICAL findings:**
```
- Pod running as root (UID 0)
- Privileged containers
- cluster-admin granted to default service account
```

**What to say:**
> "We have several CRITICAL issues. These need immediate attention because they could lead to cluster compromise."

**HIGH findings:**
```
- Dangerous capabilities granted
- Privilege escalation allowed
- No network policies
```

**What to say:**
> "The HIGH severity issues are also serious. Missing network policies means any pod can talk to any other pod, and to the internet, without restriction."

**MEDIUM/LOW findings:**
```
- Missing resource limits
- Writable root filesystem
```

**What to say:**
> "The MEDIUM and LOW issues are less critical but still important. Missing resource limits could allow a pod to consume all cluster resources, causing a denial of service."

### Step 7: Explain Specific Findings

**Pick 2-3 findings to dive deeper:**
```bash
# You can generate a JSON report for detailed analysis
python -m src.scanner --output json --file scan-report.json

# View the JSON
cat scan-report.json | python -m json.tool | less
```

**What to say:**
> "Each finding includes a description, the severity level, and specific recommendations for fixing it. This makes it actionable for developers and security teams."

---

## Part 4: Remediation (3 minutes)

### Step 8: Show Secure Configurations
```bash
# Show the secure pod configuration
cat demo/secure/pod-secure.yaml
```

**What to say (highlight improvements):**
> "In the secure version, we're running as a non-root user (UID 1000), we've disabled privilege escalation, set the root filesystem to read-only, and dropped all Linux capabilities. This follows the principle of least privilege."
```bash
# Show secure RBAC
cat demo/secure/proper-rbac.yaml
```

**What to say:**
> "Instead of cluster-admin, we've created custom roles with only the specific permissions needed. We're using dedicated service accounts, not the default one."
```bash
# Show network policies
cat demo/secure/network-policy.yaml
```

**What to say:**
> "We've implemented network policies that default-deny all traffic, then explicitly allow only what's needed. This creates network segmentation and limits lateral movement."

### Step 9: Deploy Secure Resources
```bash
# First, clean up the insecure resources
kubectl delete -f demo/insecure/

# Deploy secure alternatives
kubectl apply -f demo/secure/

# Verify they're running
kubectl get pods -A
```

**What to say:**
> "Now I'm deploying the hardened versions. Notice the pods still run successfully, but with much better security posture."

---

## Part 5: Verify Improvements (2 minutes)

### Step 10: Re-run the Scanner
```bash
# Scan again
python -m src.scanner
```

**What to say:**
> "Let's run the scanner again to verify our improvements."

### Step 11: Compare Results

**Point out the improvements:**
```
Before:
- 12 total issues
- 3 CRITICAL
- 4 HIGH

After:
- 2 total issues (or 0 if everything is fixed)
- 0 CRITICAL
- 0 HIGH
```

**What to say:**
> "We've eliminated all critical and high-severity issues. The remaining findings are minor and can be addressed based on specific application requirements."

---

## Part 6: Wrap-Up (2 minutes)

### Step 12: Demonstrate Additional Features

**JSON Export:**
```bash
python -m src.scanner --output json --file final-scan.json
```

**What to say:**
> "The scanner can export results in JSON format, making it easy to integrate into CI/CD pipelines or security dashboards."

**Namespace-specific scan:**
```bash
python -m src.scanner --namespace default
```

**What to say:**
> "You can scan specific namespaces, which is useful for large clusters with many teams."

### Step 13: Show CI/CD Integration
```bash
# Show the GitHub Actions workflow
cat .github/workflows/ci.yml
```

**What to say:**
> "This scanner can run automatically in your CI/CD pipeline. Here's a GitHub Actions workflow that runs tests and security scans on every commit."

### Step 14: Discuss Real-World Usage

**What to say:**
> "In production, you'd run this scanner:
> - Before deployments (in CI/CD)
> - On a schedule (daily or weekly)
> - After cluster upgrades
> - As part of security audits
> 
> The findings can be sent to Slack, integrated with security dashboards, or used to gate deployments."

---

## Quick Command Reference

### Cluster Management
```bash
minikube start                    # Start cluster
minikube stop                     # Stop cluster
minikube delete                   # Delete cluster
kubectl get pods -A               # View all pods
kubectl get clusterrolebindings   # View RBAC bindings
```

### Running the Scanner
```bash
python -m src.scanner                              # Full scan
python -m src.scanner --namespace default          # Scan one namespace
python -m src.scanner --output json                # JSON output
python -m src.scanner --output json --file out.json # Save to file
./run_scan.sh                                      # Use shell script
```

### Deploy Demo Resources
```bash
kubectl apply -f demo/insecure/    # Deploy vulnerable resources
kubectl apply -f demo/secure/      # Deploy hardened resources
kubectl delete -f demo/insecure/   # Clean up insecure resources
```

---

## Tips for a Great Demo

### Before Recording

1. ✅ Test the entire flow start to finish
2. ✅ Prepare a script or talking points
3. ✅ Close unnecessary applications
4. ✅ Increase terminal font size for visibility
5. ✅ Use a color scheme with good contrast
6. ✅ Clear your terminal history: `clear`

### During Recording

1. 🎤 Speak clearly and at a moderate pace
2. 📖 Explain what you're doing before doing it
3. ⏸️ Pause after important findings to let viewers process
4. 🎯 Point out specific issues in the output
5. 💡 Explain the "why" - why each issue matters
6. ✨ Show enthusiasm about security!

### Pro Tips

- **Use terminal recording tools** like `asciinema` for clean recordings
- **Zoom in** on important code or output
- **Prepare** insecure resources that demonstrate real-world scenarios
- **Relate** findings to actual security incidents (when relevant)
- **Keep it practical** - focus on actionable insights

---

## Common Demo Issues and Solutions

### Issue: Minikube won't start
**Solution:**
```bash
minikube delete
minikube start --driver=docker
```

### Issue: Scanner can't connect to cluster
**Solution:**
```bash
kubectl cluster-info
# If this fails, check minikube status
minikube status
```

### Issue: Pods won't deploy
**Solution:**
```bash
kubectl describe pod <pod-name>
kubectl get events
```

### Issue: No findings detected
**Solution:**
Make sure insecure resources are deployed:
```bash
kubectl get pods -A
kubectl apply -f demo/insecure/
```

---

## Advanced Demo Ideas

### Multi-Namespace Demo
```bash
# Create multiple namespaces with different security levels
kubectl create namespace production
kubectl create namespace development
kubectl apply -f demo/insecure/ -n development
kubectl apply -f demo/secure/ -n production
python -m src.scanner
```

### Show Docker Integration
```bash
# Build and run in Docker
docker build -t k8s-security-scanner .
docker run --rm -v ~/.kube:/root/.kube:ro k8s-security-scanner
```

### Demonstrate Automation
```bash
# Show how to use in a script
#!/bin/bash
python -m src.scanner --output json --file report.json
if grep -q "CRITICAL" report.json; then
    echo "Critical issues found! Blocking deployment."
    exit 1
fi
```

---

## Video Recording Checklist

- [ ] Terminal font size increased (18-20pt)
- [ ] Color scheme tested on camera
- [ ] Minikube cluster fresh and working
- [ ] Demo resources ready to deploy
- [ ] Script/talking points prepared
- [ ] Screen recording software tested
- [ ] Microphone tested
- [ ] Background applications closed
- [ ] Notifications disabled
- [ ] Dry run completed successfully

---

## Sample Script Outline

**Intro (30 sec):**
- "Today I'm showing you a Kubernetes security scanner I built"
- "It identifies common misconfigurations that could lead to cluster compromise"

**Setup (1 min):**
- "I have a Minikube cluster representing a typical dev environment"
- "Let's deploy some resources with security issues"

**Demo (5 min):**
- "Running the scanner reveals X critical issues"
- "Let me walk through the most severe ones"
- "Here's how to fix each issue"

**Results (2 min):**
- "After deploying secure alternatives, we've eliminated all critical risks"
- "The scanner can integrate into CI/CD pipelines"

**Outro (30 sec):**
- "This project demonstrates my understanding of Kubernetes security"
- "Link to GitHub repo in description"
- "Thanks for watching!"

---

