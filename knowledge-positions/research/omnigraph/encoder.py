"""The lexical-hash-512 encoder exactly as the JITK Rust scanner computes it.

Stored vectors come from the scanner (jitk/scanner/src/main.rs `lexical_hash_512`), so query
vectors and library-computed vectors must use the same algorithm to share its space.
Note: capture.py in the Knowledge Positions repo also calls its encoder "lexical-hash-512",
but it keeps stop-words and uses the opposite sign rule, so its vectors are NOT in this space.
"""
import hashlib
import unicodedata

import numpy as np

SPACE = "lexical-hash-512"

# Copied verbatim from the scanner's STOP list.
STOP = frozenset("""the and that this with from for are was were into not but can may its their
they our has have had only than when what which while where how use uses using used one two
three more also does each such these those been being should would could will must all any
per through without""".split())

def _is_rust_word_char(c: str) -> bool:
    """Rust `regex` \\w (Unicode Word): Alphabetic, marks, decimal digits, connector
    punctuation, join controls. Python's \\w also accepts other numerics such as '¹' (No),
    which made 2 of 294 real units hash differently, so Python's \\w is not used."""
    cat = unicodedata.category(c)
    return (c.isalpha() or cat in ("Nl", "Nd", "Pc", "Mn", "Mc", "Me")
            or c in "‌‍")


def _words(text: str):
    word = []
    for c in text:
        if _is_rust_word_char(c):
            word.append(c)
        elif word:
            yield "".join(word)
            word = []
    if word:
        yield "".join(word)


def lexical_hash_512(text: str) -> np.ndarray:
    """Scanner algorithm: lowercase, \\w+ tokens minus stop-words, sha256 per token;
    first 4 bytes mod 512 pick the slot, 5th byte even -> +1 / odd -> -1; L2-normalise."""
    v = np.zeros(512, dtype=np.float32)
    for w in _words(text.lower()):
        if w in STOP:
            continue
        h = hashlib.sha256(w.encode()).digest()
        v[int.from_bytes(h[:4], "big") % 512] += 1.0 if h[4] % 2 == 0 else -1.0
    n = float(np.sqrt(np.sum(v * v)))
    return v / n if n > 0 else v


class ScannerLexicalEncoder:
    """Encoder object in the shape the Knowledge Positions library expects (`.encode`)."""

    def encode(self, text, normalize_embeddings=True):
        return lexical_hash_512(text)
