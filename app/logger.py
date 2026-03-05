import json
from datetime import datetime

LOG_FILE = "logs/agent_traces.json"

def log_trace(state):
    entry = {
        "timestamp": str(datetime.utcnow()),
        "state": state
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
