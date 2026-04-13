-- 🔄 UPSERT (insert or update)
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR,
    p_email VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_first_name) THEN
        UPDATE contacts
        SET phone = p_phone,
            last_name = p_last_name,
            email = p_email
        WHERE first_name = p_first_name;
    ELSE
        INSERT INTO contacts(first_name, last_name, phone, email)
        VALUES (p_first_name, p_last_name, p_phone, p_email);
    END IF;
END;
$$;


-- 📦 BULK INSERT + проверка телефона + сохранение ошибок
CREATE TABLE IF NOT EXISTS invalid_contacts (
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
);


CREATE OR REPLACE PROCEDURE bulk_insert_contacts()
LANGUAGE plpgsql
AS $$
DECLARE
    c RECORD;
BEGIN
    FOR c IN SELECT * FROM temp_contacts LOOP

        -- проверка телефона
        IF c.phone ~ '^[0-9+]+$' THEN
            INSERT INTO contacts(first_name, last_name, phone)
            VALUES (c.first_name, c.last_name, c.phone);
        ELSE
            INSERT INTO invalid_contacts(first_name, last_name, phone)
            VALUES (c.first_name, c.last_name, c.phone);
        END IF;

    END LOOP;
END;
$$;


-- ❌ DELETE by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;

    ELSIF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE first_name = p_name;
    END IF;
END;
$$;