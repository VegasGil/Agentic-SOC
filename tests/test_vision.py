from agents.vision import vision

def test_vision_agent_initialization():
    assert vision.role == "Analista de Triaje (Visión)"
    assert vision.llm is not None
    assert "FRIDAY" in vision.goal or "determinar" in vision.goal.lower()