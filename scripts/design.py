"""Build original profile artwork. Run from any directory; no dependencies."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BG, PANEL, CYAN, VIOLET, TEXT, MUTED = "#0D1117", "#161B22", "#22D3EE", "#A78BFA", "#E6EDF3", "#9DA7B3"


def svg(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title><defs><linearGradient id="accent" x2="1" y2="1"><stop stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>
<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">{body}</g></svg>'''


def text(x, y, content, size=24, color=TEXT, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(content))}</text>'


def write(name, content):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


GROUPS = [
    ("Languages", CYAN, ["Python", "TypeScript", "JavaScript", "SQL", "Bash", "HTML / CSS"]),
    ("Frontend", VIOLET, ["React", "Next.js", "Redux Toolkit", "Tailwind CSS", "Vite"]),
    ("Backend", CYAN, ["FastAPI", "NestJS", "Node.js", "Express", "Pydantic"]),
    ("Data & messaging", VIOLET, ["PostgreSQL", "SQL Server", "MongoDB", "Redis", "Kafka"]),
    ("AI integrations & data", CYAN, ["OpenAI API", "Azure OpenAI", "MLflow", "Pandas", "NumPy"]),
    ("Cloud & platform", VIOLET, ["Kubernetes", "Docker", "Helm", "Argo CD", "Azure", "Azure DevOps", "AWS S3"]),
]

ICONS = {
    "Python": "python", "TypeScript": "typescript", "JavaScript": "javascript",
    "SQL": "database", "Bash": "bash", "HTML / CSS": "html5",
    "React": "react", "Next.js": "nextjs", "Redux Toolkit": "redux",
    "Tailwind CSS": "tailwindcss", "Vite": "vitejs", "FastAPI": "fastapi",
    "NestJS": "nestjs", "Node.js": "nodejs", "Express": "express",
    "Pydantic": "pydantic", "PostgreSQL": "postgresql", "SQL Server": "microsoftsqlserver",
    "MongoDB": "mongodb", "Redis": "redis", "Kafka": "apachekafka",
    "OpenAI API": "openai", "Azure OpenAI": "azure", "MLflow": "mlflow",
    "Pandas": "pandas", "NumPy": "numpy", "Kubernetes": "kubernetes",
    "Docker": "docker", "Helm": "helm", "Argo CD": "argocd",
    "Azure": "azure", "Azure DevOps": "azuredevops", "AWS S3": "amazonwebservices",
}


def icon_markup(name, x=9, y=6, size=20):
    if name == "database":
        return f'''<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{CYAN}" stroke-width="1.8">
<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 4 18 4 18 0V5M3 12c0 4 18 4 18 0"/></g>'''
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    root = ET.parse(ASSETS / "icons" / f"{name}.svg").getroot()
    root.attrib.update(x=str(x), y=str(y), width=str(size), height=str(size), **{"aria-hidden": "true"})
    # Monochrome marks need an explicit light fill on this dark badge surface.
    fill = {"pydantic": "#E92063", "mlflow": CYAN, "openai": TEXT}.get(name)
    if fill:
        root.set("fill", fill)
    if name in ("express", "apachekafka", "helm", "pandas", "amazonwebservices", "bash"):
        for element in root.iter():
            for attr in ("fill", "stroke"):
                if element.get(attr, "").lower() in ("#000", "#000000", "black", "#130f40", "#0f1689", "#150458", "#252f3e", "#293138", "#2d2d2d", "#0f1f38", "#231f20", "#130754"):
                    element.set(attr, TEXT)
        if name in ("express", "apachekafka"):
            root.set("fill", TEXT)
    return ET.tostring(root, encoding="unicode")


def slug(label):
    return label.lower().replace(" / ", "-").replace(" ", "-").replace(".", "")


def build():
    hero = f'''<rect width="840" height="300" rx="22" fill="{BG}"/>
<rect x="1" y="1" width="838" height="298" rx="21" fill="none" stroke="#30363D"/>
<path d="M610 0H840V300H710L610 200Z" fill="{PANEL}"/>
<g fill="none" stroke="url(#accent)" opacity=".55"><path d="M625 65L685 30L745 65V135L685 170L625 135Z"/><path d="M685 100L745 65L805 100V170L745 205L685 170Z"/><path d="M625 135L685 100L745 135V205L685 240L625 205Z"/></g>
<circle cx="745" cy="65" r="5" fill="{CYAN}"/><circle cx="685" cy="240" r="5" fill="{VIOLET}"/>
<rect x="36" y="35" width="5" height="21" rx="2" fill="{CYAN}"/>
{text(53,53,'JAUHAR4563 / ENGINEERING',16,MUTED,600)}
{text(36,124,'Muhammadali',48,TEXT,700)}
{text(36,178,'Jawhar',48,TEXT,700)}
<rect x="36" y="202" width="100" height="3" rx="1.5" fill="url(#accent)"/>
{text(36,241,'Full-stack Engineer',26,CYAN,600)}
{text(36,274,'Backend · AI Integrations · Cloud',21,MUTED)}'''
    write("header.svg", svg(840, 300, "Muhammadali Jawhar — Full-stack Engineer. Backend, AI Integrations and Cloud.", hero))

    projects = [
        ("shuffle", "01", "SHUFFLE", "SOCIAL / REALTIME", "A full-stack social application with chat,", "video calling and payment integrations.", "React · TypeScript · Express · MongoDB", "Socket.IO · AWS S3 · Stripe", CYAN),
        ("zenlaps", "02", "ZenLaps", "COMMERCE / BACKEND", "An e-commerce application with catalog,", "cart, orders and payment workflows.", "Node.js · Express · MongoDB · EJS", "Razorpay · Session authentication", VIOLET),
        ("github-api", "03", "GitHub API Explorer", "APIS / DATA", "A GitHub API project for exploring", "repositories, followers and user profiles.", "React · TypeScript · Express", "PostgreSQL · Redux Toolkit", CYAN),
    ]
    for name, number, title, label, line1, line2, stack1, stack2, accent in projects:
        details = {
            "shuffle": (["Social app with chat, video", "calls and payment integrations."],
                        ["React · TypeScript · Express", "MongoDB · Socket.IO · AWS S3"]),
            "zenlaps": (["E-commerce with a catalog,", "cart, orders and payments."],
                        ["Node.js · Express · MongoDB", "EJS · Razorpay"]),
            "github-api": (["Explore GitHub repositories,", "followers and user profiles."],
                           ["React · TypeScript · Express", "PostgreSQL · Redux Toolkit"]),
        }
        description, stack = details[name]
        # A fixed, readable card size lets GitHub's inline images wrap into a grid.
        # The transparent bottom gutter gives wrapped rows breathing room.
        body = f'''<rect x="1" y="1" width="278" height="190" rx="14" fill="{PANEL}" stroke="#30363D"/>
<path d="M16 1H264" stroke="{accent}" stroke-width="2"/>
{text(18,25,label,10,accent,600)}{text(243,26,number,12,MUTED,600)}
{text(18,58,title,20,TEXT,700)}
{text(18,88,description[0],13)}{text(18,108,description[1],13)}
<path d="M18 129H262" stroke="#30363D"/>
{text(18,153,stack[0],12,accent)}{text(18,174,stack[1],12,MUTED)}'''
        write(f"project-{name}-compact.svg", svg(280, 208, f"{title}. {line1} {line2} {stack1}. {stack2}.", body))

    for _, _, labels in GROUPS:
        for label in labels:
            width = max(96, round(len(label) * 7.7 + 51))
            mark = icon_markup(ICONS[label])
            if label == "HTML / CSS":
                mark = icon_markup("html5", x=5, y=8, size=16) + icon_markup("css3", x=20, y=8, size=16)
            body = f'''<rect x=".5" y=".5" width="{width-1}" height="31" rx="8" fill="{PANEL}" stroke="#30363D"/>
{mark}
{text(39,21,label,13,TEXT,600)}'''
            write(f"badges/icons/{slug(label)}.svg", svg(width, 32, label, body))


if __name__ == "__main__":
    build()
