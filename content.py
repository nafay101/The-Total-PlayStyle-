"""Content library. Add lessons, exercises, formations or positions by appending
entries to the lists/dicts below; app.py needs no changes."""

ARROW = ('<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
         '<path d="M0,0 L6,3 L0,6z" fill="#fde047"/></marker></defs>')


def svg(inner, label, w=360, h=220):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
            f'style="width:100%;max-width:420px;border-radius:8px">{ARROW}'
            f'<rect width="{w}" height="{h}" fill="#14532d"/>'
            f'<rect x="8" y="8" width="{w-16}" height="{h-16}" fill="none" stroke="#fff" stroke-width="2"/>'
            f'<line x1="{w//2}" y1="8" x2="{w//2}" y2="{h-8}" stroke="#fff" stroke-width="2"/>{inner}'
            f'<text x="16" y="28" fill="#fff" font-size="14" font-weight="700">{label}</text></svg>')


def P(x, y, t="You", c="#2563eb"):
    return (f'<circle cx="{x}" cy="{y}" r="12" fill="{c}" stroke="#fff" stroke-width="2"/>'
            f'<text x="{x}" y="{y+4}" fill="#fff" font-size="9" text-anchor="middle">{t}</text>')


def B(x, y):
    return f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="#000" stroke-width="2"/>'


def A(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fde047" stroke-width="3" '
            f'stroke-dasharray="6 4" marker-end="url(#a)"/>')


def N(x, y, s):
    return f'<text x="{x}" y="{y}" fill="#fde047" font-size="11" font-weight="700">{s}</text>'


def frames(items):
    return [(lab, cap, svg(inner, lab)) for lab, cap, inner in items]



def Z(h, s, p, e1, w1, e2, w2, k1, f1, k2, f2):
    return dict(h=h, s=s, p=p, e1=e1, w1=w1, e2=e2, w2=w2, k1=k1, f1=f1, k2=k2, f2=f2)


def fig(g, kit="#1d4ed8", skin="#e0ac69"):
    def ln(a, b, w, col, o=1):
        return (f'<line x1="{g[a][0]}" y1="{g[a][1]}" x2="{g[b][0]}" y2="{g[b][1]}" stroke="{col}" '
                f'stroke-width="{w}" stroke-linecap="round" opacity="{o}"/>')

    def arm(i, o):
        return (ln("s", "e" + i, 11, kit, o) + ln("e" + i, "w" + i, 8, skin, o)
                + f'<circle cx="{g["w"+i][0]}" cy="{g["w"+i][1]}" r="5" fill="{skin}" opacity="{o}"/>')

    def leg(i, o):
        x, y = g["f" + i]
        return (ln("p", "k" + i, 17, "#0f172a", o) + ln("k" + i, "f" + i, 11, skin, o)
                + f'<ellipse cx="{x+5}" cy="{y}" rx="10" ry="5" fill="#111"/>')
    hx, hy = g["h"]
    head = (f'<circle cx="{hx}" cy="{hy}" r="13" fill="{skin}"/>'
            f'<path d="M{hx-13},{hy} A13,13 0 0 1 {hx+13},{hy} Z" fill="#2b1b12"/>')
    return arm("1", .8) + leg("1", .8) + ln("s", "p", 24, kit) + ln("h", "s", 8, skin) + leg("2", 1) + arm("2", 1) + head


def scene(inner, label, goal=False):
    gl = '<rect x="318" y="138" width="32" height="67" fill="none" stroke="#fff" stroke-width="3"/>' if goal else ""
    return (f'<svg viewBox="0 0 360 240" role="img" aria-label="{label}" style="width:100%;border-radius:10px">{ARROW}'
            f'<rect width="360" height="240" fill="#0f3d24"/><rect y="205" width="360" height="35" fill="#166534"/>{gl}{inner}'
            f'<rect x="10" y="10" width="190" height="26" rx="6" fill="#000" opacity=".55"/>'
            f'<text x="18" y="28" fill="#fff" font-size="14" font-weight="700">{label}</text></svg>')


def sframes(items):
    return [(lab, cap, scene(inner, lab, goal)) for lab, cap, inner, goal in items]


def coach_svg():
    g = Z((100, 44), (100, 72), (98, 128), (80, 98), (66, 118), (122, 84), (150, 66), (92, 168), (88, 204), (106, 168), (112, 204))
    cones = "".join(f'<polygon points="{x},{y} {x-9},{y+16} {x+9},{y+16}" fill="#f97316"/>' for x, y in ((190, 190), (215, 190), (240, 190)))
    ball = '<circle cx="56" cy="128" r="11" fill="#fff" stroke="#111" stroke-width="2"/>'
    return (f'<svg viewBox="0 0 270 215" style="width:100%;max-width:300px">{ARROW}'
            f'<rect y="205" width="270" height="10" fill="#166534" rx="4"/>{fig(g, "#047857")}{ball}{cones}</svg>')

MATE = lambda x, y: P(x, y, "Mate", "#f97316")

LESSONS = [
    {"id": "pass-inside", "title": "Inside-foot pass", "category": "Passing", "positions": ["all"],
     "purpose": "The most reliable short pass: accurate, weighted and easy to receive.",
     "setup": "Two players 10-15 m apart, one ball, a cone gate in the middle. Swap roles every 10 passes.",
     "steps": ["Scan, then pick your target.", "Approach slightly from the side, last step long.",
               "Plant the non-kicking foot beside the ball, toes at the target.",
               "Turn the kicking foot out, ankle locked, strike the middle of the ball.",
               "Follow through towards the target and check the result."],
     "cues": ["Head up before and after the touch", "Lock the ankle", "Pass to the foot away from pressure"],
     "mistakes": ["Planting too far from the ball", "Floppy ankle", "Looking only at the ball"],
     "progress": "Add a defender passively pressing, then one-touch return passes.",
     "simplify": "Shorten the distance to 5 m and use a stationary ball.",
     "frames": frames([
         ("1 Setup", "Scan and pick the target.", P(80, 120) + B(110, 120) + MATE(290, 120)),
         ("2 Approach", "Approach at a slight angle, eyes on ball then target.",
          P(70, 150) + B(110, 120) + A(85, 143, 100, 128) + MATE(290, 120)),
         ("3 Contact", "Plant foot beside ball; strike centre with the inside of the foot.",
          P(105, 135) + B(122, 120) + A(135, 120, 270, 120) + MATE(290, 120) + N(60, 175, "Plant foot")),
         ("4 Follow-through", "Kicking foot swings through towards the target.",
          P(130, 122) + B(190, 120) + A(200, 120, 270, 120) + MATE(290, 120)),
         ("5 Result", "Ball arrives at the teammate's feet with pace they can control.",
          P(140, 122) + B(275, 120) + MATE(290, 120) + N(250, 160, "Weighted pass")),
     ])},
    {"id": "first-touch", "title": "First touch: receive and turn away from pressure", "category": "Ball control",
     "positions": ["all"], "purpose": "Control the ball into space so your next action is already on.",
     "setup": "Server passes to you; a passive defender stands behind you. Receive and exit through a cone gate.",
     "steps": ["Check your shoulder.", "Show for the ball side-on.", "Cushion with the foot away from pressure.",
               "Take the touch into space.", "Play your next action."],
     "cues": ["Open your body", "Soft contact, direct it", "Look before the ball arrives"],
     "mistakes": ["Receiving square-on", "Stopping the ball dead", "Touch towards the defender"],
     "progress": "Active defender and a time limit of 3 seconds.",
     "simplify": "No defender, slower pass.",
     "frames": frames([
         ("1 Scan", "Check shoulder to see pressure.", P(180, 120) + P(215, 150, "Def", "#dc2626") + MATE(60, 120)),
         ("2 Show", "Side-on body, ready for the ball.", P(180, 120) + B(110, 120) + A(90, 120, 150, 120) + MATE(60, 120)),
         ("3 Cushion", "Withdraw the foot on contact to absorb pace.", P(180, 120) + B(165, 122)),
         ("4 Direction", "Touch away from the defender into space.",
          P(180, 120) + B(200, 85) + A(190, 112, 205, 90) + P(215, 150, "Def", "#dc2626")),
         ("5 Next action", "Pass, dribble or shoot with your head up.", P(205, 85) + B(225, 78) + A(235, 75, 320, 60)),
     ])},
]

# Stick-figure exercise diagram
def _bridge(top):
    hip_y = 140 if top else 170
    return ('<polyline points="60,170 130,%d 170,%d 200,170" fill="none" stroke="#fff" stroke-width="5"/>' % (hip_y, 130 if not top else 120)
            + f'<circle cx="48" cy="168" r="9" fill="#fff"/>')


EXERCISES = [
    {"id": "glute-bridge", "title": "Glute bridge", "category": "Glutes / hamstrings", "positions": ["all"],
     "purpose": "Strengthen glutes and hamstrings used in sprinting and kicking.",
     "equipment": "Mat (optional)",
     "setup": "Lie on your back, knees bent, feet flat hip-width apart.",
     "steps": ["Brace your core.", "Press through heels and lift hips.", "Hold 2 seconds at the top.", "Lower under control."],
     "dose": "3 sets of 10-12 reps, rest 60 seconds", "cues": ["Ribs down", "Squeeze glutes, not lower back"],
     "mistakes": ["Arching the lower back", "Pushing through toes"],
     "progress": "Single-leg bridge or add a light weight.", "simplify": "Fewer reps, no hold.",
     "frames": [("1 Start", "Hips down, feet flat.", svg(_bridge(False), "1 Start")),
                ("2 Lift", "Drive hips up.", svg(_bridge(True), "2 Lift")),
                ("3 Hold", "Straight line shoulders to knees; squeeze.", svg(_bridge(True), "3 Hold")),
                ("4 Lower", "Return slowly.", svg(_bridge(False), "4 Lower"))]},
    {"id": "plank", "title": "Front plank", "category": "Core", "positions": ["all"],
     "purpose": "Build trunk stability for balance and duels.", "equipment": "Mat",
     "setup": "Forearms on the floor, elbows under shoulders, legs extended.",
     "steps": ["Tuck pelvis slightly.", "Keep body in a straight line.", "Breathe steadily.", "Rest after the time is up."],
     "dose": "3 x 20-40 seconds, rest 45 seconds", "cues": ["Glutes tight", "Neck neutral"],
     "mistakes": ["Hips sagging or piking"], "progress": "Add shoulder taps.", "simplify": "Knees down.",
     "frames": [("1 Setup", "Forearms down.", svg('<polyline points="60,150 120,170 250,170" fill="none" stroke="#fff" stroke-width="5"/>', "1 Setup")),
                ("2 Lift", "Lift knees.", svg('<polyline points="60,140 120,160 250,140" fill="none" stroke="#fff" stroke-width="5"/>', "2 Lift")),
                ("3 Hold", "Straight line.", svg('<polyline points="60,150 250,125" fill="none" stroke="#fff" stroke-width="5"/>', "3 Hold")),
                ("4 Breathe", "Keep breathing.", svg('<polyline points="60,150 250,125" fill="none" stroke="#fff" stroke-width="5"/>', "4 Breathe")),
                ("5 Finish", "Lower under control.", svg('<polyline points="60,160 250,170" fill="none" stroke="#fff" stroke-width="5"/>', "5 Finish"))]},
]

WARMUP = ["Jog and dynamic leg swings", "Lunge with rotation", "Skips and high knees", "Short accelerations"]
COOLDOWN = ["Easy walk", "Gentle calf, hamstring and hip flexor stretches", "Hydrate and refuel"]

BASICS = [
    {"title": "Offside", "text": "A player is in an offside position if any scoring part of their head, body or feet is nearer the opponents' goal line than both the ball and the second-last opponent. It is only an offence if they become involved in active play. There is no offside from a goal kick, throw-in or corner.",
     "ref": "https://www.theifab.com"},
    {"title": "Throw-in", "text": "Awarded when the whole ball crosses the touchline. Thrown with both hands from behind and over the head, with part of each foot on the line or ground outside it. You cannot score directly.",
     "ref": "https://www.theifab.com"},
    {"title": "Corners and goal kicks", "text": "If the attackers last touch the ball before it crosses the goal line outside the goal, it is a goal kick. If a defender touches it last, it is a corner kick.",
     "ref": "https://www.theifab.com"},
    {"title": "Fouls, free kicks and cards", "text": "Careless, reckless or excessive-force challenges are fouls. A yellow card is a caution; a red card is a sending-off. Direct and indirect free kicks differ in whether a goal can be scored without another touch.",
     "ref": "https://www.theifab.com"},
]

POSITIONS = [
    {"name": "Goalkeeper", "term": "Number 1; last line of defence.", "in": "Distribute, offer a passing option.", "out": "Shot-stop, command the box, organise the line.", "skills": "Handling, positioning, kicking", "priorities": "Footwork, communication"},
    {"name": "Centre-back", "term": "Part of the 'backs'.", "in": "Start build-up, split or step out with the ball.", "out": "Defend the box, win aerial duels, hold the line.", "skills": "Heading, tackling, passing range", "priorities": "Marking, anticipation, long passing"},
    {"name": "Full-back", "term": "Wide 'back'.", "in": "Overlap or underlap, cross.", "out": "Defend the flank, stop crosses.", "skills": "Pace, crossing, 1v1 defending", "priorities": "Endurance, recovery runs"},
    {"name": "Central midfielder", "term": "'Half' / halfback in older terms.", "in": "Link defence and attack, switch play.", "out": "Screen, press, cover.", "skills": "Scanning, passing, first touch", "priorities": "Turning, receiving under pressure"},
    {"name": "Winger", "term": "Wide forward, older 'outside-right/left'.", "in": "Beat full-backs, deliver crosses, cut inside.", "out": "Press, track back.", "skills": "Dribbling, pace, crossing", "priorities": "1v1, acceleration"},
    {"name": "Centre-forward", "term": "Striker.", "in": "Finish, hold the ball up, run in behind.", "out": "Lead the press.", "skills": "Finishing, movement", "priorities": "Shooting technique, timing of runs"},
]

NUMBERS = ("Common traditions, not rules: 1 goalkeeper; 2 and 3 full-backs (right/left); 4 and 5 centre-backs or defensive midfielders; "
           "6 defensive or central midfielder; 7 right winger; 8 box-to-box midfielder; 9 centre-forward; 10 playmaker or second striker; 11 left winger. "
           "Conventions vary by country, era, club and formation (for example Argentina and Brazil have different habits), and modern squads use fixed numbers, so a number never guarantees a position.")

# Formation points are (x, y) on a 360x220 pitch, attacking to the right.
D4 = [(85, 40), (85, 85), (85, 135), (85, 180)]
FORMATIONS = {
    "4-4-2": {"pts": [(30, 110)] + D4 + [(160, 40), (160, 85), (160, 135), (160, 180), (250, 85), (250, 135)],
              "text": "Two banks of four plus two strikers. Strengths: simple, compact, easy to organise. Weaknesses: can be outnumbered in central midfield. Build-up: wide midfielders and full-backs. Pressing: strikers lead, midfield steps up. Adjustment: drop a striker into midfield."},
    "4-3-3": {"pts": [(30, 110)] + D4 + [(160, 60), (160, 110), (160, 160), (250, 45), (250, 110), (250, 175)],
              "text": "One holding midfielder, two eights, and three forwards. Strengths: width and midfield triangles. Weaknesses: space behind full-backs. Press: front three cut passing lanes. Adjustment: invert wingers."},
    "3-5-2": {"pts": [(30, 110), (85, 65), (85, 110), (85, 155), (160, 35), (160, 185), (160, 70), (160, 110), (160, 150), (250, 85), (250, 135)],
              "text": "Three centre-backs and wing-backs. Strengths: central numbers, two strikers. Weaknesses: wide spaces if wing-backs are caught high. Adjustment: wing-backs drop to make a back five."},
    "4-2-3-1": {"pts": [(30, 110)] + D4 + [(135, 80), (135, 140), (200, 45), (200, 110), (200, 175), (270, 110)],
                "text": "Two holders behind a creative line of three and a lone striker. Strengths: balance, a clear number ten. Weaknesses: striker can be isolated. Adjustment: advance one holder."},
}
FORMATION_NOTE = "A formation is a starting shape. Players move and the shape changes in and out of possession."

STYLES = {"Possession play": "Keep the ball to control tempo.", "Counterattacking": "Win the ball, attack quickly into space.",
          "High pressing": "Win the ball high up the pitch.", "Low block": "Defend deep and compact.",
          "Direct play": "Play forward quickly, often long.", "Wing overloads": "Outnumber opponents on one flank."}

SOURCES = {"Laws of the Game (IFAB)": "https://www.theifab.com"}
HEALTH_NOTE = ("General training information only. Not medical advice. Stop if an exercise causes pain. "
               "Injury rehabilitation should be guided by a qualified clinician. Injury-prevention programmes such as FIFA 11+ "
               "are published by FIFA; check their official site for details.")


LESSONS.append({"id": "shoot-instep", "title": "Instep shooting: the power drive", "category": "Shooting",
    "positions": ["Centre-forward", "Winger", "Central midfielder"],
    "purpose": "Strike the ball hard and on target using the laces (instep), the standard technique for power shots.",
    "setup": "Place balls at the edge of the box facing a goal. Place a cone 2 m from each post as accuracy targets. Take 5 shots to each side.",
    "steps": ["Pick your target before the ball arrives.", "Approach at a slight angle, last stride longer.",
              "Plant the standing foot beside the ball, toes at the target.",
              "Lock the ankle and strike the middle of the ball with the laces, head steady over it.",
              "Swing through and land on the kicking foot."],
    "cues": ["Head down and still at contact", "Lock the ankle, toes pointed down", "Knee over the ball keeps the shot low"],
    "mistakes": ["Leaning back, which sends the ball over the bar", "Standing foot too far behind the ball", "Floppy ankle"],
    "progress": "Add a passive defender, a one-touch finish from a pass, then a time limit of 3 seconds.",
    "simplify": "Strike a stationary ball from 10 m with no run-up.",
    "frames": sframes([
        ("1 Setup", "Square up, eyes on the target.", fig(Z((70,55),(72,80),(70,130),(60,105),(55,128),(82,105),(88,125),(66,168),(64,200),(76,168),(78,200))) + B(150,198) + A(165,190,310,175), True),
        ("2 Approach", "Lean forward, longer final stride.", fig(Z((85,58),(85,82),(78,130),(68,100),(55,118),(100,98),(118,112),(62,165),(40,195),(100,160),(112,200))) + B(175,198), True),
        ("3 Plant", "Standing foot beside the ball; kicking leg swings back.", fig(Z((100,56),(98,80),(92,130),(80,98),(60,92),(115,98),(135,105),(84,165),(52,175),(100,168),(112,200))) + B(145,198) + N(90,224, "Plant foot"), True),
        ("4 Contact", "Laces through the middle of the ball, head steady.", fig(Z((118,56),(114,80),(110,128),(96,100),(80,90),(128,98),(146,108),(124,168),(128,200),(140,160),(152,196))) + B(165,196) + A(175,190,310,170) + N(130,224, "Laces on ball"), True),
        ("5 Follow-through", "Leg swings through; ball travels to the target.", fig(Z((132,58),(126,80),(120,128),(106,98),(90,110),(144,100),(158,112),(118,168),(118,200),(160,140),(190,128))) + B(262,150) + A(272,146,312,160), True),
    ])})

_bridge_top = Z((38,186),(62,184),(128,150),(85,195),(108,197),(85,195),(108,197),(170,146),(192,198),(174,148),(196,198))
_bridge_low = Z((38,186),(62,190),(128,190),(85,195),(108,197),(85,195),(108,197),(168,150),(192,198),(172,152),(196,198))
EXERCISES[0]["frames"] = sframes([
    ("1 Start", "Back flat, knees bent, feet flat.", fig(_bridge_low), False),
    ("2 Lift", "Press through the heels, lift hips.", fig(_bridge_top) + A(128,185,128,160), False),
    ("3 Hold", "Straight line from shoulders to knees; squeeze.", fig(_bridge_top) + N(95,225, "Hold 2 seconds"), False),
    ("4 Lower", "Lower slowly under control.", fig(_bridge_low) + A(128,160,128,185), False)])
_pk = Z((246,150),(222,166),(140,176),(214,198),(242,198),(214,198),(242,198),(100,186),(62,198),(104,186),(66,198))
_pk2 = Z((246,150),(222,166),(140,176),(214,198),(242,198),(214,198),(242,198),(180,190),(150,198),(184,190),(154,198))
EXERCISES[1]["frames"] = sframes([
    ("1 Setup", "Forearms down, elbows under shoulders.", fig(_pk2), False),
    ("2 Lift", "Lift the knees off the floor.", fig(_pk), False),
    ("3 Hold", "Straight line head to heels; breathe.", fig(_pk) + N(110,225, "No sagging hips"), False)])


# ---------- Basics diagrams ----------
def _off(att, passer, ball, tgt, tag, tx):
    line = '<line x1="250" y1="40" x2="250" y2="200" stroke="#fde047" stroke-width="2" stroke-dasharray="5 4"/>'
    d = P(250, 70, "D", "#dc2626") + P(250, 150, "D", "#dc2626") + P(335, 110, "GK", "#dc2626")
    return (line + d + P(att[0], att[1], "A") + P(passer[0], passer[1], "P", "#2563eb") + B(*ball)
            + A(ball[0] + 8, ball[1] - 2, tgt[0], tgt[1]) + N(tx, 196, tag) + N(200, 36, "Second-last defender line"))


_od = [("Offside: the attacker is nearer the goal line than the ball and the second-last defender when the pass is played.",
        svg(_off((290, 110), (140, 150), (156, 150), (278, 116), "OFFSIDE", 20), "Offside")),
       ("Onside: level with the second-last defender is not offside.",
        svg(_off((250, 110), (140, 150), (156, 150), (240, 116), "ONSIDE (level)", 20), "Onside, level")),
       ("Onside: beyond the defenders but behind the ball. Teammates ahead of the ball are only offside if they are past it.",
        svg(_off((272, 110), (298, 175), (310, 168), (282, 120), "ONSIDE (behind the ball)", 20), "Onside, behind ball"))]
_ti = svg(P(180, 24, "Thrower") + B(180, 8) + A(188, 38, 232, 108) + P(238, 122, "Mate", "#f97316")
          + N(20, 208, "Both feet on or behind the line"), "Throw-in")
for _b in BASICS:
    if _b["title"] == "Offside":
        _b["diagrams"] = _od
    if _b["title"] == "Throw-in":
        _b["diagrams"] = [("Ball over the head, both hands, both feet on the ground.", _ti)]

# ---------- Exercise graphics ----------
def gscene(inner, label, hl=()):
    glow = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#f97316" opacity=".5"/>' for x, y, rx, ry in hl)
    return (f'<svg viewBox="0 0 360 240" role="img" aria-label="{label}" style="width:100%;border-radius:10px">{ARROW}'
            f'<rect width="360" height="240" fill="#1e293b"/><rect y="205" width="360" height="35" fill="#334155"/>{glow}{inner}'
            f'<rect x="10" y="10" width="190" height="26" rx="6" fill="#000" opacity=".55"/>'
            f'<text x="18" y="28" fill="#fff" font-size="14" font-weight="700">{label}</text>'
            f'<text x="350" y="228" fill="#fdba74" font-size="11" text-anchor="end">Orange glow = working muscles</text></svg>')


def gframes(items):
    return [(lab, cap, gscene(inner, lab, hl)) for lab, cap, inner, hl in items]


STAND = Z((150,48),(150,74),(150,126),(140,100),(138,126),(160,100),(162,126),(147,166),(146,200),(153,166),(154,200))
SQ = Z((165,72),(155,98),(125,150),(180,98),(205,96),(182,100),(206,98),(178,152),(165,200),(180,152),(168,200))
LU = Z((152,74),(152,100),(150,150),(135,105),(148,126),(165,105),(153,126),(120,182),(95,197),(185,150),(180,200))
CR = Z((150,36),(150,62),(150,114),(140,88),(138,114),(160,88),(162,114),(147,154),(146,190),(153,154),(154,190))
PU1 = Z((246,140),(222,152),(140,172),(221,176),(220,200),(221,176),(220,200),(100,186),(62,198),(104,186),(66,198))
PU2 = Z((250,176),(226,184),(140,190),(196,196),(222,200),(196,196),(222,200),(100,194),(62,199),(104,194),(66,199))
SL = Z((150,48),(150,74),(150,126),(130,92),(110,98),(170,92),(190,98),(138,160),(118,178),(152,166),(153,200))
_ex = lambda i, t, cat, pur, eq, setup, steps, dose, cues, mist, prog, simp, fr: {
    "id": i, "title": t, "category": cat, "positions": ["all"], "purpose": pur, "equipment": eq, "setup": setup,
    "steps": steps, "dose": dose, "cues": cues, "mistakes": mist, "progress": prog, "simplify": simp, "frames": fr}
EXERCISES[0]["frames"] = gframes([
    ("1 Start", "Back flat, knees bent, feet flat.", fig(_bridge_low), []),
    ("2 Lift", "Press through the heels, lift hips.", fig(_bridge_top) + A(128,185,128,158), [(128,160,35,18)]),
    ("3 Hold", "Straight line shoulders to knees; squeeze.", fig(_bridge_top) + N(95,226,"Hold 2 seconds"), [(128,160,35,18)]),
    ("4 Lower", "Lower slowly under control.", fig(_bridge_low) + A(128,158,128,185), [])])
EXERCISES[1]["frames"] = gframes([
    ("1 Setup", "Forearms down, knees on the floor.", fig(_pk2), []),
    ("2 Lift", "Lift the knees off the floor.", fig(_pk), [(180,176,50,16)]),
    ("3 Hold", "Straight line head to heels; breathe.", fig(_pk) + N(110,226,"No sagging hips"), [(180,176,50,16)])])
EXERCISES += [
    _ex("squat", "Bodyweight squat", "Legs", "Build leg strength for jumping, sprinting and shielding.", "None",
        "Feet shoulder-width, toes slightly out.", ["Brace your core.", "Sit hips back and down.", "Thighs parallel to the floor, knees over toes.", "Drive through the feet to stand."],
        "3 x 10-12, rest 60 s", ["Chest up", "Knees track over toes"], ["Knees caving in", "Heels lifting"],
        "Jump squat or single-leg box squat.", "Squat to a chair.",
        gframes([("1 Start", "Stand tall, arms forward.", fig(STAND), []), ("2 Bottom", "Hips back, thighs parallel.", fig(SQ) + A(150,70,150,110), [(150,150,38,20)]),
                 ("3 Stand", "Drive up through the whole foot.", fig(STAND) + A(150,120,150,70), [(150,150,30,24)])])),
    _ex("reverse-lunge", "Reverse lunge", "Glutes / legs", "Train single-leg strength and balance used in every stride.", "None",
        "Stand tall, hands on hips.", ["Step one foot back.", "Lower until both knees are about 90 degrees.", "Push through the front heel to return.", "Alternate legs."],
        "3 x 8 per leg, rest 60 s", ["Torso upright", "Front knee over ankle"], ["Short step", "Front heel lifting"],
        "Hold dumbbells.", "Hold a wall for balance.",
        gframes([("1 Start", "Feet together, tall posture.", fig(STAND), []), ("2 Step back", "Back knee drops towards floor.", fig(LU) + A(140,120,100,170), [(150,160,40,24)]),
                 ("3 Return", "Push through the front heel.", fig(STAND) + A(150,120,150,70), [(150,160,30,24)])])),
    _ex("calf-raise", "Calf raise", "Calves", "Strengthen calves for push-off and ankle stability.", "A step (optional)",
        "Stand with feet hip-width.", ["Rise onto the balls of the feet.", "Pause 1 second at the top.", "Lower slowly."],
        "3 x 15, rest 45 s", ["Straight knees", "Slow lowering"], ["Bouncing", "Rolling the ankles outward"],
        "Single-leg raise.", "Hold a wall.",
        gframes([("1 Start", "Flat feet, tall.", fig(STAND), []), ("2 Rise", "Up onto the toes.", fig(CR) + A(150,120,150,80), [(147,172,10,22)]),
                 ("3 Lower", "Control the descent.", fig(STAND) + A(150,80,150,120), [(147,175,10,22)])])),
    _ex("push-up", "Push-up", "Upper body", "Upper-body strength for shielding and duels.", "Mat",
        "Hands under shoulders, body in a straight line.", ["Brace core and glutes.", "Lower the chest to a fist above the floor.", "Press back up to straight arms."],
        "3 x 8-12, rest 60 s", ["Elbows about 45 degrees", "Straight line head to heels"], ["Hips sagging", "Flaring the elbows"],
        "Feet raised.", "Hands on a bench or knees down.",
        gframes([("1 Start", "High plank.", fig(PU1), [(215,170,22,22)]), ("2 Lower", "Chest towards the floor.", fig(PU2) + A(230,160,230,185), [(215,186,22,16)]),
                 ("3 Press", "Straight arms again.", fig(PU1) + A(230,185,230,160), [(215,170,22,22)])])),
    _ex("single-leg-balance", "Single-leg balance", "Balance", "Improve ankle and hip control for turning and landing.", "None",
        "Stand on one leg, arms out for balance.", ["Lift one foot behind you.", "Keep hips level.", "Hold, then switch legs."],
        "3 x 30 s per leg, rest 30 s", ["Eyes on a fixed point", "Soft knee"], ["Hips dropping", "Holding your breath"],
        "Close your eyes or stand on a cushion.", "Lightly touch a wall.",
        gframes([("1 Setup", "Feet together, arms out.", fig(STAND), []), ("2 Lift", "Lift one foot behind.", fig(SL), [(153,175,12,28)]),
                 ("3 Hold", "Keep still and level.", fig(SL) + N(100,226,"Hold 30 seconds"), [(153,175,12,28)])])),
]
