-- Admin Messages Table
CREATE TABLE IF NOT EXISTS admin_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    recipient_name TEXT NOT NULL,
    message TEXT NOT NULL,
    sent_by TEXT DEFAULT 'admin',
    sent_at TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'sent'
);

-- Add phone number column to appointments table if not exists
ALTER TABLE appointments 
ADD COLUMN IF NOT EXISTS patient_phone TEXT DEFAULT '+1234567890';

-- Update existing appointments to have phone numbers
UPDATE appointments 
SET patient_phone = '+1234567890' 
WHERE patient_phone IS NULL;
