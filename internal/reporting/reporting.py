import os
import jinja2
from pkg.logger.logger import log_error

def generate_report(target, data, log_dir):
    template_path = "templates/report_py.html"
    output_path = os.path.join(log_dir, "report.html")

    if not os.path.exists(template_path):
        log_error(f"Template not found: {template_path}")
        return

    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = env.get_template(template_path)
        
        severity_counts = {
            "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0
        }
        for vuln in data.get("vulnerabilities", []):
            sev = vuln.get("severity", "").lower()
            if sev in severity_counts:
                severity_counts[sev] += 1
        
        # Collect technologies more robustly for the chart
        tech_map = {}
        for sub in data.get("subdomains", []):
            tech_string = sub.get("tech_stack", "N/A")
            if tech_string and tech_string != "N/A":
                # Handle comma separated techs
                techs = [t.strip() for t in tech_string.split(",")]
                for t in techs:
                    tech_map[t] = tech_map.get(t, 0) + 1
        
        tech_labels = list(tech_map.keys())
        tech_counts = list(tech_map.values())

        render_data = {
            **data,
            "severity_counts": severity_counts,
            "tech_labels": tech_labels,
            "tech_counts": tech_counts
        }

        html_content = template.render(render_data)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
    except Exception as e:
        # Fallback to simple file write if jinja fails
        log_error(f"Failed to generate report: {e}")
        with open(os.path.join(log_dir, "recon_data.json"), "w") as f:
            import json
            json.dump(data, f, indent=4)
