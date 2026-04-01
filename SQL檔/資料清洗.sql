select * from [dbo].[DimDate];

select * from [dbo].[餐飲業開店數];

ALTER TABLE 食_餐飲業每月營業額
DROP COLUMN [年月];

ALTER TABLE 食_餐飲業每月營業額
ADD [年月] NVARCHAR(50);

UPDATE 食_餐飲業每月營業額
SET [年月] = CAST([年] AS VARCHAR(4)) + RIGHT('0' + CAST([月] AS VARCHAR(2)), 2);


-- 使用 LTRIM/RTRIM 去除可能存在的空格
UPDATE 食_餐飲業每月營業額
SET [月] = RIGHT('0' + REPLACE(RTRIM(LTRIM([月])), '月', ''), 2)
WHERE [月] LIKE '%月%'; -- 只要包含「月」字就處理


UPDATE 食_餐飲業每月營業額
SET [月] = LEFT(
    SUBSTRING([月], PATINDEX('%[0-9]%', [月]), LEN([月])),
    PATINDEX('%[^0-9]%', SUBSTRING([月], PATINDEX('%[0-9]%', [月]), LEN([月])) + 'X') - 1
)
WHERE PATINDEX('%[0-9]%', [月]) > 0;

-- 永久修改資料表
UPDATE 食_餐飲業每月營業額
SET [月] = RIGHT('0' + CAST([月] AS VARCHAR(2)), 2)
WHERE LEN([月]) = 1; -- 只針對 1, 2... 這種一碼的進行處理

exec sp_help 食_餐飲業每月營業額

ALTER TABLE 食_餐飲業每月營業額
ALTER COLUMN [年月] datetime;