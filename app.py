"""Phase 9: Streamlit app. Ask a policy question as a simulated role; get an answer with [n] citations
and the excerpts it came from, or a decline.

Run (Ollama must be running with the model pulled):
    ollama serve            # if the Ollama app isn't already running
    streamlit run app.py    # optional: RAG_CONFIG=configs/<other>.yaml streamlit run app.py
"""

from __future__ import annotations

import os
import urllib.error
import urllib.request
from pathlib import Path

import streamlit as st

from src.config import load_config, resolve_path
from src.qa import ROLES, ask, log_query

CONFIG = os.environ.get("RAG_CONFIG", "configs/app.yaml")
LOG_PATH = Path("logs/queries.jsonl")
STATUS_LABEL = {"current": "current version", "superseded": "OLDER version (a newer one exists)",
                "legacy": "old document (no newer version)"}
EXAMPLES = ["How many days do I have to submit an expense claim?",
            "What was the previous rule for expense claims?",
            "Who approves a contract with a new vendor?"]


@st.cache_resource(show_spinner="Loading search indexes and models (first time only) ...")
def load(config_path: str):
    from src.index import build_indexes   # heavy imports only once
    cfg = load_config(config_path)
    return cfg, build_indexes(cfg, verbose=False)


def ollama_ready(cfg) -> str | None:
    """None if Ollama answers and has the model, else a message for the user."""
    url, model = cfg["generation"]["ollama_url"], cfg["generation"]["model"]
    try:
        with urllib.request.urlopen(f"{url}/api/tags", timeout=3) as r:
            names = r.read().decode()
    except (urllib.error.URLError, OSError):
        return f"Ollama isn't running at {url}. Start it with `ollama serve` (or open the Ollama app)."
    return None if model in names else f"Ollama is running but `{model}` isn't pulled: run `ollama pull {model}`."


def show_answer(record: dict) -> None:
    if record["declined"]:
        reason = ("the best match scored below the confidence threshold" if record["declined_by"] == "threshold"
                  else "the model found no answer in the retrieved excerpts")
        st.warning(f"{record['answer']}  \n_Declined: {reason}._")
    else:
        st.markdown(record["answer"])
        if record["invalid_citations"]:
            st.caption(f"Warning: cites excerpt(s) {record['invalid_citations']} that don't exist.")
    st.caption(f"{record['latency_s']} s · decline score {record['decline_score']}"
               + (f" (threshold {record['threshold']})" if record["threshold"] is not None else ""))
    with st.expander(f"Sources ({len(record['sources'])} excerpts the model saw)",
                     expanded=not record["declined"]):
        for s in record["sources"]:
            where = s["title"] + (f" › {s['section']}" if s["section"] else "") + \
                    (f" · page {s['page']}" if s["page"] not in (None, -1) else "")
            status = STATUS_LABEL.get(s["status"], s["status"])
            mark = "**cited**" if s["cited"] else "not cited"
            st.markdown(f"**[{s['n']}] {where}**  \nupdated {s['updated']} · {status} · {mark}")
            if s["status"] != "current":
                st.caption("This excerpt is from an older document.")
            st.text(s["text"][:1500] + (" ..." if len(s["text"]) > 1500 else ""))


def main() -> None:
    st.set_page_config(page_title="Policy Q&A", page_icon="📄", layout="wide")
    cfg, bundle = load(CONFIG)
    with st.sidebar:
        st.header("Settings")
        label = st.selectbox("Your role", list(ROLES), help="Simulated access control: Legal and Finance also "
                             "see their department's documents; everyone sees all-employee documents.")
        role = ROLES[label]
        st.divider()
        g, r = cfg["generation"], cfg["retrieval"]
        st.caption(f"Config `{CONFIG}`  \nModel `{g['model']}`  \nRetrieval: {r['mode']}"
                   + (f" + date-aware (w = {r['date_weight']})" if r["date_aware_rerank"] else "")
                   + f"  \nTop {g['context_chunks']} excerpts to the model  \n"
                   + f"Decline threshold: {g['decline_threshold'] if g['decline_threshold'] is not None else 'none (model decides)'}")
        if st.button("Clear conversation"):
            st.session_state.history = []

    st.title("Policy Q&A")
    st.caption("Answers come only from the indexed documents, with [n] citations, or the system says it "
               "couldn't find the answer. Some old document versions are synthetic test copies.")
    if problem := ollama_ready(cfg):
        st.error(problem)
        st.stop()

    history = st.session_state.setdefault("history", [])
    for item in history:
        with st.chat_message("user"):
            st.markdown(f"{item['question']}  \n_as {item['label']}_")
        with st.chat_message("assistant"):
            show_answer(item)

    if not history:
        st.markdown("**Try:** " + " · ".join(f"_{q}_" for q in EXAMPLES))
    question = st.chat_input("Ask a question about the policies")
    if question:
        with st.chat_message("user"):
            st.markdown(f"{question}  \n_as {label}_")
        with st.chat_message("assistant"):
            with st.spinner("Searching and answering ..."):
                try:
                    record = ask(question, role, bundle, cfg)
                except (urllib.error.URLError, TimeoutError) as e:
                    st.error(f"The model didn't answer ({e}). Is Ollama still running?")
                    st.stop()
            show_answer(record)
        log_query(resolve_path(str(LOG_PATH)), record, cfg)
        history.append({**record, "label": label})


if __name__ == "__main__":
    main()
