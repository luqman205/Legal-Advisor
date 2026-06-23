import os
import json
import csv
import random
from typing import List, Dict, Any
from .utils import logger, get_config

LEGAL_DOCUMENTS_CORPUS: Dict[str, List[Dict[str, Any]]] = {
    "Family Laws": [
        {
            "title": "Nikah Nama Contract Clauses & column rights",
            "statute": "Section 5 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "A Nikahnama is a legally binding marriage contract in Islam. Critical columns include Column 18 (delegated right of divorce/Talaq-e-Tafweez to the wife), Column 19 (restrictions on the husband's right to contract a second marriage), and Column 20 (dower details—prompt dower payable immediately, deferred dower payable upon divorce or death). Striking out or leaving these columns blank restricts the wife's legal rights. It is highly advised that these columns are negotiated and filled out clearly during the Nikah ceremony.",
            "q_templates": [
                "What is Column 18 in Nikahnama, and how does it delegate divorce rights?",
                "What happens if Column 19 or 20 is left blank in Nikah Nama?",
                "What are the important columns to fill in a Nikahnama marriage contract?",
                "Can a wife divorce her husband using Nikahnama?",
                "What is prompt and deferred Haq Mehr in Nikah Nama?"
            ],
            "keywords": ["nikah nama", "column 18", "column 19", "column 20", "haq mehr", "prompt dower", "deferred dower", "talaq-e-tafweez"]
        },
        {
            "title": "Mandatory Marriage Registration under MFLO",
            "statute": "Section 5 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Under Section 5 of the Muslim Family Laws Ordinance 1961, every marriage contracted under Muslim Law must be registered with the local Nikah Registrar. A Nikahnama is the official marriage contract document, and failure to register is a punishable offense carrying a fine of up to Rs. 100,000, imprisonment of up to 3 months, or both. Although an unregistered marriage remains religiously valid, it is extremely difficult to prove in court for claiming legal rights like dower, maintenance, and inheritance.",
            "q_templates": [
                "Is marriage registration mandatory in Pakistan, and what are the requirements?",
                "What is the penalty for not registering a marriage in Pakistan?",
                "How do I register my Nikahnama if the registrar failed to do so?",
                "Is an unregistered Nikah valid under Pakistani law?",
                "How do I get my official marriage certificate from Union Council?"
            ],
            "keywords": ["marriage registration", "mandatory registration", "nikah registrar", "nikahnama", "marriage certificate", "union council", "unregistered nikah"]
        },
        {
            "title": "Polygamy & Second Marriage Permission",
            "statute": "Section 6 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Under Section 6 of the MFLO 1961, a husband must obtain prior written permission from the local Union Council's Arbitration Council to contract a second marriage during the subsistence of an existing marriage. He must show the consent of the existing wife and justify the second marriage. Conducting a second marriage without permission is a criminal offense, making the husband liable to pay the entire dower amount immediately, and exposing him to up to one year of imprisonment and a fine of up to Rs. 500,000.",
            "q_templates": [
                "Is prior consent from the first wife mandatory for a second marriage in Pakistan?",
                "What is the penalty for a husband marrying a second wife without court permission?",
                "How can a first wife file a complaint if her husband marries again without consent?",
                "Can a husband have two wives without permission in Pakistan?",
                "What happens to Haq Mehr if a husband marries a second time illegally?",
                "Can a man legally contract a second marriage in Pakistan?",
                "What is the law for a husband contracting a second marriage in Pakistan?"
            ],
            "keywords": ["man", "legally", "contract", "polygamy", "second marriage", "first wife consent", "arbitration council", "permission", "illegal marriage", "haq mehr payment", "husband contract"]
        },
        {
            "title": "Spousal Maintenance Claims (Wife's Nafqah)",
            "statute": "Section 9 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Under Section 9 of the Muslim Family Laws Ordinance 1961, a husband is legally bound to provide adequate spousal maintenance (Nafqah), including food, clothing, shelter, and medical care, to his wife. If he fails to do so, the wife can apply to the Union Council Chairman to constitute an Arbitration Council to issue a maintenance certificate. Alternatively, she can file a recovery suit in the Family Court. Past maintenance is recoverable for up to three years prior to filing.",
            "q_templates": [
                "How can a wife file a suit for maintenance or recovery of dower amount Rs. {amount} under MFLO?",
                "What is the procedure for a wife to claim monthly maintenance (Nafqah) if the husband refuses?",
                "How much past maintenance can a wife claim under Section 9 of the MFLO?",
                "My husband is not giving me monthly expenses. What should I do?",
                "Can a working wife claim monthly maintenance from her husband in Pakistan?"
            ],
            "keywords": ["maintenance", "wife support", "nafqah", "monthly expenses", "past maintenance", "union council", "family court"]
        },
        {
            "title": "Child Maintenance Obligations (Child Support)",
            "statute": "Section 9 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Under Pakistani law, a father is unconditionally bound to maintain his minor children, providing for their education, clothing, food, and shelter, regardless of child custody. A father must maintain sons until they reach the age of majority (18 years) and daughters until they get married. If the father refuses, a child maintenance suit can be filed in the Family Court, and unpaid maintenance can be recovered through court warrants or property attachment.",
            "q_templates": [
                "What is the father's legal obligation to pay monthly maintenance for children?",
                "How can I file a child maintenance suit in the Family Court, and how is the amount decided?",
                "Till what age must a father pay child support for sons and daughters in Pakistan?",
                "Does a father have to pay child expenses if the kids live with the mother?",
                "Can a father refuse to pay school fees of his children after divorce?"
            ],
            "keywords": ["child maintenance", "child support", "father duty", "school fees", "age of majority", "family court"]
        },
        {
            "title": "Divorce by Husband (Talaq Notice & Certificate)",
            "statute": "Section 7 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Under Section 7 of the MFLO 1961, a husband who wishes to divorce his wife must, after pronouncing Talaq, send a written notice to the local Union Council Chairman and supply a copy to the wife. The Talaq is suspended and does not become effective until 90 days from the notice delivery, during which the Union Council forms an Arbitration Council to attempt reconciliation. If it fails, a divorce effectiveness certificate is issued.",
            "q_templates": [
                "What is the complete legal procedure for registering a Talaq at the Union Council?",
                "How long does it take for a Talaq to become effective under Pakistani law?",
                "What if the husband does not send a divorce notice to the Union Council?",
                "Is verbal divorce valid without Union Council notice?",
                "What is the reconciliation period (iddat) for divorce?"
            ],
            "keywords": ["talaq", "divorce registration", "union council notice", "reconciliation", "arbitration council", "divorce certificate"]
        },
        {
            "title": "Divorce by Wife (Court Khula & Dower Waiver)",
            "statute": "Section 8 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Under Section 8 of the MFLO 1961, a wife wanting to dissolve her marriage without a delegated right of divorce must file a suit for Khula in the Family Court. The court will issue summons, hold pre-trial reconciliation, and if it fails, decree the Khula. As consideration for Khula, the wife is usually required to waive her deferred dower (Haq Mehr) or return a portion of the prompt dower she received.",
            "q_templates": [
                "What is the complete legal procedure for registered divorce or Khula under the MFLO?",
                "What is the difference between Khula and Talaq under Pakistani family law?",
                "How can a wife file a suit for Khula, and does she lose her Haq Mehr?",
                "How do I get Khula from court if my husband refuses to sign divorce?",
                "Does a wife have to return gifts and dower to get Khula?"
            ],
            "keywords": ["khula", "court divorce", "dower waiver", "reconciliation", "haq mehr", "family court"]
        },
        {
            "title": "Child Custody (Hizanat) - Mother's Primary Rights",
            "statute": "Section 17 of the Guardians and Wards Act, 1890",
            "source": "Guardians and Wards Act, 1890",
            "text": "Child custody (Hizanat) in Pakistan is decided based on the welfare and best interest of the minor. Under Islamic jurisprudence, the mother has the primary right of physical custody of minor boys up to 7 years of age and minor girls up to puberty. However, she can lose this right if she is proven unfit due to neglect/abuse, or if she contracts a second marriage with a stranger (ghair-mahram).",
            "q_templates": [
                "Who gets child custody (Hizanat) of minor children after divorce under the Guardians and Wards Act?",
                "Under what circumstances can a mother lose custody of her minor children?",
                "Can a mother claim custody of her children if she remarries another man?",
                "At what age does a mother lose custody of a boy or girl in Pakistan?",
                "Can my husband take away my 5-year-old child from me legally?"
            ],
            "keywords": ["child custody", "hizanat", "mother rights", "minor welfare", "unfit mother", "remarriage"]
        },
        {
            "title": "Child Custody - Father's Rights & Natural Guardianship",
            "statute": "Section 17 of the Guardians and Wards Act, 1890",
            "source": "Guardians and Wards Act, 1890",
            "text": "Under Pakistani law, the father is the natural legal guardian (Vilayah) of minor children, while the mother holds physical custody (Hizanat). The father is responsible for education, healthcare, and religion. A father can claim physical custody of a boy after 7 years of age and a girl after puberty by filing a petition in the Guardian Court, which evaluates if the transfer serves the child's welfare.",
            "q_templates": [
                "At what age can a father claim custody of a son or daughter in Pakistan?",
                "What is the difference between legal guardianship (Vilayah) and physical custody (Hizanat)?",
                "How can a father file a petition in the Guardian Court to get custody of his children?",
                "Does the father automatically get custody of children after they turn 7?",
                "Who is the natural legal guardian of a child under Pakistani law?"
            ],
            "keywords": ["father custody", "natural guardian", "vilayah", "guardianship", "guardian court", "child age"]
        },
        {
            "title": "Parental Visitation Rights & Schedules",
            "statute": "Section 12 of the Guardians and Wards Act, 1890",
            "source": "Guardians and Wards Act, 1890",
            "text": "The non-custodial parent (usually the father) has a legal right to meet his children. He can file a petition for visitation rights under Section 12 of the Guardians and Wards Act 1890. The Guardian Court sets a detailed visitation schedule (e.g. meetings in court premises, weekend home stays, or vacation custody). Violations of visitation schedules can result in court fines or modification of custody.",
            "q_templates": [
                "What are the legal rights of a non-custodial parent to meet their children?",
                "How can a father obtain court-ordered visitation rights (interim custody)?",
                "What is the penalty if a mother refuses to follow the court visitation schedule?",
                "Can I get my child's meeting schedule if my ex-wife blocks meetings?",
                "Can a father take his children home for weekends under court orders?"
            ],
            "keywords": ["visitation rights", "child visitation", "father meeting", "court schedule", "interim custody", "contempt of court"]
        },
        {
            "title": "Travel Consent & International Relocation of Minors",
            "statute": "Section 25 of the Guardians and Wards Act, 1890",
            "source": "Guardians and Wards Act, 1890",
            "text": "A parent holding physical custody cannot take minor children abroad or relocate them permanently without the written consent of the other parent (the natural guardian) or permission from the Guardian Court. Doing so constitutes removal from lawful custody. If a parent attempts to take children abroad illegally, the other parent can apply to place the children's names on the Exit Control List (ECL).",
            "q_templates": [
                "Does the mother need the father's consent as natural guardian to travel abroad with minor children?",
                "Can a parent relocate children to another city or country without court permission?",
                "How can I stop my ex-spouse from taking my children abroad without my consent?",
                "Can a mother make a child's passport without the father's signature?",
                "Can a father block a child from traveling abroad with the mother?"
            ],
            "keywords": ["travel consent", "passport", "international travel", "child abduction", "relocation", "exit control list", "ecl"]
        },
        {
            "title": "Iddat Period Rules and Rights",
            "statute": "Section 7 of the Muslim Family Laws Ordinance, 1961",
            "source": "Muslim Family Laws Ordinance, 1961",
            "text": "Iddat is the mandatory waiting period a Muslim woman must observe after divorce or her husband's death. For divorce, the iddat period is 90 days (or 3 menstruation cycles) from the date the divorce notice is received by the Union Council, or until delivery if pregnant. For the death of the husband, the iddat is 4 months and 10 days. During iddat, the husband must provide maintenance and housing.",
            "q_templates": [
                "What is the iddat period after divorce or the husband's death in Pakistan?",
                "Is the husband bound to pay maintenance to his wife during her iddat period?",
                "Can a woman marry another man during her iddat period under Pakistani law?",
                "How long is the waiting period (iddat) after divorce?",
                "What are the rights of a widow regarding iddat and maintenance?"
            ],
            "keywords": ["iddat", "waiting period", "widow", "divorce waiting", "iddat maintenance", "remarriage restriction"]
        },
        {
            "title": "Court Marriage Procedure & Consent",
            "statute": "Child Marriage Restraint Act & Specific Provisions of Shariah",
            "source": "Specific Provisions of Shariah",
            "text": "Court marriage in Pakistan is conducted through a civil process where an adult male and female (18 years or older) sign a Nikah contract in the presence of a Nikah Registrar and magistrate. The female must sign an affidavit of free will stating she is marrying without coercion. To protect themselves from false abduction FIRs filed by the bride's family, the couple should file a petition in the High Court seeking police protection.",
            "q_templates": [
                "What is the complete legal procedure for court marriage in Pakistan?",
                "Can parents file an abduction case if an adult couple does a court marriage?",
                "What is the minimum age limit and documentation required for a court marriage?",
                "How do I do a court marriage in Lahore or Karachi?",
                "How do I get police protection after a court marriage?"
            ],
            "keywords": ["court marriage", "free will", "affidavit", "police protection", "high court", "abduction case", "adult consent"]
        },
        {
            "title": "Legal Age of Marriage (Child Marriage Restraint Act)",
            "statute": "Child Marriage Restraint Act, 1929",
            "source": "Child Marriage Restraint Act, 1929",
            "text": "The legal age of marriage in Pakistan is governed by the Child Marriage Restraint Act. In Sindh, the minimum marriageable age is 18 years for both males and females. In Punjab, Islamabad, KPK, and Balochistan, the minimum age is 18 for males and 16 for females. Marrying or facilitating the marriage of a child below the legal age is a criminal offense punishable by fines and imprisonment of up to 2 years.",
            "q_templates": [
                "What is the minimum legal age of marriage for boys and girls in Punjab and Sindh?",
                "What is the penalty for child marriage or marrying a minor in Pakistan?",
                "Can a minor's Nikah be legally nullified under the Child Marriage Restraint Act?",
                "What is the legal age to get married in Karachi and Lahore?",
                "Can parents arrange a marriage for a 15 year old girl?"
            ],
            "keywords": ["legal age", "marriage age", "child marriage", "minor marriage", "punishment", "sindh marriage act"]
        },
        {
            "title": "Women's Inheritance Rights under Shariah",
            "statute": "Section 498-A of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Women in Pakistan are entitled to their legal inheritance shares under Shariah law. Denying a woman her inheritance by force, coercion, or deceit is a severe criminal offense under Section 498-A of the Pakistan Penal Code (PPC), carrying a punishment of 5 to 10 years imprisonment and a fine of up to Rs. 1 million. Aggrieved women can file suits in civil courts to recover their inherited property or register complaints. Under Shariah, daughters inherit property from their deceased father or mother, and widows inherit from their deceased husbands.",
            "q_templates": [
                "What are the inheritance rights of daughters and widows under Pakistani law?",
                "What is the penalty for denying a sister or daughter her share in family property?",
                "How can a woman recover her inherited property if her brothers refuse to give it?",
                "Do daughters get a share in father's land under Pakistani law?",
                "Can a father gift all his property to sons, excluding daughters?",
                "Do daughters inherit father's property under Pakistani law?"
            ],
            "keywords": ["inherit", "inheritance", "daughter inheritance", "women inheritance", "sister share", "section 498-a", "ppc", "shariah inheritance", "father property", "property inheritance"]
        }
    ],
    "Criminal Laws": [
        {
            "title": "FIR Registration & Refusal (Section 154 CrPC)",
            "statute": "Section 154 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Under Section 154 of the Code of Criminal Procedure (CrPC), police are legally bound to register a First Information Report (FIR) for cognizable offenses immediately upon receiving information. If the SHO refuses to register the FIR, the complainant can file a petition under Section 22-A & 22-B of the CrPC before the Sessions Judge (acting as Justice of Peace), who has the power to order the police to register the FIR and initiate investigation. A false FIR can be challenged in the High Court for quashment under Section 561-A CrPC.",
            "q_templates": [
                "How to register an FIR in Pakistan and what to do if SHO refuses?",
                "What is a Section 22-A petition for FIR registration?",
                "Can police refuse to file an FIR under Section 154 CrPC?",
                "My FIR is not being registered by the police. What is the legal remedy?",
                "What is the procedure for registering a police complaint for criminal actions?",
                "fir registration",
                "sho refused fir",
                "section 22-a petition",
                "false fir remedy"
            ],
            "keywords": ["fir", "police", "sho", "section 22-a", "refusal", "cognizable", "complaint", "quashment", "561-a"]
        },
        {
            "title": "Arrest Rights & Remand Safeguards (Section 54, 61, 167 CrPC)",
            "statute": "Sections 54, 61, and 167 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Under Section 54 of the CrPC, police can arrest a person without a warrant under specific conditions (e.g. involvement in a cognizable offense). However, Section 61 dictates that an arrested person cannot be detained in police custody for more than 24 hours without a magistrate's order under Section 167 (physical remand). The accused has a right to be informed of the grounds of arrest, consult legal counsel, and undergo medical examination if subjected to custodial violence.",
            "q_templates": [
                "What are my rights if arrested under Section 54 CrPC, and what is the remand limit?",
                "How long can police keep a suspect in custody without presenting them to a court?",
                "What is physical remand and judicial remand under Section 167 CrPC?",
                "Can police keep me in thana for more than 24 hours without court permission?",
                "What is the maximum duration of police physical remand in Pakistan?",
                "arrest rights",
                "physical remand duration",
                "detained by police",
                "24 hours custody"
            ],
            "keywords": ["arrest", "remand", "custody", "magistrate", "section 54", "remand limit", "police detention", "section 167", "section 61"]
        },
        {
            "title": "Pre-Arrest & Protective Bail (Section 498 CrPC)",
            "statute": "Section 498 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Pre-arrest bail is sought under Section 498 CrPC from the Sessions Court or High Court to prevent arrest in case of a false, malicious, or politically motivated FIR. The applicant must show that the arrest would cause irreparable loss of dignity and that there is prima facie malice on the part of the police or complainant. Protective bail is granted by a High Court to allow the accused to reach the concerned trial court without being arrested en route.",
            "q_templates": [
                "How can I apply for pre-arrest or protective bail under Section 498 CrPC?",
                "What is the difference between pre-arrest bail and protective bail under Pakistani law?",
                "Can I get protective bail from the High Court to avoid arrest?",
                "What are the requirements to obtain pre-arrest bail under section 498?",
                "I am facing a false criminal case and fear arrest. How do I get bail?",
                "pre-arrest bail",
                "protective bail",
                "bail before arrest",
                "section 498 bail"
            ],
            "keywords": ["bail", "pre-arrest bail", "protective bail", "section 498", "crpc", "arrest warrant", "malicious fir"]
        },
        {
            "title": "Post-Arrest Bail (Section 496 & 497 CrPC)",
            "statute": "Sections 496 and 497 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Post-arrest bail is filed after an accused is arrested. Under Section 496 CrPC, bail is a matter of right for bailable offenses. For non-bailable offenses, bail is governed by Section 497 CrPC, where the court exercises discretion. Bail is generally not granted if the offense falls under the prohibitory clause (punishable by death or life imprisonment), unless exceptions apply: the accused is under 16, a woman, or sick/infirm, or there are sufficient grounds for further inquiry.",
            "q_templates": [
                "What is the procedure for post-arrest bail in bailable and non-bailable offenses under Section 497 CrPC?",
                "Can a woman or a minor get bail easily in non-bailable offenses?",
                "What is the prohibitory clause in bail matters under Section 497?",
                "How can an accused get post-arrest bail after physical remand ends?",
                "What happens if a person is arrested for a non-bailable offense?",
                "post arrest bail",
                "section 497 bail",
                "bailable offense bail",
                "non bailable bail"
            ],
            "keywords": ["post-arrest bail", "bailable", "non-bailable", "section 496", "section 497", "prohibitory clause", "minor bail", "women bail"]
        },
        {
            "title": "Murder & Intentional Homicide (Section 302 PPC)",
            "statute": "Section 302 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 302 of the Pakistan Penal Code (PPC), Qatl-i-Amd (intentional murder) is punishable by: (a) death as Qisas (retribution); (b) death or imprisonment for life as Tazir (discretionary punishment) if proof is not up to Shariah standards; or (c) imprisonment for up to 25 years where Qisas is not applicable. The compromise in murder cases is allowed under Section 345 CrPC if the heirs of the victim agree to forgive or accept Diyat (blood money).",
            "q_templates": [
                "What is the punishment for murder under Section 302 PPC in Pakistan?",
                "What are Qisas, Diyat, and Tazir in homicide cases under Pakistani law?",
                "Can a murder case be settled out of court through compromise or blood money?",
                "What is Qatl-i-Amd and its legal penalty under the Pakistan Penal Code?",
                "What happens if heirs of a murder victim forgive the killer?",
                "302 ppc",
                "murder punishment",
                "diyat blood money",
                "qisas and diyat"
            ],
            "keywords": ["murder", "homicide", "302", "ppc", "qatl-i-amd", "qisas", "diyat", "tazir", "compromise", "death penalty"]
        },
        {
            "title": "Types of Homicide: Qatl-i-Shibh-i-Amd, Qatl-i-Khata, Qatl-bis-Sabab",
            "statute": "Sections 315, 318, and 321 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Unintentional homicides under the PPC include: 1) Qatl-i-Shibh-i-Amd (Section 315 PPC - act with intent to cause hurt but causing death, punished with Diyat and up to 25 years imprisonment); 2) Qatl-i-Khata (Section 318 PPC - death caused by mistake or accident without intent, punished with Diyat and up to 10 years imprisonment); and 3) Qatl-bis-Sabab (Section 321 PPC - causing death by an unlawful intermediary act, punished with Diyat and up to 5 years).",
            "q_templates": [
                "What is Qatl-i-Khata and the punishment for accidental death in Pakistan?",
                "What is the difference between Qatl-i-Amd and Qatl-i-Shibh-i-Amd?",
                "What is the penalty for causing death by negligence or accident under PPC?",
                "What is Qatl-bis-Sabab and when is it applicable?",
                "accidental death law",
                "qatl-i-khata penalty",
                "unintentional murder"
            ],
            "keywords": ["homicide", "qatl", "shibh-i-amd", "khata", "bis-sabab", "accidental death", "negligence", "diyat", "section 315", "section 318", "section 321"]
        },
        {
            "title": "Bodily Hurt & Injuries: Shajjah, Jurh, Arsh, and Daman",
            "statute": "Sections 332 and 337 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 332 PPC, hurt is defined as causing pain, harm, disease, infirmity, or injury. It is divided into: 1) Shajjah (injuries on head or face, Section 337-A PPC); and 2) Jurh (bodily wounds, Section 337-B PPC). Punishments include Qisas or payment of compensation: 'Arsh' (fixed compensation under law, e.g., for loss of limb or organ) or 'Daman' (court-determined compensation for other injuries), along with imprisonment up to 10 years depending on severity.",
            "q_templates": [
                "What are the legal punishments for causing bodily hurt or injury under Section 337 PPC?",
                "What is the difference between Arsh and Daman compensation under Pakistani law?",
                "What is Shajjah and Jurh and their legal penalties under the Pakistan Penal Code?",
                "How is compensation calculated for losing a limb or eye in an assault?",
                "hurt laws",
                "shajjah and jurh",
                "arsh daman",
                "assault injury punishment"
            ],
            "keywords": ["hurt", "injury", "assault", "shajjah", "jurh", "arsh", "daman", "compensation", "section 337", "bodily harm"]
        },
        {
            "title": "Kidnapping & Abduction Penalties under PPC",
            "statute": "Sections 359, 361, 365, and 365-A of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 359 PPC, kidnapping can be from Pakistan or from lawful guardianship (Section 361, taking a minor under 14 for males or 16 for females without consent). Kidnapping or abducting with intent to cause secret confinement is punished under Section 365 PPC with up to 7 years. Kidnapping for ransom (Section 365-A PPC) is a grave offense tried under the Anti-Terrorism Act, carrying the death penalty or imprisonment for life, along with forfeiture of property.",
            "q_templates": [
                "What is the punishment for kidnapping or abduction under Section 365 PPC?",
                "What are the legal penalties for kidnapping for ransom under Section 365-A PPC?",
                "What constitutes kidnapping from lawful guardianship under Pakistani law?",
                "What is the difference between kidnapping and abduction under the PPC?",
                "kidnapping for ransom",
                "abduction under 365-a",
                "minor kidnapping law"
            ],
            "keywords": ["kidnapping", "abduction", "ransom", "minor kidnapping", "guardianship", "section 365", "section 365-a", "death penalty", "confining"]
        },
        {
            "title": "Theft, Robbery, & Dacoity Penalties under PPC",
            "statute": "Sections 378, 379, 390, 392, and 395 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Theft (Section 378 PPC) involves dishonestly moving property without consent, carrying up to 3 years imprisonment under Section 379. Theft in a house (Section 380) carries up to 7 years. Robbery (Section 390) is theft or extortion accompanied by immediate threat of death or hurt, carrying up to 10 years (or 14 years on highways at night under Section 392). Dacoity (Section 395) is robbery committed by a gang of 5 or more persons, carrying up to life imprisonment or 10 years and fine.",
            "q_templates": [
                "What is the penalty for committing theft under Section 379 PPC or robbery under Section 392 PPC?",
                "What constitutes dacoity and what is its punishment under Section 395 PPC?",
                "What is the penalty for house-breaking or stealing from a house in Pakistan?",
                "What is the difference between theft, robbery, and dacoity under PPC?",
                "theft 379 ppc",
                "robbery highway night",
                "dacoity gang penalty"
            ],
            "keywords": ["theft", "mischief", "robbery", "dacoity", "stealing", "housebreaking", "section 379", "section 392", "section 395", "punishment", "gang robbery"]
        },
        {
            "title": "Rape & Sexual Assault Laws (Zina-bil-Jabr)",
            "statute": "Sections 375 and 376 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 375 PPC, Zina-bil-Jabr (rape) is defined as sexual intercourse with a woman against her consent, without her consent, or under coercion/deception. Under Section 376 PPC, rape is punished with death or imprisonment for a term not less than 10 years and up to 25 years, along with a fine. Gang rape (Section 376(2) PPC) carries mandatory death or life imprisonment. Conduct of DNA testing and forensic examinations is legally mandatory in rape investigations.",
            "q_templates": [
                "What is the punishment for rape or sexual assault under Section 376 PPC?",
                "What is the law on gang rape in Pakistan and its legal penalties?",
                "Is DNA testing mandatory for rape cases in Pakistan?",
                "What constitutes rape (Zina-bil-Jabr) under the Pakistan Penal Code?",
                "rape punishment",
                "sexual assault law",
                "dna test rape case"
            ],
            "keywords": ["rape", "assault", "sexual assault", "zina-bil-jabr", "forensic", "dna test", "section 375", "section 376", "death penalty", "gang rape"]
        },
        {
            "title": "Criminal Defamation & Libel under PPC",
            "statute": "Sections 499 and 500 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 499 PPC, defamation involves making or publishing false imputations concerning a person, intending to harm or knowing it will harm their reputation. It includes spoken words, writing, or representations. Defamation is a criminal offense under Section 500 PPC, carrying a punishment of up to 2 years imprisonment, a fine, or both. Truth for public good and fair comment are legal exceptions.",
            "q_templates": [
                "What is the penalty for criminal defamation under Section 500 PPC?",
                "How do I file a criminal defamation case in Pakistan for false statements?",
                "What constitutes defamation under Section 499 PPC and what are its exceptions?",
                "Can I go to jail for writing false comments about someone online or in print?",
                "defamation law",
                "section 500 ppc",
                "reputation damage",
                "libel slander"
            ],
            "keywords": ["defamation", "libel", "slander", "reputation", "false accusation", "section 499", "section 500", "imprisonment", "fine"]
        },
        {
            "title": "Dishonestly Issuing Bounced Cheques (Section 489-F PPC)",
            "statute": "Section 489-F of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 489-F of the Pakistan Penal Code (PPC), anyone who dishonestly issues a cheque for repayment of a loan or fulfillment of an obligation, which is dishonored upon presentation, commits a criminal offense. The punishment is up to 3 years imprisonment, a fine, or both. The complainant must prove that the cheque was issued with dishonest intent and bounced due to insufficient funds or closed accounts.",
            "q_templates": [
                "What is the penalty for cheque bounce under Section 489-F PPC in Pakistan?",
                "How do I register an FIR for a bounced cheque and what is the legal process?",
                "Can a person get bail in a cheque bounce case under Section 489-F?",
                "What are the defenses available if my cheque bounced and a case is filed?",
                "cheque bounce",
                "section 489-f ppc",
                "bounced check",
                "dishonor of cheque"
            ],
            "keywords": ["cheque", "bounce", "dishonor", "section 489-f", "ppc", "bounced check", "cheque bouncing", "loan repayment", "bail"]
        },
        {
            "title": "Cheating and Fraud Penalties under PPC",
            "statute": "Sections 415 and 420 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Cheating (Section 415 PPC) involves deceiving a person to deliver property or consent to retain property, or inducing them to do or omit an act causing harm to body, mind, or reputation. Cheating and dishonestly inducing delivery of property is punished under Section 420 PPC with up to 7 years imprisonment and a fine. It is a cognizable and non-bailable offense.",
            "q_templates": [
                "What is the punishment for cheating and fraud under Section 420 PPC?",
                "What constitutes cheating under Section 415 PPC and how do I file a fraud case?",
                "My business partner defrauded me of property. What is the legal action?",
                "Can I register an FIR under Section 420 PPC for financial fraud?",
                "cheating 420",
                "fraud case ppc",
                "financial fraud"
            ],
            "keywords": ["cheating", "fraud", "defrauded", "420", "section 420", "ppc", "deception", "property delivery"]
        },
        {
            "title": "Criminal Breach of Trust & Embezzlement under PPC",
            "statute": "Sections 405, 406, and 409 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Criminal Breach of Trust (Section 405 PPC) occurs when someone is entrusted with property and dishonestly misappropriates or converts it to their own use. It is punished under Section 406 PPC with up to 7 years imprisonment, a fine, or both. If committed by a public servant, banker, merchant, or agent, it is punished under Section 409 PPC with imprisonment for life or up to 10 years and a fine.",
            "q_templates": [
                "What is the punishment for criminal breach of trust under Section 406 PPC?",
                "What constitutes criminal breach of trust by a public servant or banker under Section 409 PPC?",
                "How is embezzlement of entrusted property penalized under Pakistani law?",
                "My agent sold my property and pocketed the cash. Can I file a breach of trust case?",
                "breach of trust",
                "section 406 ppc",
                "section 409 public servant"
            ],
            "keywords": ["breach of trust", "embezzlement", "misappropriation", "trustee", "agent fraud", "section 406", "section 409", "entrusted property"]
        },
        {
            "title": "Forgery & Fabrication of Fake Documents under PPC",
            "statute": "Sections 463, 464, 468, and 471 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Forgery (Section 463 PPC) is making a false document or electronic record with intent to cause damage or commit fraud. Forgery for the purpose of cheating is punished under Section 468 PPC with up to 7 years imprisonment and a fine. Using a forged document as genuine (knowing it is forged) is penalized under Section 471 PPC with the same punishment as if the document was forged by the user.",
            "q_templates": [
                "What is the penalty for fabricating fake land documents or registry forgery under Section 468 PPC?",
                "What constitutes forgery under Section 463 PPC and what are the penalties?",
                "What is the punishment under Section 471 PPC for using forged papers as genuine?",
                "Someone made a fake power of attorney in my name. What is the criminal penalty?",
                "forgery fake document",
                "section 468 forgery",
                "section 471 fake paper"
            ],
            "keywords": ["forgery", "fake document", "fabrication", "power of attorney", "fake signature", "section 468", "section 471", "cheating"]
        },
        {
            "title": "Criminal Trespass & Property Damage under PPC",
            "statute": "Sections 427, 441, and 447 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Criminal Trespass (Section 441 PPC) is entering another's property with intent to commit an offense, or to intimidate, insult, or annoy. It is punished under Section 447 PPC with up to 3 months imprisonment and a fine. Mischief causing damage to property (Section 425/427 PPC) is punished with up to 2 years imprisonment or fine if the damage caused is fifty rupees or more.",
            "q_templates": [
                "What is the punishment for criminal trespass under Section 447 PPC?",
                "What is the penalty for damaging property or house trespass under Section 427 PPC?",
                "My neighbor entered my land forcefully and destroyed my crops. What is the law?",
                "What constitutes criminal trespass on private property?",
                "criminal trespass 447",
                "property damage 427"
            ],
            "keywords": ["trespass", "criminal trespass", "property damage", "mischief", "encroach", "section 447", "section 427", "annoyance"]
        },
        {
            "title": "Narcotics Possession Penalties under CNSA 1997",
            "statute": "Section 9 of the Control of Narcotics Substances Act, 1997",
            "source": "Control of Narcotics Substances Act (CNSA), 1997",
            "text": "Under Section 9 of the Control of Narcotics Substances Act (CNSA) 1997, penalties for possessing, trafficking, or financing narcotics (Charas, Heroin, Opium, Ice) are scaled by quantity: (a) up to 2 years for under 100 grams; (b) up to 7 years and fine for 100 grams to 1 kilogram; and (c) death penalty or life imprisonment (with a minimum of 14 years) and a fine for quantities exceeding 1 kilogram.",
            "q_templates": [
                "What is the punishment for drug possession or carrying narcotics under the CNSA 1997?",
                "What are the penalties for possession of more than 1 kg of drugs (Section 9-C CNSA)?",
                "Is bail granted in narcotics or drug trafficking cases in Pakistan?",
                "What are the legal limits of drug quantities and their respective punishments?",
                "cnsa drug possession",
                "section 9-c narcotics",
                "trafficking drug penalty"
            ],
            "keywords": ["drugs", "narcotics", "cnsa", "charas", "heroin", "opium", "ice", "possession", "trafficking", "section 9-c", "life imprisonment"]
        },
        {
            "title": "Cyber Crimes & Harassment under PECA 2016",
            "statute": "Prevention of Electronic Crimes Act (PECA), 2016",
            "source": "Prevention of Electronic Crimes Act (PECA), 2016",
            "text": "The Prevention of Electronic Crimes Act (PECA) 2016 criminalizes digital offenses. Under Section 20, dignity of a natural person is protected (defamation/online slander, up to 3 years). Under Section 21, uploading or sharing sexually explicit photos/videos without consent carries up to 5 years. Cyberstalking and online harassment of women are penalized under Section 24. Complaints are filed with the FIA Cyber Crime Wing.",
            "q_templates": [
                "How do I file a complaint for online harassment or cyber stalking under PECA 2016?",
                "What is the punishment for sharing private photos online without consent under PECA?",
                "What is the penalty for online defamation or fake accounts under Section 20 PECA?",
                "How does the FIA Cyber Crime Wing handle online blackmailing or extortion?",
                "cyber crime fia",
                "peca 2016 harassment",
                "online blackmailing"
            ],
            "keywords": ["cyber", "online", "harassment", "stalking", "peca", "fia", "blackmail", "defamation", "explicit photo", "spoofing"]
        },
        {
            "title": "Anti-Terrorism Act & Violent Crimes in Pakistan",
            "statute": "Section 6 of the Anti-Terrorism Act, 1997",
            "source": "Anti-Terrorism Act (ATA), 1997",
            "text": "Under Section 6 of the Anti-Terrorism Act (ATA) 1997, terrorism is defined as any act designed to coerce, intimidate, or overawe the government, public, or sect, by causing death, grievous bodily harm, extortion, or sectarian hatred. Cases are tried in special Anti-Terrorism Courts (ATC) with rapid trial schedules. Punishments include death, life imprisonment, and forfeiture of property. Bail is highly restricted.",
            "q_templates": [
                "What is the legal definition of terrorism under Section 6 of the Anti-Terrorism Act?",
                "What are the penalties and trial procedures in Anti-Terrorism Courts (ATC)?",
                "Are extortion and target killing tried under the Anti-Terrorism Act in Pakistan?",
                "Can an accused get bail in an ATA case?",
                "anti terrorism act",
                "atc court trial",
                "sectarian violence law"
            ],
            "keywords": ["terrorism", "ata", "atc", "extortion", "target killing", "sectarian", "anti-terrorism", "grievous harm"]
        },
        {
            "title": "Right of Private Defense (Self-Defense) under PPC",
            "statute": "Sections 96 to 106 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 96 PPC, nothing is an offense which is done in the exercise of the right of private defense. Section 97 grants the right to defend one's body and property. Under Section 100 PPC, the right of private defense of the body extends to causing death if there is reasonable apprehension of: death, grievous hurt, rape, unnatural lust, kidnapping, or wrongful confinement. The right must not exceed the harm necessary.",
            "q_templates": [
                "What is the law of self-defense (right of private defense) under the PPC?",
                "When does the right of private defense of the body extend to causing death (Section 100 PPC)?",
                "Can I kill someone in self-defense under Pakistani law if attacked?",
                "What are the limitations of the right of private defense of property?",
                "self defense law",
                "private defense 100 ppc",
                "killing in self defense"
            ],
            "keywords": ["self-defense", "private defense", "defend", "body", "property", "section 96", "section 100", "open-guard", "attacked", "justification"]
        },
        {
            "title": "Criminal Court Hierarchy & Sentencing Jurisdiction (Section 6 CrPC)",
            "statute": "Sections 6, 28, 29, 31, and 32 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Under Section 6 of the Code of Criminal Procedure (CrPC), criminal cases in Pakistan are tried by the High Courts, Courts of Session (Sessions Judges and Additional Sessions Judges), and Judicial Magistrates. Judicial Magistrates are divided into three classes: 1) Magistrate of the First Class (can sentence up to 3 years imprisonment and Rs. 45,000 fine); 2) Magistrate of the Second Class (up to 1 year and Rs. 15,000 fine); and 3) Magistrate of the Third Class (up to 1 month and Rs. 3,000 fine). Sessions Judges can pass any sentence authorized by law, including the death penalty (which requires High Court confirmation). Special courts like Anti-Terrorism Courts (ATC) and CNS Courts try specific offences.",
            "q_templates": [
                "Which courts hear criminal cases in Pakistan and what are their sentencing powers?",
                "What is the hierarchy of criminal courts under Section 6 of the CrPC?",
                "Criminal cases kis adalat mein sune jate hain?",
                "What is the sentencing power of a First Class Magistrate in Pakistan?",
                "Can a Sessions Judge award the death penalty under Pakistani law?",
                "criminal court jurisdiction",
                "court hierarchy crpc",
                "sessions court powers",
                "magistrate court classes"
            ],
            "keywords": ["adalat", "court", "criminal cases", "hierarchy", "magistrate", "sessions court", "high court", "sentencing power", "jurisdiction", "section 6", "section 31", "section 32", "crpc"]
        },
        {
            "title": "Private Criminal Complaint / Istighasa (Section 200 CrPC)",
            "statute": "Section 200 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Under Section 200 of the Code of Criminal Procedure (CrPC), an aggrieved person can file a direct private criminal complaint (known as Istighasa) before a Magistrate of competent jurisdiction, completely bypassing the police. The Magistrate examines the complainant on oath, records their statement, and if prima facie evidence exists, issues summons or warrants to the accused. This is a vital legal remedy when the police refuse to register an FIR (Section 154) or if the police investigation is suspected to be biased.",
            "q_templates": [
                "How do I file a private criminal complaint (Istighasa) directly in court under Section 200 CrPC?",
                "What is Istighasa and how is it filed when police refuses to cooperate?",
                "Can I bypass the police and file a criminal case directly before a Magistrate?",
                "What is the procedure of a private complaint under Section 200 of the CrPC?",
                "private complaint court",
                "istighasa procedure",
                "direct criminal case",
                "section 200 crpc"
            ],
            "keywords": ["istighasa", "private complaint", "complaint", "magistrate", "bypass police", "section 200", "sworn statement", "summons", "crpc"]
        },
        {
            "title": "Cognizable vs Non-Cognizable Offenses & Arrest Powers",
            "statute": "Section 4(1)(f) and 4(1)(n) of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "Under the Code of Criminal Procedure (CrPC), offenses are divided into two main categories: 1) Cognizable Offense (Section 4(1)(f)): A serious offense (e.g., murder, theft, rape) where police can arrest the accused without a warrant and initiate an investigation without magistrate approval. 2) Non-Cognizable Offense (Section 4(1)(n)): A less severe offense (e.g., simple assault, defamation) where police cannot arrest without a warrant, and can only investigate upon receiving a direct order from a Magistrate under Section 155 CrPC.",
            "q_templates": [
                "What is the difference between cognizable and non-cognizable offenses in Pakistan?",
                "Can police arrest someone without an arrest warrant under Pakistani law?",
                "When does the police need a warrant to make an arrest under the CrPC?",
                "What is a cognizable offense under Section 4-1-f of the CrPC?",
                "arrest without warrant",
                "cognizable offense",
                "non-cognizable warrant",
                "police arrest power"
            ],
            "keywords": ["cognizable", "non-cognizable", "warrant", "arrest without warrant", "section 4", "police power", "crpc", "investigation"]
        },
        {
            "title": "Police Statements (Section 161) vs Judicial Confessions (Section 164)",
            "statute": "Sections 161 and 164 of the Code of Criminal Procedure, 1898",
            "source": "Code of Criminal Procedure (CrPC), 1898",
            "text": "During investigation, statements recorded by the police under Section 161 CrPC are not signed by the witness and cannot be used as primary evidence in court against the accused. Conversely, a confession or statement recorded under Section 164 CrPC is made voluntarily before a Magistrate. The Magistrate must warn the accused that they are not bound to confess, and that any confession can be used against them. A Section 164 judicial confession is highly admissible as substantive evidence.",
            "q_templates": [
                "What is the difference between a Section 161 statement to police and a Section 164 confession before a Magistrate?",
                "Are statements given to the police during interrogation admissible in court?",
                "What are the requirements for a valid judicial confession under Section 164 CrPC?",
                "Can I retract a confession made under police pressure?",
                "161 statement police",
                "164 confession magistrate",
                "judicial statement",
                "police pressure confession"
            ],
            "keywords": ["confession", "statement", "section 161", "section 164", "magistrate confession", "police statement", "admissibility", "evidence", "interrogation"]
        },
        {
            "title": "Penalties for False Accusation & Malicious Prosecution (Section 182 & 211 PPC)",
            "statute": "Sections 182 and 211 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Filing false criminal charges carries severe penalties under the Pakistan Penal Code (PPC). Under Section 182 PPC, giving false information to a public servant with intent to cause them to use their lawful power to injure someone is punished with up to 6 months imprisonment, a fine, or both. Under Section 211 PPC, falsely instituting criminal proceedings with intent to cause injury to a person is punished with up to 2 years imprisonment, a fine, or both; if the false charge is for an offense carrying death or life imprisonment, the false accuser can face up to 7 years in prison.",
            "q_templates": [
                "What is the punishment for filing a false FIR or false police complaint under PPC?",
                "What are the penalties for false accusation under Section 211 PPC?",
                "What constitutes a crime under Section 182 PPC for lying to the police?",
                "Can I sue someone for malicious prosecution if they filed a fake case against me?",
                "false fir punishment",
                "fake complaint penalty",
                "section 182 ppc",
                "section 211 fake case"
            ],
            "keywords": ["false accusation", "fake case", "malicious prosecution", "lying to police", "section 182", "section 211", "false charges", "ppc"]
        },
        {
            "title": "Exemptions & Limits of Right of Private Defense (Section 99 PPC)",
            "statute": "Section 99 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "The right of private defense is subject to strict limitations under Section 99 of the Pakistan Penal Code (PPC). There is no right of private defense: 1) Against an act done by a public servant (e.g., police officer) in good faith under color of their office, even if not strictly justifiable by law; 2) Against an act done by direction of a public servant; 3) In cases where there is time to seek protection of public authorities; and 4) The right in no case extends to inflicting more harm than is necessary for the purpose of defense.",
            "q_templates": [
                "What are the limitations of the right of self-defense under Section 99 PPC?",
                "Can I use self-defense against a police officer executing a warrant?",
                "When is self-defense not allowed under the Pakistan Penal Code?",
                "What constitutes excessive force in self-defense under Section 99 PPC?",
                "self defense limits",
                "section 99 ppc",
                "no self defense",
                "excessive force law"
            ],
            "keywords": ["self-defense", "private defense", "limits", "section 99", "public servant", "police defense", "excessive force", "limitations", "ppc"]
        },
        {
            "title": "Criminal Conspiracy Penalties (Section 120-A & 120-B PPC)",
            "statute": "Sections 120-A and 120-B of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 120-A of the Pakistan Penal Code (PPC), a criminal conspiracy is defined as an agreement between two or more persons to do or cause to be done: 1) An illegal act, or 2) An act which is not illegal by illegal means. Under Section 120-B PPC, whoever is a party to a criminal conspiracy to commit an offense carrying death, life imprisonment, or rigorous imprisonment of 2 years or more shall be punished in the same manner as if they had abetted the offense (if no express punishment is provided). For other conspiracies, the punishment is up to 6 months imprisonment, a fine, or both.",
            "q_templates": [
                "What is the punishment for criminal conspiracy under Section 120-B PPC?",
                "What constitutes a criminal conspiracy under Section 120-A of the PPC?",
                "How is a conspiracy to commit a crime penalized in Pakistan?",
                "Can I be charged with a crime if I only planned it with others but didn't execute it?",
                "criminal conspiracy",
                "section 120-b conspiracy",
                "planning a crime penalty",
                "section 120-a ppc"
            ],
            "keywords": ["conspiracy", "criminal conspiracy", "agreement", "planning crime", "section 120-a", "section 120-b", "abettor", "ppc"]
        },
        {
            "title": "Assaulting or Outraging Modesty of a Woman (Section 354, 354-A, 509 PPC)",
            "statute": "Sections 354, 354-A, and 509 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "The PPC severely penalizes offenses against women's dignity. Under Section 354 PPC, assaulting or using criminal force on a woman with intent to outrage her modesty is punished with up to 2 years imprisonment, a fine, or both. Under Section 354-A PPC, assaulting or using force on a woman and stripping her of her clothes or exposing her to public view is a heinous crime carrying the death penalty or life imprisonment. Under Section 509 PPC, insulting the modesty of a woman by words, sounds, gestures, or exhibiting objects is punished with up to 3 years imprisonment and a fine.",
            "q_templates": [
                "What is the punishment for harassing or insulting the modesty of a woman under Section 509 PPC?",
                "What are the penalties for assaulting a woman to outrage her modesty under Section 354 PPC?",
                "What is Section 354-A PPC and its punishment for stripping a woman?",
                "What is the legal remedy for workplace or public harassment of women in Pakistan?",
                "harassment of women",
                "section 509 ppc",
                "section 354-a stripping",
                "outrage woman modesty"
            ],
            "keywords": ["harassment", "modesty", "women", "assaulting woman", "section 354", "section 354-a", "section 509", "stripping", "public exposure", "workplace harassment", "ppc"]
        },
        {
            "title": "Kidnapping or Abducting a Minor (Section 361 & 363 PPC)",
            "statute": "Sections 361 and 363 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 361 of the Pakistan Penal Code (PPC), kidnapping from lawful guardianship is defined as taking or enticing any minor (under 14 years for males, or under 16 years for females) or any person of unsound mind, out of the keeping of their lawful guardian, without the guardian's consent. Under Section 363 PPC, whoever commits this offense is punished with imprisonment of up to 7 years and a fine.",
            "q_templates": [
                "What is the punishment for kidnapping a minor from their parents under Section 363 PPC?",
                "What constitutes kidnapping from lawful guardianship under Section 361 PPC?",
                "What is the age limit for kidnapping of minor males and females under PPC?",
                "Can a parent be charged with kidnapping their own child?",
                "minor kidnapping",
                "section 361 guardianship",
                "section 363 minor kidnapping",
                "lawful guardian consent"
            ],
            "keywords": ["kidnapping", "minor", "guardianship", "lawful guardian", "section 361", "section 363", "enticing", "consent", "ppc"]
        },
        {
            "title": "Juvenile Justice System & Child Rights in Criminal Law (JJSA 2018)",
            "statute": "Sections 6, 9, 12, and 16 of the Juvenile Justice System Act, 2018",
            "source": "Juvenile Justice System Act (JJSA), 2018",
            "text": "The Juvenile Justice System Act (JJSA) 2018 provides special legal protections for children under 18 accused of crimes. Key safeguards include: 1) Absolute prohibition of the death penalty for juvenile offenders; 2) Prohibition of handcuffing or placing juveniles in police lockups alongside adult criminals; 3) Mandatory right to bail for children accused of minor or major offenses (except heinous offenses if there are reasonable grounds to believe it would associate them with criminals); 4) Trial in exclusive, child-friendly Juvenile Courts; and 5) Protection of identity (no publication of name or photographs of the juvenile).",
            "q_templates": [
                "What are the rights and legal protections for child offenders under the Juvenile Justice System Act 2018?",
                "Can a juvenile offender be sentenced to death under Pakistani law?",
                "Are police allowed to handcuff a child under 18 or keep them in adult jail?",
                "How does bail work for juvenile offenders in Pakistan?",
                "juvenile justice",
                "child offender rights",
                "handcuffing minor",
                "jjsa 2018"
            ],
            "keywords": ["juvenile", "child offender", "jjsa", "minor", "death penalty minor", "lockup", "handcuff", "juvenile court", "bail juvenile"]
        },
        {
            "title": "Definition and Punishment for Abetment (Section 107 & 109 PPC)",
            "statute": "Sections 107 and 109 of the Pakistan Penal Code, 1860",
            "source": "Pakistan Penal Code (PPC), 1860",
            "text": "Under Section 107 of the Pakistan Penal Code (PPC), a person abets the doing of a thing if they: 1) Instigate a person to do it; 2) Engage in a conspiracy to do it; or 3) Intentionally aid the act by any omission or commission. Under Section 109 PPC, whoever abets any offense shall, if the act abetted is committed in consequence of the abetment and no express punishment is provided by law, be punished with the punishment provided for the original offense itself.",
            "q_templates": [
                "What is the definition of abetment and its punishment under Section 109 PPC?",
                "How is aiding and abetting a crime penalized under the Pakistan Penal Code?",
                "What constitutes abetment under Section 107 PPC?",
                "If I helped someone plan a theft, will I get the same punishment as the thief?",
                "abetment",
                "aiding and abetting",
                "section 109 ppc",
                "section 107 instigating"
            ],
            "keywords": ["abetment", "abet", "aiding", "abetting", "instigate", "conspiracy aid", "section 107", "section 109", "ppc"]
        }
    ],
    "Civil Laws": [
        {
            "title": "Specific Performance & Declaration under Specific Relief Act",
            "statute": "Sections 12 and 42 of the Specific Relief Act, 1877",
            "source": "Specific Relief Act, 1877",
            "text": "Under Section 12 of the Specific Relief Act 1877, a party can sue to enforce specific performance of a contract if monetary compensation is inadequate. Section 42 governs declaratory suits, allowing a person to seek a court declaration regarding their legal character or right to property if denied by another party. Civil suits must be filed in the competent Civil Court.",
            "q_templates": [
                "How can I file a suit for specific performance under Section 12 or a declaration under Section 42?",
                "What is the legal process to declare ownership of a right or property in Pakistan?",
                "specific performance of contract",
                "declaratory suit section 42",
                "civil court declaration of title"
            ],
            "keywords": ["specific performance", "declaration", "civil suit", "contract", "section 12", "section 42"]
        },
        {
            "title": "Remedies for Illegal Dispossession of Property",
            "statute": "Section 9 of the Specific Relief Act, 1877",
            "source": "Specific Relief Act, 1877",
            "text": "Under Section 9 of the Specific Relief Act 1877, if a person is dispossessed of immovable property without consent and otherwise than in due course of law, they can file a suit to recover possession within 6 months of the dispossession, regardless of any other title. No appeal lies against a decree passed in such a suit.",
            "q_templates": [
                "What is the remedy for illegal dispossession under Section 9 of the Specific Relief Act?",
                "How can I recover possession of property if dispossessed without my consent?",
                "illegal dispossession section 9",
                "dispossessed of land without consent",
                "recovery of possession within 6 months"
            ],
            "keywords": ["dispossession", "possession", "stay order", "section 9", "recovery", "civil court"]
        },
        {
            "title": "Contract Breach & Damages under Contract Act",
            "statute": "Section 73 of the Contract Act, 1872",
            "source": "Contract Act, 1872",
            "text": "Under Section 73 of the Contract Act 1872, when a contract is breached, the injured party is entitled to compensation (damages) for any loss that naturally arose in the usual course of things or which the parties knew would likely result from the breach. Compensation is not given for remote or indirect losses.",
            "q_templates": [
                "Is a contract binding if there is a breach, and how are damages calculated under Section 73?",
                "What is the compensation for a breach of contract under the Contract Act 1872?",
                "contract breach damages",
                "section 73 contract act",
                "compensation for broken contract"
            ],
            "keywords": ["contract breach", "damages", "breach", "contract act", "section 73", "compensation"]
        },
        {
            "title": "Contract Indemnity & Arbitration Laws",
            "statute": "Section 124 of the Contract Act, 1872 & Arbitration Act, 1940",
            "source": "Contract Act, 1872",
            "text": "Section 124 of the Contract Act 1872 defines a contract of indemnity as a contract by which one party promises to save the other from loss caused by the conduct of the promisor or another person. Contractual disputes can also be referred to out-of-court arbitration under the Arbitration Act 1940 if a valid arbitration clause exists in the contract.",
            "q_templates": [
                "What is the legal framework for contract indemnity under Section 124 of the Contract Act?",
                "How does arbitration work for resolving contract disputes in Pakistan?",
                "contract indemnity section 124",
                "arbitration clause contract dispute",
                "refer dispute to arbitrator"
            ],
            "keywords": ["indemnity", "arbitration", "section 124", "dispute resolution", "arbitrator"]
        },
        {
            "title": "Requirements for a Valid Contract",
            "statute": "Sections 2 and 10 of the Contract Act, 1872",
            "source": "Contract Act, 1872",
            "text": "Under Section 10 of the Contract Act 1872, all agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void. Competency requires being of sound mind, age of majority, and not disqualified by law. Agreement without consideration is void under Section 25, subject to exceptions like natural love and affection if written and registered.",
            "q_templates": [
                "What makes a contract legally valid and binding in Pakistan?",
                "Is an agreement without consideration valid under Section 25 of the Contract Act?",
                "valid contract requirements",
                "no consideration contract",
                "competency to contract pakistan"
            ],
            "keywords": ["valid contract", "consideration", "competent to contract", "free consent", "section 10", "section 25"]
        },
        {
            "title": "Void and Voidable Agreements",
            "statute": "Sections 19 and 20 to 30 of the Contract Act, 1872",
            "source": "Contract Act, 1872",
            "text": "The Contract Act 1872 classifies agreements that are not enforceable by law as void (Section 2g) and agreements enforceable at the option of one party as voidable (Section 2i). Agreements in restraint of marriage (Section 26), restraint of trade (Section 27), restraint of legal proceedings (Section 28), or wagering agreements (Section 30) are void. Consent obtained by coercion, undue influence, fraud, or misrepresentation makes a contract voidable under Section 19 and 19-A.",
            "q_templates": [
                "What is the difference between void and voidable contracts under Pakistan law?",
                "Is a contract valid if it restricts someone from doing business or trade?",
                "void agreement",
                "voidable contract consent fraud",
                "restraint of trade void"
            ],
            "keywords": ["void contract", "voidable", "coercion", "undue influence", "fraud", "misrepresentation", "restraint of trade"]
        },
        {
            "title": "Contract of Guarantee & Surety's Liability",
            "statute": "Sections 126 and 128 of the Contract Act, 1872",
            "source": "Contract Act, 1872",
            "text": "Under Section 126 of the Contract Act 1872, a contract of guarantee is a contract to perform the promise or discharge the liability of a third person in case of their default. The person who gives the guarantee is the surety, the person in respect of whose default it is given is the principal debtor, and the person to whom it is given is the creditor. Under Section 128, the liability of the surety is co-extensive with that of the principal debtor, unless otherwise provided.",
            "q_templates": [
                "What is a contract of guarantee and what is the surety's liability under Section 128?",
                "Can a creditor sue the guarantor directly without suing the main debtor first?",
                "contract of guarantee",
                "surety liability coextensive",
                "guarantor legal liability"
            ],
            "keywords": ["guarantee", "surety", "principal debtor", "creditor", "co-extensive liability", "section 126", "section 128"]
        },
        {
            "title": "Contracts of Bailment & Pledge",
            "statute": "Sections 148 and 172 of the Contract Act, 1872",
            "source": "Contract Act, 1872",
            "text": "Section 148 of the Contract Act 1872 defines bailment as the delivery of goods by one person to another for some purpose, upon a contract that they shall, when the purpose is accomplished, be returned or otherwise disposed of. The deliverer is the bailor and the receiver is the bailee. Section 172 defines pledge as the bailment of goods as security for payment of a debt or performance of a promise. The bailor in this case is the pawnor/pledger, and the bailee is pawnee/pledgee.",
            "q_templates: [
                "What are bailment and pledge under the Contract Act, and what are the bailee's duties?",
                "What happens if a pledgee sells pledged goods without giving notice?",
                "bailment and pledge",
                "bailee duty return goods",
                "pledged goods sale notice"
            ],
            "keywords": ["bailment", "pledge", "bailor", "bailee", "pawnor", "pawnee", "section 148", "section 172"]
        },
        {
            "title": "Agency & Relationship of Principal and Agent",
            "statute": "Sections 182 and 226 of the Contract Act, 1872",
            "source": "Contract Act, 1872",
            "text": "Section 182 of the Contract Act 1872 defines an agent as a person employed to do any act for another, or to represent another in dealings with third persons. The person for whom such act is done is the principal. Under Section 226, contracts entered into through an agent, and obligations arising from acts done by an agent, may be enforced in the same manner and have the same legal consequences as if the contracts had been entered into and the acts done by the principal in person.",
            "q_templates": [
                "What is an agency contract and what is the relationship between principal and agent?",
                "Is the principal liable for the unauthorized acts of their agent?",
                "agency principal agent",
                "agent authority contract",
                "liability of principal agent acts"
            ],
            "keywords": ["agency", "agent", "principal", "authority of agent", "section 182", "section 226"]
        },
        {
            "title": "Temporary & Permanent Injunctions / Stay Orders",
            "statute": "Sections 52 to 56 of the Specific Relief Act, 1877 & CPC Order 39 Rules 1-2",
            "source": "Specific Relief Act, 1877",
            "text": "Injunctions (stay orders) are of two types: temporary and perpetual (permanent). Temporary injunctions are granted at any stage of a suit under Order 39 Rules 1 and 2 of the Code of Civil Procedure 1908 to prevent waste or damage to property. Perpetual injunctions are granted by a final decree under Section 54 of the Specific Relief Act 1877 to prevent the breach of an obligation. A stay order requires three elements: a prima facie case, balance of convenience, and irreparable loss.",
            "q_templates": [
                "How can I obtain a temporary stay order or permanent injunction in Pakistan?",
                "What are the three essential requirements for a court to grant a stay order?",
                "stay order requirements",
                "temporary injunction cpc",
                "permanent injunction stay"
            ],
            "keywords": ["injunction", "stay order", "temporary injunction", "permanent injunction", "order 39", "section 54"]
        },
        {
            "title": "Recovery of Specific Movable and Immovable Property",
            "statute": "Sections 8, 10, 11 of the Specific Relief Act, 1877",
            "source": "Specific Relief Act, 1877",
            "text": "Under Section 8 of the Specific Relief Act 1877, a person entitled to the possession of specific immovable property may recover it in the manner prescribed by the Code of Civil Procedure 1908 (filing a regular suit for possession). Section 10 allows a person entitled to the possession of specific movable property to recover it in the manner prescribed by CPC. Section 11 sets out circumstances where a person holding possession of a movable object may be compelled to deliver it to the person entitled to its immediate possession.",
            "q_templates": [
                "How do I recover possession of specific movable or immovable property under Specific Relief Act?",
                "What is the legal process under Section 8 and 10 to recover property in civil court?",
                "recovery of property specific relief",
                "section 8 recovery immovable",
                "recovery of movable property section 10"
            ],
            "keywords": ["recovery of property", "immovable property", "movable property", "section 8", "section 10", "section 11"]
        },
        {
            "title": "Cancellation and Rectification of Instruments / Deeds",
            "statute": "Sections 31 and 39 of the Specific Relief Act, 1877",
            "source": "Specific Relief Act, 1877",
            "text": "Under Section 31 of the Specific Relief Act 1877, if a contract or other instrument does not express the real intention of the parties due to fraud or mutual mistake, either party may sue for its rectification. Section 39 allows any person against whom a written instrument is void or voidable, and who has reasonable apprehension that such instrument if left outstanding may cause them serious injury, to sue to have it adjudged void and ordered to be cancelled.",
            "q_templates": [
                "How can I cancel a fraudulent deed or rectify a mistake in a contract under Section 31 or 39?",
                "What is the procedure to challenge a fake sale deed or registry in Pakistan?",
                "cancel fraudulent deed",
                "rectification of contract",
                "challenge fake sale deed registry"
            ],
            "keywords": ["cancellation", "rectification", "deed cancellation", "fraudulent deed", "section 31", "section 39"]
        },
        {
            "title": "Civil Court Hierarchy & Jurisdictions",
            "statute": "Civil Courts Ordinance, 1962 & CPC",
            "source": "Civil Courts Ordinance, 1962",
            "text": "Civil courts in Pakistan are organized hierarchically: Civil Judge Class III, Civil Judge Class II, Civil Judge Class I, Senior Civil Judge, District Judge (District & Sessions Court), and the High Court. The territorial jurisdiction is determined by the location of the subject matter or where the cause of action arose. Pecuniary jurisdiction (financial value of the suit) determines which level of Civil Judge can hear the case, with appeals lying to the District Court or the High Court based on value.",
            "q_templates": [
                "What is the hierarchy and jurisdiction of civil courts in Pakistan?",
                "How is the pecuniary and territorial jurisdiction of a civil case decided?",
                "civil court jurisdiction",
                "civil judge class hierarchy",
                "pecuniary jurisdiction civil case"
            ],
            "keywords": ["civil court", "jurisdiction", "civil judge", "district court", "pecuniary jurisdiction", "territorial jurisdiction"]
        },
        {
            "title": "Civil Suit Filing Procedure: Plaint & Written Statement",
            "statute": "CPC Orders 6, 7 & 8",
            "source": "Code of Civil Procedure, 1908",
            "text": "A civil suit is initiated by presenting a plaint (Order VII CPC) which contains the facts of the case and the relief claimed. The court then issues summons (Order V CPC) to the defendant. The defendant must submit their response in a written statement (Order VIII CPC) within the prescribed time limit. The court then frames issues, followed by the recording of evidence (examination-in-chief and cross-examination) of both parties, arguments, and finally the judgment and decree.",
            "q_templates": [
                "What is the complete legal procedure for filing and defending a civil suit in Pakistan?",
                "What is a plaint and a written statement under CPC Orders 7 and 8?",
                "civil suit procedure plaint",
                "written statement cpc",
                "summons cpc order 5"
            ],
            "keywords": ["plaint", "written statement", "summons", "cpc order 7", "cpc order 8", "civil suit procedure"]
        },
        {
            "title": "Execution of Civil Decrees",
            "statute": "Section 38 & Order 21 of CPC",
            "source": "Code of Civil Procedure, 1908",
            "text": "A decree (final order of civil court) is executed under Section 38 and Order 21 of the Code of Civil Procedure 1908. Execution is the process of enforcing the court's decree. The decree-holder must file an execution petition in the court that passed the decree or the court to which it is sent. The court can enforce execution by delivery of property, attachment and sale of property, arrest and detention in prison of the judgment-debtor, or appointing a receiver.",
            "q_templates": [
                "How is a civil court decree executed and what if the losing party refuses to comply?",
                "What is the procedure for execution of a decree under Order 21 of CPC?",
                "execution of decree cpc",
                "attach property execution",
                "judgment debtor arrest decree"
            ],
            "keywords": ["execution of decree", "order 21", "section 38", "attachment of property", "receiver", "decree holder"]
        },
        {
            "title": "Civil Appeals, Reviews, and Revisions",
            "statute": "Sections 96, 114, 115 of CPC",
            "source": "Code of Civil Procedure, 1908",
            "text": "Under CPC, an appeal (Section 96) lies against any original decree passed by a civil court to a higher court (District Court or High Court). A Review (Section 114 & Order 47) can be filed in the same court that passed the judgment if there is discovery of new evidence or an error apparent on the face of the record. A Revision (Section 115) lies to the High Court against a decision of a subordinate court where there has been an exercise of jurisdiction not vested, or failure to exercise jurisdiction.",
            "q_templates": [
                "What are the legal differences between a civil Appeal, Review, and Revision under CPC?",
                "Under what circumstances can I file a revision petition under Section 115 of CPC?",
                "civil appeal review revision",
                "revision petition section 115",
                "review petition section 114"
            ],
            "keywords": ["appeal", "review", "revision", "section 96", "section 114", "section 115", "order 47"]
        },
        {
            "title": "Limitation Period for Civil Suits",
            "statute": "Limitation Act, 1908",
            "source": "Limitation Act, 1908",
            "text": "Under Section 3 of the Limitation Act 1908, every suit instituted, appeal preferred, and application made after the prescribed period of limitation must be dismissed, even if limitation has not been set up as a defense. The limitation period varies: e.g., 3 years for contract breach from the date of breach, 6 months for recovery of possession under Section 9 Specific Relief Act, 3 years for declaratory suits under Section 42, and 30 to 90 days for civil appeals.",
            "q_templates": [
                "What is the limitation period for filing civil suits and appeals in Pakistan?",
                "Can a court accept a civil case if the limitation period has expired under the Limitation Act?",
                "limitation period civil suit",
                "limitation act schedule 1",
                "condonation of delay section 5"
            ],
            "keywords": ["limitation act", "limitation period", "section 3", "time barred suit", "condonation of delay"]
        }
    ],
    "Property Laws": [
        {
            "title": "Requirements for Valid Sale Deeds & Gift Deeds (Hiba)",
            "statute": "Section 54 of the Transfer of Property Act, 1882 & Section 122 of the Registration Act, 1908",
            "source": "Transfer of Property Act, 1882",
            "text": "Under Section 54 of the Transfer of Property Act 1882, any transfer of immovable property worth Rs. 100 or more must be done via a registered instrument. A gift (Hiba) under Islamic law requires: 1) Declaration of gift by the donor, 2) Acceptance by the donee, and 3) Delivery of physical possession of the property. Under the Registration Act 1908, sale and gift deeds must be registered with the Sub-Registrar within 4 months of execution.",
            "q_templates": [
                "What are the requirements for a valid registered sale deed or gift deed (Hiba) under property laws?",
                "How does a Hiba (gift of land) become legally binding under Islamic law in Pakistan?",
                "valid sale deed registration",
                "gift deed requirements hiba",
                "transfer of property act section 54"
            ],
            "keywords": ["sale deed", "gift deed", "hiba", "registration", "sub-registrar", "property transfer"]
        },
        {
            "title": "Land Records, Fard & Mutation (Intiqal)",
            "statute": "Land Revenue Act, 1967",
            "source": "Land Revenue Act, 1967",
            "text": "Land records in Pakistan are managed by the Revenue Department. A 'Fard' is the official record of rights showing ownership and shares in a plot. A 'Mutation' (Intiqal) is the process of updating ownership records after a sale or inheritance. In computerized areas, these are verified and issued through the Arazi Record Center (ARC) or provincial online portals.",
            "q_templates": [
                "How can I verify property records like Fard and Mutation (Intiqal) in Punjab/Sindh?",
                "What is a Patwari fard, and how does the computerized land registry work?",
                "fard and mutation verification",
                "arazi record center intiqal",
                "land revenue act records"
            ],
            "keywords": ["fard", "mutation", "intiqal", "patwari", "arazi record", "land verification"]
        },
        {
            "title": "Illegal Dispossession & Qabza Mafia Protection",
            "statute": "Sections 3 and 4 of the Illegal Dispossession Act, 2005",
            "source": "Illegal Dispossession Act, 2005",
            "text": "The Illegal Dispossession Act 2005 provides a fast-track criminal remedy against land grabbing and illegal dispossession by the qabza mafia. Under Section 4, an aggrieved owner can file a direct complaint in the Sessions Court. Under Section 8, the court can issue immediate interim orders to restore possession to the complainant during the trial and sentence violators to up to 10 years in prison.",
            "q_templates": [
                "How do I file a criminal complaint against illegal possession (qabza mafia) under the Illegal Dispossession Act?",
                "What is the fast-track remedy against land grabbers in Pakistan?",
                "illegal possession qabza mafia",
                "sessions court land grabbing complaint",
                "illegal dispossession act section 3"
            ],
            "keywords": ["illegal possession", "qabza", "land grabber", "sessions court", "dispossession act"]
        },
        {
            "title": "Land Encroachment Remedies & Boundaries",
            "statute": "Section 3 of the Illegal Dispossession Act, 2005",
            "source": "Illegal Dispossession Act, 2005",
            "text": "Under Section 3 of the Illegal Dispossession Act 2005, unauthorized entry, control, or occupation of property without lawful authority is a criminal offense carrying up to 10 years imprisonment. Aggrieved owners can seek structural demolition and eviction orders through civil courts or criminal prosecution in the Sessions Court.",
            "q_templates": [
                "What is the penalty for illegal land encroachment under the Illegal Dispossession Act 2005?",
                "How can a landowner get rid of unauthorized structures built on their property?",
                "land encroachment penalty",
                "unauthorized structures demolition",
                "boundary encroachment dispute"
            ],
            "keywords": ["encroachment", "illegal land occupation", "demolition", "boundary dispute"]
        },
        {
            "title": "Mortgages and Charges",
            "statute": "Sections 58 and 67 of the Transfer of Property Act, 1882",
            "source": "Transfer of Property Act, 1882",
            "text": "Under Section 58 of the Transfer of Property Act 1882, a mortgage is the transfer of an interest in specific immovable property for securing the payment of money advanced or to be advanced. The types of mortgages include simple mortgage, mortgage by conditional sale, usufructuary mortgage, English mortgage, equitable mortgage, and anomalous mortgage. Under Section 67, the mortgagee has a right to obtain a decree for foreclosure or sale if the debt is unpaid.",
            "q_templates": [
                "What are the types of mortgages and what is the mortgagee's foreclosure right in Pakistan?",
                "How does an equitable mortgage (mortgage by deposit of title deeds) work under Transfer of Property Act?",
                "mortgage types property act",
                "foreclosure right section 67",
                "equitable mortgage deposit title"
            ],
            "keywords": ["mortgage", "charge", "foreclosure", "simple mortgage", "equitable mortgage", "section 58", "section 67"]
        },
        {
            "title": "Leases and Tenancies",
            "statute": "Sections 105 and 106 of the Transfer of Property Act, 1882",
            "source": "Transfer of Property Act, 1882",
            "text": "Under Section 105 of the Transfer of Property Act 1882, a lease of immovable property is a transfer of a right to enjoy such property, made for a certain time or in perpetuity, in consideration of a price or rent. Under Section 106, in the absence of a written contract, a lease of immovable property for agricultural or manufacturing purposes is deemed to be a lease from year to year (terminable by 6 months notice), and a lease for other purposes is deemed to be from month to month (terminable by 15 days notice).",
            "q_templates": [
                "What is the legal definition of a lease and what are the notice requirements under Section 106?",
                "How can a landlord evict a tenant if there is no written lease agreement?",
                "lease notice requirements 15 days",
                "section 105 lease definition",
                "month to month lease notice"
            ],
            "keywords": ["lease", "tenancy", "tenant eviction", "rent agreement", "section 105", "section 106"]
        },
        {
            "title": "Gifts (Hiba) of Immovable Property",
            "statute": "Sections 122 and 123 of the Transfer of Property Act, 1882",
            "source": "Transfer of Property Act, 1882",
            "text": "Under Section 122 of the Transfer of Property Act 1882, a gift is the transfer of certain existing movable or immovable property made voluntarily and without consideration. For non-Muslims, a gift of immovable property must be registered and signed by the donor and attested by at least two witnesses (Section 123). For Muslims, the oral gift (Hiba) rules under Islamic law apply: 1) Declaration of gift (Ijab), 2) Acceptance of gift (Qubool), and 3) Delivery of physical possession (Qabza).",
            "q_templates": [
                "How is a gift of property made legally binding under Sections 122 and 123?",
                "What are the three mandatory elements for a valid Hiba under Islamic law?",
                "hiba requirements muslim",
                "property gift deed registration",
                "section 122 gift definition"
            ],
            "keywords": ["hiba", "gift deed", "delivery of possession", "ijab qubool", "section 122", "section 123"]
        },
        {
            "title": "Actionable Claims",
            "statute": "Sections 130 and 131 of the Transfer of Property Act, 1882",
            "source": "Transfer of Property Act, 1882",
            "text": "Section 130 of the Transfer of Property Act 1882 defines an actionable claim as a claim to any debt (other than a secured debt) or to any beneficial interest in movable property not in the possession of the claimant. The transfer of an actionable claim must be effected only by the execution of an instrument in writing signed by the transferor. Upon execution, all rights and remedies of the transferor vest in the transferee.",
            "q_templates": [
                "What is an actionable claim and how is it transferred under Section 130?",
                "Does the transfer of a debt require a written agreement under property law?",
                "actionable claim transfer",
                "section 130 debt transfer",
                "unsecured debt assignment"
            ],
            "keywords": ["actionable claim", "debt transfer", "assignment", "written instrument", "section 130", "section 131"]
        },
        {
            "title": "Compulsory Registration of Property Documents",
            "statute": "Section 17 of the Registration Act, 1908",
            "source": "Registration Act, 1908",
            "text": "Under Section 17 of the Registration Act 1908, registration is compulsory for documents transferring or creating rights in immovable property of value Rs. 100 or upwards. This includes sale deeds, gift deeds (except oral Hiba under Muslim personal law, though written declarations of Hiba must be registered to be accepted in court), mortgage deeds, and leases of immovable property from year to year or exceeding one year. Under Section 49, unregistered compulsory documents are inadmissible as evidence of property rights.",
            "q_templates": [
                "Which property documents are compulsory to register under Section 17 of the Registration Act?",
                "What is the legal consequence of failing to register a sale deed under Section 49?",
                "compulsory registration section 17",
                "unregistered sale deed section 49",
                "lease agreement registration requirement"
            ],
            "keywords": ["registration act", "compulsory registration", "inadmissible evidence", "section 17", "section 49"]
        },
        {
            "title": "Time Limit for Registration of Deeds",
            "statute": "Sections 23 and 25 of the Registration Act, 1908",
            "source": "Registration Act, 1908",
            "text": "Under Section 23 of the Registration Act 1908, a document must be presented for registration within 4 months from the date of its execution. If a document cannot be presented within 4 months due to urgent necessity or unavoidable accident, the Registrar may, under Section 25, permit registration on payment of a fine not exceeding 10 times the registration fee, provided the delay does not exceed an additional 4 months.",
            "q_templates": [
                "What is the time limit for registering a property sale deed after signing it?",
                "Can I register a sale deed after the 4-month limit has expired under Section 25?",
                "registration time limit 4 months",
                "delay fine section 25 registrar",
                "four months registration cpc"
            ],
            "keywords": ["registration delay", "four months limit", "fine payment", "section 23", "section 25"]
        },
        {
            "title": "Benami Property Transactions",
            "statute": "Benami Transactions Prohibition Act, 2017",
            "source": "Benami Transactions Prohibition Act, 2017",
            "text": "Under the Benami Transactions Prohibition Act 2017, a benami transaction is one where property is transferred to, or held by, a person but the consideration is paid or provided by another person, and the property is held for the immediate or future benefit of the person providing the consideration. The Act prohibits benami transactions. Violations carry criminal penalties including imprisonment from 1 to 7 years, fines up to 25% of the fair market value, and confiscation of the benami property.",
            "q_templates": [
                "What is a Benami property transaction and what are the penalties under the 2017 Act?",
                "Can the government confiscate a property if it is found to be registered in someone else's name?",
                "benami property transaction prohibition",
                "benami transactions act penalty",
                "confiscate benami land"
            ],
            "keywords": ["benami", "benami act", "confiscation of property", "transaction prohibition", "consideration payer"]
        },
        {
            "title": "Stamp Duty Requirements",
            "statute": "Sections 3 and 35 of the Stamp Act, 1899",
            "source": "Stamp Act, 1899",
            "text": "Under Section 3 of the Stamp Act 1899, instruments transferring rights (like sale deeds, gift deeds, and mortgages) are chargeable with stamp duty. Under Section 35, an instrument not duly stamped is inadmissible in evidence for any purpose, nor can it be acted upon, registered, or authenticated by any public officer, unless the duty and a penalty of 10 times the amount of deficient duty are paid.",
            "q_templates": [
                "What happens if a property document is not executed on proper stamp paper under Stamp Act?",
                "How can a document with deficient stamp duty be made admissible in court under Section 35?",
                "stamp duty section 3",
                "deficient stamp paper section 35",
                "proper stamp paper duty penalty"
            ],
            "keywords": ["stamp duty", "stamp act", "deficient stamp duty", "inadmissible stamp paper", "section 3", "section 35"]
        },
        {
            "title": "Easement Rights and Prescription",
            "statute": "Sections 4 and 15 of the Easements Act, 1882",
            "source": "Easements Act, 1882",
            "text": "Section 4 of the Easements Act 1882 defines an easement as a right which the owner or occupier of certain land possesses for the beneficial enjoyment of that land, to do and continue to do something, or to prevent something from being done in or upon other land. Under Section 15, easement rights of light, air, support, or way can be acquired by prescription through peaceable, open, and uninterrupted enjoyment for 20 years (or 60 years against the government).",
            "q_templates": [
                "What is an easement right and how is it acquired by prescription under Section 15?",
                "How many years of uninterrupted use of a path are required to claim a right of way?",
                "easement right prescription",
                "right of way easements act",
                "twenty years easement prescription"
            ],
            "keywords": ["easement", "easements act", "prescription", "right of way", "uninterrupted enjoyment", "section 4", "section 15"]
        },
        {
            "title": "Co-ownership and Partition of Joint Property",
            "statute": "Partition Act, 1893",
            "source": "Partition Act, 1893",
            "text": "Under the Partition Act 1893, co-owners of joint property have the right to seek physical division of the property. If the property cannot be physically divided without destroying its utility, any co-owner can file a suit for partition. The court may direct a sale of the property and distribution of proceeds under Section 2. Under Section 3, the court can allow other co-owners to buy out the shares of the party requesting the sale.",
            "q_templates": [
                "How can joint property be divided or partitioned among co-owners in Pakistan?",
                "Can the court order the sale of joint property if partition is physically impossible?",
                "suit for partition of joint land",
                "partition act buy out share",
                "divide joint family property"
            ],
            "keywords": ["partition", "partition act", "co-ownership", "joint property division", "buy out share", "suit for partition"]
        },
        {
            "title": "Adverse Possession of Immovable Property",
            "statute": "Article 144 of the Limitation Act, 1908",
            "source": "Limitation Act, 1908",
            "text": "Adverse possession allows a person in hostile, continuous, and open possession of immovable property for 12 years or more to claim legal ownership, barring the original owner's right to recover it under Article 144 of the Limitation Act 1908. However, recent judgments of the Supreme Court of Pakistan have heavily restricted the doctrine of adverse possession, declaring it contrary to Islamic injunctions and requiring strict compliance with hostile intent and notice.",
            "q_templates": [
                "What is adverse possession and does it give ownership rights after 12 years in Pakistan?",
                "Can a squatter claim ownership of land if they live there for over 12 years?",
                "adverse possession 12 years",
                "limitation act article 144 land",
                "squatter land claim ownership"
            ],
            "keywords": ["adverse possession", "limitation act article 144", "squatter", "twelve years possession", "hostile possession"]
        }
    ],
    "Labour Laws": [
        {
            "title": "Wage Payment Delays & Recovery Procedures",
            "statute": "Sections 5 and 15 of the Payment of Wages Act, 1936",
            "source": "Payment of Wages Act, 1936",
            "text": "Under Section 5 of the Payment of Wages Act 1936, employers must pay wages within 7 to 10 days of the end of the wage period. If wages are delayed or unauthorized deductions are made, the employee can apply to the Authority (Workmen's Compensation Commissioner/Labor Commissioner) under Section 15. The Authority can order payment of wages and compensation up to 10 times the deducted amount.",
            "q_templates": [
                "What is the legal recourse if an employer delays salary payments under the Payment of Wages Act?",
                "How can a worker recover unpaid wages or salary deductions in Pakistan?",
                "delayed salary recourse payment of wages",
                "recover unpaid wages labor commissioner",
                "payment of wages act section 15"
            ],
            "keywords": ["salary", "wages", "labor commissioner", "unpaid wages", "deduction"]
        },
        {
            "title": "Wrongful Termination & Gratuity Calculation",
            "statute": "Standing Order 12 of the Industrial and Commercial Employment (Standing Orders) Ordinance, 1968",
            "source": "Standing Orders Ordinance, 1968",
            "text": "Standing Order 12 of the Industrial and Commercial Employment (Standing Orders) Ordinance 1968 regulates termination. A permanent worker cannot be terminated without 1 month's written notice or salary, and a written order stating explicit reasons. Upon termination, a worker is entitled to gratuity calculated at 30 days' wages for every completed year of service based on the last basic salary.",
            "q_templates": [
                "What are the worker rights against wrongful termination under Standing Order 12?",
                "How is employee gratuity calculated under the Standing Orders Ordinance 1968?",
                "wrongful termination standing order 12",
                "calculate gratuity completed years service",
                "notice period for termination salary"
            ],
            "keywords": ["gratuity", "wrongful termination", "notice period", "standing order 12", "severance"]
        },
        {
            "title": "Disciplinary Actions & Misconduct Inquiries",
            "statute": "Standing Order 15 of the Industrial and Commercial Employment (Standing Orders) Ordinance, 1968",
            "source": "Standing Orders Ordinance, 1968",
            "text": "Standing Order 15 dictates that an employee cannot be dismissed for misconduct unless they are served a written show-cause notice detailing the allegations within 30 days of the incident, and given a fair chance to defend themselves in an independent domestic inquiry. Instant dismissal without due process is illegal.",
            "q_templates": [
                "What is the legal process for dismissal due to misconduct under Standing Order 15?",
                "Can an employer fire an employee instantly for bad behavior or absence?",
                "dismissal misconduct domestic inquiry",
                "show cause notice show-cause cpc",
                "instant dismissal due process illegal"
            ],
            "keywords": ["misconduct", "show-cause", "inquiry", "dismissal", "standing order 15", "disciplinary"]
        },
        {
            "title": "Labor Court Grievance Petitions",
            "statute": "Section 25-A of the Industrial Relations Act",
            "source": "Industrial Relations Act",
            "text": "Under Section 25-A of the Industrial Relations Act, an employee must first send a written grievance notice to the employer within 30 days of the grievance. If the employer does not respond or resolve the issue, the worker can file a petition in the Labor Court within 30 days of the employer's reply (or the expiry of response time).",
            "q_templates": [
                "How do I file a grievance petition in the Labor Court under the Standing Orders Ordinance?",
                "What is the time limit for filing a labor dispute in court after termination?",
                "grievance petition labor court",
                "grievance notice 30 days employer",
                "industrial relations act section 25-a"
            ],
            "keywords": ["labor court", "grievance notice", "petition", "section 25-a", "standing orders"]
        },
        {
            "title": "Employment Contracts & Written Letters",
            "statute": "Standing Order 2-A of the Standing Orders Ordinance, 1968",
            "source": "Standing Orders Ordinance, 1968",
            "text": "Under Standing Order 2-A, every worker at the time of their appointment, transfer, or promotion must be provided with a written order of employment showing the terms, conditions, nature of work, salary, and details of service. Verbal agreements are illegal, and every commercial establishment employing 20 or more workers (or industrial employing 50 or more) must strictly implement written contracts.",
            "q_templates": [
                "Is a written employment letter mandatory for workers in Pakistan under Standing Orders?",
                "What is the legality of a verbal labor contract under Standing Order 2-A?",
                "written appointment letter mandatory",
                "verbal employment agreement legality",
                "standing order 2-a written contract"
            ],
            "keywords": ["written letter", "appointment letter", "verbal agreement", "employment terms", "standing order 2-a"]
        },
        {
            "title": "Maternity Benefits & Leave",
            "statute": "Maternity Benefit Act, 1958",
            "source": "Maternity Benefit Act, 1958",
            "text": "Under the Maternity Benefit Act 1958, every female worker is entitled to paid maternity leave of 12 weeks (6 weeks pre-delivery and 6 weeks post-delivery). She must have worked with the employer for at least 4 months preceding delivery. It is unlawful for an employer to terminate or dismiss a woman during her maternity leave or because of her pregnancy.",
            "q_templates": [
                "What are the maternity leave benefits and duration for female workers in Pakistan?",
                "Can an employer terminate a female worker because she is pregnant or on maternity leave?",
                "maternity leave duration weeks",
                "terminate pregnant female employee",
                "maternity benefit act paid leave"
            ],
            "keywords": ["maternity", "pregnancy", "paid leave", "maternity benefit", "female worker"]
        },
        {
            "title": "Social Security Registration & Benefits",
            "statute": "Provincial Employees' Social Security Ordinance, 1965",
            "source": "Social Security Ordinance, 1965",
            "text": "Under the Social Security Ordinance 1965, employers must register their employees with provincial social security institutions (like PESSI in Punjab, SESSI in Sindh) and pay monthly contributions. Registered workers are entitled to free medical treatment, sickness benefits, maternity benefits, injury benefits, disablement pension, and survivor's pension for their families.",
            "q_templates": [
                "How does social security registration work for labor and what are PESSI/SESSI benefits?",
                "Is it mandatory for an employer to contribute to the employee's social security card?",
                "sessi registration benefits medical",
                "pessi social security contribution",
                "social security ordinance 1965"
            ],
            "keywords": ["social security", "pessi", "sessi", "medical benefit", "contribution"]
        },
        {
            "title": "Employees' Old-Age Benefits Institution",
            "statute": "EOBI Act, 1976",
            "source": "EOBI Act, 1976",
            "text": "Under the EOBI Act 1976, all industrial and commercial establishments employing 5 or more workers must register with EOBI. Employers contribute 5% of the minimum wage and employees contribute 1% towards the old-age pension fund. Upon reaching retirement age (60 for men, 55 for women) and completing 15 years of insurable employment, workers are entitled to a monthly Old-Age Pension.",
            "q_templates": [
                "What is EOBI pension and who is eligible under the Old-Age Benefits Act?",
                "Is my employer legally required to register me with EOBI and pay pension contributions?",
                "eobi monthly pension eligibility",
                "employer eobi registration 5 employees",
                "eobi act 1976 old age"
            ],
            "keywords": ["eobi", "pension", "retirement age", "contribution", "old-age benefits"]
        },
        {
            "title": "Working Hours, Overtime & Rest Intervals",
            "statute": "Factories Act, 1934 & Shops and Establishments Ordinance, 1969",
            "source": "Factories Act, 1934",
            "text": "Under the Factories Act 1934 and Shops and Establishments laws, a worker cannot work more than 9 hours a day or 48 hours a week without overtime. Rest intervals of 1 hour after 6 hours of work (or half-an-hour after 5 hours) are mandatory. Any work done exceeding normal hours must be compensated as overtime at double the ordinary rate of pay (Section 47).",
            "q_templates": [
                "What are the legal limits on daily working hours and overtime pay calculation?",
                "Is an employer required to pay double salary for overtime hours worked under the Factories Act?",
                "overtime double rate calculation",
                "maximum daily working hours cpc",
                "rest interval factories act"
            ],
            "keywords": ["overtime", "working hours", "rest interval", "double pay", "factories act"]
        },
        {
            "title": "Weekly Holidays & Annual Paid Leaves",
            "statute": "Factories Act, 1934 & Shops and Establishments Ordinance, 1969",
            "source": "Factories Act, 1934",
            "text": "Under labor laws, every worker is entitled to one weekly holiday (usually Sunday). Under Section 49-B of the Factories Act 1934, after completing 12 months of continuous service, a worker is entitled to 14 consecutive days of annual paid leave. In addition, workers are entitled to 10 days of casual leave, 16 days of sick leave (on half-pay), and all gazetted public holidays.",
            "q_templates": [
                "How many paid leaves, sick leaves, and weekly holidays is an employee entitled to?",
                "What happens to unused annual paid leaves under the Factories Act?",
                "annual paid leaves 14 days",
                "sick leave casual leave limit",
                "weekly holiday Sunday factories"
            ],
            "keywords": ["paid leaves", "weekly holiday", "casual leave", "sick leave", "section 49-b"]
        },
        {
            "title": "Workplace Safety & Occupational Health Standards",
            "statute": "Chapter III of the Factories Act, 1934 & OSH Acts",
            "source": "Factories Act, 1934",
            "text": "Chapter III of the Factories Act 1934 requires employers to maintain safe and healthy working conditions. This includes proper ventilation, temperature control, lighting, sanitation, clean drinking water, fire escapes, and fencing of dangerous machinery. Employers who fail to provide safety equipment face heavy fines, factory closure, and liability for worker injuries.",
            "q_templates": [
                "What are the employer's duties regarding workplace safety and healthy conditions under Factories Act?",
                "Can a worker refuse to work if the machinery is unsafe or there are no fire escapes?",
                "workplace safety factories act",
                "machinery safety occupational health",
                "fire escapes ventilation sanitation"
            ],
            "keywords": ["safety", "occupational health", "machinery safety", "fire escape", "factories act"]
        },
        {
            "title": "Compensation for Workplace Injuries & Death",
            "statute": "Workmen's Compensation Act, 1923",
            "source": "Workmen's Compensation Act, 1923",
            "text": "Under Section 3 of the Workmen's Compensation Act 1923, an employer is liable to pay compensation if a worker suffers personal injury or death due to an accident arising out of and in the course of employment. The compensation amount is determined by Schedule IV based on the level of disablement or death. For death or permanent total disablement, a lump-sum compensation must be paid to the worker or their legal heirs.",
            "q_templates": [
                "What is the compensation for a worker injured or deceased at the workplace under the 1923 Act?",
                "How is the disablement compensation calculated under the Workmen's Compensation Act?",
                "workmen compensation injury death",
                "lump sum compensation heirs",
                "workmen compensation act schedule 4"
            ],
            "keywords": ["workmen compensation", "injury", "accidental death", "disablement", "section 3"]
        },
        {
            "title": "Prohibition of Child Labor",
            "statute": "Employment of Children Act, 1991",
            "source": "Employment of Children Act, 1991",
            "text": "The Constitution of Pakistan (Article 11) and child labor laws strictly prohibit the employment of children below the age of 14 in any factory, mine, or hazardous employment. Hazardous occupations include brick kilns, glass factories, chemical processes, and deep-sea fishing. Employers violating child labor restrictions face criminal prosecution, jail sentences up to 5 years, and severe fines.",
            "q_templates": [
                "What is the legal minimum age to work in factories and what is the penalty for employing children?",
                "Which occupations are classified as hazardous for children under child labor laws?",
                "child labor minimum age",
                "hazardous occupations child labor",
                "employment of children act penalty"
            ],
            "keywords": ["child labor", "minimum age", "hazardous", "employment prohibition", "article 11"]
        },
        {
            "title": "Provident Fund & Gratuity Alternatives",
            "statute": "Standing Order 12(6) of Standing Orders Ordinance, 1968",
            "source": "Standing Orders Ordinance, 1968",
            "text": "Under Standing Order 12(6), an employer can provide a Contributory Provident Fund instead of a gratuity scheme, provided the fund contributions are mutually agreed and the employer's contribution is not less than the employee's contribution. If a worker is registered under a provident fund, they receive the accumulated balances (both employee and employer shares) upon termination or retirement, instead of gratuity.",
            "q_templates": [
                "Can an employer offer a Provident Fund instead of Gratuity under Standing Orders?",
                "What are the rules regarding employer contributions to a Contributory Provident Fund?",
                "provident fund instead of gratuity",
                "contributory provident fund rules",
                "standing order 12 6 provident"
            ],
            "keywords": ["provident fund", "gratuity alternative", "contributory", "standing order 12 6", "employer contribution"]
        },
        {
            "title": "Labor Unions & Collective Bargaining Agent",
            "statute": "Industrial Relations Act, 2012",
            "source": "Industrial Relations Act, 2012",
            "text": "The Constitution (Article 17) and Industrial Relations Acts guarantee workers the right to form trade unions and bargain collectively through a certified Collective Bargaining Agent (CBA). A CBA is elected via secret ballot by union members. The CBA has the sole right to represent workers in negotiations, raise industrial disputes, sign binding agreements (settlements), and declare legal strikes under prescribed conditions.",
            "q_templates": [
                "What are the legal rights of trade unions and how is a Collective Bargaining Agent (CBA) elected?",
                "Can employees go on strike legally under the Industrial Relations Act?",
                "trade union right collective bargaining",
                "cba election secret ballot",
                "legal strike industrial relations act"
            ],
            "keywords": ["trade union", "cba", "collective bargaining", "strike", "industrial relations", "article 17"]
        }
    ],
    "Tax Laws": [
        {
            "title": "Income Tax Return Filings & Non-Filer Consequences",
            "statute": "Section 114 of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under Section 114 of the Income Tax Ordinance 2001, any individual with taxable income exceeding the threshold (Rs. 600,000 for salaried employees) must file an annual tax return with the FBR. Non-filers face higher withholding tax rates, penalties, bank account freezing, and restrictions on buying property or vehicles. Under Section 182, a penalty is imposed for late filing. Under Section 182A, late filers are not included in the Active Taxpayer List (ATL) until a surcharge is paid.",
            "q_templates": [
                "Who is legally required to file an income tax return, and what is the penalty for non-filing?",
                "What are the consequences of being a non-filer under FBR rules?",
                "income tax return filer non filer",
                "penalty for late filing income tax",
                "fbr active taxpayer list surcharge"
            ],
            "keywords": ["income tax", "fbr", "tax return", "filer", "non-filer", "withholding tax"]
        },
        {
            "title": "Assessment Amendments & Default Surcharge",
            "statute": "Sections 122 and 205 of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under Section 122 of the Income Tax Ordinance 2001, the FBR Commissioner can amend a filed tax assessment if audit findings show under-reported income, after giving a show-cause notice. Section 205 imposes a default surcharge (KIBOR + 3% per annum) for late tax payments. Appeals can be filed before the Commissioner Inland Revenue (Appeals) and the ATIR.",
            "q_templates": [
                "What is default surcharge under Section 205, and how can the Commissioner amend assessments?",
                "How can I appeal against an amended tax assessment notice from FBR?",
                "default surcharge section 205",
                "amend tax assessment fbr notice",
                "appeal amended assessment commissioner appeals"
            ],
            "keywords": ["default surcharge", "assessment", "audit", "appeal", "fbr notice", "section 205"]
        },
        {
            "title": "Sales Tax Registrations & Refunds",
            "statute": "Sections 3 and 10 of the Sales Tax Act, 1990",
            "source": "Sales Tax Act, 1990",
            "text": "Under Section 3 of the Sales Tax Act 1990, a standard sales tax of 18% is levied on taxable supplies and imports. Businesses meeting the threshold must register with the FBR. Under Section 10, a registered person can claim a refund for excess input tax (tax paid on purchases) over output tax (tax on sales) under zero-rated exports or specific conditions.",
            "q_templates": [
                "What is the standard sales tax rate, and how do I register or claim refunds under the Sales Tax Act?",
                "How do I claim a refund for input sales tax from the FBR?",
                "sales tax registration threshold rate",
                "claim input sales tax refund fbr",
                "sales tax act section 3 section 10"
            ],
            "keywords": ["sales tax", "input tax", "refund", "registration", "fbr", "supplies"]
        },
        {
            "title": "Tax Fraud Penalties & Prosecution",
            "statute": "Section 33 of the Sales Tax Act, 1990 & Section 203 of the Income Tax Ordinance, 2001",
            "source": "Pakistan Tax Laws",
            "text": "Under Section 33 of the Sales Tax Act 1990, committing tax fraud, fabricating records, or issuing fake invoices carries a penalty of Rs. 25,000 or 100% of the tax evaded. It is also a criminal offense carrying up to 3 years imprisonment and prosecution. Under Section 203 of the Income Tax Ordinance 2001, deliberate tax evasion is punishable by imprisonment up to 2 years, a fine, or both.",
            "q_templates: [
                "What are the penalties for tax fraud or filing fake invoices under the Sales Tax Act 1990?",
                "Can a person go to jail for tax evasion in Pakistan?",
                "tax fraud fake invoice penalty",
                "prosecution tax evasion imprisonment",
                "sales tax act section 33 tax fraud"
            ],
            "keywords": ["tax fraud", "fake invoice", "evasion", "penalty", "prosecution", "imprisonment"]
        },
        {
            "title": "Withholding Tax on Salary, Property, and Transactions",
            "statute": "Sections 149, 153, 236C and 236K of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under the Income Tax Ordinance 2001, withholding tax (WHT) is deducted at source on various transactions. Section 149 governs tax deductions on salaries by employers. Section 153 mandates deductions on payments for goods, services, and contracts. Sections 236C and 236K levy advance tax on the sale and purchase of immovable property, with significantly higher rates for non-filers than active taxpayers.",
            "q_templates": [
                "What are the rules regarding withholding tax on salary and property transactions under the Income Tax Ordinance?",
                "What is the withholding tax rate for buying and selling property in Pakistan?",
                "withholding tax salary section 149",
                "withholding tax buy sell property",
                "wht rate non filer active taxpayer"
            ],
            "keywords": ["withholding tax", "wht", "salary", "property transaction", "non-filer", "active taxpayer"]
        },
        {
            "title": "FBR Audit Procedures & Notice Responses",
            "statute": "Sections 177 and 214C of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under Section 177 of the Income Tax Ordinance 2001, the Commissioner can call for record books and conduct a tax audit of a taxpayer. Under Section 214C, the FBR can select taxpayers for audit through random or parametric computer balloting. A taxpayer must respond to FBR audit notices within the specified time, providing cash books, bank statements, and purchase/sales ledger records.",
            "q_templates": [
                "What is the legal process of FBR audit selection and how should a taxpayer respond to notices?",
                "Can the FBR randomly select my company for a tax audit, and what documents are required?",
                "fbr tax audit selection notice",
                "respond fbr audit notice ledger",
                "section 177 section 214c audit"
            ],
            "keywords": ["tax audit", "fbr notice", "record book", "audit selection", "section 177", "section 214c"]
        },
        {
            "title": "Appeals Process: Commissioner Appeals, ATIR, and High Court",
            "statute": "Sections 127, 131, and 133 of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "If aggrieved by an FBR assessment or amendment order, a taxpayer can appeal to the Commissioner Inland Revenue (Appeals) under Section 127 within 30 days. If dissatisfied with the decision, a second appeal can be filed before the Appellate Tribunal Inland Revenue (ATIR) under Section 131. A reference on a question of law can be filed before the High Court under Section 133 within 90 days.",
            "q_templates": [
                "What is the step-by-step appeals process against FBR tax assessments?",
                "What is the limitation period to file an appeal before the Commissioner Appeals and Appellate Tribunal?",
                "appeal commissioner inland revenue appeals",
                "appellate tribunal inland revenue atir",
                "tax reference high court section 133"
            ],
            "keywords": ["appeal", "commissioner appeals", "appellate tribunal", "atir", "high court reference", "limitation"]
        },
        {
            "title": "Alternative Dispute Resolution Committee (ADRC)",
            "statute": "Section 134A of the Income Tax Ordinance, 2001 & Section 47A of the Sales Tax Act, 1990",
            "source": "Pakistan Tax Laws",
            "text": "To resolve tax disputes out of court, a taxpayer can apply to the FBR for the constitution of an Alternative Dispute Resolution Committee (ADRC) under Section 134A of the Income Tax Ordinance 2001 or Section 47A of the Sales Tax Act 1990. The ADRC, consisting of FBR officers, chartered accountants, and industry experts, tries to resolve disputes through consensus. The decision of the ADRC is binding if the taxpayer withdraws their pending appeals from courts.",
            "q_templates": [
                "What is the out-of-court tax dispute resolution process under ADRC rules?",
                "How do I apply for an Alternative Dispute Resolution Committee (ADRC) for my tax case?",
                "adrc dispute resolution fbr",
                "alternative dispute resolution committee application",
                "adrc binding decision appeal withdrawal"
            ],
            "keywords": ["adrc", "dispute resolution", "consensus", "fbr committee", "section 134a", "section 47a"]
        },
        {
            "title": "Tax Exemptions, Concessions, and Second Schedule",
            "statute": "Section 53 and the Second Schedule of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Section 53 of the Income Tax Ordinance 2001, read with the Second Schedule, provides tax exemptions, reduced rates, tax concessions, and tax credits for specific categories of taxpayers, such as charitable institutions, non-profit organizations, agricultural income, IT exports, and special economic zones. Taxpayers must meet all statutory conditions to claim these exemptions.",
            "q_templates": [
                "Who is eligible for tax exemptions and concessions under the Second Schedule?",
                "Are IT export earnings or non-profit organizations exempt from income tax in Pakistan?",
                "tax exemption second schedule fbr",
                "it export tax credit exemption",
                "charitable non-profit organization tax concession"
            ],
            "keywords": ["tax exemption", "second schedule", "tax concession", "tax credit", "charitable", "it exports"]
        },
        {
            "title": "Provincial Sales Tax on Services",
            "statute": "Provincial Sales Tax on Services Acts (e.g. Punjab Sales Tax on Services Act 2012)",
            "source": "Provincial Revenue Authorities",
            "text": "Under the Constitution of Pakistan (18th Amendment), the power to levy sales tax on services lies with the provinces. Services (like hotels, restaurants, telecommunications, IT services, consulting, and logistics) are taxed by provincial bodies like the Punjab Revenue Authority (PRA), Sindh Revenue Board (SRB), Balochistan Revenue Authority (BRA), and Khyber Pakhtunkhwa Revenue Authority (KPRA) at rates ranging from 5% to 16%.",
            "q_templates": [
                "What are the provincial sales tax rates on services and which revenue authority governs them?",
                "Is there a separate sales tax on IT services and restaurants in Punjab and Sindh?",
                "provincial sales tax services pra srb",
                "kpra kpk sales tax service",
                "punjab sales tax on services act"
            ],
            "keywords": ["provincial sales tax", "services tax", "pra", "srb", "kpra", "bra", "restaurants"]
        },
        {
            "title": "Advance Tax & Quarterly Installments",
            "statute": "Section 147 of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under Section 147 of the Income Tax Ordinance 2001, taxpayers (excluding salaried individuals and those subject only to final tax) whose latest assessed tax exceeds the threshold must pay advance tax in four quarterly installments. FBR calculates advance tax based on previous tax liability or turnover. Failure to pay advance tax results in default surcharge and penalties under Section 205.",
            "q_templates": [
                "Who is required to pay advance tax and how are the quarterly installments calculated?",
                "What are the penalties for failing to pay quarterly advance tax to FBR?",
                "advance tax quarterly installments section 147",
                "calculate advance tax quarterly fbr",
                "late payment advance tax penalty"
            ],
            "keywords": ["advance tax", "quarterly installment", "section 147", "turnover tax", "tax installment"]
        },
        {
            "title": "Federal Excise Duty (FED) & Customs Duties",
            "statute": "Federal Excise Act, 2005 & Customs Act, 1969",
            "source": "Pakistan Indirect Tax Laws",
            "text": "Under the Federal Excise Act 2005, Federal Excise Duty (FED) is levied on specific goods produced, manufactured, or imported into Pakistan, and on services like air travel and telecommunication. The Customs Act 1969 regulates the import and export of goods, levying customs duties and regulatory duties to protect domestic industries and generate revenue.",
            "q_templates": [
                "What is Federal Excise Duty (FED) and what goods or services are subject to it?",
                "How are customs duties and regulatory duties determined for imported items under the Customs Act?",
                "federal excise duty fed air travel",
                "customs duty import tariff rates",
                "regulatory duty customs act 1969"
            ],
            "keywords": ["federal excise duty", "fed", "customs duty", "regulatory duty", "import", "export"]
        },
        {
            "title": "Active Taxpayer List (ATL) Surcharge & Benefits",
            "statute": "Section 182A of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "The Active Taxpayer List (ATL) is the database of individuals and companies who file their income tax returns on time. Under Section 182A, if a return is filed late, the taxpayer is not included in the ATL until they pay a specific ATL Surcharge (Rs. 1,000 for individuals, Rs. 10,000 for companies). ATL taxpayers enjoy lower withholding tax rates on banking transactions, property, and vehicle purchases.",
            "q_templates": [
                "How do I get my name on the Active Taxpayer List (ATL) and what is the late filer surcharge?",
                "What are the benefits of being an active taxpayer compared to a non-active filer?",
                "active taxpayer list atl benefits",
                "atl late filer surcharge fbr",
                "withholding tax banking property active"
            ],
            "keywords": ["active taxpayer list", "atl", "surcharge", "late filer", "withholding benefit"]
        },
        {
            "title": "Capital Gains Tax (CGT) on Shares, Securities, and Immovable Property",
            "statute": "Sections 37 and 37A of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under Sections 37 and 37A of the Income Tax Ordinance 2001, capital gains tax (CGT) is levied on profit earned from the sale of capital assets, including shares of public companies, modaraba certificates, mutual funds, and immovable property (plots, houses). The tax rate depends on the holding period (longer holding periods usually attract lower or zero tax rates) and the taxpayer's filer status.",
            "q_templates": [
                "What is the Capital Gains Tax (CGT) rate on property sale and share trading in Pakistan?",
                "How does holding period affect capital gains tax on immovable property?",
                "capital gains tax cgt property sale",
                "cgt shares mutual funds section 37a",
                "holding period capital gains exemption"
            ],
            "keywords": ["capital gains tax", "cgt", "immovable property", "holding period", "shares", "securities"]
        },
        {
            "title": "FBR Powers of Search, Seizure, and Recovery",
            "statute": "Sections 138, 140, and 175 of the Income Tax Ordinance, 2001",
            "source": "Income Tax Ordinance, 2001",
            "text": "Under Section 175 of the Income Tax Ordinance 2001, the Commissioner has the power to enter and search any premises and seize records. Under Section 140, the FBR can recover outstanding tax liabilities directly from the taxpayer's bank accounts, employers, or debtors. Section 138 authorizes the FBR to arrest and detain defaulting taxpayers or seize and sell their property to recover dues.",
            "q_templates": [
                "What are FBR's powers regarding search, record seizure, and outstanding tax recovery?",
                "Can FBR freeze bank accounts or seize property to recover unpaid taxes under Section 140?",
                "fbr search seizure powers section 175",
                "freeze bank account tax recovery section 140",
                "arrest property sale default section 138"
            ],
            "keywords": ["search power", "seizure", "freeze bank account", "outstanding recovery", "arrest default", "section 140"]
        }
    ],
    "Consumer Protection Laws": [
        {
            "title": "Consumer Claims & Pre-Suit Legal Notice",
            "statute": "Section 28 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Section 28 of the Punjab Consumer Protection Act 2005 (and Section 27 of the Sindh Act), before filing a formal claim in the Consumer Court, a consumer must serve a mandatory 15-day written legal notice to the manufacturer or seller demanding a refund, replacement, or compensation. If unresolved, a claim must be filed in the Consumer Court within 30 days of the cause of action. No court fee is required, and consumers can represent themselves.",
            "q_templates": [
                "How do I file a claim in Consumer Court, and is a 15-day legal notice mandatory?",
                "What is the process to serve a legal notice to a shopkeeper for a bad purchase?",
                "consumer court legal notice template",
                "district consumer court complaint filing",
                "consumer court notice 15 days limit"
            ],
            "keywords": ["consumer court", "legal notice", "section 28", "complaint", "district court"]
        },
        {
            "title": "Defective Products & Manufacturer Liabilities",
            "statute": "Sections 4 & 5 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Sections 4 and 5 of the Consumer Protection Act, manufacturers are strictly liable for defective products they produce. A product is defective if it has a manufacturing defect, design defect, or lacks proper warning labels. The manufacturer must replace the defective product or refund the price to the consumer.",
            "q_templates": [
                "What is the liability of a manufacturer for selling a defective or dangerous product?",
                "How do I sue a company for a manufacturing design defect in Pakistan?",
                "defective product manufacturer liability",
                "strict product liability replacement refund",
                "manufacturing design defect consumer court"
            ],
            "keywords": ["defective product", "design defect", "strict liability", "manufacturer", "replacement", "refund"]
        },
        {
            "title": "Deficient/Negligent Services & Service Provider Liabilities",
            "statute": "Sections 13 & 15 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Sections 13 and 15 of the Consumer Protection Act, service providers (including dry cleaners, mechanics, doctors, tailors, and salons) are liable for deficient or negligent services. A service is deficient if it fails to meet the standard of care, skill, or warranty. The court can direct the provider to remedy the deficiency, refund the charges, or pay compensation.",
            "q_templates": [
                "What legal remedy is available for negligent, bad service from a mechanic or tailor?",
                "Can I sue a service provider for negligent work under the Consumer Protection Act?",
                "negligent service provider liability",
                "deficient service dry cleaner tailor",
                "remedy bad service mechanic hospital"
            ],
            "keywords": ["deficient service", "negligent service", "service provider", "compensation", "dry cleaner", "mechanic"]
        },
        {
            "title": "Online Shopping Fraud & E-commerce Scams",
            "statute": "Section 13 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Consumer Protection Acts, online stores and e-commerce platforms are fully liable for delivering defective, counterfeit, or incorrect products. If an e-commerce website sends a fake replica or damaged item and refuses to refund or exchange it, the consumer can file a complaint in the Consumer Court after serving the mandatory 15-day pre-suit legal notice.",
            "q_templates": [
                "What remedy is available if an online store delivers a fake or defective product?",
                "Can I sue an e-commerce website for sending a broken item and refusing exchange?",
                "online shopping scam consumer court",
                "fake replica delivery refund exchange",
                "ecommerce fraud legal notice website"
            ],
            "keywords": ["online shopping", "ecommerce scam", "fake product", "broken item", "refund exchange", "electronic market"]
        },
        {
            "title": "Damages for Mental Agony & Financial Loss",
            "statute": "Section 21 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Section 21 of the Consumer Protection Act, the Consumer Court has the authority to order product replacement, price refund, compensation for loss or injury, and damages for mental agony/agony caused by defective products or deficient services. The court can award substantial financial compensation to the consumer for hassle and distress.",
            "q_templates": [
                "Can a consumer claim damages for mental agony caused by faulty services in Consumer Court?",
                "What compensation can I get from a service provider for negligent work and mental stress?",
                "damages mental agony consumer court",
                "financial loss negligent service compensation",
                "section 21 consumer court award damages"
            ],
            "keywords": ["mental agony", "financial loss", "damages", "compensation", "stress", "hassle"]
        },
        {
            "title": "Mandatory Disclosures & Product Labeling Rules",
            "statute": "Section 11 & 18 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Sections 11 and 18, all manufacturers and packagers must display mandatory disclosures on products. This includes the product's weight, volume, active ingredients, retail price, manufacturing date, and expiry date. Selling products without these disclosures or selling expired goods is illegal and subject to heavy fines by the Consumer Court.",
            "q_templates": [
                "What product information must be displayed on packaging by law in Pakistan?",
                "Is it illegal to sell products without expiry dates or printed retail prices?",
                "product labeling mandatory disclosures",
                "selling expired goods consumer court",
                "printed retail price weight ingredients packaging"
            ],
            "keywords": ["product labeling", "expiry date", "retail price", "mandatory disclosures", "expired goods", "packaging"]
        },
        {
            "title": "Misleading Advertisements & False Representations",
            "statute": "Section 22 & 23 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Sections 22 and 23 of the Consumer Protection Act, false or misleading advertisements, bait advertising, and false representations regarding product quality, origin, standard, or warranty are strictly prohibited. Businesses making false claims face heavy penalties, corrective advertising orders, and liability to compensate affected consumers.",
            "q_templates": [
                "What are the penalties for false advertising or misleading product claims?",
                "Can a business be sued for bait advertising or claiming false quality standards?",
                "misleading advertisement false representations",
                "bait advertising penalty consumer",
                "false warranty quality claims shop"
            ],
            "keywords": ["misleading advertisement", "false advertising", "bait advertising", "false representation", "quality standards", "corrective advertising"]
        },
        {
            "title": "Unfair Contract Terms & Standard Form Contracts",
            "statute": "Provincial Consumer Protection Acts",
            "source": "Provincial Consumer Protection Laws",
            "text": "Consumer Protection Laws prohibit the inclusion of unfair terms in consumer contracts (such as dry cleaner slips stating the business is not liable for loss, or parking tickets waiving liability). Any standard form contract term that creates a significant imbalance in rights to the detriment of the consumer is void and unenforceable.",
            "q_templates": [
                "Are one-sided waiver clauses on dry cleaner slips or receipts legally binding?",
                "What is the legality of standard form contract waivers that exclude business liability?",
                "unfair contract terms consumer",
                "one sided waiver receipt dry cleaner",
                "exclude business liability void terms"
            ],
            "keywords": ["unfair terms", "waiver clause", "standard form contract", "exclude liability", "void agreement", "receipt waiver"]
        },
        {
            "title": "Receipts, Cash Memos, and Proof of Purchase",
            "statute": "Section 19 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Section 19 of the Consumer Protection Act, every seller of goods or services must issue a written receipt or cash memo containing the date, price, quantity, and description of goods sold. Failure to issue a cash memo is an offense, and a consumer can file a complaint against the shopkeeper in the Consumer Court.",
            "q_templates": [
                "Is a shopkeeper legally required to provide a printed receipt or cash memo for my purchase?",
                "What is the penalty if a seller refuses to issue a bill or cash receipt?",
                "cash memo receipt printed bill",
                "seller refuse issue receipt complaint",
                "section 19 proof of purchase"
            ],
            "keywords": ["cash memo", "receipt", "printed bill", "seller duty", "proof of purchase", "section 19"]
        },
        {
            "title": "Consumer Court Hierarchy, Powers, and Jurisdictions",
            "statute": "Establishment of Consumer Courts under Provincial Acts",
            "source": "Provincial Consumer Protection Laws",
            "text": "Provincial governments establish Consumer Courts at the district level, presided over by a District & Sessions Judge. These courts have the power to summon witnesses, receive evidence, inspect premises, and issue orders for refunds, replacements, and damages. Territorial jurisdiction is determined by where the transaction occurred or where the defendant works.",
            "q_templates": [
                "Who presides over the Consumer Court and what powers does it have in Pakistan?",
                "How do I determine which district consumer court has jurisdiction over my case?",
                "consumer court hierarchy powers judge",
                "territorial jurisdiction consumer court",
                "district sessions judge consumer"
            ],
            "keywords": ["consumer court", "sessions judge", "powers", "territorial jurisdiction", "pecuniary", "summon"]
        },
        {
            "title": "Limitation Period for Filing Consumer Complaints",
            "statute": "Section 28 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "A consumer complaint must be filed in the Consumer Court within 30 days of the cause of action (i.e. within 30 days of the receipt of the legal notice reply, or expiry of the 15-day notice period). The court can condone the delay if the consumer shows sufficient cause for the delay through an application for condonation.",
            "q_templates": [
                "What is the deadline or limitation period to file a case in Consumer Court?",
                "Can I file a consumer complaint after the 30-day deadline has passed?",
                "limitation period 30 days consumer",
                "condonation of delay application court",
                "deadline file consumer complaint"
            ],
            "keywords": ["limitation period", "deadline", "condonation of delay", "cause of action", "30 days limit"]
        },
        {
            "title": "Non-Compliance & Consumer Court Enforcement Penalties",
            "statute": "Section 31 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Section 31 of the Punjab Consumer Protection Act 2005, if a manufacturer or seller fails to comply with a Consumer Court order, the court can sentence them to imprisonment for up to 2 years, a fine of up to Rs. 100,000, or both. The court can issue warrants and direct the police to enforce its judgments.",
            "q_templates": [
                "What is the penalty if a manufacturer refuses to comply with a Consumer Court order?",
                "How can a court enforce a judgment against a seller who refuses to pay damages?",
                "non-compliance penalty jail sentence",
                "enforce consumer court order warrant",
                "section 31 fine imprisonment default"
            ],
            "keywords": ["non-compliance", "penalty", "imprisonment", "fine", "enforcement", "judgment"]
        },
        {
            "title": "Frivolous or False Consumer Complaints",
            "statute": "Section 30 of the Punjab Consumer Protection Act, 2005",
            "source": "Punjab Consumer Protection Act, 2005",
            "text": "Under Section 30, if the Consumer Court finds that a complaint is false, frivolous, vexatious, or filed in bad faith to harass a business, the court can dismiss the complaint and order the consumer to pay costs and compensation to the seller up to Rs. 10,000.",
            "q_templates": [
                "What happens if someone files a false or fake case in Consumer Court?",
                "Can a business get compensation for a frivolous complaint filed against it?",
                "frivolous complaint penalty false case",
                "vexatious consumer claim dismiss cost",
                "section 30 false complaint compensation"
            ],
            "keywords": ["frivolous", "false complaint", "vexatious", "dismiss", "penalty cost", "harass business"]
        },
        {
            "title": "Warranty and Guarantee Enforcement",
            "statute": "Provincial Consumer Protection Laws",
            "source": "Provincial Consumer Protection Laws",
            "text": "A seller or manufacturer is legally bound to honor any warranty, guarantee, or service contract offered at the time of purchase. If a business fails to replace defective parts, perform free repairs, or replace a product under warranty, it is a violation of the Consumer Protection Act, and the consumer can claim remedies in Consumer Court.",
            "q_templates": [
                "Can I sue a shopkeeper for failing to honor a product warranty card?",
                "What can I do if a company refuses free repair under warranty during the warranty period?",
                "warranty card guarantee honor shop",
                "company refuse repair warranty period",
                "sue failure honor product warranty"
            ],
            "keywords": ["warranty", "guarantee", "repair", "warranty card", "honor warranty", "replace parts"]
        },
        {
            "title": "Price Gouging, Overcharging, and Display of Price Lists",
            "statute": "Display of Price Lists and Overcharging Regulations",
            "source": "Provincial Consumer Laws",
            "text": "Charging a consumer above the printed retail price (price gouging/overcharging) is strictly illegal under consumer laws. Shopkeepers must prominently display a price list of essential commodities. Violators face summary fines by price control magistrates and prosecution before the Consumer Court.",
            "q_templates": [
                "Is it illegal for a shopkeeper to charge more than the printed retail price on a product?",
                "Can I file a case against a shopkeeper for overcharging or not displaying price lists?",
                "price gouging retail price overcharge",
                "display price list shopkeeper legal",
                "price control magistrate fine shop"
            ],
            "keywords": ["price gouging", "overcharging", "retail price", "price list display", "price control", "magistrate"]
        }
    ],
    "Constitutional Laws": [
        {
            "title": "Fundamental Rights to Liberty & Fair Trial",
            "statute": "Articles 9 and 10-A of the Constitution of Pakistan, 1973",
            "source": "Constitution of Pakistan, 1973",
            "text": "The Constitution of Pakistan 1973 guarantees fundamental rights in Part II, Chapter 1. Article 9 protects the security of person, stating that no person shall be deprived of life or liberty save in accordance with law. Article 10 provides safeguards against unlawful arrest/detention, and Article 10-A guarantees the right to a fair trial and due process in all civil and criminal proceedings.",
            "q_templates": [
                "What are the fundamental rights of a citizen regarding fair trial (10-A) and security (9) under the Constitution?",
                "What does Article 9 of the Constitution of Pakistan guarantee?"
            ],
            "keywords": ["fundamental rights", "article 9", "article 10-a", "fair trial", "liberty", "due process"]
        },
        {
            "title": "Writ Petitions under Article 199",
            "statute": "Article 199 of the Constitution of Pakistan, 1973",
            "source": "Constitution of Pakistan, 1973",
            "text": "Under Article 199 of the Constitution, any aggrieved citizen can file a Writ Petition in the High Court to enforce fundamental rights or challenge illegal actions of public authorities. The High Court can issue five writs: Mandamus (ordering public duty), Prohibition (stopping excess of authority), Certiorari (quashing illegal orders), Habeas Corpus (releasing illegal detainees), and Quo Warranto (challenging public office title).",
            "q_templates": [
                "How do I file a Writ Petition under Article 199 of the Constitution in the High Court?",
                "What are the types of writs a citizen can file against government actions?"
            ],
            "keywords": ["writ petition", "article 199", "high court", "mandamus", "certiorari", "fundamental rights"]
        },
        {
            "title": "Habeas Corpus Writs against Unlawful Detention",
            "statute": "Article 199 of the Constitution of Pakistan, 1973",
            "source": "Constitution of Pakistan, 1973",
            "text": "Habeas Corpus is a constitutional writ under Article 199 of the Constitution, which directs any person (including police or security agencies) detaining someone to produce the detainee before the High Court. If the detention is found to be without lawful authority, the court orders their immediate release.",
            "q_templates": [
                "What is a Habeas Corpus writ, and when can a High Court issue it to release a detainee?",
                "How can I legally recover a family member detained unlawfully by police?"
            ],
            "keywords": ["habeas corpus", "unlawful detention", "police custody", "release order", "illegal arrest"]
        },
        {
            "title": "Freedom of Speech & Constitutional Restrictions",
            "statute": "Article 19 of the Constitution of Pakistan, 1973",
            "source": "Constitution of Pakistan, 1973",
            "text": "Article 19 of the Constitution guarantees freedom of speech and expression, and freedom of the press. However, this right is not absolute and is subject to reasonable restrictions imposed by law in the interest of the glory of Islam, the integrity/security of Pakistan, public order, decency, or contempt of court.",
            "q_templates": [
                "Is freedom of speech absolute under Article 19 of the Constitution of Pakistan?",
                "What are the legal limits of expression and press freedom in Pakistan?"
            ],
            "keywords": ["freedom of speech", "article 19", "press freedom", "contempt of court", "restrictions"]
        }
    ]
}

class DatasetGenerator:
    def __init__(self):
        config = get_config()
        self.categories = config["categories"]
        self.output_json = config["dataset_json_path"]
        self.output_csv = config["dataset_csv_path"]

    def generate_balanced_dataset(self) -> List[Dict[str, Any]]:
        logger.info(f"Generating balanced dataset across {len(self.categories)} categories...")
        dataset = []
        
        names = ["Ahmad", "Fatima", "Zainab", "Ali", "Ayesha", "Muhammad", "Bilal", "Sana", "Usman", "Hamza"]
        cities = ["Lahore", "Karachi", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta"]
        relationships = ["husband", "neighbor", "landlord", "employer", "business partner"]
        amounts = ["50,000", "100,000", "500,000", "1,000,000", "200,000"]
        difficulties = ["Easy", "Medium", "Hard"]
        
        count = 1

        for category in self.categories:
            topics = LEGAL_DOCUMENTS_CORPUS.get(category, [])
            if not topics:
                topics = [{
                    "title": f"General Statutory Codex of {category}",
                    "statute": f"General Statutes regarding {category}",
                    "source": f"Pakistan Statutory Laws ({category})",
                    "text": f"This is the official legal document regulating {category} in the territory of Pakistan.",
                    "q_templates": [f"What is the legal framework regarding {category} in Pakistan?"],
                    "keywords": [category.lower(), "statutory", "legal", "court"]
                }]

            records_for_this_cat = 1000 if category == "Family Laws" else (3000 if (category == "Criminal Laws" or category == "Civil Laws" or category == "Property Laws" or category == "Labour Laws" or category == "Tax Laws" or category == "Consumer Protection Laws") else 150)
            cat_count = 0
            while cat_count < records_for_this_cat:
                topic = topics[cat_count % len(topics)]
                
                name = random.choice(names)
                city = random.choice(cities)
                relation = random.choice(relationships)
                amount = random.choice(amounts)
                
                chosen_q_template = random.choice(topic["q_templates"])
                chosen_q = chosen_q_template.replace("{amount}", amount)

                question_styles = [
                    f"Case Ref {count:05d}: My name is {name} from {city}. {chosen_q}",
                    f"Case Ref {count:05d}: In {city}, I have a dispute with my {relation}. {chosen_q}",
                    f"Case Ref {count:05d}: Regarding {topic['title']} under {topic.get('source', 'Pakistani Law')}: {chosen_q}"
                ]
                final_q = random.choice(question_styles)
                final_a = topic["text"].strip()
                
                record = {
                    "id": f"L_QA_{count:06d}",
                    "category": category,
                    "question": final_q,
                    "answer": final_a,
                    "source": topic.get("source", "Constitution and Statutes of Pakistan"),
                    "keywords": topic.get("keywords", [category.lower()]) + [city.lower(), relation],
                    "difficulty": random.choice(difficulties),
                    "language": "English",
                    "title": topic["title"],
                    "statute": topic.get("statute", "Statutory Provisions of Pakistan")
                }
                
                dataset.append(record)
                count += 1
                cat_count += 1

        random.shuffle(dataset)
        return dataset

    def run(self):
        logger.info("Initializing upgraded legal dataset compiler...")
        dataset = self.generate_balanced_dataset()
        
        seen_qs = set()
        deduped_dataset = []
        for r in dataset:
            if r["question"] not in seen_qs:
                seen_qs.add(r["question"])
                deduped_dataset.append(r)
                
        logger.info(f"Deduplicated dataset: {len(deduped_dataset)} valid entries.")
        
        # Save to JSON
        os.makedirs(os.path.dirname(self.output_json), exist_ok=True)
        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(deduped_dataset, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved dataset JSON to {self.output_json}")
        
        # Save to CSV
        with open(self.output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category", "question", "answer", "source", "keywords", "difficulty", "language", "title", "statute"])
            for r in deduped_dataset:
                writer.writerow([
                    r["id"], r["category"], r["question"], r["answer"], r["source"], 
                    ",".join(r["keywords"]), r["difficulty"], r["language"], r.get("title", ""), r.get("statute", "")
                ])
        logger.info(f"Saved dataset CSV to {self.output_csv}")

if __name__ == "__main__":
    generator = DatasetGenerator()
    generator.run()
