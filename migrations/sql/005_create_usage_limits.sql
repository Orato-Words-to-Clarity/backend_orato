CREATE TABLE usage_limits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_llama_tokens INTEGER NOT NULL DEFAULT 0,
    total_whisper_tokens INTEGER NOT NULL DEFAULT 0,
    UNIQUE (user_id, date)
);
