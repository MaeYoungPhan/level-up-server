SELECT g.id,
    u.first_name || ' ' || u.last_name AS full_name, 
    g.user_id,
    e.id,
    e.date,
    e.time,
    a.gamer_id,
    s.name AS game_name
FROM levelupapi_gamer g
JOIN auth_user u
    ON g.user_id = u.id
JOIN levelupapi_event e
    ON e.organizer_id = g.id
JOIN levelupapi_game s
    ON e.game_id = s.id
JOIN levelupapi_eventattendee a
    ON e.id = a.event_id