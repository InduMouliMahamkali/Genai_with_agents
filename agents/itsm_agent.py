# agents/itsm_agent.py

import json
import os
import uuid
from datetime import datetime

TICKET_DB_PATH = "data/itsm_db.json"

class ITSMAgent:
    def __init__(self):
        if not os.path.exists(TICKET_DB_PATH):
            with open(TICKET_DB_PATH, 'w') as f:
                json.dump([], f)

    def _load_tickets(self):
        with open(TICKET_DB_PATH, 'r') as f:
            return json.load(f)

    def _save_tickets(self, tickets):
        with open(TICKET_DB_PATH, 'w') as f:
            json.dump(tickets, f, indent=2)

    def create_ticket(self, description, user="anonymous"):
        ticket_id = "INC" + str(uuid.uuid4())[:8].upper()
        ticket = {
            "id": ticket_id,
            "description": description,
            "status": "Open",
            "created_at": str(datetime.now()),
            "created_by": user
        }

        tickets = self._load_tickets()
        tickets.append(ticket)
        self._save_tickets(tickets)

        return f"✅ Ticket `{ticket_id}` created for: {description}"

    def get_ticket(self, ticket_id):
        tickets = self._load_tickets()
        for ticket in tickets:
            if ticket["id"].lower() == ticket_id.lower():
                return json.dumps(ticket, indent=2)
        return f"❌ No ticket found with ID `{ticket_id}`."

    def list_open_tickets(self):
        tickets = self._load_tickets()
        open_tickets = [t for t in tickets if t["status"].lower() == "open"]
        if not open_tickets:
            return "✅ No open tickets."
        return "\n\n".join([f"🔹 {t['id']} — {t['description']}" for t in open_tickets])

    def update_ticket(self, ticket_id, status):
        tickets = self._load_tickets()
        for ticket in tickets:
            if ticket["id"].lower() == ticket_id.lower():
                ticket["status"] = status
                self._save_tickets(tickets)
                return f"✅ Ticket `{ticket_id}` updated to status: `{status}`"
        return f"❌ No ticket found with ID `{ticket_id}`."

    def answer_query(self, query: str):
        q = query.lower()

        if "create" in q or "raise" in q:
            return self.create_ticket(description=query)

        elif "status of" in q or "check ticket" in q:
            words = q.split()
            for word in words:
                if word.startswith("inc"):
                    return self.get_ticket(word)

        elif "open tickets" in q or "show incidents" in q:
            return self.list_open_tickets()

        elif "update" in q:
            # crude parser: "update INC1234 to closed"
            parts = q.split()
            ticket_id = next((p for p in parts if p.startswith("inc")), None)
            status = parts[-1].capitalize()
            return self.update_ticket(ticket_id, status)

        return "❓ Sorry, I couldn’t understand your ITSM query."
