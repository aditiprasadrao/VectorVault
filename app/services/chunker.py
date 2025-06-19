import textwrap

def chunk_text(text, max_len=500):
    return textwrap.wrap(text, max_len)
