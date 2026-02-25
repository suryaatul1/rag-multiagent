# Maximum allowed size for a single file (50 MB)
from typing import Tuple

MAX_FILE_SIZE: int = 50 * 1024 * 1024

# Maximum allowed total size for all uploaded files (200 MB)
MAX_TOTAL_SIZE: int = 200 * 1024 * 1024

# Allowed file types for upload
ALLOWED_TYPES = (".txt", ".pdf", ".docx", ".md" , ".png")