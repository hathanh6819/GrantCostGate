import importlib.util,json,sys,types
from pathlib import Path
import pytest

AUTHORITY="0x1111111111111111111111111111111111111111"
EXECUTOR="0x2222222222222222222222222222222222222222"
RECIPIENT="0x3333333333333333333333333333333333333333"
OUTSIDER="0x4444444444444444444444444444444444444444"
ACTION="sha256:"+"a"*64
SECTION="200.423";EXPENSE="Purchase alcoholic beverages for the grant-funded project celebration."
XML=b'''<?xml version="1.0"?><DIV8 N="200.423" TYPE="SECTION" hierarchy_metadata="{&quot;citation&quot;:&quot;2 CFR 200.423&quot;}"><HEAD>200.423 Alcoholic beverages.</HEAD><P>The cost of alcoholic beverages is unallowable.</P></DIV8>'''

class TreeMap(dict):
    @classmethod
    def __class_getitem__(cls,_):return cls
class U256(int):pass
class Address(str):pass
class ContractBase:
    def __init_subclass__(cls,**kw):
        original=cls.__dict__.get("__init__")
        def init(self,*args,**kwargs):
            for name,kind in cls.__annotations__.items():
                if kind is TreeMap:setattr(self,name,TreeMap())
            original(self,*args,**kwargs)
        cls.__init__=init
class Write:
    def __call__(self,fn):return fn
class Public:write=Write();view=staticmethod(lambda fn:fn)
class Response:
    def __init__(self,status=200,body=XML):self.status=status;self.body=body
class Nondet:
    def __init__(self):
        self.response=Response();self.answer={"decision":"UNALLOWABLE","directly_addressed":True,"requires_documentation":False,"requires_prior_approval":False,"reason_code":"ALCOHOL_PROHIBITED"};self.web=types.SimpleNamespace(get=self.get)
    def get(self,url,headers=None):self.last_url=url;return self.response
    def exec_prompt(self,*_,**__):return self.answer
class Eq:
    forced=None
    def prompt_comparative(self,fn,*_,**__):return self.forced if self.forced is not None else fn()

@pytest.fixture
def runtime(monkeypatch):
    nondet=Nondet();gl=types.ModuleType("genlayer");gl.__all__=["gl","u256","Address","TreeMap","typing"]
    gl.gl=gl;gl.Contract=ContractBase;gl.public=Public();gl.nondet=nondet;gl.eq_principle=Eq();gl.message=types.SimpleNamespace(sender_address=AUTHORITY);gl.message_raw={"datetime":"2026-09-27T00:00:00+00:00"};gl.u256=U256;gl.Address=Address;gl.TreeMap=TreeMap;gl.typing=types.SimpleNamespace(Any=object)
    monkeypatch.setitem(sys.modules,"genlayer",gl);spec=importlib.util.spec_from_file_location("grant_cost_gate_test",Path("contracts/grant_cost_gate.py"));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.GrantCostGate(),gl,nondet

def create(c):return c.create_commitment(EXPENSE,SECTION,Address(RECIPIENT),U256(12500),ACTION,Address(EXECUTOR),U256(86400))
def set_allowable(n):
    n.response=Response(body=XML.replace(b"200.423",b"200.425"));n.answer={"decision":"ALLOWABLE","directly_addressed":True,"requires_documentation":False,"requires_prior_approval":False,"reason_code":"AUDIT_COST_ALLOWED"}

def test_unallowable_blocks_capability(runtime):
    c,_,_=runtime;assert int(create(c))==1;assert c.assess_commitment(U256(1),U256(1))=="BLOCKED"
    r=c.get_commitment(U256(1));assert r["decision"]=="UNALLOWABLE" and r["revision"]==2 and len(r["evidence_digest"])==71
    assert c.consume_authorization(U256(1),U256(2),Address(RECIPIENT),U256(12500),ACTION)=="ONLY_SPEND_EXECUTOR"

def test_allowable_issues_bound_single_use_capability(runtime):
    c,g,n=runtime;set_allowable(n);assert int(c.create_commitment("Necessary audit services required by the federal award.","200.425",Address(RECIPIENT),U256(12500),ACTION,Address(EXECUTOR),U256(86400)))==1
    assert c.assess_commitment(U256(1),U256(1))=="AUTHORIZED"
    g.message.sender_address=EXECUTOR
    assert c.consume_authorization(U256(1),U256(2),Address(RECIPIENT),U256(12500),ACTION)=="AUTHORIZATION_CONSUMED"
    assert c.get_commitment(U256(1))["status"]=="CONSUMED"
    assert c.consume_authorization(U256(1),U256(3),Address(RECIPIENT),U256(12500),ACTION)=="NOT_AUTHORIZED"

def test_last_mile_rejects_wrong_payload_without_mutation(runtime):
    c,g,n=runtime;set_allowable(n);c.create_commitment("Necessary audit services required by the federal award.","200.425",Address(RECIPIENT),U256(12500),ACTION,Address(EXECUTOR),U256(86400));c.assess_commitment(U256(1),U256(1));before=c.get_commitment(U256(1));g.message.sender_address=EXECUTOR
    assert c.consume_authorization(U256(1),U256(2),Address(OUTSIDER),U256(12500),ACTION)=="SEALED_ACTION_MISMATCH"
    assert c.consume_authorization(U256(1),U256(2),Address(RECIPIENT),U256(12501),ACTION)=="SEALED_ACTION_MISMATCH"
    assert c.consume_authorization(U256(1),U256(2),Address(RECIPIENT),U256(12500),"sha256:"+"b"*64)=="SEALED_ACTION_MISMATCH"
    assert c.get_commitment(U256(1))==before

def test_permissionless_creation_but_only_bound_roles_can_operate(runtime):
    c,g,n=runtime;set_allowable(n);c.create_commitment("Necessary audit services required by the federal award.","200.425",Address(RECIPIENT),U256(1),ACTION,Address(EXECUTOR),U256(86400));c.assess_commitment(U256(1),U256(1))
    g.message.sender_address=OUTSIDER;assert c.revoke_authorization(U256(1),U256(2))=="ONLY_COMMITMENT_AUTHORITY"
    g.message.sender_address=AUTHORITY;assert c.revoke_authorization(U256(1),U256(2))=="REVOKED"
    g.message.sender_address=OUTSIDER;assert int(c.create_commitment(EXPENSE,SECTION,Address(RECIPIENT),U256(9),"sha256:"+"c"*64,Address(OUTSIDER),U256(86400)))==2
    assert c.get_commitment(U256(2))["authority"]==OUTSIDER and c.get_commitment(U256(2))["executor"]==OUTSIDER

def test_conditional_never_authorizes(runtime):
    c,_,n=runtime;n.response=Response(body=XML.replace(b"200.423",b"200.421"));n.answer={"decision":"CONDITIONAL","directly_addressed":True,"requires_documentation":True,"requires_prior_approval":False,"reason_code":"DOCUMENTATION_REQUIRED"}
    c.create_commitment("Advertising used solely to recruit personnel for the federal award.","200.421",Address(RECIPIENT),U256(10),ACTION,Address(EXECUTOR),U256(86400));assert c.assess_commitment(U256(1),U256(1))=="CONDITIONAL"

@pytest.mark.parametrize("status,body,reason",[(503,XML,"SOURCE_UNAVAILABLE"),(200,b"short","SOURCE_SIZE_INVALID"),(200,XML.replace(b"200.423",b"200.425"),"SOURCE_IDENTITY_MISMATCH")])
def test_source_failures_fail_closed(runtime,status,body,reason):
    c,_,n=runtime;n.response=Response(status,body);create(c);assert c.assess_commitment(U256(1),U256(1))=="UNRESOLVED";assert c.get_commitment(U256(1))["reason"]==reason

def test_consensus_conflict_and_retry(runtime):
    c,g,_=runtime;create(c);g.eq_principle.forced='{"different":"outputs"}';assert c.assess_commitment(U256(1),U256(1))=="UNRESOLVED";assert c.retry_unresolved(U256(1),U256(2))=="PENDING";assert c.get_commitment(U256(1))["revision"]==3

def test_expiry_blocks_assessment_and_consumption(runtime):
    c,g,n=runtime;set_allowable(n);c.create_commitment("Necessary audit services required by the federal award.","200.425",Address(RECIPIENT),U256(1),ACTION,Address(EXECUTOR),U256(3600));g.message_raw["datetime"]="2026-09-27T02:00:00+00:00";assert c.assess_commitment(U256(1),U256(1))=="COMMITMENT_EXPIRED"

@pytest.mark.parametrize("action,amount,expiry,expected",[("bad",1,86400,"INVALID_ACTION_DIGEST"),(ACTION,0,86400,"INVALID_AMOUNT"),(ACTION,1,10,"INVALID_EXPIRY")])
def test_input_gates(runtime,action,amount,expiry,expected):
    c,_,_=runtime;assert c.create_commitment(EXPENSE,SECTION,Address(RECIPIENT),U256(amount),action,Address(EXECUTOR),U256(expiry))==expected and c.get_total()==0

def test_duplicate_find_and_protocol(runtime):
    c,_,_=runtime;create(c);assert create(c)=="COMMITMENT_EXISTS:1";assert c.find_commitment(Address(AUTHORITY),EXPENSE,SECTION,Address(RECIPIENT),U256(12500),ACTION,Address(EXECUTOR))["id"]==1
    p=c.get_protocol();assert p["architecture"]=="permissionless-sealed-spend-capability" and p["roles"]=="per-commitment authority and executor" and p["custody"] is False
