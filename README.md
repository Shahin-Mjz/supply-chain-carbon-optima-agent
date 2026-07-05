# 🌍 Supply Chain Carbon Optima Agent

An open-source, local-first multi-agent system designed to help small businesses calculate carbon footprints and optimize shipping logistics without the overhead of expensive enterprise software.

## The Pitch & Value Proposition
Small businesses often lack the budget for enterprise ESG (Environmental, Social, and Governance) software. Supply chain data is notoriously messy, existing in unstructured emails, raw invoices, or handwritten notes. 

The **Carbon Optima Agent** solves this by using a multi-agent ADK 2.0 workflow to:
1. **Scrub** sensitive financial and personal data from raw text.
2. **Extract** core supply chain metrics into a strict, validated schema.
3. **Analyze** the route and suggest actionable, eco-friendly transportation alternatives.

## Project Structure
```
carbon-optima-agent/
├── app/                       # Core agent code
│   ├── agent.py               # Main agent logic
│   ├── fast_api_app.py        # FastAPI Backend server
│   └── app_utils/             # App utilities and helpers
├── tests/                     # Unit, integration, and load tests
├── GEMINI.md                  # AI-assisted development guide
└── pyproject.toml             # Project dependencies
```
### 1. Data Models (`app/models.py`)
We use `Pydantic` to define a strict data contract (`SupplyChainData`). The system forces the LLM to output exact variables: `origin`, `destination`, `shipping_method`, `weight_kg`, and `distance_km`.
### 2. The Multi-Agent Workflow (`app/agent.py`)
The application executes through a defined graph pipeline:
* **Node 1: Security Screen (Python)** - Intercepts the raw user input and uses Regex to redact email addresses and financial pricing before the data ever touches an LLM.
* **Node 2: Data Extractor (`LlmAgent`)** - Reads the sanitized text and maps the unstructured logistics data into our strict Pydantic JSON schema.
* **Node 3: Carbon Optimizer (`LlmAgent`)** - Evaluates the validated JSON and acts as an expert consultant, returning a 3-point markdown strategy for greener transport alternatives.
* **Node 4: Error Handler** - A fallback node that catches `ValidationError` exceptions if the user inputs garbage text, politely asking for missing metrics.
> 💡 **Tip:** Use [Antigravity CLI](https://antigravity.google/) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

## Security Features
**Shift-Left Data Privacy:** Supply chain invoices often contain proprietary pricing and partner emails. This agent implements a localized `@node` in the ADK workflow that intercepts the user's input and scrubs `[REDACTED EMAIL]` and `[REDACTED AMOUNT]` before passing the payload to the LLM, ensuring zero leak of sensitive PII or financial data.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)


## Quick Start

1. **Clone the** [**Repository**](https://github.com/Shahin-Mjz/supply-chain-carbon-optima-agent.git)**:**
```bash
   git clone <Repo Link>
```
2. Set your API Key:
Create a `.env` file in the root directory and add your Gemini key:
```bash
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
```
3. Install `agents-cli` and its skills if not already installed:
```bash
uvx google-agents-cli setup
```
4. Install required packages:
```bash
agents-cli install
```
5. Test the agent with a local web server:
```bash
agents-cli playground
```
6. Try this test prompt in the chat:
"We shipped 850 kilos of electronics from Shenzhen to Los Angeles on a cargo plane. The distance is 11,600 km and it cost $14,000. How can we make this greener?"

> Watch as the agent redacts the $14,000, extracts the metrics, and provides an ocean-freight alternative!

You can also use features from the [ADK](https://adk.dev/) CLI with `uv run adk`.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `agents-cli eval`    | Evaluate agent behavior (generate, grade, analyze, and more — see `agents-cli eval --help`) |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        || [A2A Inspector](https://github.com/a2aproject/a2a-inspector) | Launch A2A Protocol Inspector                                                        |

## Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit your agent logic in `app/agent.py` and test with `agents-cli playground` - it auto-reloads on save.

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.

## A2A Inspector

This agent supports the [A2A Protocol](https://a2a-protocol.org/). Use the [A2A Inspector](https://github.com/a2aproject/a2a-inspector) to test interoperability.
See the [A2A Inspector docs](https://github.com/a2aproject/a2a-inspector) for details.
