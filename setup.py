"""
Kubernetes Security Scanner - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kubernetes-security-scanner",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive security auditing tool for Kubernetes clusters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR-USERNAME/kubernetes-security-scanner",
    packages=find_packages(exclude=["tests", "demo", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "k8s-scan=src.scanner:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="kubernetes security scanner audit devops cloud-security k8s",
    project_urls={
        "Bug Reports": "https://github.com/YOUR-USERNAME/kubernetes-security-scanner/issues",
        "Source": "https://github.com/YOUR-USERNAME/kubernetes-security-scanner",
        "Documentation": "https://github.com/YOUR-USERNAME/kubernetes-security-scanner/blob/main/README.md",
    },
)