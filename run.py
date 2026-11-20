"""Entry point for AgentHive SaaS."""
import os
import sys

# Ensure the project root is on the path (always, for package discovery)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Also add parent so 'agenthive' can be found as top-level package
parent = os.path.dirname(project_root)
if parent not in sys.path:
    sys.path.insert(0, parent)

# Now import and run the FastAPI app
import uvicorn
from agenthive.app.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )