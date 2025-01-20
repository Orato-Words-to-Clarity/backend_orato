-- Step 1: Add a new column `new_transcription_id` of type UUID
ALTER TABLE transcriptions ADD COLUMN new_transcription_id UUID DEFAULT uuid_generate_v4();

-- Step 2: Copy the data from `transcription_id` to `new_transcription_id`
UPDATE transcriptions SET new_transcription_id = uuid_generate_v4();

-- Step 3: Drop the old `transcription_id` column
ALTER TABLE transcriptions DROP COLUMN transcription_id;

-- Step 4: Rename `new_transcription_id` to `transcription_id`
ALTER TABLE transcriptions RENAME COLUMN new_transcription_id TO transcription_id;

-- Step 5: Add a unique constraint on `transcription_id` if needed (optional)
ALTER TABLE transcriptions ADD CONSTRAINT transcription_id_unique UNIQUE (transcription_id);
