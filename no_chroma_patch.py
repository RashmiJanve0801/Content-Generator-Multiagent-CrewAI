import sys
from unittest.mock import MagicMock

# Mock chromadb module
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.api'] = MagicMock()
sys.modules['chromadb.api.types'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()

from crewai.utilities.embedding_configurator import EmbeddingConfigurator

# Disable embedding function to prevent chromadb/sqlite usage
EmbeddingConfigurator.get_default_embedding_function = lambda *_args, **_kwargs: None
