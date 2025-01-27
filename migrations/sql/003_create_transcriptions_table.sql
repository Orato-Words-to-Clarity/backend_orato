CREATE TABLE IF NOT EXISTS transcriptions (
    transcription_id SERIAL PRIMARY KEY,
    audio_id INTEGER NOT NULL REFERENCES audio(audio_id),
    text TEXT NOT NULL,
    embedding_id INTEGER,
    language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);