DO $$
DECLARE
    weapon_id   weapon.weaponid%TYPE;
    incident_id weapon.incidentid%TYPE;

BEGIN
    weapon_id := 1000000;
    incident_id := '20220526TXDUA';
    FOR counter IN 1..10
        LOOP
            INSERT INTO weapon(weaponid, incidentid, weaponcaliber, weapondetails, weapontype)
             VALUES (counter + weapon_id, incident_id , null, null, null|| 100+counter);
        END LOOP;
END;
$$;

SELECT * FROM weapon;