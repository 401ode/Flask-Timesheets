# -*- coding: utf-8 -*-
"""Agency models."""
import datetime as dt

from flask_login import UserMixin
from state_time.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Agency(SurrogatePK, Model):
    """ A State Agency."""

    __tablename__ = 'agencies'
    agency_code = Column(db.Integer, primary_key=True)
    agency_name = Column(db.String(100), nullable=False)
    agency_acronym = Column(db.String(10), nullable=False)
    cost_centers = db.relationship('CostCenter',
                                   backref='agency',
                                   lazy=True)

    def __init__(self, agency_code, agency_name, agency_acronym, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self,
            agency_code=agency_code,
            agency_name=agency_name,
            agency_acronym=agency_acronym
            ** kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Agency({agency_acronym!r})>'.format(
            username=self.agency_acronym)


class CostCenter(SurrogatePK, Model):
    """
    Cost Center within an agency.
    """
    __tablename__ = 'costcenters'
    agency = db.Column(
        db.Integer,
        db.ForeignKey('agency.id'),
        nullable=False)
    cost_center_name = Column(db.String(40))
    cost_center_code = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return "{} - {}".format(
            self.agency_name, self.cost_center_name
        )
