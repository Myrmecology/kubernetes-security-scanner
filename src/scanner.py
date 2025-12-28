"""
Main scanner module - Entry point for Kubernetes Security Scanner
"""

import sys
import argparse
from datetime import datetime
from colorama import init, Fore, Style

from src.utils.k8s_client import K8sClient
from src.checks.pod_security import PodSecurityChecker
from src.checks.rbac_checker import RBACChecker
from src.checks.network_policy import NetworkPolicyChecker
from src.checks.resource_limits import ResourceLimitChecker
from src.utils.reporter import Reporter

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class SecurityScanner:
    """Main security scanner orchestrator"""

    def __init__(self, namespace=None, output_format="text"):
        """
        Initialize the security scanner

        Args:
            namespace (str): Specific namespace to scan, or None for all namespaces
            output_format (str): Output format - 'text', 'json', or 'html'
        """
        self.namespace = namespace
        self.output_format = output_format
        self.k8s_client = None
        self.findings = []

    def connect_to_cluster(self):
        """Establish connection to Kubernetes cluster"""
        try:
            print(f"{Fore.CYAN}🔌 Connecting to Kubernetes cluster...{Style.RESET_ALL}")
            self.k8s_client = K8sClient()
            cluster_info = self.k8s_client.get_cluster_info()
            print(f"{Fore.GREEN}✅ Connected to cluster: {cluster_info['name']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Server: {cluster_info['server']}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to connect to cluster: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Make sure kubectl is configured and you have cluster access{Style.RESET_ALL}")
            return False

    def run_checks(self):
        """Execute all security checks"""
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🔍 Starting Kubernetes Security Scan{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

        # Get namespaces to scan
        if self.namespace:
            namespaces = [self.namespace]
            print(f"{Fore.CYAN}📦 Scanning namespace: {self.namespace}{Style.RESET_ALL}\n")
        else:
            namespaces = self.k8s_client.get_namespaces()
            print(f"{Fore.CYAN}📦 Scanning all namespaces ({len(namespaces)} found){Style.RESET_ALL}\n")

        # Initialize checkers
        checkers = [
            PodSecurityChecker(self.k8s_client),
            RBACChecker(self.k8s_client),
            NetworkPolicyChecker(self.k8s_client),
            ResourceLimitChecker(self.k8s_client)
        ]

        # Run each checker
        for checker in checkers:
            print(f"{Fore.YELLOW}⚡ Running {checker.__class__.__name__}...{Style.RESET_ALL}")
            try:
                findings = checker.check(namespaces)
                self.findings.extend(findings)
                print(f"{Fore.GREEN}   ✓ Found {len(findings)} issues{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}   ✗ Error: {str(e)}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

    def generate_report(self):
        """Generate and display the security report"""
        reporter = Reporter(self.findings, output_format=self.output_format)

        if self.output_format == "text":
            reporter.print_console_report()
        elif self.output_format == "json":
            report = reporter.generate_json_report()
            print(report)
        else:
            print(f"{Fore.RED}Unsupported output format: {self.output_format}{Style.RESET_ALL}")

    def save_report(self, filename):
        """Save report to file"""
        reporter = Reporter(self.findings, output_format=self.output_format)
        try:
            if self.output_format == "json":
                reporter.save_json_report(filename)
                print(f"\n{Fore.GREEN}📄 Report saved to: {filename}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}File saving only supported for JSON format{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to save report: {str(e)}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Kubernetes Security Scanner - Identify cluster misconfigurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan all namespaces
  python -m src.scanner

  # Scan specific namespace
  python -m src.scanner --namespace production

  # Generate JSON report
  python -m src.scanner --output json --file report.json

  # Scan and save results
  python -m src.scanner --namespace default --output json --file results.json
        """
    )

    parser.add_argument(
        "-n", "--namespace",
        help="Specific namespace to scan (default: all namespaces)",
        default=None
    )

    parser.add_argument(
        "-o", "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "-f", "--file",
        help="Output file path (only for JSON format)",
        default=None
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Kubernetes Security Scanner v1.0.0"
    )

    args = parser.parse_args()

    # Print banner
    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Kubernetes Security Scanner v1.0.0{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Scanning for misconfigurations and vulnerabilities{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    # Initialize scanner
    scanner = SecurityScanner(
        namespace=args.namespace,
        output_format=args.output
    )

    # Connect to cluster
    if not scanner.connect_to_cluster():
        sys.exit(1)

    # Run security checks
    try:
        scanner.run_checks()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error during scan: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

    # Generate report
    scanner.generate_report()

    # Save to file if requested
    if args.file:
        scanner.save_report(args.file)

    print(f"\n{Fore.GREEN}✅ Scan complete!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()