-- Step 1: Drop the foreign key constraint from transcriptions before modifying the audio table
ALTER TABLE transcriptions
DROP CONSTRAINT IF EXISTS transcriptions_audio_id_fkey;

-- Step 2: Alter the audio table to add the new_audio_id column of type UUID
ALTER TABLE audio ADD COLUMN new_audio_id UUID DEFAULT uuid_generate_v4();

-- Step 3: Drop the old audio_id column from the audio table
ALTER TABLE audio DROP COLUMN audio_id;

-- Step 4: Rename the new_audio_id column to audio_id in the audio table
ALTER TABLE audio RENAME COLUMN new_audio_id TO audio_id;

-- Step 5: Add a unique constraint on the audio_id column in the audio table
ALTER TABLE audio
ADD CONSTRAINT audio_id_unique UNIQUE (audio_id);

-- Step 6: Alter the transcriptions table's audio_id column to UUID type
ALTER TABLE transcriptions
ALTER COLUMN audio_id SET DATA TYPE UUID USING uuid_generate_v4();

-- Step 7: Recreate the foreign key constraint between transcriptions and audio
ALTER TABLE transcriptions
ADD CONSTRAINT transcriptions_audio_id_fkey
FOREIGN KEY (audio_id) REFERENCES audio(audio_id);

-- Step 8: Create indexes on the audio_id column in both tables (optional but recommended for performance)
CREATE INDEX IF NOT EXISTS idx_audio_id ON transcriptions(audio_id);
CREATE INDEX IF NOT EXISTS idx_audio_id ON audio(audio_id);
