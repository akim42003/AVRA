# db/models.py

from sqlalchemy import create_engine, Column, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from .config import DATABASE_URI

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=True)

# Define the base class for declarative models
Base = declarative_base()

# Define the AudioSegments model
class AudioSegment(Base):
    __tablename__ = 'audio_segments'
    segment_index = Column(Integer, primary_key=True, autoincrement=True)
    length_ms = Column(Float, nullable=False)

    #spectrograms = relationship('SpectrogramSegment', back_populates='audio_segment')

# Define the SpectrogramSegments model
class SpectrogramSegment(Base):
    __tablename__ = 'spectrogram_segments'
    id = Column(Integer, primary_key=True)
    audio_index = Column(Integer, nullable = False)
    segment_index = Column(Integer, nullable=False)
    width_pixels = Column(Integer, nullable=False)

    #audio_segment = relationship('AudioSegment', back_populates='spectrograms')

def create_tables():
    Base.metadata.create_all(engine)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()
