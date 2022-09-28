insert into exchange_acronyms (operating_mic, acronym) values
('XLON', 'LSE')
on conflict (operating_mic, acronym) do nothing;