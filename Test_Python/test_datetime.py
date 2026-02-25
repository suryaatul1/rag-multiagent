import os
from datetime import datetime, timedelta
from pathlib import Path

path = Path("/a_MultiAgentic_RAG/project_root/test_docling/docs/ocr_test.pdf")

cache_age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
print(type(cache_age))
test = cache_age >  timedelta(days=100)
print(datetime.now() + timedelta(days=100))
print(cache_age)
print(test)