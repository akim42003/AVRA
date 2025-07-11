# db/db_utils.py

from .models import get_session, AudioSegment, SpectrogramSegment

def add_audio_segment(length_ms):
    session = get_session()
    audio_segment = AudioSegment(length_ms=length_ms)
    session.add(audio_segment)
    session.commit()
    #return audio_segment.segment_index

def add_spectrogram_segment(audio_index, segment_index, width_pixels):
    session = get_session()
    spectrogram_segment = SpectrogramSegment(audio_index =audio_index, segment_index=segment_index, width_pixels=width_pixels)
    session.add(spectrogram_segment)
    session.commit()

def get_audio_segments():
    session = get_session()
    return session.query(AudioSegment).all()

def get_spectrogram_segments(start_index, end_index):
    session = get_session()
    try:
        results = session.query(
            SpectrogramSegment.id,
            SpectrogramSegment.audio_index, 
            SpectrogramSegment.segment_index, 
            SpectrogramSegment.width_pixels
        ).filter(
            SpectrogramSegment.audio_index.between(start_index, end_index)
        ).distinct().all()
    finally:
        session.close()
    return results

def close_session(session):
    session.close()
