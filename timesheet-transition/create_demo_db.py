#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from state_time import bcrypt, week_day_dates, encrypt_password, app
from models import *
from itertools import product
from datetime import time
from faker import Faker

fake = Faker()
fake.seed(42)

# remove sqlite DB:
if isinstance(db, FlaskDB):
    _db = db.database
else:
    _db = db

if os.path.exists(_db.database):
    try:
        os.remove(_db.database)
    except BaseException:  # if fails, drop all model tables:
        drop_tables()

# create all tales from the scratch:
create_tables()

# Breaks:
for code, name, length in (
    ("5H", "5 hrs", 300),
    ("HH", "1/2 hr", 30),
    ("1H", "1 hr", 60),
    ("1.5H", "1 1/2 hr", 90),
    ("2H", "2 hrs", 120),
    ("15M", "15 min", 15),
    ("45M", "45 min", 45),
    ("1H15M", "1 hr 15 min", 75),
    ("1H45M", "1 hr 45 min", 105),
    ("2H15M", "2 hrs 15 min", 135),
    ("2H30M", "2 hrs 30 min", 150),
    ("2H45M", "2 hrs 45 min", 165),
    ("3H0M", "3 hrs ", 180),
    ("3H15M", "3 hrs 15 min", 195),
    ("3H30M", "3 hrs 30 min", 210),
    ("3H45M", "3 hrs 45 min", 225),
    ("4H0M", "4 hrs ", 240),
    ("4H15M", "4 hrs 15 min", 255),
    ("4H30M", "4 hrs 30 min", 270),
        ("4H45M", "4 hrs 45 min", 285),):
    Break(code=code, name=name, minutes=length).save()


# Create all roles:
emp = user_datastore.create_role(name="emp")
approver = user_datastore.create_role(name="approver")
admin = user_datastore.create_role(name="admin")

# Companies:
Company.insert_many((dict(code=code, name=name) for code, name in (
    ('Z4M4Q0', fake.company()),
    ('B4J4L6', fake.company()),
    ('Y9P9S3', fake.company()),
    ('V9A5K4', fake.company()),
    ('Y0U5B3', fake.company()),
    ('T3N2Y6', fake.company()),
    ('Q6U3Y9', fake.company()),
    ('W9J2M9', fake.company()),
    ('Y3Z9T9', fake.company()),
    ('R2H4P5', fake.company()),
))).execute()

# Users
with app.app_context():
    test_password = encrypt_password('12345')
for id, (username, email, first_name, last_name) in enumerate((
    ('user0', fake.email(), fake.first_name(), fake.last_name()),
    ('user1', fake.email(), fake.first_name(), fake.last_name()),
    ('user2', fake.email(), fake.first_name(), fake.last_name()),
    ('approver0', fake.email(), fake.first_name(), fake.last_name()),
    ('approver1', fake.email(), fake.first_name(), fake.last_name()),
    ('approver2', fake.email(), fake.first_name(), fake.last_name()),
    ('admin0', fake.email(), fake.first_name(), fake.last_name()),
    ('admin1', fake.email(), fake.first_name(), fake.last_name()),
        ('admin2', fake.email(), fake.first_name(), fake.last_name())), 1):
    user = user_datastore.create_user(
        username=username,
        # code=username.upper(),
        email=email,
        password=test_password,
        first_name=first_name,
        last_name=last_name,
        workplace=Company.get(id=id))
    user.save()
    if "user" in username:
        user.roles = [emp]
    else:
        user.approves_for = [
            Company.get(
                id=company_id) for company_id in range(
                id, id + 2)]
        user.roles.add(approver)
        if "admin" in username:
            user.roles.add(admin)
    user.save()


# Timesheet entries
week_dates = list(week_day_dates())
for no, (user, day) in enumerate(product(User.select(), week_dates)):
    entry = Entry(
        date=day,
        user=user,
        started_at=time(7, no * 10 % 60, 0),
        finished_at=time(16, no * 7 % 60, 0),
        break_for=Break.get(id=no % 20 + 1)
    )
    entry.save()
