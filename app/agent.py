import json
import re
from pydantic import ValidationError
from google_adk.workflows import Workflow, node, Event, Context, START, END
from google_adk.agents import LlmAgent
from app.models import SupplyChainData

# ==========================================
# 1. Initialize the Specialized Agents
# ==========================================

extraction_agent = LlmAgent(
    name="data_extractor",
    system_prompt=(
        "You are a strict data extraction tool. Review the user's raw text "
        "and extract the supply chain metrics. Output strictly valid JSON."
    ),
    response_model=SupplyChainData
)

optimization_agent = LlmAgent(
    name="carbon_optimizer",
    system_prompt=(
        "You are a supply chain sustainability expert. Review the provided JSON data "
        "and generate a 3-point markdown strategy with actionable, eco-friendly "
        "alternatives."
    )
)

# ==========================================
# 2. Define the Graph Nodes
# ==========================================

@node
def security_screen(ctx: Context) -> Event:
    """Intercepts and scrubs sensitive PII/Financial data before LLM execution."""
    raw_text = ctx.get("user_input", "")
    
    # Redact email addresses
    clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED EMAIL]', raw_text)
    # Redact dollar amounts to protect pricing confidentiality
    clean_text = re.sub(r'\$\d+(?:,\d{3})*(?:\.\d+)?', '[REDACTED AMOUNT]', clean_text)
    
    # Overwrite the original input with the sanitized text
    ctx.set("user_input", clean_text)
    return Event("safe")

@node
def extract_data(ctx: Context) -> Event:
    """Takes unstructured text and forces it into structured JSON."""
    safe_text = ctx.get("user_input")
    
    try:
        structured_data = extraction_agent.run(safe_text)
        ctx.set("parsed_data", structured_data.model_dump())
        return Event("success")
    except ValidationError as e:
        ctx.set("error", str(e))
        return Event("failed")

@node
def generate_strategy(ctx: Context) -> Event:
    """Evaluates the clean JSON and writes the optimization plan."""
    structured_data = ctx.get("parsed_data")
    prompt = f"Analyze this route and suggest greener alternatives: {json.dumps(structured_data)}"
    strategy_markdown = optimization_agent.run(prompt)
    
    ctx.set("final_output", strategy_markdown)
    return Event("complete")

@node
def handle_missing_data(ctx: Context) -> Event:
    """Fallback node if the user inputs garbage text."""
    ctx.set("final_output", "Error: Could not extract necessary supply chain metrics. Please ensure you include origin, destination, weight, and distance.")
    return Event("complete")

# ==========================================
# 3. Wire the Execution Graph
# ==========================================

workflow = Workflow(name="carbon_optima_workflow")

# Register the nodes
workflow.add_node("security", security_screen)
workflow.add_node("extract", extract_data)
workflow.add_node("optimize", generate_strategy)
workflow.add_node("error_handler", handle_missing_data)

# Define the new routing logic (Edges)
workflow.add_edge(START, "security")
workflow.add_edge("security", "extract")

# Conditional routing based on extraction success
workflow.add_conditional_edge("extract", {
    "success": "optimize",
    "failed": "error_handler"
})

workflow.add_edge("optimize", END)
workflow.add_edge("error_handler", END)

# Compile the final agent app for the local server
agent_app = workflow.compile()
