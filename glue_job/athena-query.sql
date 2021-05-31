SELECT COUNT(*) as Notification_Count
FROM "default"."crawlermwa_controltower_lll_security_topic_noncompliant_notifications"
WHERE  newEvaluationResult.resultRecordedTime > to_iso8601(current_timestamp - interval '20' minute);