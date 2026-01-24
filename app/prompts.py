"""LLM prompt templates for generator and judge."""

from langchain.prompts import PromptTemplate


GENERATOR_PROMPT = PromptTemplate.from_template(
    """You are a Greek language expert. Translate the following English verb to Modern Greek and provide EXACTLY 6 present-tense conjugations with pronouns.

Example 1:
English verb: to love
{{
  "english": "to love",
  "greek": "αγαπώ",
  "conjugations": [
    {{"pronoun": "εγώ", "form": "αγαπώ"}},
    {{"pronoun": "εσύ", "form": "αγαπάς"}},
    {{"pronoun": "αυτός/αυτή/αυτό", "form": "αγαπά"}},
    {{"pronoun": "εμείς", "form": "αγαπάμε"}},
    {{"pronoun": "εσείς", "form": "αγαπάτε"}},
    {{"pronoun": "αυτοί/αυτές/αυτά", "form": "αγαπούν"}}
  ]
}}

Example 2:
English verb: to read
{{
  "english": "to read",
  "greek": "διαβάζω",
  "conjugations": [
    {{"pronoun": "εγώ", "form": "διαβάζω"}},
    {{"pronoun": "εσύ", "form": "διαβάζεις"}},
    {{"pronoun": "αυτός/αυτή/αυτό", "form": "διαβάζει"}},
    {{"pronoun": "εμείς", "form": "διαβάζουμε"}},
    {{"pronoun": "εσείς", "form": "διαβάζετε"}},
    {{"pronoun": "αυτοί/αυτές/αυτά", "form": "διαβάζουν"}}
  ]
}}

Now translate this verb:
English verb: {verb}

Return ONLY valid JSON in the exact format shown above with no additional text or explanation."""
)


JUDGE_PROMPT = PromptTemplate.from_template(
    """You are an expert judge for Modern Greek verb conjugations. Review the translation and conjugations for correctness.

REFERENCE EXAMPLES of correct Modern Greek present tense conjugations:

"to write" = γράφω:
- εγώ γράφω
- εσύ γράφεις
- αυτός/αυτή/αυτό γράφει
- εμείς γράφουμε
- εσείς γράφετε
- αυτοί/αυτές/αυτά γράφουν

"to speak" = μιλώ:
- εγώ μιλώ
- εσύ μιλάς
- αυτός/αυτή/αυτό μιλάει
- εμείς μιλάμε
- εσείς μιλάτε
- αυτοί/αυτές/αυτά μιλούν

Now evaluate this submission:
Original English verb: {english_verb}

Generated output:
{generated_output}

Your task:
1. Check if the Greek translation is correct
2. Verify all 6 conjugations match Modern Greek present tense patterns
3. Correct any errors
4. Assign confidence: 1.0 (perfect), 0.8-0.95 (minor fixes), 0.5-0.75 (major fixes), <0.5 (complete rewrite)
5. Explain your corrections in notes

Return ONLY valid JSON with no additional text:
{{
  "english": "the original English verb",
  "greek": "the correct Greek infinitive form",
  "conjugations": [
    {{"pronoun": "εγώ", "form": "correct form"}},
    {{"pronoun": "εσύ", "form": "correct form"}},
    {{"pronoun": "αυτός/αυτή/αυτό", "form": "correct form"}},
    {{"pronoun": "εμείς", "form": "correct form"}},
    {{"pronoun": "εσείς", "form": "correct form"}},
    {{"pronoun": "αυτοί/αυτές/αυτά", "form": "correct form"}}
  ],
  "confidence": 0.95,
  "notes": "Brief explanation of corrections or validation"
}}"""
)
