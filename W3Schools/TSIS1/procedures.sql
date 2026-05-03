-- Procedure to add a phone number to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact % not found', p_contact_name;
    ELSE
        INSERT INTO phones (contact_id, phone, type) 
        VALUES (v_contact_id, p_phone, p_type);
    END IF;
END;
$$;

-- Procedure to move contact to group (creates group if missing)
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;
    
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;

-- Function for advanced searching across name, email, and multiple phones
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (contact_id INT, name VARCHAR, email VARCHAR, phone VARCHAR) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;