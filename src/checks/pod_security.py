"""
Pod security checker - Identifies insecure pod configurations
"""


class PodSecurityChecker:
    """Check pods for security misconfigurations"""

    def __init__(self, k8s_client):
        """
        Initialize pod security checker

        Args:
            k8s_client: Kubernetes client instance
        """
        self.k8s_client = k8s_client
        self.findings = []

    def check(self, namespaces):
        """
        Run all pod security checks

        Args:
            namespaces (list): List of namespaces to check

        Returns:
            list: List of security findings
        """
        self.findings = []

        for namespace in namespaces:
            try:
                pods = self.k8s_client.get_pods(namespace)
                for pod in pods:
                    self._check_pod_security(pod)
            except Exception as e:
                # Log error but continue checking other namespaces
                pass

        return self.findings

    def _check_pod_security(self, pod):
        """Check individual pod for security issues"""
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace

        # Check each container in the pod
        if pod.spec.containers:
            for container in pod.spec.containers:
                self._check_container_security(pod_name, namespace, container)

    def _check_container_security(self, pod_name, namespace, container):
        """Check container security configuration"""
        container_name = container.name

        # Check if running as root
        if self._is_running_as_root(container):
            self.findings.append(
                {
                    "severity": "CRITICAL",
                    "category": "Pod Security",
                    "title": f"Container running as root (UID 0)",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f'Container "{container_name}" in pod "{pod_name}" is running as root user (UID 0)',
                    "recommendation": "Set runAsUser to a non-zero value in securityContext",
                    "remediation": "Add securityContext with runAsUser: 1000 (or any non-zero UID)",
                }
            )

        # Check for privileged containers
        if self._is_privileged(container):
            self.findings.append(
                {
                    "severity": "CRITICAL",
                    "category": "Pod Security",
                    "title": f"Privileged container detected",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f'Container "{container_name}" is running in privileged mode',
                    "recommendation": "Remove privileged: true from securityContext unless absolutely necessary",
                    "remediation": "Set privileged: false or remove the privileged field entirely",
                }
            )

        # Check for dangerous capabilities
        dangerous_caps = self._check_capabilities(container)
        if dangerous_caps:
            self.findings.append(
                {
                    "severity": "HIGH",
                    "category": "Pod Security",
                    "title": f"Dangerous capabilities granted",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f'Container has dangerous capabilities: {", ".join(dangerous_caps)}',
                    "recommendation": "Remove unnecessary capabilities, especially CAP_SYS_ADMIN and CAP_NET_ADMIN",
                    "remediation": 'Drop all capabilities and add only required ones using drop: ["ALL"] and add: [...]',
                }
            )

        # Check if allowPrivilegeEscalation is enabled
        if self._allows_privilege_escalation(container):
            self.findings.append(
                {
                    "severity": "HIGH",
                    "category": "Pod Security",
                    "title": f"Privilege escalation allowed",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container allows privilege escalation",
                    "recommendation": "Set allowPrivilegeEscalation: false in securityContext",
                    "remediation": "Add allowPrivilegeEscalation: false to container securityContext",
                }
            )

        # Check for missing security context
        if not container.security_context:
            self.findings.append(
                {
                    "severity": "MEDIUM",
                    "category": "Pod Security",
                    "title": f"Missing security context",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container has no securityContext defined",
                    "recommendation": "Define a securityContext with appropriate settings",
                    "remediation": "Add securityContext with runAsNonRoot: true, allowPrivilegeEscalation: false",
                }
            )

        # Check for readOnlyRootFilesystem
        if not self._has_readonly_root_filesystem(container):
            self.findings.append(
                {
                    "severity": "LOW",
                    "category": "Pod Security",
                    "title": f"Root filesystem is writable",
                    "resource_name": f"{pod_name}/{container_name}",
                    "namespace": namespace,
                    "description": f"Container root filesystem is not read-only",
                    "recommendation": "Set readOnlyRootFilesystem: true unless write access is required",
                    "remediation": "Add readOnlyRootFilesystem: true to securityContext and use volumes for writable data",
                }
            )

    def _is_running_as_root(self, container):
        """Check if container is running as root"""
        if container.security_context:
            run_as_user = container.security_context.run_as_user
            if run_as_user is not None and run_as_user == 0:
                return True
            # If runAsUser is not set but runAsNonRoot is False or not set, it might run as root
            run_as_non_root = container.security_context.run_as_non_root
            if run_as_user is None and (
                run_as_non_root is None or run_as_non_root is False
            ):
                return True
        else:
            # No security context means it could run as root
            return True
        return False

    def _is_privileged(self, container):
        """Check if container is privileged"""
        if container.security_context and container.security_context.privileged:
            return True
        return False

    def _check_capabilities(self, container):
        """Check for dangerous Linux capabilities"""
        dangerous_capabilities = [
            "SYS_ADMIN",
            "NET_ADMIN",
            "SYS_MODULE",
            "SYS_RAWIO",
            "SYS_PTRACE",
            "SYS_BOOT",
            "MAC_ADMIN",
            "MAC_OVERRIDE",
        ]

        found_dangerous = []

        if container.security_context and container.security_context.capabilities:
            if container.security_context.capabilities.add:
                for cap in container.security_context.capabilities.add:
                    # Remove CAP_ prefix if present for comparison
                    cap_name = cap.replace("CAP_", "")
                    if cap_name in dangerous_capabilities:
                        found_dangerous.append(cap_name)

        return found_dangerous

    def _allows_privilege_escalation(self, container):
        """Check if privilege escalation is allowed"""
        if container.security_context:
            allow_priv_esc = container.security_context.allow_privilege_escalation
            # If not explicitly set to False, it's potentially allowed
            if allow_priv_esc is None or allow_priv_esc is True:
                return True
        else:
            # No security context means default behavior (allowed)
            return True
        return False

    def _has_readonly_root_filesystem(self, container):
        """Check if root filesystem is read-only"""
        if (
            container.security_context
            and container.security_context.read_only_root_filesystem
        ):
            return True
        return False
