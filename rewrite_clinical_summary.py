#!/usr/bin/env python3
"""
用自己整理的 pocket-card 風格短摘要，覆蓋 KMUH 抓出的 kmuh_detail。
資料層級：universal pharmacology facts（事實，非任何單一來源逐字）。
覆寫 → 同樣的「📋 藥典完整資料」按鈕，內容自己寫。
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent
JSON = ROOT / "peds_drugs.json"

# 7 個欄位簡短整理（事實層級，自己組織格式）
# 格式短，pocket-card 風，避免任何來源 prose 風格
CLINICAL = {
    # ===== 退燒/止痛 =====
    "antiphen_syrup": {
        "臨床用途": "發燒、輕度疼痛", "禁忌": "嚴重肝功能不全、過敏",
        "副作用": "肝毒性（過量）、罕見過敏皮疹", "警語": "Max 75 mg/kg/day；間隔 ≥4 hr；勿與其他含 acetaminophen 製品併用",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    "acetaminophen_tab": {
        "臨床用途": "發燒、輕度疼痛", "禁忌": "嚴重肝功能不全",
        "副作用": "肝毒性（過量）、皮疹", "警語": "通常 ≥30 kg 才開錠劑；max 4 g/day（兒童 75 mg/kg/day）",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    "idefen_syrup": {
        "臨床用途": "發燒、發炎性疼痛", "禁忌": "<6 月、消化道潰瘍、aspirin 三聯（asthma+rhinitis+nasal polyp）、嚴重腎/肝衰竭",
        "副作用": "GI upset、消化道出血、急性腎損傷、血小板功能↓",
        "警語": "<6 月禁用；脫水/腎前性低灌流期間慎用；max 40 mg/kg/day",
        "懷孕分級": "AU TGA: C（第 3 trimester D）", "授乳": "相容", "管制性藥品": "—"
    },
    "voren_supp": {
        "臨床用途": "嬰幼兒退燒備用", "禁忌": "活動性消化道出血、嚴重腎衰、aspirin 三聯",
        "副作用": "GI upset、肛門刺激、罕見肝功能異常",
        "警語": "Max 2 supp/day；發燒未退時勿短時內重複 PR + PO NSAID",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 鼻水/過敏 =====
    "peace_syrup": {
        "臨床用途": "感冒鼻塞流鼻水（複方）", "禁忌": "MAOI 治療中、嚴重 HTN、CAD、甲亢",
        "副作用": "嗜睡、口乾、興奮（pseudoephedrine 部分）",
        "警語": "<2 歲不建議；含 pseudoephedrine 注意 BP/HR",
        "懷孕分級": "—", "授乳": "短期可", "管制性藥品": "—"
    },
    "cypromin_syrup": {
        "臨床用途": "過敏、流鼻水、止癢；亦用於食慾不振", "禁忌": "Glaucoma、BPH、MAOI、新生兒",
        "副作用": "嗜睡、口乾、體重增加（食慾↑）",
        "警語": "First-gen 抗組織胺，鎮靜效果明顯",
        "懷孕分級": "AU TGA: B2", "授乳": "短期可（可能↓奶量）", "管制性藥品": "—"
    },
    "cypromin_tab": {
        "臨床用途": "過敏、流鼻水、止癢", "禁忌": "Glaucoma、BPH、MAOI、新生兒",
        "副作用": "嗜睡、口乾", "警語": "First-gen 抗組織胺，注意嗜睡",
        "懷孕分級": "AU TGA: B2", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 止咳/感冒 =====
    "secorine_syrup": {
        "臨床用途": "感冒症狀緩解（複方）", "禁忌": "MAOI、嚴重 HTN",
        "副作用": "嗜睡、口乾、興奮",
        "警語": "<2 歲不建議；含 methylephedrine 注意 BP/HR",
        "懷孕分級": "—", "授乳": "短期可", "管制性藥品": "—"
    },
    "glyo_syrup": {
        "臨床用途": "止咳", "禁忌": "<1 歲、低鉀血症、嚴重高血壓",
        "副作用": "假性高醛固酮症（長期 / 大量）：高血壓、低鉀、水腫",
        "警語": "<1 歲避免（含複方甘草）；勿長期大量使用",
        "懷孕分級": "—", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 化痰 =====
    "actein_granule": {
        "臨床用途": "化痰（mucolytic）", "禁忌": "Acetylcysteine 過敏",
        "副作用": "GI upset、罕見支氣管痙攣（吸入劑型）",
        "警語": "氣喘患者慎用；與抗生素間隔 1-2 hr 服用",
        "懷孕分級": "AU TGA: B2", "授乳": "資料不足", "管制性藥品": "—"
    },
    "acc_effervescent": {
        "臨床用途": "化痰（mucolytic）", "禁忌": "Acetylcysteine 過敏",
        "副作用": "GI upset、口腔黏膜刺激",
        "警語": "<6 歲建議改用 granule 劑型；溶於水後立即服用",
        "懷孕分級": "AU TGA: B2", "授乳": "資料不足", "管制性藥品": "—"
    },
    "soltan_syrup": {
        "臨床用途": "化痰（mucolytic）", "禁忌": "Ambroxol 過敏",
        "副作用": "GI upset、罕見過敏",
        "警語": "罕見嚴重皮膚反應（Stevens-Johnson）",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 抗生素 =====
    "zithromax_susp": {
        "臨床用途": "Mycoplasma、中耳炎、咽炎、CAP", "禁忌": "Macrolide 過敏、肝功能異常",
        "副作用": "GI upset、味覺異常、QT 延長（高劑量）",
        "警語": "QT 延長風險（注意 baseline ECG）；mycoplasma 3 天即可",
        "懷孕分級": "AU TGA: B1", "授乳": "短期可", "管制性藥品": "—"
    },
    "zithromax_tab": {
        "臨床用途": "Mycoplasma、中耳炎、咽炎、CAP", "禁忌": "Macrolide 過敏",
        "副作用": "GI upset、QT 延長（高劑量）",
        "警語": "QT 延長風險；max 500 mg/day",
        "懷孕分級": "AU TGA: B1", "授乳": "短期可", "管制性藥品": "—"
    },
    "amoxicillin_susp": {
        "臨床用途": "中耳炎、咽炎、CAP、URI", "禁忌": "Penicillin 過敏",
        "副作用": "GI upset、皮疹（特別是 EBV 感染時）、罕見過敏性休克",
        "警語": "EBV / IM 感染時皮疹率高；中耳炎/CAP 用高劑量 80-90 mg/kg/day",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    "amoxicillin_cap": {
        "臨床用途": "中耳炎、咽炎、CAP、URI", "禁忌": "Penicillin 過敏",
        "副作用": "GI upset、皮疹",
        "警語": "通常 ≥30 kg 才開膠囊；高劑量 80-90 mg/kg/day",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    "curam_susp": {
        "臨床用途": "中耳炎、CAP、複雜 URI（amoxicillin/clavulanate 7:1）", "禁忌": "Penicillin 過敏、cholestatic jaundice 病史",
        "副作用": "GI upset（特別腹瀉）、皮疹、罕見肝功能異常",
        "警語": "Clavulanate 部分易拉肚子；中耳炎/CAP 80-90 mg/kg/day（amox 計）",
        "懷孕分級": "AU TGA: B1", "授乳": "相容", "管制性藥品": "—"
    },
    "curam_tab": {
        "臨床用途": "中耳炎、CAP、複雜 URI（875/125 tab）", "禁忌": "Penicillin 過敏、cholestatic jaundice 病史",
        "副作用": "GI upset、皮疹",
        "警語": "≥30 kg 適用；max 3 g/day amox",
        "懷孕分級": "AU TGA: B1", "授乳": "相容", "管制性藥品": "—"
    },
    # ===== 流感 =====
    "tamiflu": {
        "臨床用途": "Influenza A/B 治療與預防", "禁忌": "Oseltamivir 過敏",
        "副作用": "N/V（最常見）、頭痛、罕見神經精神症狀",
        "警語": "症狀 48 hr 內最有效；neuropsychiatric event 罕見但需衛教家屬",
        "懷孕分級": "AU TGA: B1", "授乳": "相容", "管制性藥品": "—"
    },
    "rapiacta_iv": {
        "臨床用途": "Influenza A/B 治療（無法口服 / 重症）", "禁忌": "Peramivir 過敏",
        "副作用": "腹瀉、罕見過敏、嗜中性球↓",
        "警語": "≥6 月適用；Single IV 15-30 min；嚴重肝腎功能異常需調量",
        "懷孕分級": "AU TGA: B1", "授乳": "資料不足", "管制性藥品": "—"
    },
    "xofluza_tab": {
        "臨床用途": "Influenza A/B 治療（單次口服）", "禁忌": "Baloxavir 過敏",
        "副作用": "腹瀉、頭痛（少見）",
        "警語": "≥1 歲適用；勿與含鈣 / 鎂 / 鐵製品併服（吸收↓）",
        "懷孕分級": "—（資料不足）", "授乳": "資料不足", "管制性藥品": "—"
    },
    "relenza_inh": {
        "臨床用途": "Influenza A/B 治療（吸入）", "禁忌": "氣喘、COPD、乳糖過敏",
        "副作用": "支氣管痙攣（氣喘患者）、頭痛、咳嗽",
        "警語": "≥7 歲適用；氣喘患者誘發 bronchospasm，使用前先用 bronchodilator",
        "懷孕分級": "AU TGA: B1", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== Croup / 支氣管擴張 =====
    "epinephrine_inh_croup": {
        "臨床用途": "Croup（中重度氣道阻塞）", "禁忌": "—（緊急情況下無絕對禁忌）",
        "副作用": "心跳↑、震顫、HTN（短暫）",
        "警語": "用後觀察 2-4 hr 看是否反彈（rebound）；類固醇併用降低 admit 機率",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    "terbutaline_neb": {
        "臨床用途": "氣喘、bronchiolitis bronchodilation", "禁忌": "Tachyarrhythmia 嚴重者",
        "副作用": "心跳↑、震顫、低鉀（高劑量）",
        "警語": "重複使用注意 K+；急性 asthma 與 ipratropium 併用",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    "ipratropium_neb": {
        "臨床用途": "氣喘急性發作（與 β-agonist 併用）", "禁忌": "Atropine 過敏、glaucoma",
        "副作用": "口乾、咳嗽、罕見急性 angle-closure glaucoma（眼睛接觸）",
        "警語": "與 β-agonist 併用發作前 24 hr；勿單獨用於急性發作",
        "懷孕分級": "AU TGA: B1", "授乳": "資料不足", "管制性藥品": "—"
    },
    "exdila_syrup": {
        "臨床用途": "氣喘 maintenance / mild bronchoconstriction", "禁忌": "Tachyarrhythmia",
        "副作用": "心悸、震顫、口乾",
        "警語": "≥6 歲建議；急性發作不適合（onset 慢）",
        "懷孕分級": "—", "授乳": "資料不足", "管制性藥品": "—"
    },
    "meptin_tab": {
        "臨床用途": "氣喘 maintenance", "禁忌": "Tachyarrhythmia 嚴重者",
        "副作用": "心悸、震顫",
        "警語": "Long-acting 形式；急性 asthma 用 nebulization",
        "懷孕分級": "—", "授乳": "資料不足", "管制性藥品": "—"
    },
    # ===== 類固醇 =====
    "prednisolone_tab": {
        "臨床用途": "Croup、Asthma、皮膚過敏、自體免疫", "禁忌": "活動性感染（系統性）、live vaccine 24 hr 內",
        "副作用": "短期：高血糖、情緒；長期：腎上腺抑制、Cushing 樣外觀、骨質疏鬆",
        "警語": "Croup / Asthma 短療程通常 3 天；無需 taper（療程 <14 天）",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    "methylpred_inj": {
        "臨床用途": "Croup、Asthma 急性發作、anaphylaxis", "禁忌": "Live vaccine 24 hr 內、systemic fungal infection",
        "副作用": "短期：高血糖、HTN；長期同 corticosteroid 全身副作用",
        "警語": "急性發作首選 IV/IM；通常 single dose 或 ≤72 hr",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    # ===== 止吐 =====
    "aswell_syrup": {
        "臨床用途": "Nausea / vomiting / GERD", "禁忌": "GI 阻塞 / 穿孔、pheochromocytoma、tardive dyskinesia 病史",
        "副作用": "嗜睡、躁動、EPS（年紀小風險高）",
        "警語": "<1 歲 EPS 風險高；併 diphenhydramine 預防 EPS；max 5 day 療程",
        "懷孕分級": "AU TGA: A", "授乳": "可（少量）", "管制性藥品": "—"
    },
    "promeran_tab": {
        "臨床用途": "Nausea / vomiting", "禁忌": "GI 阻塞 / 穿孔、tardive dyskinesia 病史",
        "副作用": "嗜睡、EPS、罕見 NMS",
        "警語": "Max 5 day 療程；急性 EPS 用 diphenhydramine 治療",
        "懷孕分級": "AU TGA: A", "授乳": "可", "管制性藥品": "—"
    },
    "primperan_inj": {
        "臨床用途": "Nausea / vomiting（急救快速）", "禁忌": "GI 阻塞 / 穿孔、pheochromocytoma",
        "副作用": "EPS（特別年紀小）、嗜睡、罕見 NMS",
        "警語": "Slow IV push（<2 min）；併 diphenhydramine 預防 EPS",
        "懷孕分級": "AU TGA: A", "授乳": "可", "管制性藥品": "—"
    },
    "novamin_inj": {
        "臨床用途": "Nausea / vomiting（IM 強效）", "禁忌": "<2 歲、嚴重 CNS depression、GI 阻塞",
        "副作用": "EPS、鎮靜、姿勢性低血壓",
        "警語": "<2 歲禁用；EPS 風險比 metoclopramide 低",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 腸胃道其他 =====
    "kascoal_tab": {
        "臨床用途": "脹氣、消化不良", "禁忌": "—",
        "副作用": "罕見過敏",
        "警語": "Simethicone 不吸收，安全性極高",
        "懷孕分級": "—", "授乳": "相容", "管制性藥品": "—"
    },
    "lgg_pack": {
        "臨床用途": "急性腸胃炎輔助、antibiotic-associated diarrhea 預防", "禁忌": "免疫低下 / 中央靜脈導管（罕見 sepsis 風險）",
        "副作用": "脹氣（短暫）",
        "警語": "免疫不全患者罕見 bacteremia；早產兒慎用",
        "懷孕分級": "—", "授乳": "相容", "管制性藥品": "—"
    },
    "mgo_tab": {
        "臨床用途": "便秘、消化不良（制酸）", "禁忌": "嚴重腎衰、腸阻塞",
        "副作用": "腹瀉、罕見高鎂血症（腎衰患者）",
        "警語": "腎衰患者勿用；max 2.1 g/day",
        "懷孕分級": "—", "授乳": "相容", "管制性藥品": "—"
    },
    "glycerin_supp": {
        "臨床用途": "便秘（PR）", "禁忌": "肛門撕裂 / 嚴重痔瘡",
        "副作用": "肛門刺激",
        "警語": "短期使用；勿與其他刺激性 laxative 併用",
        "懷孕分級": "—", "授乳": "相容", "管制性藥品": "—"
    },
    "smecta": {
        "臨床用途": "急性腹瀉（吸附型）", "禁忌": "腸阻塞",
        "副作用": "便秘",
        "警語": "與其他口服藥物間隔 1-2 hr 服用（吸附其他藥物）",
        "懷孕分級": "AU TGA: A", "授乳": "相容", "管制性藥品": "—"
    },
    # ===== 點滴 =====
    "taita1": {
        "臨床用途": "新生兒 / 嬰兒水分基底（D5W）", "禁忌": "高血糖、嚴重低鈉",
        "副作用": "輸液過量：水腫、稀釋性低鈉",
        "警語": "依 4-2-1 rule 計算 maintenance；嬰兒監測血糖",
        "懷孕分級": "—", "授乳": "—", "管制性藥品": "—"
    },
    "taita2": {
        "臨床用途": "兒童 maintenance（D5 1/3 saline）", "禁忌": "嚴重高/低鈉",
        "副作用": "輸液過量水腫；長時間使用 hypotonic 注意低鈉血症",
        "警語": "近年指南建議 isotonic（如 D5NS）；hypotonic 監測 Na",
        "懷孕分級": "—", "授乳": "—", "管制性藥品": "—"
    },
    "taita5": {
        "臨床用途": "兒童 maintenance（含較多葡萄糖）", "禁忌": "高血糖、嚴重高/低鈉",
        "副作用": "高血糖、靜脈炎（糖份高）",
        "警語": "糖份較高，IV 注入處易疼痛；糖尿病或 stress hyperglycemia 慎用",
        "懷孕分級": "—", "授乳": "—", "管制性藥品": "—"
    },
    # ===== 止痛針劑 =====
    "morphine_inj": {
        "臨床用途": "中重度疼痛", "禁忌": "呼吸抑制中、paralytic ileus、嚴重 asthma 急性期",
        "副作用": "呼吸抑制、嗜睡、N/V、便秘、瘙癢、histamine release",
        "警語": "新生兒劑量減半；呼吸抑制備 naloxone；緩慢 IV push",
        "懷孕分級": "AU TGA: C", "授乳": "短期可（小心嬰兒嗜睡）", "管制性藥品": "管 1"
    },
    "fentanyl_inj": {
        "臨床用途": "急性疼痛、procedural sedation analgesia", "禁忌": "呼吸抑制中、severe asthma",
        "副作用": "呼吸抑制、嗜睡、chest wall rigidity（快速 push）、低 BP",
        "警語": "Push 過快可能 chest wall rigidity；備 naloxone；slow IV over 1-2 min",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "管 1"
    },
    # ===== 鎮靜 =====
    "midazolam_dormicum": {
        "臨床用途": "Procedural sedation、anxiolysis、status epilepticus", "禁忌": "重症肌無力、acute angle-closure glaucoma、呼吸衰竭",
        "副作用": "呼吸抑制（與 opioid 共用尤其）、嗜睡、罕見 paradoxical agitation",
        "警語": "備 flumazenil；新生兒癲癇現場 IM/IN 是好選擇（RAMPART）",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "管 4"
    },
    "ketamine": {
        "臨床用途": "Procedural sedation、RSI induction、急性疼痛 sub-dissociative", "禁忌": "<3 月、active psychosis、未控制 HTN、global eyeball injury、thyrotoxicosis",
        "副作用": "BP↑、ICP↑、IOP↑、laryngospasm（罕見 ~0.4%）、emergence reaction、N/V、nystagmus、hypersalivation",
        "警語": "Barbiturates 不可同 syringe（precipitate）；備 atropine + midaz 處理 emergence；hemodynamic-stable，適合 hypotension/shock",
        "懷孕分級": "AU TGA: B3", "授乳": "短期可", "管制性藥品": "管 3"
    },
    "citosol": {
        "臨床用途": "Anesthesia induction、procedural sedation", "禁忌": "Porphyria、嚴重 asthma、status asthmaticus",
        "副作用": "呼吸抑制、低血壓、myocardial depression",
        "警語": "Slow IV titrate；備 airway equipment；老人 / 心衰減量",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "管 4"
    },
    "chloral_hydrate": {
        "臨床用途": "Procedural sedation（影像 / EEG）", "禁忌": "嚴重肝腎衰竭、嚴重心律不整",
        "副作用": "呼吸抑制（高劑量）、GI upset、罕見 arrhythmia",
        "警語": "近年因安全考量歐美已停產；單次 procedure max 100 mg/kg or 2 g",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 抽搐 =====
    "lorazepam_inj": {
        "臨床用途": "Status epilepticus first-line、anxiolysis", "禁忌": "重症肌無力、acute angle-closure glaucoma",
        "副作用": "呼吸抑制、嗜睡、罕見 paradoxical agitation",
        "警語": "Slow IV push over 2-5 min；備 flumazenil；max 4 mg/dose",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "管 4"
    },
    "diazepam_iv": {
        "臨床用途": "Status epilepticus second-line、anxiolysis、muscle spasm", "禁忌": "重症肌無力、嚴重呼吸衰竭",
        "副作用": "呼吸抑制、嗜睡、靜脈炎（IV）",
        "警語": "Slow IV push over 2-3 min；max 10 mg/dose；first-line 仍是 lorazepam",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "管 4"
    },
    "diazepam_pr": {
        "臨床用途": "院前 / 居家熱痙攣、status epilepticus（無 IV access）", "禁忌": "重症肌無力、肛門撕裂",
        "副作用": "呼吸抑制、嗜睡",
        "警語": "0.5 mg/kg PR；max 20 mg/dose；可 5-10 min 後再給一次",
        "懷孕分級": "AU TGA: C", "授乳": "短期可", "管制性藥品": "管 4"
    },
    "keppra_iv": {
        "臨床用途": "Status epilepticus second-line（loading）", "禁忌": "Levetiracetam 過敏",
        "副作用": "嗜睡、躁動、罕見精神症狀（aggression / depression）",
        "警語": "ESETT 2019: 60 mg/kg over 10 min；Renal impairment 需減量",
        "懷孕分級": "AU TGA: B3", "授乳": "短期可", "管制性藥品": "—"
    },
    "keppra_syrup": {
        "臨床用途": "Epilepsy maintenance（口服）", "禁忌": "Levetiracetam 過敏",
        "副作用": "嗜睡、躁動、行為改變（兒童）",
        "警語": "Initial 20 mg/kg/day → titrate 至 40-60 mg/kg/day；BID",
        "懷孕分級": "AU TGA: B3", "授乳": "短期可", "管制性藥品": "—"
    },
    "keppra_tab": {
        "臨床用途": "Epilepsy maintenance（口服）", "禁忌": "Levetiracetam 過敏",
        "副作用": "嗜睡、躁動",
        "警語": "Max 3000 mg/day；renal 調量",
        "懷孕分級": "AU TGA: B3", "授乳": "短期可", "管制性藥品": "—"
    },
    "depakine_iv": {
        "臨床用途": "Status epilepticus second-line（loading）", "禁忌": "肝病、線粒體疾病、urea cycle disorder、孕婦",
        "副作用": "肝毒性、胰臟炎、血小板↓、高血氨",
        "警語": "ESETT 2019: 40 mg/kg over 10 min；rate 1.5-3 mg/kg/min",
        "懷孕分級": "AU TGA: D", "授乳": "短期可", "管制性藥品": "—"
    },
    "depakine_syrup": {
        "臨床用途": "Epilepsy maintenance（口服）", "禁忌": "肝病、線粒體疾病、urea cycle disorder",
        "副作用": "肝毒性、體重↑、震顫、脫髮",
        "警語": "監測 LFT、CBC；目標血清 50-100 µg/mL；< 2 歲 hepatotoxicity 風險高",
        "懷孕分級": "AU TGA: D", "授乳": "短期可", "管制性藥品": "—"
    },
    "depakine_tab": {
        "臨床用途": "Epilepsy maintenance（口服）", "禁忌": "肝病、線粒體疾病、urea cycle disorder",
        "副作用": "肝毒性、體重↑、震顫",
        "警語": "≥30 kg 適合錠劑；< 2 歲 hepatotoxicity 風險高",
        "懷孕分級": "AU TGA: D", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 過敏/EPS =====
    "vena_inj": {
        "臨床用途": "急性過敏、anaphylaxis 輔助、EPS reversal", "禁忌": "<3 月、acute asthma 急性期",
        "副作用": "嗜睡、口乾、尿滯留、罕見 paradoxical agitation",
        "警語": "Anaphylaxis 仍以 epinephrine 為主；EPS 用 1-2 mg/kg IV",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    "vena_tab": {
        "臨床用途": "過敏、止癢、輕度鎮靜", "禁忌": "<3 月、glaucoma、BPH",
        "副作用": "嗜睡、口乾",
        "警語": "<3 歲慎用；max 5 mg/kg/day or 300 mg/day",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== 肌肉鬆弛 =====
    "succinylcholine": {
        "臨床用途": "RSI（快速肌肉鬆弛）", "禁忌": "燒傷 24 hr 後、上 / 下運動神經元損傷、嚴重高鉀、家族 malignant hyperthermia",
        "副作用": "高鉀血症、bradycardia（兒童特別）、myalgia、罕見 malignant hyperthermia",
        "警語": "兒童 IV 1-2 mg/kg / IM 3-4 mg/kg；備 atropine 預防 brady、dantrolene 處理 MH",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    # ===== PALS 急救藥 =====
    "epinephrine_arrest": {
        "臨床用途": "Cardiac arrest、anaphylaxis、severe bradycardia、croup（IH）", "禁忌": "—（緊急情況下無絕對禁忌）",
        "副作用": "心跳↑、HTN、震顫、肺水腫（過量）",
        "警語": "Arrest 用 1:10000（0.1 mg/mL）IV/IO 0.01 mg/kg；勿與 NaHCO3 同 IV line（inactivate）",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    "amiodarone_arrest": {
        "臨床用途": "Refractory VF/pVT、wide-QRS tachy", "禁忌": "嚴重 sinus brady、SA/AV block（無 pacemaker）、iodine 過敏",
        "副作用": "Hypotension（rapid push）、QT 延長、肺纖維化（長期）、肝/甲狀腺異常",
        "警語": "Arrest 時可 rapid push；非 arrest 用 IV over 20-60 min；max 300 mg first dose, 150 mg subsequent",
        "懷孕分級": "AU TGA: C", "授乳": "避免", "管制性藥品": "—"
    },
    "lidocaine_arrest": {
        "臨床用途": "Refractory VF/pVT 替代藥（無 amiodarone 時）", "禁忌": "嚴重 SA/AV block、Adams-Stokes",
        "副作用": "CNS（drowsiness、seizure 高劑量）、bradycardia、低 BP",
        "警語": "Bolus 1 mg/kg；ROSC 後 maintenance 20-50 µg/kg/min；max total 3 mg/kg",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    "atropine_brady": {
        "臨床用途": "Symptomatic bradycardia（vagal tone↑或 primary AV block）、organophosphate poisoning", "禁忌": "Glaucoma（angle-closure）、myasthenia gravis、tachyarrhythmia",
        "副作用": "口乾、視力模糊、心跳↑、尿滯留",
        "警語": "Min 0.1 mg（避免 paradoxical brady）；max 0.5 mg single；可 repeat 1 次",
        "懷孕分級": "AU TGA: A", "授乳": "短期可", "管制性藥品": "—"
    },
    "adenosine": {
        "臨床用途": "SVT 終止", "禁忌": "2nd/3rd degree AV block（無 pacemaker）、sick sinus syndrome、嚴重 asthma",
        "副作用": "短暫 asystole / heart block（預期反應）、flushing、胸悶、罕見 bronchospasm",
        "警語": "Rapid push + immediate flush（用 stopcock 雙針或最近 IV line）；半衰期 <10 sec；給藥前打開 ECG print",
        "懷孕分級": "AU TGA: B2", "授乳": "短期可", "管制性藥品": "—"
    },
}


def main():
    with open(JSON) as f:
        data = json.load(f)

    replaced = 0
    skipped = 0
    for d in data['drugs']:
        # 清掉舊的 kmuh_detail
        d.pop('kmuh_detail', None)
        if d['id'] in CLINICAL:
            d['kmuh_detail'] = CLINICAL[d['id']]
            replaced += 1
        else:
            skipped += 1

    with open(JSON, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ {replaced} 個藥用自整理 clinical summary 取代 KMUH 抓出資料")
    if skipped:
        print(f"   {skipped} 個藥沒寫（無 7 欄位）")


if __name__ == '__main__':
    main()
