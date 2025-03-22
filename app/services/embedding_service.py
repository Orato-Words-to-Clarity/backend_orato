import re
import requests
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()
# TranscriptProcessor 
class TranscriptProcessor:
    def __init__(self):
        # Initialize variables
        self.transcript = ""
        self.sentences = []
        self.embeddings = []
        
        # Huggingface API Configuration
        self.hf_api_key = os.getenv('HUGGING_FACE_API_KEY')
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        
        # Pinecone API Configuration
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = "orato"
        self.dimension = 384
        self._initialize_pinecone()
    
    # Initialize Pinecone
    def _initialize_pinecone(self):
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-west-2'
                )
            )
        self.index = self.pc.Index(self.index_name)
        
    # Accepts a transcript and stores it in the object
    def accept_transcript(self, transcript: str):
        if not transcript:
            raise ValueError("Transcript cannot be empty.")
        
        self.transcript = transcript
        print("Transcript accepted and stored.")
    
    # Splits the transcript into sentences
    def split_into_sentences(self):
        if not self.transcript:
            raise ValueError("Transcript is empty. Please provide a valid transcript.")
        
        self.sentences = re.split(r'(?<=[.!?]) +', self.transcript.strip())
        
        print("Transcript has been split into sentences.")
        for i, sentence in enumerate(self.sentences, start=1):
            print(f"Sentence {i}: {sentence}")
    
    # Generates embeddings for each sentence using huggingface'
    def generate_embeddings(self):
        if not self.sentences:
            raise ValueError("No sentences found. Please split the transcript into sentences first.")
        print("Generating embeddings for each sentence...")
        payload = {
            "inputs": self.sentences,
            "options": {"wait_for_model": True}
        }
        
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            self.embeddings = response.json()
            print("Embeddings generated successfully.")
            # print(self.embeddings)
        else:
            print("Failed to generate embeddings. Error {response.status_code}: {response.text}")
            raise Exception(f"Erorr {response.status_code}: {response.text}")
    
    # Stores the embeddings in Pinecone
    def upsert_embeddings_to_pinecone(self, transcription_id:str):
        if not self.embeddings:
            raise ValueError("No embeddings found. Please generate embeddings first.")
        print("Upserting embeddings to Pinecone...")
        vectors = [
            {
                "id": f"sentence_{i}",
                "values": embedding,
                "metadata": {"text": sentence, "transcription_id": transcription_id}
            }
            for i, (sentence, embedding) in enumerate(zip(self.sentences, self.embeddings))
        ]
        self.index.upsert(vectors=vectors, namespace=transcription_id)
        print("Embeddings upserted successfully.")
    
    # Similarity search using Pinecone
    def query_similar_sentences(self, query_sentence: str,transcription_id: str, top_k: int = 5):
        if not query_sentence:
            raise ValueError("Query sentence cannot be empty.")
        
        print("Generating embeddings for the query sentence...")
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": query_sentence, "options": {"wait_for_model": True}}
        )
        if response.status_code != 200:
            print(f"Failed to generate embeddings for the query sentence. Error {response.status_code}: {response.text}")
            raise Exception(f"Error {response.status_code}: {response.text}")
        
        query_embedding = response.json()
        # print("Raw query embedding:", query_embedding)
        
        if isinstance(query_embedding, list) and isinstance(query_embedding[0], list):
            query_embedding = query_embedding[0]
        
        if not isinstance(query_embedding, list) or len(query_embedding) != self.dimension:
            raise ValueError(f"Query embedding has an unexpected format or dimension: {query_embedding}")
        
        
        print("Querying similar sentences...")
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=transcription_id
        )
        print(f"Top {top_k} similar sentences:")
        relevant_sentences = ""
        for match in results["matches"]:
            relevant_sentences = (f"Score: {match['score']:0.4f} | Sentence: {match['metadata']['text']}\n") 
            
        return relevant_sentences
                

transcript_processor = TranscriptProcessor()
