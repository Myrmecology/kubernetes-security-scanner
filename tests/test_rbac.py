"""
Unit tests for RBAC Checker
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.checks.rbac_checker import RBACChecker


class TestRBACChecker:
    """Test cases for RBACChecker"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_k8s_client = Mock()
        self.checker = RBACChecker(self.mock_k8s_client)

    def test_checker_initialization(self):
        """Test that checker initializes correctly"""
        assert self.checker.k8s_client == self.mock_k8s_client
        assert self.checker.findings == []

    def test_detects_cluster_admin_binding(self):
        """Test detection of cluster-admin role bindings"""
        # Create mock cluster role binding with cluster-admin
        mock_binding = self._create_mock_cluster_role_binding(
            binding_name="dangerous-binding",
            role_name="cluster-admin",
            subject_name="default",
            subject_kind="ServiceAccount"
        )

        self.mock_k8s_client.get_cluster_role_bindings.return_value = [mock_binding]
        self.mock_k8s_client.get_role_bindings.return_value = []
        
        findings = self.checker.check(["default"])
        
        # Should detect cluster-admin binding
        assert len(findings) > 0
        assert any("cluster-admin" in f['title'].lower() for f in findings)
        assert any(f['severity'] == 'CRITICAL' for f in findings)

    def test_detects_elevated_role_binding(self):
        """Test detection of elevated role bindings"""
        # Create mock role binding with admin role
        mock_binding = self._create_mock_role_binding(
            binding_name="admin-binding",
            namespace="production",
            role_name="admin",
            subject_name="app-sa",
            subject_kind="ServiceAccount"
        )

        self.mock_k8s_client.get_cluster_role_bindings.return_value = []
        self.mock_k8s_client.get_role_bindings.return_value = [mock_binding]
        
        findings = self.checker.check(["production"])
        
        # Should detect elevated role
        assert len(findings) > 0
        assert any("elevated" in f['title'].lower() or "admin" in f['title'].lower() for f in findings)

    def test_default_service_account_gets_critical_severity(self):
        """Test that default SA with cluster-admin gets CRITICAL severity"""
        # Create mock binding with default SA
        mock_binding = self._create_mock_cluster_role_binding(
            binding_name="bad-default-binding",
            role_name="cluster-admin",
            subject_name="default",
            subject_kind="ServiceAccount"
        )

        self.mock_k8s_client.get_cluster_role_bindings.return_value = [mock_binding]
        self.mock_k8s_client.get_role_bindings.return_value = []
        
        findings = self.checker.check(["default"])
        
        # Default SA should get CRITICAL severity
        critical_findings = [f for f in findings if f['severity'] == 'CRITICAL']
        assert len(critical_findings) > 0

    def test_no_findings_for_proper_rbac(self):
        """Test that properly configured RBAC doesn't generate findings"""
        # Create mock binding with custom role (not admin/cluster-admin/edit)
        mock_binding = self._create_mock_role_binding(
            binding_name="proper-binding",
            namespace="default",
            role_name="custom-viewer",
            subject_name="app-sa",
            subject_kind="ServiceAccount"
        )

        self.mock_k8s_client.get_cluster_role_bindings.return_value = []
        self.mock_k8s_client.get_role_bindings.return_value = [mock_binding]
        
        findings = self.checker.check(["default"])
        
        # Should have no critical findings for custom roles
        assert len(findings) == 0

    def _create_mock_cluster_role_binding(self, binding_name, role_name, 
                                          subject_name, subject_kind):
        """Helper to create mock cluster role binding"""
        mock_binding = Mock()
        mock_binding.metadata.name = binding_name
        
        # Role reference
        mock_binding.role_ref = Mock()
        mock_binding.role_ref.name = role_name
        
        # Subject
        mock_subject = Mock()
        mock_subject.kind = subject_kind
        mock_subject.name = subject_name
        mock_subject.namespace = "default"
        
        mock_binding.subjects = [mock_subject]
        
        return mock_binding

    def _create_mock_role_binding(self, binding_name, namespace, role_name,
                                  subject_name, subject_kind):
        """Helper to create mock role binding"""
        mock_binding = Mock()
        mock_binding.metadata.name = binding_name
        mock_binding.metadata.namespace = namespace
        
        # Role reference
        mock_binding.role_ref = Mock()
        mock_binding.role_ref.name = role_name
        
        # Subject
        mock_subject = Mock()
        mock_subject.kind = subject_kind
        mock_subject.name = subject_name
        
        mock_binding.subjects = [mock_subject]
        
        return mock_binding


if __name__ == "__main__":
    pytest.main([__file__, "-v"])