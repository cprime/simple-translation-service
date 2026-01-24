"""LangChain chains for generator and judge LLMs."""

import json
from langchain_community.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser

from app.prompts import GENERATOR_PROMPT, JUDGE_PROMPT


def create_generator_chain():
    """Create the generator chain that translates and conjugates verbs."""
    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0,
        format="json"
    )

    chain = GENERATOR_PROMPT | llm | StrOutputParser()
    return chain


def create_judge_chain():
    """Create the judge chain that validates and corrects conjugations."""
    llm = ChatOllama(
        model="qwen2.5:14b",
        temperature=0,
        format="json"
    )

    chain = JUDGE_PROMPT | llm | StrOutputParser()
    return chain


def process_conjugation(verb: str) -> dict:
    """
    Process a verb through generator and judge chains.

    Args:
        verb: English verb to conjugate

    Returns:
        dict: Judge-validated conjugation result

    Raises:
        ValueError: If LLM output is malformed
    """
    generator_chain = create_generator_chain()
    judge_chain = create_judge_chain()

    # Step 1: Generate initial conjugations
    generator_output = generator_chain.invoke({"verb": verb})

    # Parse generator output to ensure it's valid JSON
    try:
        generated_data = json.loads(generator_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Generator produced malformed JSON: {e}")

    # Step 2: Judge validates and corrects
    judge_output = judge_chain.invoke({
        "english_verb": verb,
        "generated_output": generator_output
    })

    # Parse judge output
    try:
        judge_data = json.loads(judge_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Judge produced malformed JSON: {e}")

    # Validate judge output has required fields
    required_fields = ["english", "greek", "conjugations", "confidence", "notes"]
    for field in required_fields:
        if field not in judge_data:
            raise ValueError(f"Judge output missing required field: {field}")

    return judge_data
