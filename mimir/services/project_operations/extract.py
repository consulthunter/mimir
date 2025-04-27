import os
from sentence_transformers import SentenceTransformer
import chromadb
from bs4 import BeautifulSoup



class Extract:

    def __init__(self, project):
        self.project = project
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.chromadb.PersistentClient(os.path.join(self.project.project_output_dir, "docs.db"))
        self.collection = self.chroma_client.get_or_create_collection("project_docs")

    async def run_extract(self):
        self.index_docs()
        # self.query_docs()

    def extract_text_from_html(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            return soup.get_text(separator="\n", strip=True)

    def load_docs_from_folder(self, folder):
        docs = []
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                if ext in (".md", ".txt"):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                elif ext == ".html":
                    content = self.extract_text_from_html(path)
                else:
                    continue
                if content:
                    docs.append((path, content))
        return docs

    def index_docs(self):
        all_docs = []

        # Load README
        readme_path = os.path.join(self.project.project_temp_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                all_docs.append(("README.md", f.read().strip()))

        # Load /docs content
        docs_path = os.path.join(self.project.project_temp_dir, "docs")
        if os.path.exists(docs_path):
            all_docs.extend(self.load_docs_from_folder(docs_path))

        # Add to Chroma
        for i, (file_path, text) in enumerate(all_docs):
            self.project.logger.log_info(f"Indexing: {file_path}")
            embedding = self.model.encode([text])[0].tolist()
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[f"{file_path}_{i}"]
            )