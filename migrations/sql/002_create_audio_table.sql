CREATE TABLE IF NOT EXISTS audio (
    audio_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);