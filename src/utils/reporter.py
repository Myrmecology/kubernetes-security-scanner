"""
Report generation utilities
"""

import json
from datetime import datetime
from colorama import Fore, Style
from tabulate import tabulate


class Reporter:
    """Generate security scan reports in various formats"""

    # Severity colors
    SEVERITY_COLORS = {
        'CRITICAL': Fore.RED,
        'HIGH': Fore.LIGHTRED_EX,
        'MEDIUM': Fore.YELLOW,
        'LOW': Fore.LIGHTYELLOW_EX,
        'INFO': Fore.CYAN
    }

    # Severity icons
    SEVERITY_ICONS = {
        'CRITICAL': '🔴',
        'HIGH': '🟠',
        'MEDIUM': '🟡',
        'LOW': '🟢',
        'INFO': 'ℹ️'
    }

    def __init__(self, findings, output_format="text"):
        """
        Initialize reporter

        Args:
            findings (list): List of security findings
            output_format (str): Output format - 'text' or 'json'
        """
        self.findings = findings
        self.output_format = output_format
        self.timestamp = datetime.now().isoformat()

    def print_console_report(self):
        """Print detailed findings to console"""
        if not self.findings:
            print(f"\n{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ No security issues found!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}\n")
            return

        print(f"\n{Fore.RED}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.RED}⚠️  Security Issues Detected{Style.RESET_ALL}")
        print(f"{Fore.RED}{'=' * 60}{Style.RESET_ALL}\n")

        # Group findings by severity
        findings_by_severity = self._group_by_severity()

        # Print findings for each severity level
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            if severity in findings_by_severity:
                self._print_severity_group(severity, findings_by_severity[severity])

        # Print summary
        self._print_summary()

    def _group_by_severity(self):
        """Group findings by severity level"""
        grouped = {}
        for finding in self.findings:
            severity = finding.get('severity', 'INFO')
            if severity not in grouped:
                grouped[severity] = []
            grouped[severity].append(finding)
        return grouped

    def _print_severity_group(self, severity, findings):
        """Print a group of findings with the same severity"""
        color = self.SEVERITY_COLORS.get(severity, Fore.WHITE)
        icon = self.SEVERITY_ICONS.get(severity, '•')

        print(f"{color}{'─' * 60}{Style.RESET_ALL}")
        print(f"{color}{icon} {severity} Issues ({len(findings)}){Style.RESET_ALL}")
        print(f"{color}{'─' * 60}{Style.RESET_ALL}\n")

        for i, finding in enumerate(findings, 1):
            print(f"{color}[{severity}] {finding.get('title', 'Unknown Issue')}{Style.RESET_ALL}")
            print(f"  Resource: {finding.get('resource_name', 'N/A')}")
            print(f"  Namespace: {finding.get('namespace', 'N/A')}")
            print(f"  Category: {finding.get('category', 'N/A')}")
            
            if finding.get('description'):
                print(f"  Description: {finding['description']}")
            
            if finding.get('recommendation'):
                print(f"  {Fore.CYAN}💡 Recommendation: {finding['recommendation']}{Style.RESET_ALL}")
            
            if finding.get('remediation'):
                print(f"  {Fore.GREEN}🔧 Remediation: {finding['remediation']}{Style.RESET_ALL}")
            
            print()  # Blank line between findings

    def _print_summary(self):
        """Print summary statistics"""
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Summary{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

        # Count by severity
        severity_counts = {}
        for finding in self.findings:
            severity = finding.get('severity', 'INFO')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Create summary table
        table_data = []
        total = 0
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                icon = self.SEVERITY_ICONS.get(severity, '•')
                table_data.append([f"{icon} {severity}", count])
                total += count

        table_data.append(['─' * 20, '─' * 5])
        table_data.append(['TOTAL ISSUES', total])

        print(tabulate(table_data, headers=['Severity', 'Count'], tablefmt='simple'))
        print()

        # Security posture assessment
        critical_count = severity_counts.get('CRITICAL', 0)
        high_count = severity_counts.get('HIGH', 0)

        if critical_count > 0:
            print(f"{Fore.RED}🚨 Security Posture: CRITICAL - Immediate action required!{Style.RESET_ALL}")
        elif high_count > 0:
            print(f"{Fore.YELLOW}⚠️  Security Posture: NEEDS ATTENTION - Address high-priority issues{Style.RESET_ALL}")
        elif total > 0:
            print(f"{Fore.YELLOW}⚡ Security Posture: FAIR - Minor improvements recommended{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✅ Security Posture: EXCELLENT - No issues detected{Style.RESET_ALL}")

        print()

    def generate_json_report(self):
        """
        Generate JSON report

        Returns:
            str: JSON formatted report
        """
        report = {
            'scan_metadata': {
                'timestamp': self.timestamp,
                'total_findings': len(self.findings),
                'scanner_version': '1.0.0'
            },
            'summary': self._generate_summary(),
            'findings': self.findings
        }
        return json.dumps(report, indent=2)

    def _generate_summary(self):
        """Generate summary statistics"""
        severity_counts = {}
        categories = {}

        for finding in self.findings:
            severity = finding.get('severity', 'INFO')
            category = finding.get('category', 'Unknown')

            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            categories[category] = categories.get(category, 0) + 1

        return {
            'severity_breakdown': severity_counts,
            'category_breakdown': categories,
            'total_issues': len(self.findings)
        }

    def save_json_report(self, filename):
        """
        Save report to JSON file

        Args:
            filename (str): Output file path
        """
        report = self.generate_json_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)