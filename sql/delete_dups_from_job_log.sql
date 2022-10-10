DELETE FROM job_log a
    USING job_log b
WHERE a.id < b.id
  AND a.id_job = b.id_job and a.msg = b.msg;