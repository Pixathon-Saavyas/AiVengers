
from uagents import Bureau

from agents.analyzer_agent  import analyzer_agent
from agents.u import user_agent


if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8002/submit", port=8000)
    print(f"Adding agent to Bureau: {analyzer_agent.address}")
    bureau.add(analyzer_agent)
    print(f"Adding user agent to Bureau: {user_agent.address}")
    bureau.add(user_agent)
