# -*- coding: utf-8 -*-
"""Grant, Grant Task, Allocation models."""
import datetime as dt

from flask_login import UserMixin
from state_time.database import Column, Model, SurrogatePK, db, reference_col, relationship


class GrantAward(SurrogatePK, Model):
    __tablename__ = 'grantawards'
    agency = db.Column(
        db.Integer,
        db.ForeignKey('agency.id'),
        nullable=False
    )

    grant_award = Column(
        db.String(40),
        primary_key=True
    )

    grant_award_description = Column(
        db.String(100),
        unique=False
    )

    grant_award_start_date = Column(
        db.Date,
        nullable=False
    )

    grant_award_end_date = Column(
        db.Date,
        nullable=False
    )


class GrantAwardTask(SurrogatePK, Model):
    """
    The class for holding information regarding Federal or other Grant Award Tasks to which
    time can be allotted.

    For RI-specific purposes, these will be created dynamically based on data in the
    GrantGrantTaskExport GovGrants GMS object.

    These objects should not be maintained manually in this system, but modified using
    the standard GMS process.
    """

    __tablename__ = 'grantawardtasks'

    grant_award_id = Column(
        db.Integer,
        db.ForeignKey('GrantAward.id')
    )

    grant_award_description = Column(
        db.String(100),
        unique=False
    )

    grant_award_start_date = Column(
        db.Date,
        nullable=False
    )

    grant_award_end_date = Column(
        db.Date,
        nullable=False
    )

    percent_allotted = Column(
        db.Float,
        , precision=(1, 4)
        default=0.00
    )


class Allocation(SurrogatePK, Model):
    """
   At a minimum, need a spot for:
   - The associated grant.
   - The legacy account number?
   - The RISAIL Account Number?
   - Definitely the RIFANS account number.
   - The percentage of that task paid by the given Grant task.
   """
