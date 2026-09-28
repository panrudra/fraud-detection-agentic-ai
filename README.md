================================================================================
AGENTIC AI FRAUD DETECTION & FORENSIC ADJUDICATION ENGINE
================================================================================
Repository: https://github.com/panrudra/fraud-detection-agentic-ai
 
1. SYSTEM EXPLANATION & ARCHITECTURE
--------------------------------------------------------------------------------
This project implements an event-driven multi-agent orchestration engine
designed to handle complex financial crime investigations (Tier-3 triage).
 
The execution model proceeds through four deterministic stages:
 
[Stage 1: Alert Ingestion]
A flagged transaction payload is ingested into a LangGraph state graph. The
payload includes transaction metadata, historical behavior averages, network
counterparty hops, and geolocation details.
 
[Stage 2: Specialist Agent Investigation]
The state graph distributes evidence to three specialized LLM agents:
- Behavioral Profiler: Quantifies deviations in spending velocity and anomalies
  in login device/IP patterns compared to baseline behavior.
- Graph AML Detective: Detects structural topologies, such as rapid mule ring
  hops, layering activity, and proxy IP cloaking.
- Compliance Auditor: Validates statutory reporting thresholds under PMLA and
  central banking compliance guidelines.
 
[Stage 3: Adjudication & Dossier Generation]
The Chief Adjudicator node synthesizes all forensic findings into a calibrated
risk evaluation, makes an operational decision (ALLOW, FLAG_MANUAL_REVIEW,
BLOCK_AND_FREEZE), and writes a regulatory Suspicious Activity Report (SAR).
 
[Stage 4: Strict Output Validation]
The final result is passed through a Pydantic schema ('FraudDossier') to ensure
type safety, structured consistency, and zero unstructured hallucination.
 
 
2. HOW TO EXECUTE THE CODE
--------------------------------------------------------------------------------
 
METHOD A: Run Directly in the Cloud (GitHub Actions)
---------------------------------------------------
* For Invited Collaborators:
  1. Open repository: https://github.com/panrudra/fraud-detection-agentic-ai
  2. Click on the "Actions" tab at the top.
  3. In the left panel, select "Run Agentic AI Fraud Detection".
  4. Click the "Run workflow" dropdown on the right side and click the green button.
  5. Open the triggered execution to view live traces and the final FraudDossier.
 
* For External Evaluators (Fork & Execute):
  1. Click "Fork" at the top right of the repository page.
  2. In your forked repository, go to Settings -> Secrets and variables -> Actions.
  3. Click "New repository secret".
     - Name: OPENAI_APIKEY
     - Secret: <Your OpenAI API Key>
  4. Go to the "Actions" tab, enable workflows if prompted, and click "Run workflow".
 
 
METHOD B: Local Environment Execution
-------------------------------------
1. Clone the repository:
   git clone https://github.com/panrudra/fraud-detection-agentic-ai.git
   cd fraud-detection-agentic-ai
 
2. Create and activate a Python virtual environment:
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
 
3. Install required dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt
 
4. Export your OpenAI API Key:
   # On Windows (cmd):
   set OPENAI_API_KEY=your_key_here
   # On Windows (PowerShell):
   $env:OPENAI_API_KEY="your_key_here"
   # On macOS/Linux:
   export OPENAI_API_KEY="your_key_here"
 
5. Run the engine:
   python multi_agent_fraud_graph.py
 
 
3. KEY REPOSITORY FILES
--------------------------------------------------------------------------------
- multi_agent_fraud_graph.py : LangGraph graph definition, agent nodes, and Pydantic schemas.
- requirements.txt           : Python packages with pinned urllib3==2.2.3 compatibility.
- .github/workflows/run_agent.yml : CI/CD automation pipeline for cloud execution.
================================================================================
