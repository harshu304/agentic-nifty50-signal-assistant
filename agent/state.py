from typing import TypedDict

class AgentState(TypedDict):
    stock: str
    price: float
    signal: str
    decision: str