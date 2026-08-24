from pattern_detector.domain.code_model import CodeModel, ModuleModel, FunctionModel, FunctionClauseModel
from pattern_detector.domain.value_objects import Confidence, ConfidenceLevel, Evidence, SourceLocation

def test_confidence_calculation():
    e1 = Evidence(description="Behaviour match", weight=0.7, rule_code="BEH")
    e2 = Evidence(description="Callbacks match", weight=0.6, rule_code="CB")
    conf = Confidence.from_evidences([e1, e2])
    # 1 - (1-0.7)*(1-0.6) = 1 - 0.3*0.4 = 0.88
    assert round(conf.score, 2) == 0.88
    assert conf.level == ConfidenceLevel.VERY_HIGH

def test_source_location_str():
    loc = SourceLocation(file_path="src/kv_server.erl", line=42, column=5)
    assert str(loc) == "src/kv_server.erl:42:5"

def test_circular_dependency_detection():
    m1 = ModuleModel(name="mod_a", file_path="mod_a.erl")
    f1 = FunctionModel(name="foo", arity=0, calls=[("mod_b", "bar", 0)])
    m1.functions["foo/0"] = f1

    m2 = ModuleModel(name="mod_b", file_path="mod_b.erl")
    f2 = FunctionModel(name="bar", arity=0, calls=[("mod_a", "foo", 0)])
    m2.functions["bar/0"] = f2

    cm = CodeModel()
    cm.modules["mod_a"] = m1
    cm.modules["mod_b"] = m2

    cycles = cm.find_circular_dependencies()
    assert len(cycles) == 1
    assert "mod_a" in cycles[0] and "mod_b" in cycles[0]
