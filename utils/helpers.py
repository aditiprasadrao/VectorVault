def chunk_text(text: str, chunk_size: int = 512) -> list[str]:
    """Split text into smaller chunks for embedding"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
