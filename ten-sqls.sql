
-- 選擇欲參加的活動：系統會新增參訪者報名資訊新增至資料庫。(l)
INSERT INTO registration (user_id, activity_id, status)
VALUES (?, ?, ?);


-- 取消欲參加的活動：若臨時無法參加，可以取消報名參加的活動。(l) 
UPDATE registration
SET status = 'C'
WHERE user_id = ? AND activity_id = ?;

-- 查詢自身參加過的活動
SELECT *
FROM activity a
JOIN registration r ON a.activity_id = r.activity_id
WHERE r.user_id = ?;

-- 查詢收容所收容率：可以查詢目前收容所的收容率狀態
SELECT
    s.shelter_id,
    s.name,
    s.capacity,
    COUNT(a.animal_id) AS current_animals,
    (COUNT(a.animal_id)::FLOAT / s.capacity) * 100 AS occupancy_rate_percent
FROM
    shelter s
LEFT JOIN
    animal a ON s.shelter_id = a.shelter_id AND a.leave_at IS NULL
GROUP BY
    s.shelter_id, s.name, s.capacity;

-- 計算貓和狗的平均留存率（待多久
SELECT
    a.shelter_id,
    s.name AS shelter_name,
    a.species,
    AVG(EXTRACT(EPOCH FROM COALESCE(a.leave_at, CURRENT_TIMESTAMP) - a.arrived_at) / 86400) AS avg_stay_days
FROM
    animal a
JOIN
    shelter s ON a.shelter_id = s.shelter_id
GROUP BY
    a.shelter_id, s.name, a.species;

-- 打卡
INSERT INTO punch (employee_id, punch_type) 
VALUES (?, ?);