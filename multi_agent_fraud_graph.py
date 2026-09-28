import json
import os
from typing import Annotated, Dict, Any, List, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

class FraudDossier(BaseModel):
    verdict: str = Field(description="Action: 'APPROVE', 'CHALLENGE_STEPUP_MFA', 'BLOCK_AND_FREEZE'")
    calibrated_risk_score: float = Field(description="Risk probability 0.0 to 1.0")
    confidence: float = Field(description="Confidence 0.0 to 1.0")
    key_risk_indicators: List[str] = Field(description="Consolidated findings")
    sar_narrative: str = Field(description="Formal regulatory SAR summary")
    recommended_mitigation: str = Field(description="Actionable mitigation instructions")

class MultiAgentFraudState(TypedDict):
    transaction_alert: Dict[str, Any]
    behavioral_report: Optional[str]
    graph_aml_report: Optional[str]
    compliance_report: Optional[str]
    final_adjudication: Optional[Dict[str, Any]]

def behavioral_agent(state: MultiAgentFraudState) -> Dict[str, Any]:
    alert = state["transaction_alert"]
    res = llm.invoke([
        SystemMessage(content="You are a Behavioral Risk Analyst."),
        HumanMessage(content=f"Analyze velocity and anomaly: {json.dumps(alert)}")
    ])
    return {"behavioral_report": res.content}

def graph_aml_agent(state: MultiAgentFraudState) -> Dict[str, Any]:
    alert = state["transaction_alert"]
    res = llm.invoke([
        SystemMessage(content="You are a Graph AML Detective."),
        HumanMessage(content=f"Evaluate mule ring topology for IP: {alert.get('ip_address')}")
    ])
    return {"graph_aml_report": res.content}

def compliance_agent(state: MultiAgentFraudState) -> Dict[str, Any]:
    alert = state["transaction_alert"]
    res = llm.invoke([
        SystemMessage(content="You are a Compliance & Statutory Auditor."),
        HumanMessage(content=f"Evaluate RBI & PMLA compliance for amount: {alert.get('transaction_amount')}")
    ])
    return {"compliance_report": res.content}

def adjudicator_agent(state: MultiAgentFraudState) -> Dict[str, Any]:
    structured_llm = llm.with_structured_output(FraudDossier)
    prompt = f"""Synthesize findings into a final FraudDossier:
Alert: {json.dumps(state['transaction_alert'])}
Behavioral: {state['behavioral_report']}
AML Graph: {state['graph_aml_report']}
Compliance: {state['compliance_report']}"""
    dossier = structured_llm.invoke([HumanMessage(content=prompt)])
    return {"final_adjudication": dossier.model_dump()}

builder = StateGraph(MultiAgentFraudState)
builder.add_node("behavioral_agent", behavioral_agent)
builder.add_node("graph_aml_agent", graph_aml_agent)
builder.add_node("compliance_agent", compliance_agent)
builder.add_node("adjudicator_agent", adjudicator_agent)

builder.add_edge(START, "behavioral_agent")
builder.add_edge(START, "graph_aml_agent")
builder.add_edge("behavioral_agent", "compliance_agent")
builder.add_edge("graph_aml_agent", "compliance_agent")
builder.add_edge("compliance_agent", "adjudicator_agent")
builder.add_edge("adjudicator_agent", END)

app = builder.compile()

if __name__ == "__main__":
    alert = {
        "alert_id": "ALT-IIT-2026",
        "user_id": "USR_9821",
        "transaction_amount": 145000.00,
        "currency": "INR",
        "recipient_acc": "ACC_MULE_883",
        "recipient_type": "wallet",
        "ip_address": "198.51.100.42",
        "cross_border": True
    }
    result = app.invoke({
        "transaction_alert": alert,
        "behavioral_report": None,
        "graph_aml_report": None,
        "compliance_report": None,
        "final_adjudication": None
    })
    dossier = result["final_adjudication"]
    print("\n================ FINAL ADJUDICATED REPORT ================")
    print("Verdict   :", dossier["verdict"])
    print("Risk Score:", dossier["calibrated_risk_score"])
    print("Mitigation:", dossier["recommended_mitigation"])
    print("Narrative :", dossier["sar_narrative"])
    print("==========================================================")
