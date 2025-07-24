# agents/devops_agent.py

import subprocess
import json
import os

class DevOpsAgent:
    def __init__(self, agent_id="devops_agent", config=None):
        self.agent_id = agent_id
        self.config = config or {}

        self.kpi_path = self.config.get("kpi_path", "data/kpi_report.json")
        self.etl_script = self.config.get("etl_script", "scripts/run_etl.py")
        self.db_sync_script = self.config.get("db_sync_script", "scripts/db_sync.py")
        self.dashboard_script = self.config.get("dashboard_script", "scripts/update_dashboard.py")

    def _run_script(self, script_path):
        if not os.path.exists(script_path):
            return f"❌ Script not found: {script_path}"
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return f"✅ Task completed:\n{result.stdout}"
            else:
                return f"❌ Error running script:\n{result.stderr}"
        except Exception as e:
            return f"❌ Exception: {str(e)}"

    def _show_kpi(self):
        if not os.path.exists(self.kpi_path):
            return "❌ KPI report not found."

        with open(self.kpi_path, "r") as f:
            kpis = json.load(f)

        response = "📊 **Latest KPIs:**\n"
        for key, value in kpis.items():
            response += f"- {key}: {value}\n"
        return response

    def answer_query(self, query):
        query_lower = query.lower()

        if "etl" in query_lower or "run pipeline" in query_lower:
            return self._run_script(self.etl_script)

        elif "sync" in query_lower and ("db" in query_lower or "database" in query_lower):
            return self._run_script(self.db_sync_script)

        elif "dashboard" in query_lower or "update dashboard" in query_lower or "refresh dashboard" in query_lower:
            return self._run_script(self.dashboard_script)

        elif "kpi" in query_lower or "report" in query_lower or "metrics" in query_lower:
            return self._show_kpi()

        else:
            return "❓ I couldn’t recognize the DevOps task. Try asking about ETL, DB sync, dashboards, or KPIs."
