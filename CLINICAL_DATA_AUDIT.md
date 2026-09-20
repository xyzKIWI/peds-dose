# 臨床資料查核記錄

查核日期：2026-09-21（Asia/Taipei）

## 高醫岡山 Clodrin

- 院內頁面：[3CLO30](https://www.kmugh.org.tw/web/drugsearch/drugsearch.aspx?Search=3CLO30#Link)
- 院內頁面顯示：Clodrin 10% 灌腸用（100 mg/mL），30 mL/Bot；學名 Chloral Hydrate；「外用局部用」。
- 院內頁面連結仿單：[https://www.kmuh.org.tw/med/medpdf/cPDF/C3CLO30.pdf](https://www.kmuh.org.tw/med/medpdf/cPDF/C3CLO30.pdf)
- 官方仿單（衛部罕藥製字第 000020 號，版本尾註 CTRA-104 20190422）明寫：每 mL 含 Chloral hydrate 100 mg；兒童無痛檢查前鎮靜；口服使用，避免肛門給藥；限醫療機構並需適當監測。
- 仿單劑量只保留在可展開參考資料，不是快捷預設：EEG 為 25-50 mg/kg PO；無痛檢查為嬰兒 30-50 mg/kg PO，兒童 50-60 mg/kg PO，需要時 30 分鐘後追加 10-20 mg/kg 一次；累計不超過 100 mg/kg，嬰兒不超過 1 g，兒童不超過 2 g。
- 結論：院內網頁與官方仿單的途徑相互衝突。已標記 `verification_required`，並暫停所有快捷 mg/mL 結果，等岡山藥劑科確認實際作業。

## 高醫岡山 Midatin

- 院內頁面：[Midatin 查詢結果](https://www.kmugh.org.tw/web/drugsearch/drugsearch.aspx?Search=midatin#Link)
- 2026-09-21 查核時同時顯示兩個規格：
  - 新品 `2MID50`：「美得定注射液 50mL（南光）」；Midatin 50 mg/50 mL/Bag，即 1 mg/mL；頁面未標示缺藥。
  - 舊品 `2MIDAT`：「美得定注射液（南光）（缺藥）」；Midatin 15 mg/3 mL/Amp，即 5 mg/mL。
- 新品官方仿單：[B2MID50.pdf](https://www.kmuh.org.tw/med/medpdf/bPDF/B2MID50.pdf)，版本日期 2024-03-29；標示每 mL 含 Midazolam 1 mg，包裝包含 50 mL 塑膠軟袋。
- 仿單兒科知覺鎮靜及 ICU 鎮靜依年齡、途徑與反應分層，且要求緩慢滴定及監測；因此新品目前只顯示仿單參考範圍，不啟用單一快捷劑量。
- 結論：`2MID50` 列為目前院內新供應品；`2MIDAT` 保留為舊缺藥品。兩者濃度相差五倍，不可沿用舊安瓿的 mL 速算。

## 待院內複核

- Ketamine 院內 HIS 截圖已確認 `2KET10`、Ketalar 500 mg/10 mL、開藥單位 Vial，範例途徑為 IM；網站以原液 c.c. ÷ 10 mL 換算 `0.xx Vial`。IV 是否稀釋、最終濃度與院內處置鎮靜 protocol 仍待複核；目前 IV 1 mg/kg 與追加 0.5 mg/kg 來自 RCEM 2020，不代表院內已核定。
- Thiopental 的「目前無藥」由使用者提供，尚待藥劑科定期複核。
- Acetaminophen、Ibuprofen、Curam 與第二批藥品仍需逐項核對岡山院內規格與現行 protocol。

此記錄無病人識別資料。「快捷預設」與「可查閱參考範圍」已分開，未確認項目不轉成一鍵給藥結果。
