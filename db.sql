SELECT g.id, u.first_name || ' ' || u.last_name AS full_name, s.id,
    s.name,
    s.game_type_id,
    s.max_players
FROM levelupapi_gamer g
JOIN auth_user u
    ON g.user_id = u.id
JOIN levelupapi_game s
    ON s.gamer_id = g.user_id