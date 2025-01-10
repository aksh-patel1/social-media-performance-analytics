from langflow.load import run_flow_from_json
import os
from dotenv import load_dotenv

load_dotenv()

TWEAKS = {
  "Prompt-D4Tlk": {},
  "OpenAIModel-06Kop": {
      "model_name": "gpt-4o",
      "api_key": os.getenv("OPENAI_API_KEY")
  },
  "CustomComponent-RxJSz": {},
  "File-G9ILJ": {},
  "File-1Y6hF": {},
  "CustomComponent-ajfls": {},
  "CustomComponent-eFuHu": {},
  "ChatInput-iY3bZ": {},
  "ChatOutput-g2kPl": {}
}

result = run_flow_from_json(flow="../social-media-performance-analytics-langflow-config.json",
                            input_value="STATIC,  REEL",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)