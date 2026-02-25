from pathlib import Path

from a_MultiAgentic_RAG.project_root.my_configs.Setting import settings

file = Path("/a_MultiAgentic_RAG/project_root/test_docling/docs/ocr_test.pdf")
file_ext = tuple(x for x in settings.ALLOWED_TYPES)
print(file_ext)
print(file.name.endswith(tuple(settings.ALLOWED_TYPES)))
print(file.name)