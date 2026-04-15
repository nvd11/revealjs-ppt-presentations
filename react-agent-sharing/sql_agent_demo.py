import json

# Mock DB and LLM for demonstration purposes
class MockDB:
    def query(self, sql):
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

class MockLLM:
    def chat(self, messages):
        # Mocking an LLM response: first time asks for tool, second time gives answer
        if len(messages) == 2:
            return '{"tool": "execute_sql", "args": {"sql_string": "SELECT * FROM users"}}'
        return "The users in the database are Alice and Bob."

db = MockDB()
llm = MockLLM()

class SqlAgent:

    # 1. Build a Tool
    def execute_sql(self, sql_string: str):
        print(f"[Tool Executing] Running SQL: {sql_string}")
        return db.query(sql_string)

    # 2. System Prompt
    sys_prompt = """You are a SQL Agent. 
    Tool: execute_sql(sql_string).
    To use a tool, you MUST output JSON: 
    {"tool": "execute_sql", "args": {"sql_string": "SELECT..."}}
    Otherwise, output final answer in plain text."""

    def run(self, user_query: str):
        print(f"[User Query] {user_query}\n" + "-"*40)
        messages = [self.sys_prompt, user_query]
        
        while True:
            # 3. Call LLM
            res_text = llm.chat(messages)
            print(f"[LLM Output] {res_text}")

            # 4 & 6. Parse JSON to Check Intent
            try:
                action = json.loads(res_text)
                if isinstance(action, dict) and "tool" in action and "args" in action:
                    # 4. Intent Yes -> Execute Tool
                    sql = action["args"]["sql_string"]
                    tool_data = self.execute_sql(sql)
                    print(f"[Observation] {tool_data}\n" + "-"*40)

                    # 5. Append Response & Loop
                    messages.append(res_text)
                    messages.append(f"Observation: {tool_data}")
                    continue
            except json.JSONDecodeError:
                pass

            # No JSON / No Tool -> Return final answer
            return res_text

if __name__ == "__main__":
    agent = SqlAgent()
    final_answer = agent.run("Who are the users in our database?")
    print(f"\n[Final Answer] {final_answer}")
