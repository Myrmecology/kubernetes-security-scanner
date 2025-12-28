#!/bin/bash

# Kubernetes Security Scanner - Run Script
# This script simplifies running the security scanner

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Kubernetes Security Scanner${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python is not installed${NC}"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${YELLOW}Warning: kubectl is not installed or not in PATH${NC}"
    echo -e "${YELLOW}The scanner requires kubectl to connect to Kubernetes${NC}"
    exit 1
fi

# Check if connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Not connected to a Kubernetes cluster${NC}"
    echo -e "${YELLOW}Please configure kubectl to connect to your cluster${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $($PYTHON_CMD --version)${NC}"
echo -e "${GREEN}✓ kubectl found: $(kubectl version --client --short 2>/dev/null || kubectl version --client)${NC}"
echo -e "${GREEN}✓ Cluster connection verified${NC}"
echo ""

# Check if dependencies are installed
if ! $PYTHON_CMD -c "import kubernetes" &> /dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    $PYTHON_CMD -m pip install -r requirements.txt
    echo ""
fi

# Run the scanner with any passed arguments
echo -e "${CYAN}Starting security scan...${NC}"
echo ""

$PYTHON_CMD -m src.scanner "$@"

exit 0