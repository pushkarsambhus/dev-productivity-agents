import re
from .llm import enrich_suggestions

RULES = [
    {
        "name": "npm_404_dependency",
        "pattern": r"ERR! 404 Not Found|No matching version found|E404",
        "classification": "dependency_error",
        "suggestions": [
            "Check package name/version in package.json",
            "Run `npm cache clean --force` then `npm ci`",
            "Verify registry auth/token",
            "If behind proxy, configure npm proxy",
        ],
    },
    {
        "name": "maven_missing_artifact",
        "pattern": r"Could not find artifact|Failed to collect dependencies",
        "classification": "dependency_error",
        "suggestions": [
            "Check groupId/artifactId/version in pom.xml",
            "Ensure repository credentials are set (settings.xml)",
            "Try `mvn -U clean install` to force updates",
            "Check if artifact is in internal Nexus/Artifactory",
        ],
    },
]

def triage_log(text: str) -> dict:
    signals = []
    for rule in RULES:
        if re.search(rule["pattern"], text, flags=re.IGNORECASE | re.MULTILINE):
            signals.append(rule)

    if not signals:
        return {
            "tool": "build_fixer_agent",
            "classification": "unknown",
            "top_signals": [],
            "suggestions": [
                "Search for the first error stack or 'Caused by'",
                "Retry with clean build (clean caches, reinstall deps)",
                "Check recent dependency changes or env differences between local and CI",
            ],
            "llm_enriched": False,
        }

    classification = signals[0]["classification"]
    top_signals = [s["name"] for s in signals]
    suggestions = []
    for s in signals:
        suggestions.extend(s["suggestions"])

    seen = set()
    dedup = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            dedup.append(s)

    return {
        "tool": "build_fixer_agent",
        "classification": classification,
        "top_signals": top_signals,
        "suggestions": dedup,
        "llm_enriched": False,
    }
