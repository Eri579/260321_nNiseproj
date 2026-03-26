--建一個虛擬資料表整理年月及「截至該月底」的累計店數
WITH MonthList AS (
    SELECT CAST('2018-01-01' AS DATE) AS MonthStart
    UNION ALL
    SELECT DATEADD(MONTH, 1, MonthStart)
    FROM MonthList
    WHERE MonthStart < '2026-12-01'
),
MonthlyCumulative AS (
    SELECT 
        YEAR(m.MonthStart) AS RptYear,
        MONTH(m.MonthStart) AS RptMonth,
        s.縣市,
        s.行政區,
        COUNT(*) AS TotalCount,
        EOMONTH(m.MonthStart) AS EndOfMonth --每個月最後一天
    FROM MonthList m
    INNER JOIN 全國5大超商資料集 s ON s.西元設立日期 <= EOMONTH(m.MonthStart)
    GROUP BY YEAR(m.MonthStart), MONTH(m.MonthStart), s.縣市, s.行政區, EOMONTH(m.MonthStart)
)
INSERT INTO Fact_便利商店密度 ([年度], [月份], [縣市], [行政區], [店面數], [土地面積], [超商密度]) --INSERT進事實表
SELECT 
    mc.RptYear,
    mc.RptMonth,
    mc.縣市,
    mc.行政區,
    mc.TotalCount,
    da.土地面積,
    CAST(mc.TotalCount AS DECIMAL(18,6)) / da.土地面積 AS Density --轉換型別避免整數除法
FROM MonthlyCumulative mc
INNER JOIN 各縣市鄉鎮市區土地面積及人口密度 da ON mc.縣市 = da.縣市 AND mc.行政區 = da.行政區 
OPTION (MAXRECURSION 200); --預設遞迴次數維100，不夠，所以調整上限為200