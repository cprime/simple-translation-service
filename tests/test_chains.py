"""Tests for LangChain chains and processing logic."""

import pytest
import json
from app.chains import create_generator_chain, create_judge_chain, process_conjugation


class TestGeneratorChain:
    """Tests for the generator chain."""

    def test_generator_chain_creation(self):
        """Test that generator chain can be created."""
        chain = create_generator_chain()
        assert chain is not None

    @pytest.mark.slow
    def test_generator_produces_json(self):
        """Test that generator outputs valid JSON."""
        chain = create_generator_chain()
        result = chain.invoke({"verb": "to be"})

        # Should be valid JSON
        data = json.loads(result)
        assert isinstance(data, dict)


class TestJudgeChain:
    """Tests for the judge chain."""

    def test_judge_chain_creation(self):
        """Test that judge chain can be created."""
        chain = create_judge_chain()
        assert chain is not None

    @pytest.mark.slow
    def test_judge_produces_json(self):
        """Test that judge outputs valid JSON."""
        chain = create_judge_chain()
        sample_input = json.dumps({
            "english": "to be",
            "greek": "είμαι",
            "conjugations": [
                {"pronoun": "εγώ", "form": "είμαι"},
                {"pronoun": "εσύ", "form": "είσαι"},
                {"pronoun": "αυτός/αυτή/αυτό", "form": "είναι"},
                {"pronoun": "εμείς", "form": "είμαστε"},
                {"pronoun": "εσείς", "form": "είστε"},
                {"pronoun": "αυτοί/αυτές/αυτά", "form": "είναι"}
            ]
        })

        result = chain.invoke({
            "english_verb": "to be",
            "generated_output": sample_input
        })

        # Should be valid JSON
        data = json.loads(result)
        assert isinstance(data, dict)


class TestProcessConjugation:
    """Tests for the full conjugation processing pipeline."""

    @pytest.mark.slow
    def test_process_conjugation_returns_dict(self):
        """Test that process_conjugation returns a dictionary."""
        result = process_conjugation("to be")
        assert isinstance(result, dict)

    @pytest.mark.slow
    def test_process_conjugation_has_required_fields(self):
        """Test that result has all required fields."""
        result = process_conjugation("to be")

        required_fields = ["english", "greek", "conjugations", "confidence", "notes"]
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"

    @pytest.mark.slow
    def test_process_conjugation_conjugations_structure(self):
        """Test that conjugations have correct structure."""
        result = process_conjugation("to be")

        assert isinstance(result['conjugations'], list)
        assert len(result['conjugations']) == 6

        for conj in result['conjugations']:
            assert 'pronoun' in conj
            assert 'form' in conj

    @pytest.mark.slow
    def test_process_conjugation_confidence_range(self):
        """Test that confidence is in valid range."""
        result = process_conjugation("to be")
        assert 0.0 <= result['confidence'] <= 1.0

    @pytest.mark.slow
    def test_process_conjugation_different_verbs(self):
        """Test that different verbs produce different results."""
        result1 = process_conjugation("to have")
        result2 = process_conjugation("to write")

        # Results should be different
        assert result1['greek'] != result2['greek']

    @pytest.mark.slow
    def test_process_conjugation_handles_simple_verb(self):
        """Test that simple verbs are processed successfully."""
        # This test verifies the function works end-to-end
        result = process_conjugation("to go")
        assert result is not None
        assert 'greek' in result
