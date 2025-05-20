import sys
from unittest.mock import MagicMock

# Completely block chromadb and its submodules
for mod in ['chromadb', 'chromadb.api', 'chromadb.errors', 
            'chromadb.api.types', 'chromadb.utils', 
            'chromadb.config', 'chromadb.api.models']:
    sys.modules[mod] = MagicMock()

# Create a more thorough mock for chromadb
chromadb_mock = MagicMock()
chromadb_mock.errors = MagicMock()  # Mock the errors submodule
sys.modules['chromadb'] = chromadb_mock

# Mock the KnowledgeStorage class to avoid chromadb dependencies
class MockKnowledgeStorage:
    def __init__(self, *args, **kwargs):
        pass
    def add(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        return []
    def clear(self, *args, **kwargs):
        pass

# Inject our mock before crewai tries to import the real one
sys.modules['crewai.knowledge.storage.knowledge_storage'] = MagicMock()
sys.modules['crewai.knowledge.storage.knowledge_storage'].KnowledgeStorage = MockKnowledgeStorage
