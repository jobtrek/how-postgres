#!/usr/bin/env python3
"""Generate data.sql for the equipment-loans dataset.

Deterministic: the same seed always writes the same file. Standard library only.

    python3 datasets/equipment-loans/generate.py > datasets/equipment-loans/data.sql

The data simulates the IT team of Brevia SA lending equipment from January 2021 to the
reference date. Every row satisfies the constraints of schema.sql.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta

SEED = 20260930
START = date(2021, 1, 4)
REF = date(2026, 9, 30)  # "today" in the dataset
FAR = date(9999, 12, 31)
DOMAIN = "brevia.example"

rng = random.Random(SEED)

# --------------------------------------------------------------------------- reference data

FIRST_NAMES = """Adrien Alice Amélie Anaïs Antoine Arnaud Aurélie Baptiste Camille Céline Chloé Clara
Damien David Diane Dylan Élodie Emma Enzo Éric Fabien Fanny Florian Gaëlle Hugo Inès Jade Jérôme
Joël Julie Julien Karim Kevin Laura Léa Leila Liam Lina Loïc Lucas Luca Manon Marc Marie Mathieu
Maxime Mélanie Nadia Nathan Noah Noémie Océane Olivier Pauline Pierre Rafael Romain Sarah Sofia
Steve Théo Thomas Valentin Yann Yasmine Zoé Ana Bruno Elif Goran Ivana Mehmet Nuno Sanja Tiago""".split()

LAST_NAMES = """Aebischer Bachmann Baumann Berset Blanc Bonvin Bovet Brunner Chappuis Chevalley Clerc
Cuendet Da Silva Delacrétaz Dubois Ducret Dumas Favre Ferreira Fontana Gay Gerber Girard Gonzalez
Graf Guex Haldimann Henchoz Jaquier Jordan Keller Kohler Krasniqi Lambert Lehmann Lopes Maillard
Marti Martin Mercier Meyer Monnier Morel Moser Müller Nicolet Oliveira Pasche Perrin Pereira Python
Rey Richard Rochat Rossi Roulin Sauter Schmid Schneider Vonlanthen Steiner Studer Tissot Vaucher
Vuilleumier Weber Wenger Zbinden Zufferey Berisha Hoxha Yilmaz Rodrigues Santos Russo Bianchi""".split()

DEPARTMENTS = [
    "Management", "Finance", "Human Resources", "Sales", "Marketing",
    "Customer Support", "IT", "Logistics",
]

# department -> (head title, [(title, weight)], apprentice title or None)
TITLES = {
    "Management": ("Head of operations", [("Executive assistant", 2), ("Project manager", 2)], None),
    "Finance": ("Head of finance", [("Accountant", 4), ("Payroll specialist", 2)], "Commercial apprentice"),
    "Human Resources": ("Head of HR", [("HR specialist", 3), ("Recruiter", 2)], "Commercial apprentice"),
    "Sales": ("Head of sales", [("Account manager", 4), ("Sales representative", 5)], "Commercial apprentice"),
    "Marketing": ("Head of marketing", [("Marketing specialist", 3), ("Graphic designer", 2), ("Content creator", 2)], None),
    "Customer Support": ("Head of support", [("Support agent", 8)], None),
    "IT": ("IT manager", [("System administrator", 2), ("IT technician", 3), ("Software developer", 5)], "ICT apprentice"),
    "Logistics": ("Head of logistics", [("Warehouse clerk", 5), ("Delivery driver", 4)], "Logistics apprentice"),
}
DEPT_SIZE = {
    "Management": 5, "Finance": 12, "Human Resources": 8, "Sales": 26, "Marketing": 12,
    "Customer Support": 22, "IT": 24, "Logistics": 20,
}
IT_STAFF = {"IT manager", "System administrator", "IT technician"}

BRANDS = ["Lenovo", "Dell", "HP", "Apple", "Logitech", "Jabra", "Samsung", "Fairphone", "Eizo", "Epson"]
CATEGORIES = ["laptop", "screen", "docking station", "headset", "keyboard", "mouse", "phone", "tablet", "projector"]

# (brand, category, name, first year sold, last year sold, price low, price high)
MODELS = [
    ("Lenovo", "laptop", "ThinkPad T14 Gen 1", 2019, 2021, 1250, 1450),
    ("Lenovo", "laptop", "ThinkPad T14 Gen 3", 2022, 2023, 1300, 1500),
    ("Lenovo", "laptop", "ThinkPad T14 Gen 5", 2024, 2026, 1350, 1600),
    ("Dell", "laptop", "Latitude 5410", 2019, 2021, 1100, 1300),
    ("Dell", "laptop", "Latitude 5440", 2023, 2026, 1150, 1400),
    ("Apple", "laptop", "MacBook Pro 14 M1", 2021, 2022, 2100, 2400),
    ("Apple", "laptop", "MacBook Pro 14 M3", 2023, 2026, 2200, 2600),
    ("HP", "laptop", "EliteBook 840 G7", 2019, 2022, 1200, 1400),
    ("Dell", "screen", "P2422H", 2019, 2023, 210, 260),
    ("Dell", "screen", "P2725H", 2024, 2026, 230, 280),
    ("Eizo", "screen", "FlexScan EV2795", 2020, 2026, 820, 900),
    ("Samsung", "screen", "ViewFinity S6", 2022, 2026, 290, 340),
    ("Lenovo", "docking station", "ThinkPad USB-C Dock Gen 2", 2019, 2026, 220, 260),
    ("Dell", "docking station", "WD19S", 2019, 2026, 190, 230),
    ("Jabra", "headset", "Evolve2 40", 2020, 2026, 110, 140),
    ("Jabra", "headset", "Evolve2 65", 2021, 2026, 190, 230),
    ("Logitech", "headset", "Zone Wired", 2019, 2023, 90, 110),
    ("Logitech", "keyboard", "MX Keys", 2019, 2026, 100, 120),
    ("Logitech", "keyboard", "K120", 2019, 2026, 15, 20),
    ("Logitech", "mouse", "MX Master 3S", 2022, 2026, 95, 110),
    ("Logitech", "mouse", "M185", 2019, 2026, 15, 20),
    ("Apple", "phone", "iPhone 12", 2020, 2022, 750, 850),
    ("Apple", "phone", "iPhone 15", 2023, 2026, 800, 900),
    ("Samsung", "phone", "Galaxy A52", 2020, 2022, 330, 380),
    ("Samsung", "phone", "Galaxy A55", 2023, 2026, 380, 430),
    ("Fairphone", "phone", "Fairphone 5", 2023, 2026, 600, 650),
    ("Apple", "tablet", "iPad 10th gen", 2022, 2026, 480, 550),
    ("Samsung", "tablet", "Galaxy Tab S6 Lite", 2020, 2026, 330, 380),
    ("Epson", "projector", "EB-W49", 2019, 2026, 650, 720),
]

REPAIR_TEXT = {
    "laptop": ["Screen cracked", "Battery does not hold charge", "Keyboard keys stuck after a spill",
               "Does not boot", "Hinge broken", "Fan very loud", "Charging port loose"],
    "screen": ["Dead pixels", "No signal on any input", "Stand broken"],
    "docking station": ["Ethernet port dead", "No video output"],
    "headset": ["Microphone not working", "Headband broken", "Left speaker silent"],
    "keyboard": ["Several keys not responding"],
    "mouse": ["Scroll wheel broken"],
    "phone": ["Screen cracked", "Battery swollen", "Does not charge", "Camera blurry"],
    "tablet": ["Screen cracked", "Does not charge"],
    "projector": ["Lamp burnt out", "Image blurry, lens damaged"],
}
REPAIR_COST = {
    "laptop": (90, 650), "screen": (60, 280), "docking station": (40, 120), "headset": (30, 90),
    "keyboard": (15, 40), "mouse": (10, 30), "phone": (80, 260), "tablet": (90, 220), "projector": (120, 320),
}

# --------------------------------------------------------------------------- model


@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
    email: str
    job_title: str
    department_id: int
    supervisor_id: int | None
    hired_on: date
    left_on: date | None

    def active(self, day: date) -> bool:
        return self.hired_on <= day and (self.left_on is None or self.left_on > day)


@dataclass
class Device:
    id: int
    tag: str
    serial: str
    model_id: int
    category: str
    purchased_on: date
    price: float
    busy_until: date = date.min  # last day it is unavailable
    retired_on: date | None = None
    open_repair: bool = False


@dataclass
class LoanItem:
    loan_id: int
    device_id: int
    condition_out: str
    returned_on: date | None = None
    condition_in: str | None = None


@dataclass
class Loan:
    id: int
    borrower_id: int
    handed_out_by_id: int
    loaned_on: date
    due_on: date | None
    note: str | None
    items: list[LoanItem] = field(default_factory=list)


@dataclass
class Repair:
    id: int
    device_id: int
    reported_by_id: int | None
    reported_on: date
    description: str
    closed_on: date | None
    cost: float | None


def rand_date(lo: date, hi: date) -> date:
    return lo + timedelta(days=rng.randint(0, max(0, (hi - lo).days)))


def weekday_on_or_after(d: date) -> date:
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


# --------------------------------------------------------------------------- employees

employees: list[Employee] = []
used_emails: set[str] = set()


def ascii_slug(s: str) -> str:
    table = str.maketrans("àâäáãçéèêëíîïñóôöõúùûüÿ", "aaaaaceeeeiiinoooouuuuy")
    return "".join(c for c in s.lower().translate(table) if c.isalnum())


def new_employee(title: str, dept_id: int, supervisor: int | None, hired: date, left: date | None) -> Employee:
    while True:
        first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
        base = f"{ascii_slug(first)}.{ascii_slug(last)}"
        email = f"{base}@{DOMAIN}"
        n = 2
        while email in used_emails:
            email = f"{base}{n}@{DOMAIN}"
            n += 1
        break
    used_emails.add(email)
    e = Employee(len(employees) + 1, first, last, email, title, dept_id, supervisor, hired, left)
    employees.append(e)
    return e


def maybe_left(hired: date, rate: float) -> date | None:
    if rng.random() < rate:
        lo = max(hired + timedelta(days=200), START)
        if lo < REF:
            return weekday_on_or_after(rand_date(lo, REF - timedelta(days=10)))
    return None


ceo = new_employee("Chief executive officer", 1, None, date(2009, 3, 2), None)
dept_heads: dict[int, Employee] = {}
for dept_id, dept in enumerate(DEPARTMENTS, start=1):
    head_title, titles, apprentice_title = TITLES[dept]
    head = new_employee(head_title, dept_id, ceo.id, rand_date(date(2010, 1, 1), date(2019, 6, 1)), None)
    dept_heads[dept_id] = head
    trainer = None
    if dept == "IT":
        trainer = new_employee("ICT trainer", dept_id, head.id, date(2016, 8, 1), None)
    # current and former staff
    for _ in range(DEPT_SIZE[dept]):
        title = rng.choices([t for t, _ in titles], [w for _, w in titles])[0]
        hired = weekday_on_or_after(rand_date(date(2011, 1, 1), REF - timedelta(days=20)))
        new_employee(title, dept_id, head.id, hired, maybe_left(hired, 0.22))
    # apprentices: one or two start every August, three or four years long
    if apprentice_title:
        years = 4 if apprentice_title == "ICT apprentice" else 3
        for year in range(2018, 2027):
            for _ in range(2 if dept == "IT" else rng.choice([0, 1, 1])):
                hired = date(year, 8, 1)
                end = date(year + years, 7, 31)
                left = end if end <= REF else None
                if left is None and rng.random() < 0.08:  # broke off the apprenticeship
                    left = weekday_on_or_after(rand_date(hired + timedelta(days=90), REF - timedelta(days=10)))
                sup = trainer.id if trainer else head.id
                new_employee(apprentice_title, dept_id, sup, hired, left)

by_id = {e.id: e for e in employees}

# user accounts: everyone except warehouse clerks and drivers; three leavers were never disabled
accounts: list[tuple[int, str, date, date | None]] = []
used_usernames: set[str] = set()
leavers = [e for e in employees if e.left_on]
forgotten_accounts = {e.id for e in rng.sample(leavers, 3)}
for e in employees:
    if e.job_title in ("Warehouse clerk", "Delivery driver"):
        continue
    base = (ascii_slug(e.first_name)[0] + ascii_slug(e.last_name))[:16]
    username, n = base, 2
    while username in used_usernames:
        username, n = f"{base}{n}", n + 1
    used_usernames.add(username)
    disabled = None if e.id in forgotten_accounts else e.left_on
    accounts.append((e.id, username, e.hired_on, disabled))

# --------------------------------------------------------------------------- devices

brand_id = {b: i for i, b in enumerate(BRANDS, start=1)}
category_id = {c: i for i, c in enumerate(CATEGORIES, start=1)}
models = [(i, *m) for i, m in enumerate(MODELS, start=1)]
devices: list[Device] = []
used_serials: set[str] = set()


def buy(category: str, day: date) -> Device:
    purchased = day - timedelta(days=rng.randint(2, 25))
    if day == START:  # stock bought before the database existed
        purchased = rand_date(date(2017, 6, 1), date(2020, 12, 15))
    year = min(purchased.year, 2026)
    choices = [m for m in models if m[2] == category and m[4] <= year <= m[5]]
    if not choices:  # before the oldest model of the list: take the oldest one
        choices = [min((m for m in models if m[2] == category), key=lambda m: m[4])]
    mid, brand, _, _, _, _, lo, hi = rng.choice(choices)
    while True:
        serial = brand[:2].upper() + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(10))
        if serial not in used_serials:
            used_serials.add(serial)
            break
    d = Device(len(devices) + 1, f"BRV-{len(devices) + 1:05d}", serial, mid, category,
               purchased, round(rng.uniform(lo, hi), 2))
    devices.append(d)
    return d


def free(d: Device, day: date) -> bool:
    return d.retired_on is None and not d.open_repair and d.busy_until < day and d.purchased_on <= day


def acquire(category: str, day: date, prefer_new: bool = False) -> Device:
    pool = [d for d in devices if d.category == category and free(d, day)]
    age_limit = 2 if prefer_new else 5
    pool = [d for d in pool if (day - d.purchased_on).days < age_limit * 365] or pool
    if pool and not (prefer_new and rng.random() < 0.6):
        return rng.choice(pool)
    return buy(category, day)


# --------------------------------------------------------------------------- loans and repairs

loans: list[Loan] = []
repairs: list[Repair] = []
open_items: dict[int, list[LoanItem]] = {}  # employee id -> long-term items still out
events: dict[date, list[tuple]] = {}
kept_after_leaving = {e.id for e in rng.sample([e for e in leavers if e.left_on and e.left_on > date(2023, 1, 1)
                                                and e.job_title not in ("Warehouse clerk",)], 4)}


def schedule(day: date, *event) -> None:
    if day <= REF:
        events.setdefault(day, []).append(event)


def it_staff(day: date, not_for: int | None = None) -> int:
    staff = [e for e in employees if e.job_title in IT_STAFF and e.active(day) and e.id != not_for]
    return rng.choice(staff).id


def kit_for(e: Employee) -> list[str]:
    t = e.job_title
    if t == "Warehouse clerk":
        return []  # shares the warehouse terminal
    if t == "Delivery driver":
        return ["phone"]
    kit = ["laptop"]
    if "apprentice" in t:
        return kit + ["headset"]
    kit.append("docking station")
    if rng.random() < 0.7:
        kit.append("screen")
    if t == "Support agent" or rng.random() < 0.5:
        kit.append("headset")
    if rng.random() < 0.35:
        kit += ["keyboard", "mouse"]
    if DEPARTMENTS[e.department_id - 1] in ("Sales", "Management") or t in IT_STAFF or t.startswith("Head"):
        kit.append("phone")
    return kit


def new_loan(borrower: Employee, day: date, due: date | None, note: str | None) -> Loan:
    loan = Loan(len(loans) + 1, borrower.id, it_staff(day, borrower.id), day, due, note)
    loans.append(loan)
    return loan


def hand_out(loan: Loan, d: Device, until: date) -> LoanItem:
    cond = "new" if (loan.loaned_on - d.purchased_on).days < 30 else rng.choice(["good", "good", "good", "worn"])
    item = LoanItem(loan.id, d.id, cond)
    loan.items.append(item)
    d.busy_until = until
    return item


def give_back(item: LoanItem, day: date, condition: str | None = None) -> None:
    d = devices[item.device_id - 1]
    item.returned_on = day
    item.condition_in = condition or rng.choice(["good", "good", "worn"])
    d.busy_until = day
    age = (day - d.purchased_on).days
    if item.condition_in != "damaged" and age > 5 * 365 and rng.random() < 0.7:
        d.retired_on = day


def start_repair(d: Device, day: date, reporter: int | None) -> None:
    lo, hi = REPAIR_COST[d.category]
    closed = day + timedelta(days=rng.randint(3, 35))
    cost: float | None = round(rng.uniform(lo, hi), 2)
    if closed > REF:
        closed, cost = None, None
    elif rng.random() < 0.1:
        cost = None  # repaired but never invoiced
    repairs.append(Repair(len(repairs) + 1, d.id, reporter, day, rng.choice(REPAIR_TEXT[d.category]), closed, cost))
    d.open_repair = True
    if closed:
        schedule(closed, "repaired", d.id)


def workstation(e: Employee, day: date, note: str) -> None:
    kit = kit_for(e)
    if not kit:
        return
    loan = new_loan(e, day, None, note)
    for category in kit:
        d = acquire(category, day, prefer_new=category in ("laptop", "phone"))
        item = hand_out(loan, d, FAR)
        open_items.setdefault(e.id, []).append(item)
        if category in ("laptop", "phone"):
            years = rng.uniform(3, 4.5)
            if rng.random() < 0.12 * years:  # breaks before the refresh
                schedule(weekday_on_or_after(day + timedelta(days=rng.randint(60, int(years * 365)))), "break", e.id, item)
            else:
                schedule(weekday_on_or_after(day + timedelta(days=int(years * 365))), "refresh", e.id, item)


def replace(e: Employee, item: LoanItem, day: date, note: str) -> None:
    if not e.active(day) or item not in open_items.get(e.id, []):
        return
    category = devices[item.device_id - 1].category
    loan = new_loan(e, day, None, note)
    d = acquire(category, day, prefer_new=True)
    new_item = hand_out(loan, d, FAR)
    open_items[e.id].remove(item)
    open_items[e.id].append(new_item)
    years = rng.uniform(3, 4.5)
    schedule(weekday_on_or_after(day + timedelta(days=int(years * 365))), "refresh", e.id, new_item)


SHORT_NOTES = ["Client presentation", "Trade fair", "Training day", "Visitor", "Temporary replacement",
               "Home office week", "Onboarding of an intern", None, None, None]
SHORT_WEIGHTS = {"projector": 3, "tablet": 2, "screen": 2, "headset": 2, "laptop": 2,
                 "phone": 1, "keyboard": 1, "mouse": 1}

# initial workstations for people already there on START
for e in employees:
    if e.active(START):
        workstation(e, START, "Workstation inventory (migrated from the spreadsheet)")
for e in employees:
    if e.hired_on > START:
        schedule(e.hired_on if e.hired_on.weekday() < 5 else weekday_on_or_after(e.hired_on), "hire", e.id)
    if e.left_on and e.left_on > START:
        schedule(e.left_on, "leave", e.id)

day = START
while day <= REF:
    for ev in events.get(day, []):
        kind = ev[0]
        if kind == "hire":
            workstation(by_id[ev[1]], day, "Workstation setup")
        elif kind == "leave":
            if ev[1] in kept_after_leaving:
                continue  # left the company with the equipment
            for item in open_items.pop(ev[1], []):
                give_back(item, day)
        elif kind == "refresh":
            e, item = by_id[ev[1]], ev[2]
            if e.active(day) and item in open_items.get(e.id, []):
                give_back(item, day, "worn")
                replace(e, item, day, "Device refresh")
        elif kind == "break":
            e, item = by_id[ev[1]], ev[2]
            if e.active(day) and item in open_items.get(e.id, []):
                give_back(item, day, "damaged")
                start_repair(devices[item.device_id - 1], day, e.id)
                replace(e, item, day, "Replacement after a breakdown")
        elif kind == "repaired":
            d = devices[ev[1] - 1]
            d.open_repair = False
            if (day - d.purchased_on).days > 4 * 365 and rng.random() < 0.4:
                d.retired_on = day
    if day.weekday() < 5:
        for _ in range(rng.choices([0, 1, 2, 3], [35, 40, 18, 7])[0]):
            borrower = rng.choice([e for e in employees if e.active(day) and e.job_title != "Warehouse clerk"])
            planned = rng.choice([1, 2, 3, 5, 7, 14, 30])
            due = day + timedelta(days=planned)
            loan = new_loan(borrower, day, due, rng.choice(SHORT_NOTES))
            cats = list(SHORT_WEIGHTS)
            n = rng.choices([1, 2, 3], [70, 22, 8])[0]
            picked = set(rng.choices(cats, [SHORT_WEIGHTS[c] for c in cats], k=n))
            if rng.random() < 0.3:
                ret = due + timedelta(days=rng.randint(1, 25))  # late
            else:
                ret = day + timedelta(days=rng.randint(0, planned))
            for category in picked:
                d = acquire(category, day)
                item = hand_out(loan, d, ret)
                lag = timedelta(days=rng.randint(1, 10)) if len(picked) > 1 and rng.random() < 0.1 else timedelta()
                back = ret + lag
                if back <= REF:
                    damaged = rng.random() < 0.02
                    item.returned_on, item.condition_in = back, ("damaged" if damaged else rng.choice(["good", "good", "worn"]))
                    d.busy_until = back
                    if damaged:
                        schedule(back, "short_damage", d.id, borrower.id)
                else:
                    d.busy_until = FAR
        # devices that break in the stock now and then
        if rng.random() < 0.04:
            stock = [d for d in devices if free(d, day)]
            if stock:
                start_repair(rng.choice(stock), day, it_staff(day))
    for ev in events.get(day, []):
        if ev[0] == "short_damage":
            d = devices[ev[1] - 1]
            if not d.open_repair and d.retired_on is None and d.busy_until <= day:
                start_repair(d, day, ev[2])
    day += timedelta(days=1)

# new devices waiting in the stock, never lent
for category, count in [("laptop", 8), ("screen", 6), ("headset", 5), ("phone", 4), ("mouse", 3)]:
    for _ in range(count):
        buy(category, rand_date(date(2026, 8, 15), REF))

# an old projector nobody ever borrowed
buy("projector", date(2019, 5, 20))

# --------------------------------------------------------------------------- SQL output


def lit(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v:.2f}" if isinstance(v, float) else str(v)
    if isinstance(v, date):
        return f"'{v.isoformat()}'"
    return "'" + str(v).replace("'", "''") + "'"


def insert(out, table: str, columns: list[str], rows: list[tuple], identity: bool) -> None:
    if not rows:
        return
    override = " overriding system value" if identity else ""
    for i in range(0, len(rows), 500):
        chunk = rows[i:i + 500]
        out.write(f"insert into {table} ({', '.join(columns)}){override} values\n")
        out.write(",\n".join("    (" + ", ".join(lit(v) for v in r) + ")" for r in chunk))
        out.write(";\n\n")


def status(d: Device) -> str:
    if d.retired_on and d.retired_on <= REF:
        return "retired"
    if d.open_repair:
        return "in_repair"
    return "in_service"


out = sys.stdout
out.write("-- Equipment loans: data generated by generate.py (seed %d). Do not edit by hand.\n" % SEED)
out.write(f"-- Reference date of the dataset: {REF.isoformat()}.\n\n")
out.write("set search_path to equipment_loans;\n\nbegin;\n\n")
insert(out, "department", ["id", "name"], [(i, n) for i, n in enumerate(DEPARTMENTS, start=1)], True)
# insert employees ordered so a supervisor always exists before the people reporting to them
insert(out, "employee",
       ["id", "first_name", "last_name", "email", "job_title", "department_id", "supervisor_id", "hired_on", "left_on"],
       [(e.id, e.first_name, e.last_name, e.email, e.job_title, e.department_id, e.supervisor_id, e.hired_on, e.left_on)
        for e in employees], True)
insert(out, "user_account", ["employee_id", "username", "created_on", "disabled_on"], accounts, False)
insert(out, "brand", ["id", "name"], [(i, b) for b, i in brand_id.items()], True)
insert(out, "device_category", ["id", "name"], [(i, c) for c, i in category_id.items()], True)
insert(out, "device_model", ["id", "brand_id", "category_id", "name"],
       [(m[0], brand_id[m[1]], category_id[m[2]], m[3]) for m in models], True)
insert(out, "device", ["id", "inventory_tag", "serial_number", "model_id", "purchased_on", "purchase_price", "status"],
       [(d.id, d.tag, d.serial, d.model_id, d.purchased_on, d.price, status(d)) for d in devices], True)
insert(out, "loan", ["id", "borrower_id", "handed_out_by_id", "loaned_on", "due_on", "note"],
       [(l.id, l.borrower_id, l.handed_out_by_id, l.loaned_on, l.due_on, l.note) for l in loans if l.items], True)
insert(out, "loan_item", ["loan_id", "device_id", "condition_out", "returned_on", "condition_in"],
       [(i.loan_id, i.device_id, i.condition_out, i.returned_on, i.condition_in)
        for l in loans for i in l.items], False)
insert(out, "repair", ["id", "device_id", "reported_by_id", "reported_on", "description", "closed_on", "cost"],
       [(r.id, r.device_id, r.reported_by_id, r.reported_on, r.description, r.closed_on, r.cost) for r in repairs], True)
# move each identity past the inserted ids, so new rows get the next free id
out.write("do $$\nbegin\n")
for table in ["department", "employee", "brand", "device_category", "device_model", "device", "loan", "repair"]:
    out.write(f"    perform setval(pg_get_serial_sequence('equipment_loans.{table}', 'id'), "
              f"(select max(id) from equipment_loans.{table}));\n")
out.write("end\n$$;\n\ncommit;\n")
