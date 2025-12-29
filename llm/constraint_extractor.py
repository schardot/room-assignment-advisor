from typing import Dict

# Try to initialize Ollama LLM - prefer langchain_ollama, fallback to langchain_community
llm = None
prompt = None

try:
    from langchain_ollama import OllamaLLM  # type: ignore
    from langchain_core.prompts import PromptTemplate
    llm = OllamaLLM(model="llama3", temperature=0)
    prompt = PromptTemplate(
        input_variables=["notes"],
        template="""
You extract room allocation constraints from hotel booking notes.

Notes:
"{notes}"

Return ONLY a JSON object with this structure:
{{
  "no_stairs": boolean
}}

If the notes do not mention stairs, accessibility, elderly, mobility issues, or similar, return false.
"""
    )
except ImportError:
    try:
        # Fallback to deprecated import for backwards compatibility
        from langchain_community.llms import Ollama  # type: ignore
        from langchain_core.prompts import PromptTemplate
        llm = Ollama(model="llama3", temperature=0)
        prompt = PromptTemplate(
            input_variables=["notes"],
            template="""
You extract room allocation constraints from hotel booking notes.

Notes:
"{notes}"

Return ONLY a JSON object with this structure:
{{
  "no_stairs": boolean
}}

If the notes do not mention stairs, accessibility, elderly, mobility issues, or similar, return false.
"""
        )
    except ImportError:
        # No langchain packages available - will use keyword matching fallback
        pass

def extract_constraints(notes: str) -> Dict[str, bool]:
    if not notes or not notes.strip():
        return {"no_stairs": False}

    # Use LLM if available
    if llm is not None and prompt is not None:
        try:
            response = llm.invoke(prompt.format(notes=notes))
            response = response.lower()
            return {
                "no_stairs": "true" in response
            }
        except Exception:
            # Fall through to keyword matching on any error
            pass

    # Fallback to keyword matching
    notes_lower = notes.lower()
    no_stairs_keywords = [
        "no stairs", "no stair", "ground floor", "first floor",
        "wheelchair", "mobility", "cannot climb", "can't climb",
        "unable to climb", "difficulty with stairs", "stairs difficult",
        "avoid stairs", "no steps", "accessible", "disability",
        "elderly", "senior", "walking difficulty", "mobility aid",
    ]
    no_stairs = any(keyword in notes_lower for keyword in no_stairs_keywords)

    return {"no_stairs": no_stairs}
