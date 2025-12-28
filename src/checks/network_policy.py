"""
Network policy checker - Validates network segmentation and policies
"""


class NetworkPolicyChecker:
    """Check network policies for security issues"""

    def __init__(self, k8s_client):
        """
        Initialize network policy checker

        Args:
            k8s_client: Kubernetes client instance
        """
        self.k8s_client = k8s_client
        self.findings = []

    def check(self, namespaces):
        """
        Run all network policy checks

        Args:
            namespaces (list): List of namespaces to check

        Returns:
            list: List of security findings
        """
        self.findings = []

        for namespace in namespaces:
            # Skip system namespaces for network policy checks
            if namespace.startswith("kube-"):
                continue

            try:
                self._check_namespace_network_policies(namespace)
            except Exception as e:
                # Log error but continue checking other namespaces
                pass

        return self.findings

    def _check_namespace_network_policies(self, namespace):
        """Check network policies in a namespace"""
        try:
            # Get all network policies in namespace
            policies = self.k8s_client.get_network_policies(namespace)

            # Get all pods in namespace to check coverage
            pods = self.k8s_client.get_pods(namespace)

            if not policies:
                # No network policies found
                if len(pods) > 0:
                    self.findings.append(
                        {
                            "severity": "HIGH",
                            "category": "Network Policy",
                            "title": f"No network policies defined",
                            "resource_name": "NetworkPolicy",
                            "namespace": namespace,
                            "description": f'Namespace "{namespace}" has {len(pods)} pods but no network policies',
                            "recommendation": "Implement network policies to control traffic between pods",
                            "remediation": "Create default-deny ingress/egress policies and allow only necessary traffic",
                        }
                    )
            else:
                # Check individual policies for issues
                for policy in policies:
                    self._check_policy_configuration(policy, namespace)

                # Check if there's a default deny policy
                has_default_deny = self._has_default_deny_policy(policies)
                if not has_default_deny:
                    self.findings.append(
                        {
                            "severity": "MEDIUM",
                            "category": "Network Policy",
                            "title": f"Missing default deny policy",
                            "resource_name": "NetworkPolicy",
                            "namespace": namespace,
                            "description": f"No default-deny network policy found in namespace",
                            "recommendation": "Implement a default-deny policy and explicitly allow required traffic",
                            "remediation": "Create a policy that selects all pods with empty ingress/egress rules",
                        }
                    )

        except Exception as e:
            pass

    def _check_policy_configuration(self, policy, namespace):
        """Check individual network policy for security issues"""
        policy_name = policy.metadata.name

        # Check for overly permissive ingress rules
        if policy.spec.ingress:
            for rule in policy.spec.ingress:
                if self._is_rule_too_permissive(rule):
                    self.findings.append(
                        {
                            "severity": "MEDIUM",
                            "category": "Network Policy",
                            "title": f"Overly permissive ingress rule",
                            "resource_name": policy_name,
                            "namespace": namespace,
                            "description": f"Network policy has ingress rule allowing traffic from all sources",
                            "recommendation": "Restrict ingress to specific namespaces or pod selectors",
                            "remediation": "Add namespaceSelector or podSelector to limit traffic sources",
                        }
                    )

        # Check for overly permissive egress rules
        if policy.spec.egress:
            for rule in policy.spec.egress:
                if self._is_rule_too_permissive(rule):
                    self.findings.append(
                        {
                            "severity": "LOW",
                            "category": "Network Policy",
                            "title": f"Overly permissive egress rule",
                            "resource_name": policy_name,
                            "namespace": namespace,
                            "description": f"Network policy allows unrestricted egress traffic",
                            "recommendation": "Restrict egress to specific destinations",
                            "remediation": "Add to: section with specific namespaceSelector or podSelector",
                        }
                    )

    def _is_rule_too_permissive(self, rule):
        """Check if a network policy rule is too permissive"""
        # If there's no 'from' (for ingress) or 'to' (for egress), it allows all
        if hasattr(rule, "from_") and not rule.from_:
            return True
        if hasattr(rule, "to") and not rule.to:
            return True

        # Check if rule allows from all namespaces without restrictions
        if hasattr(rule, "from_") and rule.from_:
            for peer in rule.from_:
                # Empty namespaceSelector means all namespaces
                if (
                    peer.namespace_selector is not None
                    and not peer.namespace_selector.match_labels
                ):
                    return True

        if hasattr(rule, "to") and rule.to:
            for peer in rule.to:
                # Empty namespaceSelector means all namespaces
                if (
                    peer.namespace_selector is not None
                    and not peer.namespace_selector.match_labels
                ):
                    return True

        return False

    def _has_default_deny_policy(self, policies):
        """Check if namespace has a default deny policy"""
        for policy in policies:
            # A default deny policy typically:
            # 1. Selects all pods (empty podSelector)
            # 2. Has empty ingress/egress rules or missing entirely

            if policy.spec.pod_selector and not policy.spec.pod_selector.match_labels:
                # Selects all pods
                # Check if it denies by default (empty rules or no rules)
                if not policy.spec.ingress or not policy.spec.egress:
                    return True

        return False
