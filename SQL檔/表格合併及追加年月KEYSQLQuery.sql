select * from [dbo].[行_出國旅客數]

SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    CHARACTER_MAXIMUM_LENGTH AS [長度],
    IS_NULLABLE AS [允許空值]
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = '產業用電量'

DROP TABLE [dbo].[行_出國旅客數]

ALTER TABLE [dbo].[行_出國旅客數]
DROP COLUMN 年月KEY


ALTER TABLE [dbo].[行_市區汽車客運路線與車輛數]
ADD [年月KEY] AS (YEAR([年月]) * 100 + MONTH([年月]));

ALTER TABLE [dbo].[行_出國旅客數]
ADD [年月] AS (
    CAST([年] AS VARCHAR(4)) + 
    RIGHT('0' + CAST([月] AS VARCHAR(2)), 2));


ALTER TABLE [dbo].[產業用電量]
ALTER COLUMN [年月] DATE;

