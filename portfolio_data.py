"""Structured portfolio metadata, project catalog, and AI/ML skill index."""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Project:
    """Represents a featured engineering or AI/ML portfolio project."""

    slug: str
    title: str
    category: str
    technologies: List[str]
    summary: List[str]
    live_url: str
    source_url: str
    featured: bool = True


@dataclass(frozen=True)
class Education:
    """Academic record and semester SGPA breakdown."""

    degree: str
    institution: str
    year: str
    semester_sgpa: Dict[str, float]

    @property
    def average_sgpa(self) -> float:
        if not self.semester_sgpa:
            return 0.0
        return round(sum(self.semester_sgpa.values()) / len(self.semester_sgpa), 3)


PROFILE: Dict[str, Any] = {
    "name": "Praneeth Reddy Kadavakolla",
    "headline": "AI & ML Undergraduate | Python & JavaScript Developer",
    "bio": (
        "Second-year B.Tech student in AI & ML at Jain University. "
        "I build with Python and JavaScript, and I am seeking an AI/ML "
        "internship where I can learn by shipping real models."
    ),
    "github_url": "https://github.com/praneeth3112",
    "portfolio_url": "https://portfolio-praneethreddy.netlify.app",
    "open_to_internships": True,
}

PROJECTS: List[Project] = [
    Project(
        slug="my-manga-tracker",
        title="My Manga Tracker",
        category="AI & Web",
        technologies=["HTML", "CSS", "JavaScript", "AniList API", "Gemini API"],
        summary=[
            (
                "A single-page app loading live manga data from the AniList "
                "GraphQL API with search, status filters, and pagination."
            ),
            (
                "Calls the Google Gemini API to recommend new series from "
                "completed lists, with CSV import and browser persistence."
            ),
        ],
        live_url="https://mymangatracke.netlify.app",
        source_url="https://github.com/praneeth3112/python-learning/blob/main/animegng%20.html",
    ),
    Project(
        slug="neon-arena",
        title="Neon Arena",
        category="Games",
        technologies=["HTML5 Canvas", "JavaScript"],
        summary=[
            (
                "A twin-stick arena shooter in the browser supporting 2-player "
                "local versus or 3 AI bots that chase, strafe, and fire."
            ),
            (
                "Built collision detection, bullet physics, dash and reload "
                "mechanics, particle effects, and keyboard, touch, or gamepad input."
            ),
        ],
        live_url="https://neonarenapvpandbot.netlify.app",
        source_url=(
            "https://github.com/praneeth3112/python-learning/blob/main/"
            "pythonlearning/neon-arena-2p-keyboard-mobile-console-shooter.html"
        ),
    ),
    Project(
        slug="python-learning",
        title="Python Learning",
        category="Python",
        technologies=["Python", "Flask", "Git"],
        summary=[
            (
                "Practice repository of Python programs, algorithms, and "
                "exercises maintained under version control."
            ),
        ],
        live_url="https://github.com/praneeth3112/python-learning",
        source_url="https://github.com/praneeth3112/python-learning",
    ),
]

SKILLS: Dict[str, List[str]] = {
    "Languages": ["Python", "C", "JavaScript", "TypeScript"],
    "AI and data": ["NumPy", "SQL", "Google Gemini API"],
    "Web": ["HTML", "CSS", "React", "Flask"],
    "Tools": ["Git", "Linux", "VS Code"],
}

EDUCATION = Education(
    degree="B.Tech in Computer Science & Engineering (AI & ML)",
    institution="Jain University",
    year="Second Year",
    semester_sgpa={"Semester 1": 7.65, "Semester 2": 6.435},
)


def list_all_technologies() -> List[str]:
    """Return a sorted, deduplicated list of all technologies used."""
    tech_set = {tech for project in PROJECTS for tech in project.technologies}
    for group_items in SKILLS.values():
        tech_set.update(group_items)
    return sorted(tech_set)


def export_portfolio_dict() -> Dict[str, Any]:
    """Return a JSON-serializable representation of the entire portfolio."""
    return {
        "profile": PROFILE,
        "projects": [asdict(project) for project in PROJECTS],
        "skills": SKILLS,
        "technologies": list_all_technologies(),
        "education": {
            **asdict(EDUCATION),
            "average_sgpa": EDUCATION.average_sgpa,
        },
    }
