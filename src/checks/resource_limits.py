"""
Resource limits checker - Identifies missing resource constraints
"""


class ResourceLimitChecker:
    """Check for missing resource limits and quotas"""

    def __init__(self, k8s_client):
        """
        Initialize resource limit checker

        Args:
            k8s_client: Kubernetes client instance
        """
        self.k8s_client = k8s_client
        self.findings = []

    def check(self, namespaces):
        """
        Run all resource limit checks

        Args:
            namespaces (list): List of namespaces to check

        Returns:
            list: List of security findings
        """
        self.findings = []

        for namespace in namespaces:
            # Skip system namespaces
            if namespace.startswith("kube-"):
                continue

            try:
                self._check_pod_resource_limits(namespace)
            except Exception as e:
                # Log error but continue checking other namespaces
                pass

        return self.findings

    def _check_pod_resource_limits(self, namespace):
        """Check pods for missing resource limits"""
        try:
            pods = self.k8s_client.get_pods(namespace)

            for pod in pods:
                pod_name = pod.metadata.name

                # Check each container in the pod
                if pod.spec.containers:
                    for container in pod.spec.containers:
                        self._check_container_resources(pod_name, namespace, container)

        except Exception as e:
            pass

    def _check_container_resources(self, pod_name, namespace, container):
        """Check container resource configuration"""
        container_name = container.name

        # Check if resources are defined
        if not container.resources:
            self.findings.append(
                {
                    "severity": "MEDIUM",
                    "category": "Resource Limits",
                    "title": f"No resource limits or requests defined",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container has no resource limits or requests defined",
                    "recommendation": "Define both resource requests and limits",
                    "remediation": "Add resources.requests and resources.limits for CPU and memory",
                }
            )
            return

        # Check for missing CPU limits
        if not self._has_cpu_limit(container):
            self.findings.append(
                {
                    "severity": "LOW",
                    "category": "Resource Limits",
                    "title": f"Missing CPU limit",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container has no CPU limit defined",
                    "recommendation": "Set CPU limits to prevent resource exhaustion",
                    "remediation": 'Add resources.limits.cpu (e.g., "500m" or "1")',
                }
            )

        # Check for missing memory limits
        if not self._has_memory_limit(container):
            self.findings.append(
                {
                    "severity": "MEDIUM",
                    "category": "Resource Limits",
                    "title": f"Missing memory limit",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container has no memory limit defined - risk of OOM issues",
                    "recommendation": "Set memory limits to prevent pod from consuming excessive memory",
                    "remediation": 'Add resources.limits.memory (e.g., "512Mi" or "1Gi")',
                }
            )

        # Check for missing CPU requests
        if not self._has_cpu_request(container):
            self.findings.append(
                {
                    "severity": "LOW",
                    "category": "Resource Limits",
                    "title": f"Missing CPU request",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container has no CPU request defined",
                    "recommendation": "Set CPU requests for proper scheduling",
                    "remediation": 'Add resources.requests.cpu (e.g., "250m")',
                }
            )

        # Check for missing memory requests
        if not self._has_memory_request(container):
            self.findings.append(
                {
                    "severity": "LOW",
                    "category": "Resource Limits",
                    "title": f"Missing memory request",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container has no memory request defined",
                    "recommendation": "Set memory requests for proper scheduling",
                    "remediation": 'Add resources.requests.memory (e.g., "256Mi")',
                }
            )

    def _has_cpu_limit(self, container):
        """Check if container has CPU limit"""
        if container.resources and container.resources.limits:
            return "cpu" in container.resources.limits
        return False

    def _has_memory_limit(self, container):
        """Check if container has memory limit"""
        if container.resources and container.resources.limits:
            return "memory" in container.resources.limits
        return False

    def _has_cpu_request(self, container):
        """Check if container has CPU request"""
        if container.resources and container.resources.requests:
            return "cpu" in container.resources.requests
        return False

    def _has_memory_request(self, container):
        """Check if container has memory request"""
        if container.resources and container.resources.requests:
            return "memory" in container.resources.requests
        return False
