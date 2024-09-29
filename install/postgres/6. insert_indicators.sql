INSERT INTO public.indicators (inst_instid,indicid, name, abbreviation, unit_measure, description)

VALUES

-- GDP
('OECD','GDP', 'Gross domestic product, nominal value, market prices', 'GDP', 'National currency', ''),
('OECD','GDP_USD', 'Gross domestic product, nominal value in USD, OECD reference year exchange rates', 'GDP_USD', 'USD', ''),
('OECD','GDPV', 'Gross domestic product, volume, market prices', 'GDPV', 'National currency', ''),
('OECD','GDPV_USD', 'Gross domestic product, volume in USD, OECD reference year exchange rates', 'GDPV_USD', 'USD', ''),

-- PCE
('OECD','CP', 'Private final consumption expenditure, nominal value, GDP expenditure approach', 'PCE', 'National currency', ''),

-- FGCE
('OECD','CG', 'Government final consumption expenditure, nominal value, GDP expenditure approach.', 'FGCE', 'National currency', ''),

-- UR
('OECD','UNR', 'Unemployment rate', 'UR', '% of labour force', ''),

-- IR

('OECD','IRL', 'Long-term interest rate', 'IRL', 'points', ''),
('OECD','IRS', 'Short-term interest rate', 'IRS', 'points', ''),

('OECD','GGFLM', 'Gross public debt, Maastricht criterion', 'PD', 'National currency', ''),
('OECD','GGFLMQ', 'Gross public debt, Maastricht criterion, as % of GDP', 'PD_GDP', '% of GDP', ''),

-- ER

('OECD','EXCHUD', 'Exchange rate', 'ER', 'national currency/USD', '')



ON CONFLICT (indicid) DO NOTHING;
