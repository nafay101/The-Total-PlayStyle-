import datetime as dt

import pandas as pd
import glob

import streamlit as st
import streamlit.components.v1 as components

import content as C

st.set_page_config(page_title="Football IQ & Performance Academy", page_icon="⚽", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&display=swap');
.block-container{max-width:1100px;padding:2.5rem 2rem 4rem}
[data-testid="stVerticalBlock"]{gap:1.4rem}
p,li{line-height:1.8;font-size:1.03rem}
h1,h2,h3,h4{font-family:'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.03em}
.lead{font-size:1.2rem;opacity:.9}
.hero{display:flex;gap:2rem;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,#052e16,#15803d);
 border-radius:20px;padding:2.2rem 2.6rem;color:#fff}
.hero>div{flex:1 1 300px}.hero h1{color:#fff;font-size:3rem;line-height:1.05;margin:.3rem 0 1rem}
.eyebrow{color:#bbf7d0;letter-spacing:.25em;font-weight:700;font-size:.8rem}
</style>""", unsafe_allow_html=True)

PAGES = ["Home", "Football basics", "Skills and techniques", "Positions and numbers", "Fitness and recovery",
         "Tactics", "Roadmap", "Progress", "Ask a question"]
ALL_ITEMS = C.LESSONS + C.EXERCISES


def go(page):
    st.session_state.page = page
    st.session_state.collapse = True


# ---------- Supabase / demo ----------
def sb():
    if "sb" not in st.session_state:
        try:
            from supabase import create_client
            st.session_state.sb = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["anon_key"])
        except Exception:
            st.session_state.sb = None
    return st.session_state.sb


def demo():
    return sb() is None


def sidebar_auth():
    if demo():
        st.sidebar.warning("DEMO MODE: no database configured. Data is not private and is lost on refresh.")
        return
    if st.session_state.get("user"):
        st.sidebar.success(f"Signed in: {st.session_state.user.email}")
        if st.sidebar.button("Sign out"):
            sb().auth.sign_out()
            st.session_state.user = None
            st.rerun()
        return
    with st.sidebar.form("auth"):
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        c1, c2 = st.columns(2)
        si, su = c1.form_submit_button("Sign in"), c2.form_submit_button("Sign up")
    if si or su:
        try:
            r = sb().auth.sign_in_with_password({"email": email, "password": pw}) if si else \
                sb().auth.sign_up({"email": email, "password": pw})
            if r.user and r.session:
                st.session_state.user = r.user
                st.rerun()
            else:
                st.sidebar.info("Check your email to confirm, then sign in.")
        except Exception as e:
            st.sidebar.error(f"Auth failed: {e}")


def load_rows():
    if demo():
        return st.session_state.setdefault("demo_rows", [])
    try:
        return sb().table("sessions").select("*").order("date").execute().data
    except Exception:
        st.error("Database not set up correctly. Run supabase_schema.sql (see README).")
        return []


def save_row(row):
    if demo():
        st.session_state.setdefault("demo_rows", []).append(row)
    else:
        sb().table("sessions").insert(row).execute()


# ---------- components ----------
def render_item(it):
    with st.container(border=True):
        st.markdown(f"## {it['title']}")
        st.caption(it["category"].upper())
        st.markdown(f"<p class='lead'>{it['purpose']}</p>", unsafe_allow_html=True)
        photos = sorted(glob.glob(f"assets/{it['id']}_*"))
        st.markdown("#### Technique, step by step")
        cols = st.columns(3, gap="large")
        for i, (lab, cap, img) in enumerate(it["frames"]):
            with cols[i % 3]:
                with st.container(border=True):
                    if i < len(photos):
                        st.image(photos[i], use_container_width=True)
                    else:
                        st.markdown(img, unsafe_allow_html=True)
                    st.markdown(f"**{lab}**")
                    st.write(cap)
        st.divider()
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("#### Setup")
            if "equipment" in it:
                st.write(f"Equipment: {it['equipment']}")
            st.write(it["setup"])
            st.markdown("#### Steps")
            st.markdown("\n".join(f"{i}. {s}" for i, s in enumerate(it["steps"], 1)))
            if "dose" in it:
                st.markdown(f"**Sets/reps/rest:** {it['dose']}")
        with c2:
            st.markdown("#### Coaching cues")
            st.markdown("\n".join(f"- {s}" for s in it["cues"]))
            st.markdown("#### Common mistakes")
            st.markdown("\n".join(f"- {s}" for s in it["mistakes"]))
            st.markdown(f"**Harder:** {it['progress']}")
            st.markdown(f"**Easier:** {it['simplify']}")


def pitch_formation(pts):
    inner = "".join(C.P(x, y, str(i + 1), "#1d4ed8") for i, (x, y) in enumerate(pts))
    return C.svg(inner, "Starting shape")


# ---------- pages ----------
def home():
    st.markdown("<div class='hero'><div><p class='eyebrow'>TRAIN LIKE A PROFESSIONAL</p><h1>Football IQ & Performance Academy</h1><p>Learn the game, master technique, follow structured training and track every session.</p></div><div>" + C.coach_svg() + "</div></div>", unsafe_allow_html=True)
    rows = load_rows()
    week = [r for r in rows if r["date"] >= str(dt.date.today() - dt.timedelta(days=7))]
    c = st.columns(3)
    c[0].metric("Sessions logged", len(rows))
    c[1].metric("Minutes this week", sum(r["minutes"] for r in week))
    c[2].metric("Next lesson", C.LESSONS[0]["title"])
    b = st.columns(3)
    b[0].button("Start learning", on_click=go, args=("Skills and techniques",))
    b[1].button("Build my roadmap", on_click=go, args=("Roadmap",))
    b[2].button("Log a session", on_click=go, args=("Progress",))
    st.subheader("Recent activity")
    if rows:
        st.dataframe(pd.DataFrame(rows[-5:])[["date", "kind", "minutes", "effort"]], hide_index=True)
    else:
        st.info("No sessions yet. Log your first one to see progress here.")


def basics():
    st.title("Football basics")
    st.markdown(C.svg(C.P(60, 110, "GK") + C.B(180, 110) + C.A(190, 110, 300, 110) + C.N(120, 190, "Attacking direction"), "The pitch"),
                unsafe_allow_html=True)
    for b in C.BASICS:
        with st.expander(b["title"], expanded=False):
            st.write(b["text"])
            st.markdown(f"[IFAB reference]({b['ref']})")


def skills():
    st.title("Skills and techniques")
    cats = sorted({l["category"] for l in C.LESSONS})
    sel = st.selectbox("Topic", cats)
    for l in [l for l in C.LESSONS if l["category"] == sel]:
        render_item(l)


def positions():
    st.title("Positions and numbers")
    names = [p["name"] for p in C.POSITIONS]
    sel = st.selectbox("Choose your position", names)
    p = next(p for p in C.POSITIONS if p["name"] == sel)
    st.markdown(f"**Traditional term:** {p['term']}  \n**In possession:** {p['in']}  \n**Out of possession:** {p['out']}  \n"
                f"**Useful skills:** {p['skills']}  \n**Training priorities:** {p['priorities']}")
    st.markdown("**Relevant lessons and drills**")
    for it in ALL_ITEMS:
        if "all" in it["positions"] or sel in it["positions"]:
            st.write(f"- {it['title']} ({it['category']})")
    st.subheader("Shirt numbers")
    st.info(C.NUMBERS)


def fitness():
    st.title("Fitness and recovery")
    st.warning(C.HEALTH_NOTE)
    st.markdown("**Warm-up:** " + "; ".join(C.WARMUP) + "  \n**Cooldown:** " + "; ".join(C.COOLDOWN))
    for e in C.EXERCISES:
        render_item(e)


def tactics():
    st.title("Tactics and playing styles")
    st.caption(C.FORMATION_NOTE)
    f = st.selectbox("Formation", list(C.FORMATIONS))
    st.markdown(pitch_formation(C.FORMATIONS[f]["pts"]), unsafe_allow_html=True)
    st.write(C.FORMATIONS[f]["text"])
    st.subheader("Styles")
    for k, v in C.STYLES.items():
        st.write(f"- **{k}**: {v}")


def build_plan(level, pos, days, minutes, offset):
    pool = [i for i in ALL_ITEMS if "all" in i["positions"] or pos in i["positions"]]
    skill = [i for i in pool if i in C.LESSONS] or pool
    fit = [i for i in pool if i in C.EXERCISES] or pool
    n_main = 1 if level == "Beginner" else 2
    rows, k = [], offset
    for w in range(1, 5):
        for d in days:
            main = [skill[(k + j) % len(skill)]["title"] for j in range(n_main)] + [fit[k % len(fit)]["title"]]
            k += 1
            rows.append({"week": w, "day": d, "warm-up (10 min)": C.WARMUP[0], "main": "; ".join(main),
                         "main minutes": max(minutes - 15, 5), "cooldown (5 min)": C.COOLDOWN[0],
                         "total minutes": minutes})
    return pd.DataFrame(rows)


def roadmap():
    st.title("Roadmap and session builder")
    with st.form("plan"):
        level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
        pos = st.selectbox("Position", [p["name"] for p in C.POSITIONS])
        days = st.multiselect("Available days", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], default=["Tue", "Thu"])
        minutes = st.slider("Session length (min)", 30, 120, 60, 5)
        st.selectbox("Preferred style", list(C.STYLES))
        ok = st.form_submit_button("Generate plan")
    if ok:
        if not days:
            st.error("Pick at least one day.")
        else:
            st.session_state.plan_args = (level, pos, days, minutes)
            st.session_state.offset = 0
            st.session_state.plan = build_plan(level, pos, days, minutes, 0)
    if "plan" in st.session_state:
        if st.button("Regenerate with different drills"):
            st.session_state.offset += 1
            st.session_state.plan = build_plan(*st.session_state.plan_args, st.session_state.offset)
        st.caption("Plans use only the drills in the library. Edit cells below if needed. Progression: each week repeat and add quality (more reps, pressure).")
        st.session_state.plan = st.data_editor(st.session_state.plan, hide_index=True, use_container_width=True)
    else:
        st.info("Fill in the form to generate a 4-week plan.")


def progress():
    st.title("Progress")
    if not demo() and not st.session_state.get("user"):
        st.info("Sign in from the sidebar to record private progress.")
        return
    with st.form("log"):
        d = st.date_input("Date", dt.date.today())
        kind = st.selectbox("Type", ["Skills", "Fitness", "Match", "Lesson"])
        mins = st.number_input("Duration (min)", 1, 300, 45)
        eff = st.slider("Perceived effort (1-10)", 1, 10, 5)
        rate = st.slider("Self-rating of skill (1-5)", 1, 5, 3)
        notes = st.text_area("Notes", max_chars=500)
        ok = st.form_submit_button("Save session")
    if ok:
        row = {"date": str(d), "kind": kind, "minutes": int(mins), "effort": eff, "rating": rate, "notes": notes}
        if d > dt.date.today():
            st.error("Date cannot be in the future.")
        else:
            save_row(row)
            st.success("Saved.")
    rows = load_rows()
    if not rows:
        st.info("No sessions yet.")
        return
    df = pd.DataFrame(rows)
    st.line_chart(df.set_index("date")[["minutes", "effort"]])
    st.dataframe(df[["date", "kind", "minutes", "effort", "rating", "notes"]], hide_index=True)


def ask():
    st.title("Ask a question")
    st.caption("Source: local library search (no AI). Not for diagnosis, emergencies or rehab advice.")
    q = st.text_input("Your question")
    if not q:
        return
    words = [w for w in q.lower().split() if len(w) > 2]
    idx = [(b["title"], "Football basics", b["text"]) for b in C.BASICS] + \
          [(i["title"], "Skills and techniques" if i in C.LESSONS else "Fitness and recovery",
            i["purpose"] + " " + " ".join(i["steps"]) + " " + " ".join(i["cues"])) for i in ALL_ITEMS] + \
          [(f, "Tactics", v["text"]) for f, v in C.FORMATIONS.items()]
    scored = sorted(((sum(w in (t + x).lower() for w in words), t, s, x) for t, s, x in idx), reverse=True)
    hits = [h for h in scored if h[0] > 0][:3]
    if not hits:
        st.warning("The library does not have enough information to answer that.")
    for n, t, s, x in hits:
        st.markdown(f"<div class='card'><b>{t}</b> ({s})<br>{x[:300]}</div>", unsafe_allow_html=True)
        st.button(f"Open {s}", key=f"o{t}", on_click=go, args=(s,))


sidebar_auth()
st.sidebar.radio("Navigate", PAGES, key="page", on_change=lambda: st.session_state.update(collapse=True))
{"Home": home, "Football basics": basics, "Skills and techniques": skills,
 "Positions and numbers": positions, "Fitness and recovery": fitness, "Tactics": tactics,
 "Roadmap": roadmap, "Progress": progress, "Ask a question": ask}[st.session_state.page]()

if st.session_state.pop("collapse", False):
    components.html("""<script>const d=window.parent.document;
for(const s of ['[data-testid="stSidebarCollapseButton"] button','[data-testid="stSidebar"] button[kind="header"]','[data-testid="stSidebarCollapseButton"]']){const b=d.querySelector(s);if(b){b.click();break;}}
</script>""", height=0)
