CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,           -- 格式如 20260403
    Date DATE NOT NULL,            -- 標準日期格式
    [年] INT NOT NULL,               -- 年
    [季] TINYINT NOT NULL,        -- 季
    [月] TINYINT NOT NULL,          -- 月
    [日] TINYINT NOT NULL,            -- 日
    [月份名稱] NVARCHAR(10),          -- 月份名稱 (如 April)
    [星期] NVARCHAR(10),      -- 星期幾 (如 Friday)
    [年月] INT NOT NULL,          -- 你需要的年月格式 202604
    [假日] BIT NOT NULL           -- 是否為週末
);

DECLARE @StartDate DATE = '2018-01-01'; -- 設定開始日期
DECLARE @EndDate DATE = '2026-12-31';   -- 設定結束日期

WHILE @StartDate <= @EndDate
BEGIN
    INSERT INTO DimDate (
        DateKey,
        Date,
        [年],
        [季],
        [月],
        [日],
        [月份名稱],
        [星期],
        [年月],
        [假日]
    )
    SELECT 
        YEAR(@StartDate) * 10000 + MONTH(@StartDate) * 100 + DAY(@StartDate), -- 轉成 20200101
        @StartDate,
        YEAR(@StartDate),
        DATEPART(QUARTER, @StartDate),
        MONTH(@StartDate),
        DAY(@StartDate),
        DATENAME(MONTH, @StartDate),
        DATENAME(WEEKDAY, @StartDate),
        YEAR(@StartDate) * 100 + MONTH(@StartDate), -- 轉成 202001
        CASE WHEN DATEPART(WEEKDAY, @StartDate) IN (1, 7) THEN 1 ELSE 0 END; -- 1:日, 7:六

    SET @StartDate = DATEADD(DAY, 1, @StartDate); -- 跳到隔天
END;

SELECT TOP 100 * FROM DimDate ORDER BY DateKey;