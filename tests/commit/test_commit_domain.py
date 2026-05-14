import pytest


class TestCommitDomain:
    def test_creates_valid_commit(self, commit_factory):
        commit = commit_factory()

        assert commit.code == "COMM-001"
        assert commit.description == "Intervento cliente Napoli"

    def test_rejects_empty_code_and_description(self, commit_factory):
        with pytest.raises(ValueError, match="Code cannot be empty"):
            commit_factory(code="")

        with pytest.raises(ValueError, match="Description cannot be empty"):
            commit_factory(description="")
