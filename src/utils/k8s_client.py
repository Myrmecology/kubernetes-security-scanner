"""
Kubernetes API client wrapper
"""

from kubernetes import client, config
from kubernetes.client.rest import ApiException


class K8sClient:
    """Wrapper for Kubernetes API client operations"""

    def __init__(self):
        """Initialize Kubernetes client"""
        try:
            # Try to load kubeconfig (for local development)
            config.load_kube_config()
        except Exception:
            try:
                # Fall back to in-cluster config (for running inside K8s)
                config.load_incluster_config()
            except Exception as e:
                raise Exception(f"Failed to load Kubernetes configuration: {str(e)}")

        # Initialize API clients
        self.core_v1 = client.CoreV1Api()
        self.rbac_v1 = client.RbacAuthorizationV1Api()
        self.networking_v1 = client.NetworkingV1Api()
        self.apps_v1 = client.AppsV1Api()

    def get_cluster_info(self):
        """
        Get basic cluster information

        Returns:
            dict: Cluster information including name and server
        """
        try:
            # Get current context
            contexts, active_context = config.list_kube_config_contexts()
            cluster_name = active_context['context']['cluster']
            
            # Get server info
            version_info = client.VersionApi().get_code()
            
            return {
                'name': cluster_name,
                'server': active_context['context'].get('cluster', 'unknown'),
                'version': f"{version_info.major}.{version_info.minor}"
            }
        except Exception as e:
            return {
                'name': 'unknown',
                'server': 'unknown',
                'version': 'unknown'
            }

    def get_namespaces(self):
        """
        Get all namespaces in the cluster

        Returns:
            list: List of namespace names
        """
        try:
            namespaces = self.core_v1.list_namespace()
            return [ns.metadata.name for ns in namespaces.items]
        except ApiException as e:
            raise Exception(f"Failed to list namespaces: {str(e)}")

    def get_pods(self, namespace=None):
        """
        Get all pods in namespace or cluster

        Args:
            namespace (str): Specific namespace, or None for all namespaces

        Returns:
            list: List of pod objects
        """
        try:
            if namespace:
                pods = self.core_v1.list_namespaced_pod(namespace)
            else:
                pods = self.core_v1.list_pod_for_all_namespaces()
            return pods.items
        except ApiException as e:
            raise Exception(f"Failed to list pods: {str(e)}")

    def get_service_accounts(self, namespace=None):
        """
        Get all service accounts

        Args:
            namespace (str): Specific namespace, or None for all namespaces

        Returns:
            list: List of service account objects
        """
        try:
            if namespace:
                sa_list = self.core_v1.list_namespaced_service_account(namespace)
            else:
                sa_list = self.core_v1.list_service_account_for_all_namespaces()
            return sa_list.items
        except ApiException as e:
            raise Exception(f"Failed to list service accounts: {str(e)}")

    def get_roles(self, namespace=None):
        """
        Get all roles

        Args:
            namespace (str): Specific namespace, or None for all namespaces

        Returns:
            list: List of role objects
        """
        try:
            if namespace:
                roles = self.rbac_v1.list_namespaced_role(namespace)
            else:
                roles = self.rbac_v1.list_role_for_all_namespaces()
            return roles.items
        except ApiException as e:
            raise Exception(f"Failed to list roles: {str(e)}")

    def get_cluster_roles(self):
        """
        Get all cluster roles

        Returns:
            list: List of cluster role objects
        """
        try:
            cluster_roles = self.rbac_v1.list_cluster_role()
            return cluster_roles.items
        except ApiException as e:
            raise Exception(f"Failed to list cluster roles: {str(e)}")

    def get_role_bindings(self, namespace=None):
        """
        Get all role bindings

        Args:
            namespace (str): Specific namespace, or None for all namespaces

        Returns:
            list: List of role binding objects
        """
        try:
            if namespace:
                bindings = self.rbac_v1.list_namespaced_role_binding(namespace)
            else:
                bindings = self.rbac_v1.list_role_binding_for_all_namespaces()
            return bindings.items
        except ApiException as e:
            raise Exception(f"Failed to list role bindings: {str(e)}")

    def get_cluster_role_bindings(self):
        """
        Get all cluster role bindings

        Returns:
            list: List of cluster role binding objects
        """
        try:
            bindings = self.rbac_v1.list_cluster_role_binding()
            return bindings.items
        except ApiException as e:
            raise Exception(f"Failed to list cluster role bindings: {str(e)}")

    def get_network_policies(self, namespace=None):
        """
        Get all network policies

        Args:
            namespace (str): Specific namespace, or None for all namespaces

        Returns:
            list: List of network policy objects
        """
        try:
            if namespace:
                policies = self.networking_v1.list_namespaced_network_policy(namespace)
            else:
                policies = self.networking_v1.list_network_policy_for_all_namespaces()
            return policies.items
        except ApiException as e:
            raise Exception(f"Failed to list network policies: {str(e)}")

    def get_deployments(self, namespace=None):
        """
        Get all deployments

        Args:
            namespace (str): Specific namespace, or None for all namespaces

        Returns:
            list: List of deployment objects
        """
        try:
            if namespace:
                deployments = self.apps_v1.list_namespaced_deployment(namespace)
            else:
                deployments = self.apps_v1.list_deployment_for_all_namespaces()
            return deployments.items
        except ApiException as e:
            raise Exception(f"Failed to list deployments: {str(e)}")