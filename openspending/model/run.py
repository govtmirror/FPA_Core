from datetime import datetime

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime

from openspending.core import db
from openspending.model.dataset import Dataset
from openspending.model.source import Source


class Run(db.Model):

    """ A run is a generic grouping object for background operations
    that perform logging to the frontend. """

    __tablename__ = 'run'

    # Status values
    STATUS_RUNNING = 'running'
    STATUS_COMPLETE = 'complete'
    STATUS_FAILED = 'failed'
    STATUS_REMOVED = 'removed'

    # Operation values for database, two operations possible
    OPERATION_SAMPLE = 'sample'
    OPERATION_IMPORT = 'import'

    id = Column(Integer, primary_key=True)
    operation = Column(Unicode(2000))
    status = Column(Unicode(2000))
    time_start = Column(DateTime, default=datetime.utcnow)
    time_end = Column(DateTime)
    dataset_id = Column(Integer, ForeignKey('dataset.id'), nullable=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=True)

    dataset = relationship(Dataset,
                           backref=backref('runs',
                                           order_by='Run.time_start.desc()',
                                           lazy='dynamic'))
    source = relationship(Source,
                          backref=backref('runs',
                                          order_by='Run.time_start.desc()',
                                          lazy='dynamic'))

    def __init__(self, operation, dataset, source, status=None):
        self.operation = operation
        if not status:
            self.status = self.STATUS_RUNNING
        else:
            self.status = status
        self.dataset = dataset
        self.source = source


    def records_as_json(self):
        returnset = []
        for record in self.records:
            returnset.append(record.as_json())
        return returnset


    @property
    def successful_sample(self):
        """
        Returns True if the run was a sample operation (not full import)
        and ran without failures.
        """
        return self.operation == self.OPERATION_SAMPLE and \
            self.status == self.STATUS_COMPLETE

    @property
    def successful_load(self):
        """
        Returns True if the run was an import operation (not a sample)
        and ran without failures.
        """
        return self.operation == self.OPERATION_IMPORT and \
            self.status == self.STATUS_COMPLETE

    @property
    def is_running(self):
        """
        Returns True if the run is currently running
        """
        return self.status == self.STATUS_RUNNING

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()

    def __repr__(self):
        if not self.source:
            return "<OldRun(%r)>" % (self.id)
        else:
            return "<Run(%r, %r)>" % (self.source.id, self.id)
