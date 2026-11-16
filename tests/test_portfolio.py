"""Unit tests for portfolio data, API filtering, and language ratio targets."""

import unittest

from app import filter_projects, get_health_payload
from build import (
    compute_language_bytes,
    compute_language_percentages,
    validate_index_html,
    validate_projects,
)
from portfolio_data import EDUCATION, PROJECTS, SKILLS, export_portfolio_dict, list_all_technologies


class PortfolioDataTests(unittest.TestCase):
    def test_project_urls_and_summaries_are_valid(self) -> None:
        self.assertEqual(validate_projects(), [])
        self.assertGreaterEqual(len(PROJECTS), 3)

    def test_index_html_metadata_present(self) -> None:
        self.assertEqual(validate_index_html(), [])

    def test_education_average_sgpa(self) -> None:
        self.assertAlmostEqual(EDUCATION.average_sgpa, 7.043, places=3)

    def test_skills_include_python_and_flask(self) -> None:
        self.assertIn("Python", SKILLS["Languages"])
        self.assertIn("Flask", SKILLS["Web"])
        self.assertIn("Python", list_all_technologies())

    def test_export_portfolio_dict_keys(self) -> None:
        data = export_portfolio_dict()
        self.assertEqual(set(data.keys()), {"profile", "projects", "skills", "technologies", "education"})


class PortfolioApiTests(unittest.TestCase):
    def test_filter_by_category(self) -> None:
        res = filter_projects(category="Games")
        self.assertEqual(res["count"], 1)
        self.assertEqual(res["projects"][0]["slug"], "neon-arena")

    def test_filter_by_technology(self) -> None:
        res = filter_projects(tech="Gemini")
        self.assertEqual(res["count"], 1)
        self.assertEqual(res["projects"][0]["slug"], "my-manga-tracker")

    def test_filter_by_search_query(self) -> None:
        res = filter_projects(query="algorithms")
        self.assertEqual(res["count"], 1)
        self.assertEqual(res["projects"][0]["slug"], "python-learning")

    def test_health_payload(self) -> None:
        health = get_health_payload()
        self.assertEqual(health["status"], "ok")
        self.assertEqual(health["project_count"], len(PROJECTS))


class LanguageBalanceTests(unittest.TestCase):
    def test_python_share_at_least_forty_percent(self) -> None:
        byte_counts = compute_language_bytes()
        percentages = compute_language_percentages()
        self.assertIn("Python", byte_counts)
        self.assertGreaterEqual(percentages["Python"], 45.0)


if __name__ == "__main__":
    unittest.main()
