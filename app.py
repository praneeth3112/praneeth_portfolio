"""Flask and standard-library API server for Praneeth's AI/ML portfolio."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs

from portfolio_data import EDUCATION, PROFILE, PROJECTS, SKILLS, export_portfolio_dict

ROOT_DIR = Path(__file__).resolve().parent
DIST_INDEX = ROOT_DIR / "dist" / "index.html"
DEV_INDEX = ROOT_DIR / "index.html"


def resolve_html_entry() -> Optional[Path]:
    """Return the built dist/index.html if available, else root index.html."""
    if DIST_INDEX.exists():
        return DIST_INDEX
    if DEV_INDEX.exists():
        return DEV_INDEX
    return None


def filter_projects(
    query: Optional[str] = None,
    category: Optional[str] = None,
    tech: Optional[str] = None,
) -> Dict[str, Any]:
    """Filter portfolio projects by search term, category, or technology."""
    q = (query or "").strip().lower()
    cat = (category or "").strip().lower()
    t = (tech or "").strip().lower()

    matched: List[Dict[str, Any]] = []
    for project in PROJECTS:
        if cat and cat != "all" and project.category.lower() != cat:
            continue
        if t and not any(t in item.lower() for item in project.technologies):
            continue
        if q:
            in_title = q in project.title.lower()
            in_summary = any(q in line.lower() for line in project.summary)
            in_tech = any(q in item.lower() for item in project.technologies)
            if not (in_title or in_summary or in_tech):
                continue

        matched.append(
            {
                "slug": project.slug,
                "title": project.title,
                "category": project.category,
                "technologies": project.technologies,
                "summary": project.summary,
                "live_url": project.live_url,
                "source_url": project.source_url,
            }
        )

    return {"count": len(matched), "projects": matched}


def get_health_payload() -> Dict[str, Any]:
    """Return service metadata and portfolio summary counts."""
    return {
        "status": "ok",
        "owner": PROFILE["name"],
        "project_count": len(PROJECTS),
        "skill_groups": len(SKILLS),
        "average_sgpa": EDUCATION.average_sgpa,
    }


def run_flask_app(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Serve portfolio pages and JSON endpoints using Flask."""
    from flask import Flask, Response, jsonify, request

    app = Flask(__name__)

    @app.get("/")
    def index() -> Response:
        html_path = resolve_html_entry()
        if html_path is None:
            return Response("index.html not found", status=404)
        return Response(html_path.read_text(encoding="utf-8"), mimetype="text/html")

    @app.get("/api/health")
    def api_health() -> Response:
        return jsonify(get_health_payload())

    @app.get("/api/profile")
    def api_profile() -> Response:
        return jsonify(export_portfolio_dict())

    @app.get("/api/projects")
    def api_projects() -> Response:
        return jsonify(
            filter_projects(
                query=request.args.get("q"),
                category=request.args.get("category"),
                tech=request.args.get("tech"),
            )
        )

    @app.get("/api/skills")
    def api_skills() -> Response:
        return jsonify(SKILLS)

    app.run(host=host, port=port, debug=False)


class StdlibPortfolioHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP request handler fallback when Flask is absent."""

    def _send_bytes(self, status: int, content_type: str, payload: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, status: int, data: Any) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self._send_bytes(status, "application/json; charset=utf-8", body)

    def do_GET(self) -> None:
        path, _, raw_query = self.path.partition("?")
        params = {k: v[0] for k, v in parse_qs(raw_query).items() if v}

        if path == "/":
            html_path = resolve_html_entry()
            if html_path is None:
                self._send_bytes(404, "text/plain; charset=utf-8", b"index.html not found")
            else:
                self._send_bytes(200, "text/html; charset=utf-8", html_path.read_bytes())
        elif path == "/api/health":
            self._send_json(200, get_health_payload())
        elif path == "/api/profile":
            self._send_json(200, export_portfolio_dict())
        elif path == "/api/projects":
            self._send_json(
                200,
                filter_projects(
                    query=params.get("q"),
                    category=params.get("category"),
                    tech=params.get("tech"),
                ),
            )
        elif path == "/api/skills":
            self._send_json(200, SKILLS)
        else:
            self._send_json(404, {"error": "Endpoint not found"})


def run_stdlib_server(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Start the built-in Python HTTP server."""
    server = HTTPServer((host, port), StdlibPortfolioHandler)
    print(f"Serving portfolio API on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    try:
        run_flask_app()
    except ImportError:
        run_stdlib_server()
