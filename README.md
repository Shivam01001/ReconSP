# 🛡️ ReconSP — Automated Attack Surface Intelligence

ReconSP is a high-performance **Go-based reconnaissance orchestration tool** designed for cybersecurity analysts, bug bounty hunters, and red teamers. It automates the complex pipeline of discovering subdomains, identifying live assets, uncovering hidden endpoints, and scanning for vulnerabilities.

Designed to run seamlessly on both **Windows** and **Kali Linux**, ReconSP converts raw reconnaissance data into actionable intelligence through a premium HTML dashboard.

🔗 **GitHub Repository**: [github.com/Shivam01001/ReconSP](https://github.com/Shivam01001/ReconSP)

---

## 🚀 Key Features

*   **Infrastructure Discovery**: Recursive subdomain enumeration (crt.sh, subfinder, amass).
*   **Active Fingerprinting**: HTTP live host detection and technology stack identification.
*   **JS & API Intelligence**: Extract hidden endpoints and API paths from JavaScript files.
*   **Secret Detection**: Automated regex scanning for AWS keys, Google API keys, JWTs, and Base64-encoded strings.
*   **Vulnerability Scanning**: Full integration with **Nuclei** and its massive template library.
*   **Cloud & Takeover Detection**: Identify exposed S3 buckets and orphaned CNAMEs for subdomain takeovers.
*   **Premium Reporting**: Generates a high-end, responsive HTML report with TailwindCSS and Chart.js analytics.

---

## 🛠️ Installation & Setup (From 0)

### 🐧 On Kali Linux

1.  **Clone & Enter Directory**:
    ```bash
    git clone https://github.com/Shivam01001/ReconSP.git ReconSP
    cd ReconSP
    ```

2.  **Run the Installer**:
    The included `install.sh` script is the heart of the Kali installation. It automatically installs:
    - **Go** (Golang)
    - **Subfinder**
    - **Nuclei**
    - **Amass** & **Httpx**
    - **Assetfinder**
    
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

3.  **Run Your First Scan**:
    ```bash
    ./reconsp -u example.com -d 1
    ```

---

### 🪟 On Windows

1.  **Install Go**: Download and install the latest version from [go.dev/dl](https://go.dev/dl/).
2.  **Add Tools to PATH**: (Optional but Recommended) Download binary releases of [Subfinder](https://github.com/projectdiscovery/subfinder) and [Nuclei](https://github.com/projectdiscovery/nuclei) and add them to your system environment variables.
3.  **Run the Setup Script**:
    ```powershell
    .\setup.bat
    ```
4.  **Run Your First Scan**:
    ```powershell
    .\reconsp.exe -u example.com -d 1
    ```

---

## 📊 Usage Guide

ReconSP is designed with a simple "two-parameter" approach:

```bash
reconsp -u <target-domain> -d <depth>
```

| Parameter | Alias | Description |
| :--- | :--- | :--- |
| `-u` | `--url` | The target domain to scan (e.g., target.com) |
| `-d` | `--depth` | Recursive depth for subdomain discovery (1-3) |

### Example Scenario
To perform a deep 3-level scan on a target:
```bash
./reconsp -u target.com -d 3
```

---

## 📂 Output Structure

All results are saved in the `logs/<target>/` directory:
*   `report.html` — **The main dashboard (Open this!)**
*   `subdomains.txt` — List of discovered hosts.
*   `vulnerabilities.json` — Detailed Nuclei scan results.
*   `errors.log` — Technical troubleshooting logs.
*   `screenshots/` — Visual site snapshots (if enabled).

---

## ⚙️ Configuration

Modify `configs/config.yaml` to customize:
*   **Rate Limits**: (Default: 100 req/sec) to avoid WAF blocking.
*   **Workers**: Concurrency control for high-speed scanning.
*   **API Keys**: Add keys for Shodan or SecurityTrails to enhance discovery.

---

## ⚖️ License & Disclaimer
*ReconSP is provided for authorized security testing and research purposes only. Unauthorized scanning of third-party infrastructure is illegal.*

**Developed with ❤️ for the Security Community.**
