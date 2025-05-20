from crewai.utilities.embedding_configurator import EmbeddingConfigurator

# Disable embedding function to prevent chromadb/sqlite usage
EmbeddingConfigurator.get_default_embedding_function = lambda *_args, **_kwargs: None
