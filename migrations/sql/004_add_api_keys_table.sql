CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    groq_api_key_encrypted TEXT NULL,
    huggingface_api_key_encrypted TEXT NULL
);
