try:
    import tiktoken

    ENCODING = tiktoken.get_encoding("cl100k_base")
    TIKTOKEN_AVAILABLE = True
except ImportError:
    ENCODING = None
    TIKTOKEN_AVAILABLE = False


def estimate_tokens(text: str) -> int:
    if TIKTOKEN_AVAILABLE and ENCODING is not None:
        return len(ENCODING.encode(text))
    else:
        return round(len(text) / 4)
