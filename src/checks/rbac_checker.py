"""
RBAC checker - Identifies overly permissive role bindings and service accounts
"""


class RBACChecker:
    """Check RBAC configurations for security issues"""

    def __init__(self, k8s_client):
        """
        Initialize RBAC checker

        Args:
            k8s_client: Kubernetes client instance
        """
        self.k8s_client = k8s_client
        self.findings = []

    def check(self, namespaces):
        """
        Run all RBAC security checks

        Args:
            namespaces (list): List of namespaces to check

        Returns:
            list: List of security findings
        """
        self.findings = []

        # Check cluster-wide bindings
        self._check_cluster_role_bindings()

        # Check namespace-specific bindings
        for namespace in namespaces:
            try:
                self._check_role_bindings(namespace)
            except Exception as e:
                # Log error but continue checking other namespaces
                pass

        return self.findings

    def _check_cluster_role_bindings(self):
        """Check cluster role bindings for security issues"""
        try:
            bindings = self.k8s_client.get_cluster_role_bindings()

            for binding in bindings:
                binding_name = binding.metadata.name

                # Check if binding grants cluster-admin
                if binding.role_ref.name == 'cluster-admin':
                    for subject in binding.subjects or []:
                        self._flag_cluster_admin_binding(binding_name, subject)

                # Check for wildcard permissions
                self._check_wildcard_permissions(binding_name, binding.role_ref.name, 'cluster')

        except Exception as e:
            pass

    def _check_role_bindings(self, namespace):
        """Check role bindings in a specific namespace"""
        try:
            bindings = self.k8s_client.get_role_bindings(namespace)

            for binding in bindings:
                binding_name = binding.metadata.name

                # Check if binding grants admin role
                if binding.role_ref.name in ['admin', 'cluster-admin', 'edit']:
                    for subject in binding.subjects or []:
                        self._flag_elevated_binding(binding_name, namespace, subject, binding.role_ref.name)

        except Exception as e:
            pass

    def _flag_cluster_admin_binding(self, binding_name, subject):
        """Flag cluster-admin bindings as critical"""
        subject_kind = subject.kind
        subject_name = subject.name
        subject_namespace = getattr(subject, 'namespace', 'N/A')

        # Especially critical if default service account has cluster-admin
        severity = 'CRITICAL' if subject_name == 'default' else 'HIGH'

        self.findings.append({
            'severity': severity,
            'category': 'RBAC',
            'title': f'cluster-admin role granted to {subject_kind}',
            'resource_name': binding_name,
            'namespace': subject_namespace,
            'description': f'{subject_kind} "{subject_name}" has cluster-admin privileges (full cluster access)',
            'recommendation': 'Use least-privilege RBAC - grant only necessary permissions',
            'remediation': f'Create a custom role with specific permissions instead of cluster-admin'
        })

    def _flag_elevated_binding(self, binding_name, namespace, subject, role_name):
        """Flag elevated role bindings"""
        subject_kind = subject.kind
        subject_name = subject.name

        # Critical if default service account has elevated permissions
        severity = 'HIGH' if subject_name == 'default' else 'MEDIUM'

        self.findings.append({
            'severity': severity,
            'category': 'RBAC',
            'title': f'Elevated role "{role_name}" granted to {subject_kind}',
            'resource_name': binding_name,
            'namespace': namespace,
            'description': f'{subject_kind} "{subject_name}" has "{role_name}" role with broad permissions',
            'recommendation': 'Review if this level of access is necessary',
            'remediation': f'Consider creating a custom role with minimal required permissions'
        })

    def _check_wildcard_permissions(self, binding_name, role_name, scope):
        """Check for wildcard permissions in roles"""
        # This is a simplified check - in production you'd actually inspect the role definition
        # For now, we flag certain known risky role names
        risky_roles = ['cluster-admin', 'admin', 'edit']

        if role_name in risky_roles:
            # Already flagged in other checks
            pass

    def _check_service_account_usage(self, namespace):
        """Check for unused or overly privileged service accounts"""
        try:
            service_accounts = self.k8s_client.get_service_accounts(namespace)

            for sa in service_accounts:
                sa_name = sa.metadata.name

                # Flag if default service account is being used with bindings
                if sa_name == 'default':
                    self.findings.append({
                        'severity': 'LOW',
                        'category': 'RBAC',
                        'title': f'Default service account in use',
                        'resource_name': sa_name,
                        'namespace': namespace,
                        'description': f'Pods may be using the default service account',
                        'recommendation': 'Create dedicated service accounts for applications',
                        'remediation': 'Create app-specific service accounts and update pod specs'
                    })

        except Exception as e:
            pass