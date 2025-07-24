import json

class HRAgent:
    def __init__(self, agent_id, config):
        self.agent_id = agent_id
        self.config = config
        with open("data/hr_db.json", "r") as f:
            self.hr_data = json.load(f)

    def answer_query(self, query, session_id=None):
        if not session_id or session_id not in self.hr_data:
            return "⚠️ Unauthorized or unknown employee. Please log in."

        profile = self.hr_data[session_id]
        query = query.lower()

        if "leave" in query:
            used = profile["leaves"]["used"]
            remaining = profile["leaves"]["remaining"]
            return f"📝 You’ve used {used} leaves. You have {remaining} remaining."

        elif "salary" in query:
            return f"💵 Your current salary is {profile['salary']}."

        elif "appraisal" in query or "rating" in query:
            return f"📈 Your last appraisal was: {profile['last_appraisal']}."

        elif "holiday" in query:
            holidays = ", ".join(profile["holiday_list"])
            return f"🎉 Upcoming holidays: {holidays}"

        else:
            return "🤔 I couldn’t understand the HR request. Try asking about leaves, salary, appraisals, or holidays."
