"""Streamlit UI for the ATC Readback Verifier.

Run locally:   streamlit run app/streamlit_app.py   (uses the ollama backend)
Hosted (cloud): set EXTRACTOR_BACKEND=hf and HF_TOKEN in the app's secrets.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Make `src/` importable without installing the package (e.g. on Streamlit Cloud).
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

from atc_verifier import verify  # noqa: E402
from atc_verifier.extract.base import get_extractor  # noqa: E402

load_dotenv(ROOT / ".env")


def _load_streamlit_secrets() -> None:
    """Bridge Streamlit Cloud secrets into env vars.

    On Streamlit Community Cloud, secrets are exposed via ``st.secrets`` and are
    NOT set as environment variables, but our backends read ``os.getenv(...)``.
    Copy the ones we care about across (without overriding anything already in
    the environment, e.g. a local ``.env``). Locally there is no secrets file,
    so accessing ``st.secrets`` is wrapped to fail silently.
    """
    try:
        for key in ("EXTRACTOR_BACKEND", "MODEL_NAME", "HF_TOKEN", "OLLAMA_HOST"):
            if key not in os.environ and key in st.secrets:
                os.environ[key] = str(st.secrets[key])
    except Exception:
        pass


_load_streamlit_secrets()

EXAMPLES = {
    "Correct readback": (
        "Speedbird 245, descend flight level 240, turn left heading 270.",
        "Descend flight level 240, left heading 270, Speedbird 245.",
    ),
    "Wrong altitude (substitution)": (
        "Speedbird 245, descend flight level 240.",
        "Descend flight level 250, Speedbird 245.",
    ),
    "Transposed runway (21 -> 12)": (
        "Vueling 38 Lima, line up and wait runway 21.",
        "Line up and wait runway 12, Vueling 38 Lima.",
    ),
    "Omitted item": (
        "Iberia 6020, turn right heading 120, contact Tower 118.7.",
        "Right heading 120, Iberia 6020.",
    ),
    "Callsign error": (
        "Speedbird 245, climb flight level 280.",
        "Climb flight level 280, Speedbird 254.",
    ),
}


@st.cache_resource(show_spinner=False)
def _extractor(backend: str, model: str):
    kwargs = {"model": model} if model else {}
    return get_extractor(backend, **kwargs)


def main() -> None:
    st.set_page_config(page_title="ATC Readback Verifier", page_icon="🛫", layout="centered")
    st.title("🛫 ATC Readback Verifier")
    st.caption(
        "Check whether a pilot's readback correctly matches the controller's "
        "instruction, and flag any discrepancy."
    )

    with st.sidebar:
        st.header("Settings")
        default_backend = os.getenv("EXTRACTOR_BACKEND", "ollama")
        backend = st.selectbox(
            "Extraction backend",
            options=["ollama", "hf"],
            index=0 if default_backend == "ollama" else 1,
            help="ollama = local model; hf = Hugging Face Inference API (needs HF_TOKEN).",
        )
        model = st.text_input(
            "Model (optional override)",
            value=os.getenv("MODEL_NAME", ""),
            placeholder="qwen2.5:3b  or  Qwen/Qwen2.5-7B-Instruct",
        )
        st.markdown("---")
        st.subheader("Load an example")
        choice = st.selectbox("Example", ["—"] + list(EXAMPLES.keys()))
        if choice != "—":
            st.session_state["instruction"], st.session_state["readback"] = EXAMPLES[choice]

    instruction = st.text_area(
        "Controller instruction",
        key="instruction",
        height=90,
        placeholder="Speedbird 245, climb flight level 280.",
    )
    readback = st.text_area(
        "Pilot readback",
        key="readback",
        height=90,
        placeholder="Climb flight level 280, Speedbird 245.",
    )

    if st.button("Verify readback", type="primary", use_container_width=True):
        if not instruction.strip() or not readback.strip():
            st.warning("Please enter both an instruction and a readback.")
            return
        try:
            with st.spinner("Extracting fields and comparing…"):
                extractor = _extractor(backend, model.strip())
                result = verify(instruction, readback, extractor)
        except Exception as exc:
            st.error(f"Could not run the verifier: {exc}")
            if backend == "ollama":
                st.info("Is Ollama running and the model pulled? Try `ollama pull qwen2.5:3b`.")
            else:
                st.info("The HF backend needs a valid HF_TOKEN in the app secrets.")
            return

        _render_result(result)


def _render_result(result) -> None:
    verdict = result.verdict
    if verdict.is_match:
        st.success("✅ MATCH — the readback is correct.")
    else:
        st.error(f"❌ DISCREPANCY — {len(verdict.discrepancies)} issue(s) found.")
        for d in verdict.discrepancies:
            st.markdown(
                f"- **{d.field}** · _{d.category.replace('_', ' ')}_ — {d.detail}"
            )

    with st.expander("Show extracted fields"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Instruction**")
            st.json(result.instruction_fields.raw or {})
        with col2:
            st.markdown("**Readback**")
            st.json(result.readback_fields.raw or {})


if __name__ == "__main__":
    main()
