import hashlib
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import joblib
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter



sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from project_root.my_configs.Setting import settings
from project_root.my_utilities.util_logging import logging

logger = logging.getLogger(__name__)



class DocumentProcessor:
    def __init__(self):
        self.headers = [("#", "Header 1"), ("##", "Header 2")]
        self.cache_dir = Path(settings.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def validate_files(self, files: List) -> None:
        """Validate the total size of the uploaded files."""
        total_size = sum(os.path.getsize(f) for f in files)
        if total_size > settings.MAX_TOTAL_SIZE:
            raise ValueError(f"Total size exceeds {settings.MAX_TOTAL_SIZE // 1024 // 1024}MB limit")

    def process(self, files: List) -> List:
        """Process files with caching for subsequent queries"""
        self.validate_files(files)
        all_chunks = []
        seen_hashes = set()

        for file in files:
            try:
                # Generate content-based hash for caching
                with open(file, "rb") as f:
                    file_hash = self._generate_hash(f.read())

                cache_path = self.cache_dir / f"{file.name}_{file_hash}.joblib"

                if self._is_cache_valid(cache_path):
                    logger.info(f"Loading from cache: {file.name}")
                    chunks = self._load_from_cache(cache_path)
                else:
                    logger.info(f"Processing and caching: {file.name}")
                    chunks = self._process_file(file)
                    self._save_to_cache(chunks, cache_path)

                # Deduplicate chunks across files
                for chunk in chunks:
                    chunk_hash = self._generate_hash(chunk.page_content.encode())
                    if chunk_hash not in seen_hashes:
                        all_chunks.append(chunk)
                        seen_hashes.add(chunk_hash)
            except ValueError:
                # fail fast for unsupported file types
                logger.error(f"Unsupported file type encountered: {file.name} — aborting")
                raise

            except Exception as e:
                logger.error(f"Failed to process {file.name}: {str(e)}")
                continue

        logger.info(f"Total unique chunks: {len(all_chunks)}")
        return all_chunks

    def _process_file(self, file) -> List:
        """Original processing logic with Docling"""
        if not file.name.endswith(settings.ALLOWED_TYPES):
            logger.warning(f"Skipping unsupported file type: {file.name}")
            #return []
            raise ValueError(f"Unsupported file type: {file.name}")

        converter = DocumentConverter()
        markdown = converter.convert(file).document.export_to_markdown()
        splitter = MarkdownHeaderTextSplitter(self.headers)
        return splitter.split_text(markdown)

    def _generate_hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def _save_to_cache(self, chunks: List, cache_path: Path):
        joblib.dump(chunks, cache_path)

    def _load_from_cache(self, cache_path: Path) -> List:
        return joblib.load(cache_path)

    def _is_cache_valid(self, cache_path: Path) -> bool:
        if not cache_path.exists():
            return False

        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        age_check= cache_age < timedelta(days=settings.CACHE_EXPIRE_DAYS)

        if age_check:
            return True
        else:
            logger.info(f"Cache expired for {cache_path.name} (age: {cache_age})")
            cache_path.unlink()
            return False