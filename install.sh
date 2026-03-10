#!/bin/bash

# ReconSP - Kali Linux Installation Script
# This will install all external tool dependencies

echo "[+] Updating system packages..."
sudo apt update -y

echo "[+] Installing Go..."
sudo apt install golang -y

echo "[+] Installing Security Tools from APT (Kali Repos)..."
sudo apt install subfinder nuclei amass httpx assetfinder -y

echo "[+] Updating Nuclei Templates..."
nuclei -update-templates

echo "[+] Initializing ReconSP Go project..."
go mod tidy

echo "[+] Building ReconSP..."
go build -o reconsp ./cmd/reconsp.go

echo "[✔] Installation Complete! Run with: ./reconsp -u example.com"
