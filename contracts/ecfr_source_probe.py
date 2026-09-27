# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import hashlib,json

URL="https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-2.xml?part=200&section=200.423"
class EcfrSourceProbe(gl.Contract):
    latest:str
    def __init__(self):self.latest="NOT_RUN"
    @gl.public.write
    def probe(self)->str:
        def fetch():
            response=gl.nondet.web.get(URL,headers={"Accept":"application/xml","User-Agent":"GrantCostGate/1.0 research-contact@example.org"});body=response.body or b""
            if int(response.status)!=200:return "SOURCE_UNAVAILABLE"
            text=body.decode("utf-8",errors="strict")
            if 'N="200.423"' not in text or "2 CFR 200.423" not in text:return "SOURCE_IDENTITY_MISMATCH"
            return json.dumps({"status":int(response.status),"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"citation":"2 CFR 200.423"},sort_keys=True,separators=(",",":"))
        self.latest=gl.eq_principle.strict_eq(fetch);return self.latest
    @gl.public.view
    def get_latest(self)->str:return self.latest
    @gl.public.view
    def fixture(self)->dict:return {"url":URL,"expected_heading":"200.423 Alcoholic beverages","expected_rule":"The cost of alcoholic beverages is unallowable."}
Contract=EcfrSourceProbe
