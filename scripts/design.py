"""Build original profile artwork. Run from any directory; no dependencies."""
from html import escape
from pathlib import Path

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
        body = f'''<rect x="1" y="1" width="718" height="258" rx="18" fill="{PANEL}" stroke="#30363D"/>
<path d="M20 1H700" stroke="{accent}" stroke-width="2"/>
{text(28,35,label,15,accent,600)}{text(658,40,number,25,MUTED,600)}
{text(28,82,title,34,TEXT,700)}
{text(28,124,line1,23)}{text(28,154,line2,23)}
<path d="M28 177H692" stroke="#30363D"/>
{text(28,208,stack1,21,accent)}{text(28,238,stack2,20,MUTED)}'''
        write(f"project-{name}.svg", svg(720, 260, f"{title}. {line1} {line2} {stack1}. {stack2}.", body))

    for _, accent, labels in GROUPS:
        for label in labels:
            width = max(84, round(len(label) * 7.7 + 38))
            body = f'''<rect x=".5" y=".5" width="{width-1}" height="31" rx="8" fill="{PANEL}" stroke="#30363D"/>
<circle cx="14" cy="16" r="3" fill="{accent}"/>
{text(25,21,label,13,TEXT,600)}'''
            write(f"badges/{slug(label)}.svg", svg(width, 32, label, body))


if __name__ == "__main__":
    build()
