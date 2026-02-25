import json

from a_MultiAgentic_RAG.project_root.agents.verification_class import VerificationClass

schema_json = {k: v for k, v in VerificationClass.schema().items()}
schema = {"properties": schema_json['properties'], "required": schema_json['required']}
print(json.dumps(schema, indent=4))

