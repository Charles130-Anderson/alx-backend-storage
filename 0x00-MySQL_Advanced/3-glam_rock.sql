-- List bands with Glam rock style by longevity
SELECT band_name,
       IFNULL(YEAR('2022-01-01') - YEAR_FORMED, 0) as lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC, band_name;
