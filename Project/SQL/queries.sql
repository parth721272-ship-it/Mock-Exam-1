-- Red & White Skill Education
-- Practical Exam - Data Analysis Set B
-- SQL Dialect: MySQL 8.0.46

USE support_quality;
-- ============================================
-- S2a - Average Resolution Time by Department
-- ============================================

SELECT
    t.department,
    ROUND(AVG(k.resolution_hours), 2) AS avg_resolution_hours
FROM tickets k
JOIN teams t
    ON k.team_id = t.team_id
GROUP BY t.department
ORDER BY avg_resolution_hours DESC;

-- ============================================
-- S2b - Teams Breaching SLA
-- ============================================

SELECT
    t.team,
    ROUND(AVG(k.resolution_hours), 2) AS avg_resolution_hours
FROM tickets k
JOIN teams t
    ON k.team_id = t.team_id
GROUP BY t.team_id, t.team
HAVING AVG(k.resolution_hours) > 24
ORDER BY avg_resolution_hours DESC;

-- ============================================
-- S2c - Top Two Channels by Breach Count
-- ============================================

SELECT
    channel,
    COUNT(*) AS breach_count
FROM tickets
WHERE resolution_hours > 24
GROUP BY channel
ORDER BY breach_count DESC, channel ASC
LIMIT 2;

-- ============================================
-- S2b - Teams Breaching SLA
-- ============================================

SELECT
    t.team,
    ROUND(AVG(k.resolution_hours), 2) AS avg_resolution_hours
FROM tickets k
JOIN teams t
    ON k.team_id = t.team_id
GROUP BY t.team_id, t.team
HAVING AVG(k.resolution_hours) > 24
ORDER BY avg_resolution_hours DESC;