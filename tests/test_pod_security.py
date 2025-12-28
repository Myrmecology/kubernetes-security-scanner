"""
Unit tests for Pod Security Checker
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.checks.pod_security import PodSecurityChecker


class TestPodSecurityChecker:
    """Test cases for PodSecurityChecker"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_k8s_client = Mock()
        self.checker = PodSecurityChecker(self.mock_k8s_client)

    def test_checker_initialization(self):
        """Test that checker initializes correctly"""
        assert self.checker.k8s_client == self.mock_k8s_client
        assert self.checker.findings == []

    def test_detects_root_user(self):
        """Test detection of containers running as root"""
        # Create mock pod with root user
        mock_pod = self._create_mock_pod(
            pod_name="test-pod",
            namespace="default",
            run_as_user=0
        )

        self.mock_k8s_client.get_pods.return_value = [mock_pod]
        
        findings = self.checker.check(["default"])
        
        # Should detect root user
        assert len(findings) > 0
        assert any("root" in f['title'].lower() for f in findings)
        assert any(f['severity'] == 'CRITICAL' for f in findings)

    def test_detects_privileged_container(self):
        """Test detection of privileged containers"""
        # Create mock pod with privileged container
        mock_pod = self._create_mock_pod(
            pod_name="privileged-pod",
            namespace="default",
            privileged=True
        )

        self.mock_k8s_client.get_pods.return_value = [mock_pod]
        
        findings = self.checker.check(["default"])
        
        # Should detect privileged container
        assert len(findings) > 0
        assert any("privileged" in f['title'].lower() for f in findings)

    def test_detects_missing_security_context(self):
        """Test detection of missing security context"""
        # Create mock pod without security context
        mock_pod = self._create_mock_pod(
            pod_name="no-context-pod",
            namespace="default",
            security_context=None
        )

        self.mock_k8s_client.get_pods.return_value = [mock_pod]
        
        findings = self.checker.check(["default"])
        
        # Should detect missing security context
        assert len(findings) > 0
        assert any("security context" in f['title'].lower() for f in findings)

    def test_no_findings_for_secure_pod(self):
        """Test that secure pods don't generate findings"""
        # Create mock pod with proper security settings
        mock_pod = self._create_mock_pod(
            pod_name="secure-pod",
            namespace="default",
            run_as_user=1000,
            privileged=False,
            read_only_root=True,
            allow_privilege_escalation=False
        )

        self.mock_k8s_client.get_pods.return_value = [mock_pod]
        
        findings = self.checker.check(["default"])
        
        # Should have minimal or no critical findings
        critical_findings = [f for f in findings if f['severity'] == 'CRITICAL']
        assert len(critical_findings) == 0

    def _create_mock_pod(self, pod_name, namespace, run_as_user=None, 
                         privileged=False, security_context=True,
                         read_only_root=False, allow_privilege_escalation=None):
        """Helper to create mock pod objects"""
        mock_pod = Mock()
        mock_pod.metadata.name = pod_name
        mock_pod.metadata.namespace = namespace

        # Create mock container
        mock_container = Mock()
        mock_container.name = "test-container"

        if security_context:
            mock_container.security_context = Mock()
            mock_container.security_context.run_as_user = run_as_user
            mock_container.security_context.privileged = privileged
            mock_container.security_context.read_only_root_filesystem = read_only_root
            mock_container.security_context.allow_privilege_escalation = allow_privilege_escalation
            mock_container.security_context.run_as_non_root = (run_as_user != 0) if run_as_user is not None else None
            mock_container.security_context.capabilities = None
        else:
            mock_container.security_context = None

        mock_pod.spec.containers = [mock_container]

        return mock_pod


if __name__ == "__main__":
    pytest.main([__file__, "-v"])