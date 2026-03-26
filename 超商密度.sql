TRUNCATE TABLE Fact_便利商店密度; --確保table是空的

--建一張每年、每區的累積店數虛擬表
WITH YearList AS (
    SELECT 2018 AS RptYear 
    UNION SELECT 2019 
    UNION SELECT 2020 
    UNION SELECT 2021 
    UNION SELECT 2022 
    UNION SELECT 2023 
    UNION SELECT 2024 
    UNION SELECT 2025 
    UNION SELECT 2026
),
CumulativeStats AS (
    SELECT 
        y.RptYear,
        s.縣市,
        s.行政區,
        COUNT(*) AS TotalCount
    FROM YearList y
    INNER JOIN 全國5大超商資料集 s ON s.西元設立日期 <= DATEFROMPARTS(y.RptYear, 12, 31) --累計至該年年底
    GROUP BY y.RptYear, s.縣市, s.行政區
)

--insert進事實資料表中
INSERT INTO Fact_便利商店密度 ([年度], [縣市], [行政區], [店面數], [土地面積], [超商密度])
SELECT 
    cs.RptYear,
    cs.縣市,
    cs.行政區,
    cs.TotalCount,
    da.土地面積,
    CAST(cs.TotalCount AS DECIMAL(18,6)) / da.土地面積 AS Density --轉換型別避免預設的整數除法
FROM CumulativeStats cs
INNER JOIN 各縣市鄉鎮市區土地面積及人口密度 da ON cs.縣市 = da.縣市 AND cs.行政區 = da.行政區;