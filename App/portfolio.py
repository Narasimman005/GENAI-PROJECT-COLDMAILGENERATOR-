import pandas as pd
import chromadb
import uuid



class Portfolio:
    def __init__(self, file_path="App/resources/my_portfolio.csv"):
        self.file_path = file_path
        self.data=pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient()
        self.collection=self.chroma_client.get_or_create_collection(name="Portfolio")
    def load_data(self):
         if not self.collection.count():
             for _, row in self.data.iterrows():
                 self.collection.add(
                     documents=[row["Techstack"]],
                     metadatas=[{"links": row["Links"]}],
                     ids=[str(uuid.uuid4())]
                 )


    """def query_data(self, skills):
         result = self.collection.query(query_texts=[skills],n_results=2)
         metadatas = result.get("metadatas", [[]])[0]
         return [m["links"] for m in metadatas]"""

    def query_data(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

