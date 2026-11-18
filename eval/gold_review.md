# Gold evidence review

Every quote below was checked automatically against the ingested corpus by `python -m src.testset`.

## lk-01 (lookup, tune)

**Q:** What is GitLab's daily reimbursement limit for internet access while travelling?

**Expected:** Up to $50 USD (or local equivalent) per day.

- `hb:finance/expenses`
  > Internet while traveling is reimbursable for up to $50 USD (or local equivalent currency) per day.
  - gold chunks: hb:finance/expenses::fixed-500-50::12
- same answer in other version(s), acceptable: syn:expenses-2023

## lk-02 (lookup, tune)

**Q:** What is the monthly limit for reimbursing a co-working space at GitLab?

**Expected:** $700 per month (pre-approval is needed).

- `hb:finance/expenses`
  > $700.00 Limit per month.
  - gold chunks: hb:finance/expenses::fixed-500-50::13
- same answer in other version(s), acceptable: syn:expenses-2023

## lk-03 (lookup, test)

**Q:** Within how many working days does GitLab's Accounts Payable team process expense reports that need AP Admin review?

**Expected:** Within 7 working days from the date submitted.

- `hb:finance/expenses`
  > Review and process all expense reports that require AP Admin review, within 7 working days from the date submitted.
  - gold chunks: hb:finance/expenses::fixed-500-50::1
- same answer in other version(s), acceptable: syn:expenses-2023

## lk-04 (lookup, test)

**Q:** How many one-off co-working days per month can a GitLab team member expense without Manager or Finance approval?

**Expected:** Up to 5 one-off days in a calendar month.

- `hb:finance/expenses`
  > Up to 5 One-off Days in a calendar month related to co-working space do not require Manager or Finance approval.
  - gold chunks: hb:finance/expenses::fixed-500-50::14
- same answer in other version(s), acceptable: syn:expenses-2023

## lk-05 (lookup, test)

**Q:** How far in advance should GitLab team members book domestic flights?

**Expected:** At least 14 days in advance.

- `hb:finance/expenses`
  > Domestic: At least 14 days in advance
  - gold chunks: hb:finance/expenses::fixed-500-50::5
- same answer in other version(s), acceptable: syn:expenses-2023

## lk-06 (lookup, tune)

**Q:** How long does GitLab retain security incident communications sent to customers?

**Expected:** 3 years.

- `hb:security/policies_and_standards/records-retention-deletion`
  > Security incident communication to customers | 3 years
  - gold chunks: hb:security/policies_and_standards/records-retention-deletion::fixed-500-50::1
- same answer in other version(s), acceptable: syn:records-retention-2023

## lk-07 (lookup, tune)

**Q:** How often are user access reviews performed for SOX in-scope applications at GitLab?

**Expected:** Quarterly (entitlement reviews of all users).

- `hb:security/security-assurance/security-compliance/access-reviews`
  > SOX In-Scope Applications | Quarterly
  - gold chunks: hb:security/security-assurance/security-compliance/access-reviews::fixed-500-50::2

## lk-08 (lookup, test)

**Q:** How long does GitLab retain its annual risk assessment report?

**Expected:** 2 years.

- `hb:security/policies_and_standards/records-retention-deletion`
  > Annual risk assessment report | 2 years
  - gold chunks: hb:security/policies_and_standards/records-retention-deletion::fixed-500-50::1
- same answer in other version(s), acceptable: syn:records-retention-2023

## lk-09 (lookup, tune)

**Q:** What are the eligibility requirements for FMLA leave at GitLab in the US?

**Expected:** 1 year of service and 1,250 hours worked in the year immediately before the leave starts.

- `hb:people-policies/leave-of-absence/us`
  > 1 year of service, AND1250hrs worked in the year immediately priorto the start of leave
  - gold chunks: hb:people-policies/leave-of-absence/us::fixed-500-50::1
- same answer in other version(s), acceptable: syn:us-leave-of-absence-2022

## lk-10 (lookup, test)

**Q:** What is GitLab's standard discretionary bonus amount?

**Expected:** $1,000 (at the current exchange rate).

- `hb:total-rewards/incentives`
  > standard discretionary bonus amount ($1,000 at the current exchange rate)
  - gold chunks: hb:total-rewards/incentives::fixed-500-50::0

## lk-11 (lookup, tune)

**Q:** Over what reference period are average weekly working hours calculated for the 48-hour limit in GitLab's people policies?

**Expected:** Usually a 17-week reference period.

- `hb:people-policies`
  > Average working hours are calculated over a 'reference' period, which is usually 17 weeks.
  - gold chunks: hb:people-policies::fixed-500-50::12
- same answer in other version(s), acceptable: syn:people-policies-2022

## lk-12 (lookup, tune)

**Q:** At Lancaster City Council, how many days of sickness absence can an employee self-certify?

**Expected:** The first 7 calendar days (pro-rated for part-time employees); longer absences need a fit note.

- `pdf:lancaster-sickness-absence`
  > The first 7 calendar days (pro-rated for part time employees) of sickness absence can be self-certified
  - gold chunks: pdf:lancaster-sickness-absence::fixed-500-50::2

## lk-13 (lookup, tune)

**Q:** How many days of annual leave do Grade 1 to 9 staff get at Middlesex University?

**Expected:** 30 days per annum.

- `pdf:middlesex-annual-leave`
  > Grades 1 to 9 30 days per annum
  - gold chunks: pdf:middlesex-annual-leave::fixed-500-50::0

## lk-14 (lookup, tune)

**Q:** What mileage rate does Brunel University London pay for the first 10,000 business miles in a tax year?

**Expected:** 45p per mile.

- `pdf:brunel-travel-expenses`
  > 45p per mile For the first 10,000 miles of the tax year
  - gold chunks: pdf:brunel-travel-expenses::fixed-500-50::15

## lk-15 (lookup, tune)

**Q:** Within what time must Malvern Town Council report a personal data breach to the Information Commissioner?

**Expected:** Within 72 hours of discovery.

- `pdf:malvern-data-protection-staff`
  > Information Commissioner within 72 hours of discovery.
  - gold chunks: pdf:malvern-data-protection-staff::fixed-500-50::5

## lk-16 (lookup, tune)

**Q:** At the University of Roehampton, how quickly should receipt of a whistleblowing concern be acknowledged?

**Expected:** Normally within 3 days of receipt.

- `pdf:roehampton-whistleblowing`
  > acknowledge receipt of the concern, normally within 3 days of receipt.
  - gold chunks: pdf:roehampton-whistleblowing::fixed-500-50::2

## lk-17 (lookup, tune)

**Q:** How many days per week can Heriot-Watt University staff seek to work remotely?

**Expected:** Up to two days per week (pro-rata for part-time staff), by agreement with their manager.

- `pdf:heriot-watt-hybrid-working`
  > may seek agreement with their manager to work remotely for up to two days per week
  - gold chunks: pdf:heriot-watt-hybrid-working::fixed-500-50::2

## lk-18 (lookup, tune)

**Q:** Within what period are University of Waikato staff expected to take their annual leave?

**Expected:** Within 12 months of the date on which it becomes due.

- `pdf:waikato-annual-leave`
  > Staff are expected to take all annual leave within 12 months of the date on which the
  - gold chunks: pdf:waikato-annual-leave::fixed-500-50::0

## lk-19 (lookup, tune)

**Q:** What is GitLab's daily limit for fuel when using a rental car on business travel?

**Expected:** $300 per day.

- `hb:finance/expenses`
  > Fuel at $300 limit per day.
  - gold chunks: hb:finance/expenses::fixed-500-50::7
- same answer in other version(s), acceptable: syn:expenses-2023

## lk-20 (lookup, test)

**Q:** What are GitLab's limits for taxis and ride-shares on business trips?

**Expected:** $300 per round trip and $150 for a single trip.

- `hb:finance/expenses`
  > Ground Transportation (taxis, ubers) at $300 limit per round trip and $150 limit for single trip.
  - gold chunks: hb:finance/expenses::fixed-500-50::11
- same answer in other version(s), acceptable: syn:expenses-2023

## pp-01 (paraphrase, tune)

**Q:** How far from my home can a co-working space be for GitLab to pay for it?

**Expected:** Within a commutable distance (about 50 km) of your primary residence, except one-off day passes while travelling.

- `hb:finance/expenses`
  > located within a commutable distance (+-50km) of the Team Member's primary residence
  - gold chunks: hb:finance/expenses::fixed-500-50::13
- same answer in other version(s), acceptable: syn:expenses-2023

## pp-02 (paraphrase, tune)

**Q:** If GitLab pays for my co-working desk for a whole month, can I still claim my home internet?

**Expected:** No; with a full month of co-working, home internet cannot be expensed (a few co-working days still allows it).

- `hb:finance/expenses`
  > if you expense a co-working space for a full month then internet for home cannot be expensed.
  - gold chunks: hb:finance/expenses::fixed-500-50::14, hb:finance/expenses::fixed-500-50::19
- same answer in other version(s), acceptable: syn:expenses-2023

## pp-03 (paraphrase, tune)

**Q:** As a GitLab Support engineer, when should I rethink the dates I want to take off?

**Expected:** If the regional team would be short by 20% or more of its people on any of those days.

- `hb:support/support-time-off`
  > the regional team would be short by 20% or more of its people
  - gold chunks: hb:support/support-time-off::fixed-500-50::2

## pp-04 (paraphrase, tune)

**Q:** If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back?

**Expected:** Three months' notice.

- `hb:people-policies`
  > The notice period you are required to give is three months.
  - gold chunks: hb:people-policies::fixed-500-50::13
- same answer in other version(s), acceptable: syn:people-policies-2022

## pp-05 (paraphrase, tune)

**Q:** Do people joining GitLab have to complete a security course when they start?

**Expected:** Yes, New Hire Security Training is required during onboarding for all team members and contractors.

- `hb:security/security-assurance/governance/sec-training`
  > New Hire Security Training is required to be completed by all GitLab Team Members and contractors/TSPs during their onboarding at GitLab.
  - gold chunks: hb:security/security-assurance/governance/sec-training::fixed-500-50::0

## pp-06 (paraphrase, tune)

**Q:** What is the best thing to do when a fake scam email from GitLab's security team lands in my inbox?

**Expected:** Report it (ideal); deleting it is acceptable.

- `hb:security/security-assurance/governance/phishing`
  > The goal is that TMs either report the phishing attempt (ideal behavior) or delete the email (acceptable behavior).
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0
- same answer in other version(s), acceptable: syn:phishing-program-2022

## pp-07 (paraphrase, test)

**Q:** How does GitLab cover the tax bill when my restricted stock units become mine?

**Expected:** Shares are automatically sold at vesting to pay the taxes, based on your country's tax rate.

- `hb:total-rewards/stock-options`
  > Shares are sold to pay the taxes due on the RSU vesting.
  - gold chunks: hb:total-rewards/stock-options::fixed-500-50::1
- same answer in other version(s), acceptable: syn:stock-options-2021

## pp-08 (paraphrase, tune)

**Q:** Can I get a bonus for recommending a friend for an internship at GitLab?

**Expected:** No, contract or temporary roles including internships are not eligible (unless the intern later converts to a team member).

- `hb:hiring/referral-process`
  > Contract or temporary roles, including Internships, are not eligible for referral bonuses.
  - gold chunks: hb:hiring/referral-process::fixed-500-50::0
- same answer in other version(s), acceptable: syn:referral-process-2022

## pp-09 (paraphrase, test)

**Q:** At Lancaster City Council, when in the morning should I let my boss know I'm too ill to work?

**Expected:** As soon as possible after 9am.

- `pdf:lancaster-sickness-absence`
  > must contact their line manager as soon as possible following 9am.
  - gold chunks: pdf:lancaster-sickness-absence::fixed-500-50::1, pdf:lancaster-sickness-absence::fixed-500-50::2

## pp-10 (paraphrase, tune)

**Q:** At Brunel University London, how long do I have to ask for my work travel costs back?

**Expected:** Within 3 months from the end of the month the expense was incurred; later claims need extra authorisation.

- `pdf:brunel-travel-expenses`
  > Claims should be submitted within 3 months from the end of the month in which the expense is incurred.
  - gold chunks: pdf:brunel-travel-expenses::fixed-500-50::7

## pp-11 (paraphrase, test)

**Q:** Can the University of Waikato make staff use holiday days while the campus is shut?

**Expected:** Yes, during a close-down period, if at least 14 days' notice is given.

- `pdf:waikato-annual-leave`
  > it can require staff to take annual leave during that period provided at least 14 days' notice is given
  - gold chunks: pdf:waikato-annual-leave::fixed-500-50::0

## pp-12 (paraphrase, test)

**Q:** If I work three days a week at Middlesex University, how much holiday do I get?

**Expected:** A proportional amount: 3/5 of the full entitlement.

- `pdf:middlesex-annual-leave`
  > if 3 days per week worked, entitled to 3/5 of full entitlement
  - gold chunks: pdf:middlesex-annual-leave::fixed-500-50::0

## pp-13 (paraphrase, tune)

**Q:** What's the most I can spend on a present for a GitLab colleague?

**Expected:** Up to $125 USD per gift, including shipping.

- `hb:finance/expenses`
  > The allowable cost for gifts is up to $125 USD (including shipping) per gift.
  - gold chunks: hb:finance/expenses::fixed-500-50::18
- same answer in other version(s), acceptable: syn:expenses-2023

## pp-14 (paraphrase, tune)

**Q:** Can I buy second-hand work equipment from an individual and claim it back from GitLab?

**Expected:** Yes, purchases from private sellers are allowed, with a screenshot of the transaction as proof.

- `hb:finance/expenses`
  > Purchasing from Private Sellers (e.g. either new or used equipment) is allowed.
  - gold chunks: hb:finance/expenses::fixed-500-50::16
- same answer in other version(s), acceptable: syn:expenses-2023

## pp-15 (paraphrase, test)

**Q:** Where should most University of Cambridge staff send a report about wrongdoing?

**Expected:** To the Registrary, by email to registraryWBdisclosure@admin.cam.ac.uk.

- `pdf:cambridge-whistleblowing`
  > Email registraryWBdisclosure@admin.cam.ac.uk
  - gold chunks: pdf:cambridge-whistleblowing::fixed-500-50::2

## ex-01 (exact_term, test)

**Q:** What is PhishArm used for at GitLab?

**Expected:** It is the preferred way (Option 1) to report phishing emails.

- `hb:security/security-assurance/governance/phishing`
  > The preference for reporting phishing emails is Option 1 via PhishArm.
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::1
- same answer in other version(s), acceptable: syn:phishing-program-2022

## ex-02 (exact_term, test)

**Q:** Which company provides GitLab's phishing simulations?

**Expected:** ProofPoint.

- `hb:security/security-assurance/governance/phishing`
  > Phishing simulations are provided by ProofPoint
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0
- same answer in other version(s), acceptable: syn:phishing-program-2022

## ex-03 (exact_term, tune)

**Q:** What is CHIME in Brunel University London's expenses policy?

**Expected:** The online system through which employees submit expense claims.

- `pdf:brunel-travel-expenses`
  > expenses are submitted online through CHIME in a timely manner
  - gold chunks: pdf:brunel-travel-expenses::fixed-500-50::3

## ex-04 (exact_term, tune)

**Q:** What does the RED data classification mean at GitLab?

**Expected:** GitLab's most sensitive, restricted data; access is privileged and must be explicitly approved.

- `hb:security/policies_and_standards/data-classification-standard`
  > This is GitLab's most sensitive data and access to it should be considered privileged and must be explicitly approved.
  - gold chunks: hb:security/policies_and_standards/data-classification-standard::fixed-500-50::1

## ex-05 (exact_term, test)

**Q:** How often are PCI in-scope applications reviewed in GitLab's access review procedure?

**Expected:** Bi-annually (every 6 months).

- `hb:security/security-assurance/security-compliance/access-reviews`
  > PCI In-Scope Applications | Bi-Annual (6 months)
  - gold chunks: hb:security/security-assurance/security-compliance/access-reviews::fixed-500-50::2

## ex-06 (exact_term, tune)

**Q:** For which GitLab entities is the default mileage rate set at $.50/mile?

**Expected:** GitLab IT BV, GitLab Korea and GitLab Japan.

- `hb:finance/expenses`
  > so please update the rate on your mileage if needed to match your local compliance laws: GitLab IT BV, GitLab Korea and GitLab Japan.
  - gold chunks: hb:finance/expenses::fixed-500-50::11
- same answer in other version(s), acceptable: syn:expenses-2023

## ex-07 (exact_term, tune)

**Q:** What is Āku Mahi at the University of Waikato?

**Expected:** The University's online leave system, used for annual leave applications and approvals.

- `pdf:waikato-annual-leave`
  > University's online leave system Āku Mahi
  - gold chunks: pdf:waikato-annual-leave::fixed-500-50::1

## ex-08 (exact_term, tune)

**Q:** What is LevelUp at GitLab?

**Expected:** GitLab's internal learning platform, where training such as Data Classification Training is available.

- `hb:security/policies_and_standards/data-classification-standard`
  > Training is available via LevelUp, GitLab's internal learning platform.
  - gold chunks: hb:security/policies_and_standards/data-classification-standard::fixed-500-50::0

## ex-09 (exact_term, tune)

**Q:** Which organisation's guidelines does GitLab's Secure Coding Training use?

**Expected:** OWASP (Open Web Application Security Project) Secure Coding Guidelines.

- `hb:security/security-assurance/governance/sec-training`
  > Secure Coding Guidelines from OWASP (Open Web Application Security Project)
  - gold chunks: hb:security/security-assurance/governance/sec-training::fixed-500-50::1

## ex-10 (exact_term, tune)

**Q:** What counts as a "Late Invoice" under GitLab's Vendor Terms and Conditions?

**Expected:** A vendor invoice submitted more than ninety (90) days after the services or products were provided.

- `hb:finance/procurement/vendor-guidelines/vendor-agreement`
  > Correct Vendor invoices must be submitted no later than ninety (90) days from the provisions of Professional Services and/or Products
  - gold chunks: hb:finance/procurement/vendor-guidelines/vendor-agreement::fixed-500-50::4

## md-01 (multi_doc, test)

**Q:** Compare the mileage rate Brunel University London pays for the first 10,000 miles with GitLab's default rate for GitLab Korea.

**Expected:** Brunel pays 45p per mile; GitLab's default for GitLab Korea (and IT BV, Japan) is $.50 per mile.

- `pdf:brunel-travel-expenses`
  > 45p per mile For the first 10,000 miles of the tax year
  - gold chunks: pdf:brunel-travel-expenses::fixed-500-50::15
- `hb:finance/expenses`
  > so please update the rate on your mileage if needed to match your local compliance laws: GitLab IT BV, GitLab Korea and GitLab Japan.
  - gold chunks: hb:finance/expenses::fixed-500-50::11
- same answer in other version(s), acceptable: syn:expenses-2023

## md-02 (multi_doc, tune)

**Q:** How quickly does the University of Roehampton acknowledge a whistleblowing concern, and who issues the University of Salford's whistleblowing policy?

**Expected:** Roehampton normally acknowledges within 3 days; Salford's policy is issued by the Director of Legal Services.

- `pdf:roehampton-whistleblowing`
  > acknowledge receipt of the concern, normally within 3 days of receipt.
  - gold chunks: pdf:roehampton-whistleblowing::fixed-500-50::2
- `pdf:salford-whistleblowing`
  > This policy is issued by the Director of Legal Services
  - gold chunks: pdf:salford-whistleblowing::fixed-500-50::0

## md-03 (multi_doc, tune)

**Q:** Compare Brunel University London's deadline for staff expense claims with GitLab's deadline for vendors to submit invoices.

**Expected:** Brunel: within 3 months from the end of the month the expense was incurred. GitLab vendors: no later than 90 days after providing the services/products.

- `pdf:brunel-travel-expenses`
  > Claims should be submitted within 3 months from the end of the month in which the expense is incurred.
  - gold chunks: pdf:brunel-travel-expenses::fixed-500-50::7
- `hb:finance/procurement/vendor-guidelines/vendor-agreement`
  > Correct Vendor invoices must be submitted no later than ninety (90) days from the provisions of Professional Services and/or Products
  - gold chunks: hb:finance/procurement/vendor-guidelines/vendor-agreement::fixed-500-50::4

## md-04 (multi_doc, tune)

**Q:** How many days of annual leave do senior managers get at Middlesex University, and how much continuous leave must a University of Waikato manager allow?

**Expected:** Middlesex senior managers get 35 days per year; Waikato managers must allow at least two weeks in a continuous period.

- `pdf:middlesex-annual-leave`
  > Senior Managers 35 days per annum
  - gold chunks: pdf:middlesex-annual-leave::fixed-500-50::0
- `pdf:waikato-annual-leave`
  > a line manager must allow a staff member to take at least two weeks of their annual leave entitlement in a continuous period.
  - gold chunks: pdf:waikato-annual-leave::fixed-500-50::0

## md-05 (multi_doc, tune)

**Q:** What do Malvern Town Council and Havant Borough Council each require when a personal data breach happens?

**Expected:** Malvern reports breaches to the Information Commissioner within 72 hours of discovery; Havant requires breaches to follow its Data Incident Report Plan.

- `pdf:malvern-data-protection-staff`
  > Information Commissioner within 72 hours of discovery.
  - gold chunks: pdf:malvern-data-protection-staff::fixed-500-50::5
- `pdf:havant-data-protection`
  > Any data security breaches must follow the Councils Data Incident Report Plan.
  - gold chunks: pdf:havant-data-protection::fixed-500-50::7

## md-06 (multi_doc, tune)

**Q:** How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed?

**Expected:** Production change records are kept 3 years; external certification systems get quarterly entitlement reviews.

- `hb:security/policies_and_standards/records-retention-deletion`
  > Production changes | 3 years
  - gold chunks: hb:security/policies_and_standards/records-retention-deletion::fixed-500-50::0
- `hb:security/security-assurance/security-compliance/access-reviews`
  > External Certification Systems | Quarterly
  - gold chunks: hb:security/security-assurance/security-compliance/access-reviews::fixed-500-50::2
- same answer in other version(s), acceptable: syn:records-retention-2023

## md-07 (multi_doc, test)

**Q:** Which third parties deliver GitLab's annual security awareness training and its phishing simulations?

**Expected:** Right Hand Cybersecurity delivers the annual security awareness training; ProofPoint runs the phishing simulations.

- `hb:security/security-assurance/governance/sec-training`
  > provided annually via Right Hand Cybersecurity, GitLab's third-party provider
  - gold chunks: hb:security/security-assurance/governance/sec-training::fixed-500-50::1
- `hb:security/security-assurance/governance/phishing`
  > Phishing simulations are provided by ProofPoint
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0
- same answer in other version(s), acceptable: syn:phishing-program-2022

## md-08 (multi_doc, tune)

**Q:** How many days of annual leave do academic staff get at Middlesex University, and within what period must University of Waikato staff use their annual leave?

**Expected:** Middlesex academic and research staff get 35 days per year; Waikato staff are expected to take their leave within 12 months of it becoming due.

- `pdf:middlesex-annual-leave`
  > Academic and research staff 35 days per annum
  - gold chunks: pdf:middlesex-annual-leave::fixed-500-50::0
- `pdf:waikato-annual-leave`
  > Staff are expected to take all annual leave within 12 months of the date on which the
  - gold chunks: pdf:waikato-annual-leave::fixed-500-50::0

## md-09 (multi_doc, test)

**Q:** What is GitLab's limit for a single taxi trip, and what mileage rate does Brunel University London pay after 10,000 miles?

**Expected:** GitLab: $150 for a single trip ($300 round trip). Brunel: 25p per mile after 10,000 miles.

- `hb:finance/expenses`
  > Ground Transportation (taxis, ubers) at $300 limit per round trip and $150 limit for single trip.
  - gold chunks: hb:finance/expenses::fixed-500-50::11
- `pdf:brunel-travel-expenses`
  > 25p per mile After 10,000 miles
  - gold chunks: pdf:brunel-travel-expenses::fixed-500-50::15
- same answer in other version(s), acceptable: syn:expenses-2023

## md-10 (multi_doc, tune)

**Q:** What is RED data at GitLab, and how often must access to Red Data systems be reviewed?

**Expected:** RED is GitLab's most sensitive restricted data with explicitly approved, privileged access; access to Red Data systems is reviewed annually.

- `hb:security/policies_and_standards/data-classification-standard`
  > This is GitLab's most sensitive data and access to it should be considered privileged and must be explicitly approved.
  - gold chunks: hb:security/policies_and_standards/data-classification-standard::fixed-500-50::1
- `hb:security/security-assurance/security-compliance/access-reviews`
  > Red Data Systems | Annual
  - gold chunks: hb:security/security-assurance/security-compliance/access-reviews::fixed-500-50::2

## lk-21 (lookup, test)

**Q:** What is the emergency medical benefit limit under GitLab's business travel insurance?

**Expected:** Up to $10,000.

- `hb:finance/travel`
  > Emergency Medical Benefits | Up to $10,000
  - gold chunks: hb:finance/travel::fixed-500-50::1
- same answer in other version(s), acceptable: syn:travel-safety-2022

## lk-22 (lookup, tune)

**Q:** How can either party terminate the GitLab Testing Agreement for convenience?

**Expected:** Immediately, upon written notice to the other party (email is sufficient).

- `hb:legal/testing-agreement`
  > Upon written notice to the other party (email is sufficient), either party may terminate this Agreement immediately for convenience.
  - gold chunks: hb:legal/testing-agreement::fixed-500-50::4
- same answer in other version(s), acceptable: hb:legal/testing-agreement-v4, hb:legal/testing-agreement-v5

## lk-23 (lookup, tune)

**Q:** When will the University of Cambridge's Hybrid Working Policy be reviewed?

**Expected:** 12 months after the implementation date (and periodically after that).

- `pdf:cambridge-hybrid-working-2023`
  > The Policy will be reviewed 12 months after the implementation date
  - gold chunks: pdf:cambridge-hybrid-working-2023::fixed-500-50::10
- same answer in other version(s), acceptable: pdf:cambridge-hybrid-working-draft-2022

## lk-24 (lookup, test)

**Q:** Under North Lanarkshire Council's IT acceptable use policy, is personal use of council IT monitored?

**Expected:** Yes, all personal use is subject to the same monitoring as business use.

- `pdf:north-lanarkshire-it-acceptable-use-v5`
  > all personal use is subject to the same monitoring activities as business use
  - gold chunks: pdf:north-lanarkshire-it-acceptable-use-v5::fixed-500-50::9
- same answer in other version(s), acceptable: pdf:north-lanarkshire-it-acceptable-use-v4

## lk-25 (lookup, tune)

**Q:** How many free coaching sessions per year does Modern Health give GitLab team members?

**Expected:** 6 per year.

- `hb:total-rewards/benefits/modern-health`
  > 6 complimentary coaching sessions per year for personal and professional growth
  - gold chunks: hb:total-rewards/benefits/modern-health::fixed-500-50::0
- same answer in other version(s), acceptable: syn:modern-health-2023

## ov-06 (outdated_version, tune)

**Q:** How long after the purchase date can I submit a GitLab expense claim and still be reimbursed without manager approval?

**Expected:** Up to 90 days; claims over 90 days are not reimbursed unless approved by the manager.

- `hb:finance/expenses`
  > Expense claims over 90 days from purchase date will not be reimbursed unless approved by the Manager.
  - gold chunks: hb:finance/expenses::fixed-500-50::1, hb:finance/expenses::fixed-500-50::2
- old version syn:expenses-2023 says: "expense claims over 60 days from purchase date will not be reimbursed unless approved by the manager."

## ov-07 (outdated_version, tune)

**Q:** What is GitLab's nightly hotel limit for business travel?

**Expected:** $300 USD per night including tax, for standard rooms.

- `hb:finance/expenses`
  > Hotel stays are reimbursable up to $300 USD (or equivalent local currency) inclusive of tax per night for standard rooms
  - gold chunks: hb:finance/expenses::fixed-500-50::8
- old version syn:expenses-2023 says: "hotel stays are reimbursable up to $250 usd (or equivalent local currency) inclusive of tax per night for standard rooms"

## ov-08 (outdated_version, tune)

**Q:** How much can I spend on meals per day while travelling for GitLab?

**Expected:** Up to $120 USD (or local equivalent) per day.

- `hb:finance/expenses`
  > Meals while traveling on Company business are reimbursable, up to $120 USD (or local equivalent currency) per day.
  - gold chunks: hb:finance/expenses::fixed-500-50::9, hb:finance/expenses::fixed-500-50::10
- old version syn:expenses-2023 says: "meals while traveling on company business are reimbursable, up to $100 usd (or local equivalent currency) per day."

## ov-09 (outdated_version, test)

**Q:** What minimum password length does GitLab's password standard require?

**Expected:** 12 characters.

- `hb:security/policies_and_standards/password-standard`
  > For systems where a password can be configured the minimum password length needs to be set to 12 characters.
  - gold chunks: hb:security/policies_and_standards/password-standard::fixed-500-50::1
- old version syn:password-standard-2022 says: "for systems where a password can be configured the minimum password length needs to be set to 8 characters."

## ov-10 (outdated_version, test)

**Q:** What is the maximum expiry period for a GitLab personal access token?

**Expected:** 30 days.

- `hb:security/policies_and_standards/token-management-standard`
  > Personal Access Tokens - 30 days
  - gold chunks: hb:security/policies_and_standards/token-management-standard::fixed-500-50::3, hb:security/policies_and_standards/token-management-standard::fixed-500-50::4
- old version syn:token-management-standard-2023 says: "personal access tokens - 90 days"

## ov-11 (outdated_version, tune)

**Q:** How long is parental leave for GitLab team members in the US?

**Expected:** 16 weeks (job protected, except in certain circumstances).

- `hb:people-policies/leave-of-absence/us`
  > Parental Leave | 16 weeks
  - gold chunks: hb:people-policies/leave-of-absence/us::fixed-500-50::1
- old version syn:us-leave-of-absence-2022 says: "parental leave | 12 weeks"

## ov-12 (outdated_version, tune)

**Q:** For how long does someone I refer to GitLab count as my referral?

**Expected:** 6 months from the date Talent Acquisition receives the referral, for jobs in the same job family.

- `hb:hiring/referral-process`
  > Your referral is classified as your referral for 6 months
  - gold chunks: hb:hiring/referral-process::fixed-500-50::2
- old version syn:referral-process-2022 says: "your referral is classified as your referral for 12 months"

## ov-13 (outdated_version, tune)

**Q:** How long do I have to exercise vested GitLab stock options after leaving the company?

**Expected:** 90 days after termination.

- `hb:total-rewards/stock-options`
  > they have 90 days post termination to exercise their vested options.
  - gold chunks: hb:total-rewards/stock-options::fixed-500-50::0
- old version syn:stock-options-2021 says: "they have 30 days post termination to exercise their vested options."

## ov-14 (outdated_version, tune)

**Q:** How often does GitLab run phishing simulation campaigns?

**Expected:** At least once each fiscal quarter.

- `hb:security/security-assurance/governance/phishing`
  > At a minimum, one phishing simulation campaign will take place each fiscal quarter.
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0, hb:security/security-assurance/governance/phishing::fixed-500-50::3
- old version syn:phishing-program-2022 says: "at a minimum, one phishing simulation campaign will take place twice per fiscal year."

## ov-15 (outdated_version, test)

**Q:** After how many days of unreported absence can a GitLab team member be terminated for job abandonment?

**Expected:** Three consecutive workdays with no calendar entry and no contact with their supervisor (unless otherwise required by law).

- `hb:people-policies`
  > When a team member is absent from work for three consecutive workdays
  - gold chunks: hb:people-policies::fixed-500-50::5
- old version syn:people-policies-2022 says: "when a team member is absent from work for five consecutive workdays"

## ov-16 (outdated_version, tune)

**Q:** How far in advance should GitLab team members book international flights?

**Expected:** At least 21 days in advance.

- `hb:finance/expenses`
  > International: At least 21 days in advance
  - gold chunks: hb:finance/expenses::fixed-500-50::5
- old version syn:expenses-2023 says: "international: at least 30 days in advance"

## ov-17 (outdated_version, tune)

**Q:** What is GitLab's daily limit for parking and tolls on business travel?

**Expected:** $150 per day.

- `hb:finance/expenses`
  > Parking and tolls  at $150 limit per day.
  - gold chunks: hb:finance/expenses::fixed-500-50::11, hb:finance/expenses::fixed-500-50::12
- old version syn:expenses-2023 says: "parking and tolls at $100 limit per day."

## ov-18 (outdated_version, test)

**Q:** What is GitLab's yearly reimbursement limit for business cards?

**Expected:** $60 per year (ordered via Moo).

- `hb:finance/expenses`
  > Limit is set to $60/year.
  - gold chunks: hb:finance/expenses::fixed-500-50::13
- old version syn:expenses-2023 says: "limit is set to $40/year."

## ov-19 (outdated_version, test)

**Q:** When can I expense dry cleaning during a GitLab business trip?

**Expected:** If the stay is over 5 days.

- `hb:finance/expenses`
  > Dry cleaning is allowable if the stay is over 5 days.
  - gold chunks: hb:finance/expenses::fixed-500-50::9
- old version syn:expenses-2023 says: "dry cleaning is allowable if the stay is over 7 days."

## ov-20 (outdated_version, test)

**Q:** For applications where a password is the only authentication, how often must GitLab passwords expire?

**Expected:** Within a maximum of 90 calendar days.

- `hb:security/policies_and_standards/password-standard`
  > For applications where a password is the only source of authentication, a password must be expired within a maximum of 90 calendar days.
  - gold chunks: hb:security/policies_and_standards/password-standard::fixed-500-50::1
- old version syn:password-standard-2022 says: "for applications where a password is the only source of authentication, a password must be expired within a maximum of 60 calendar days."

## ov-21 (outdated_version, tune)

**Q:** After how many failed login attempts must a GitLab system temporarily lock the account?

**Expected:** After 10 failed attempts.

- `hb:security/policies_and_standards/password-standard`
  > Repeated failed login attempts need to trigger a temporary account lockout after 10 failed attempts.
  - gold chunks: hb:security/policies_and_standards/password-standard::fixed-500-50::1
- old version syn:password-standard-2022 says: "repeated failed login attempts need to trigger a temporary account lockout after 5 failed attempts."

## ov-22 (outdated_version, tune)

**Q:** What is the maximum lifetime of a GitLab group access token?

**Expected:** 1 year.

- `hb:security/policies_and_standards/token-management-standard`
  > Group Tokens – 1 year
  - gold chunks: hb:security/policies_and_standards/token-management-standard::fixed-500-50::4
- old version syn:token-management-standard-2023 says: "group tokens – 2 years"

## ov-23 (outdated_version, test)

**Q:** When do unexercised GitLab stock options expire?

**Expected:** 10 years after they were issued (if they haven't expired earlier through termination).

- `hb:total-rewards/stock-options`
  > your stock options expire 10 years after they were issued.
  - gold chunks: hb:total-rewards/stock-options::fixed-500-50::8
- old version syn:stock-options-2021 says: "your stock options expire 7 years after they were issued."

## ov-24 (outdated_version, test)

**Q:** How long can a new Support on-call alert go unacknowledged before the Support Manager on-call is alerted?

**Expected:** 10 minutes (Senior Support Managers are alerted after a further 5 minutes).

- `hb:support/on-call`
  > If a new alert has not been acknowledged after 10 minutes, the Support Manager on-call is alerted.
  - gold chunks: hb:support/on-call::fixed-500-50::3
- old version syn:support-on-call-2023 says: "if a new alert has not been acknowledged after 15 minutes, the support manager on-call is alerted."

## ov-25 (outdated_version, tune)

**Q:** During a long customer emergency call, how often should a GitLab Support engineer plan to take a break?

**Expected:** About every 90 minutes.

- `hb:support/on-call`
  > you plan to take a break each 90 minutes
  - gold chunks: hb:support/on-call::fixed-500-50::2
- old version syn:support-on-call-2023 says: "you plan to take a break each 60 minutes"

## ov-26 (outdated_version, tune)

**Q:** How long can a business trip last and still be covered by GitLab's travel insurance?

**Expected:** Less than 180 days.

- `hb:finance/travel`
  > Trip Duration | Covered for trips less than 180 days
  - gold chunks: hb:finance/travel::fixed-500-50::1
- old version syn:travel-safety-2022 says: "trip duration | covered for trips less than 90 days"

## ov-27 (outdated_version, tune)

**Q:** What is the maximum baggage protection under GitLab's business travel insurance?

**Expected:** $2,500.

- `hb:finance/travel`
  > Baggage Protection | Maximum of $2,500
  - gold chunks: hb:finance/travel::fixed-500-50::1
- old version syn:travel-safety-2022 says: "baggage protection | maximum of $1,500"

## ov-28 (outdated_version, tune)

**Q:** How many free therapy sessions per year does Modern Health give GitLab team members?

**Expected:** 6 per year.

- `hb:total-rewards/benefits/modern-health`
  > 6 complimentary therapy sessions per year with licensed mental health professionals
  - gold chunks: hb:total-rewards/benefits/modern-health::fixed-500-50::0
- old version syn:modern-health-2023 says: "4 complimentary therapy sessions per year with licensed mental health professionals"

## ov-29 (outdated_version, tune)

**Q:** Up to what age are team members' children eligible for Modern Health?

**Expected:** Up to age 27.

- `hb:total-rewards/benefits/modern-health`
  > Children up to age 27
  - gold chunks: hb:total-rewards/benefits/modern-health::fixed-500-50::0
- old version syn:modern-health-2023 says: "children up to age 26"

## ov-30 (outdated_version, tune)

**Q:** How much of base salary does GitLab's US short- and long-term disability insurance replace?

**Expected:** Up to 66.7% of base salary.

- `hb:total-rewards/benefits/general-and-entity-benefits/inc-benefits-us`
  > replacing up to 66.7% of base salary for qualifying disabilities
  - gold chunks: hb:total-rewards/benefits/general-and-entity-benefits/inc-benefits-us::fixed-500-50::6
- old version syn:inc-benefits-us-2023 says: "replacing up to 60% of base salary for qualifying disabilities"

## ov-31 (outdated_version, tune)

**Q:** How much dental coverage per year do GitLab UK team members get?

**Expected:** £400 per year (80% reimbursement).

- `hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk`
  > Dental coverage: £400 per year (80% reimbursement)
  - gold chunks: hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk::fixed-500-50::0
- old version syn:ltd-benefits-uk-2023 says: "dental coverage: £300 per year (80% reimbursement)"

## ov-32 (outdated_version, tune)

**Q:** How long does GitLab's recruiting team take to review a referral submission?

**Expected:** 5 business days (per the SLA).

- `hb:hiring/referral-operations`
  > please allow us 5 business days to review the submission.
  - gold chunks: hb:hiring/referral-operations::fixed-500-50::2
- old version syn:referral-operations-2023 says: "please allow us 10 business days to review the submission."

## ov-33 (outdated_version, tune)

**Q:** How long does GitLab retain production backup test records?

**Expected:** 1 year.

- `hb:security/policies_and_standards/records-retention-deletion`
  > Production backup tests | 1 year
  - gold chunks: hb:security/policies_and_standards/records-retention-deletion::fixed-500-50::0
- old version syn:records-retention-2023 says: "production backup tests | 2 years"

## ov-34 (outdated_version, tune)

**Q:** How long does GitLab keep risk treatment plans?

**Expected:** 3 years.

- `hb:security/policies_and_standards/records-retention-deletion`
  > Risk treatment plans | 3 years
  - gold chunks: hb:security/policies_and_standards/records-retention-deletion::fixed-500-50::1
- old version syn:records-retention-2023 says: "risk treatment plans | 5 years"

## ov-35 (outdated_version, test)

**Q:** How long should a GitLab manager try to reach an absent team member before contacting their People Business Partner?

**Expected:** 24 hours.

- `hb:people-policies`
  > If a manager is unable to reach a team member via email or Slack within a 24 hour period they should contact their People Business Partner.
  - gold chunks: hb:people-policies::fixed-500-50::5
- old version syn:people-policies-2022 says: "if a manager is unable to reach a team member via email or slack within a 48 hour period they should contact their people business partner."

## ov-36 (outdated_version, tune)

**Q:** If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again?

**Expected:** 6 months.

- `hb:hiring/referral-process`
  > we recommend waiting 6 months to refer them again
  - gold chunks: hb:hiring/referral-process::fixed-500-50::2
- old version syn:referral-process-2022 says: "we recommend waiting 3 months to refer them again"

## ov-37 (outdated_version, test)

**Q:** Who has to approve a GitLab travel booking that goes over the policy limits?

**Expected:** The manager: manager approval must be attached to the claim.

- `hb:finance/expenses`
  > All items booked which are over the limits set will need to have manager approval attached to the claim.
  - gold chunks: hb:finance/expenses::fixed-500-50::11, hb:finance/expenses::fixed-500-50::12
- old version syn:expenses-2023 says: "all items booked which are over the limits set will need to have vp approval attached to the claim."

## ov-38 (outdated_version, tune)

**Q:** Whose approval is needed if a GitLab team member books more than 5 co-working days in a month?

**Expected:** Manager AND Finance approval, obtained before submitting expenses.

- `hb:finance/expenses`
  > If more than 5 days are booked in the month, then Manager and Finance approval
  - gold chunks: hb:finance/expenses::fixed-500-50::14
- old version syn:expenses-2023 says: "if more than 5 days are booked in the month, then manager approval"

## ov-39 (outdated_version, test)

**Q:** Can I expense room service as a meal during a GitLab business trip?

**Expected:** Yes, room service is allowable as a meal (e.g. breakfast, lunch or dinner).

- `hb:finance/expenses`
  > Room service is allowable as a meal for e.g. breakfast/lunch/dinner.
  - gold chunks: hb:finance/expenses::fixed-500-50::9
- old version syn:expenses-2023 says: "room service is not reimbursable as a meal for e.g. breakfast/lunch/dinner."

## ov-40 (outdated_version, tune)

**Q:** Can I give a gift card as a gift and expense it at GitLab?

**Expected:** No, cash and cash equivalents such as gift cards are not allowed.

- `hb:finance/expenses`
  > Cash or cash equivalents, such as gift cards, are not allowed
  - gold chunks: hb:finance/expenses::fixed-500-50::17
- old version syn:expenses-2023 says: "cash is not allowed, but gift cards are allowed"

## ov-41 (outdated_version, test)

**Q:** When a group of GitLab team members can't split a meal bill, who should pay it?

**Expected:** The most senior team member present pays and submits it for reimbursement.

- `hb:finance/expenses`
  > If this is not practicable to do due to the group size, then the most senior Team Member present should pay the bill
  - gold chunks: hb:finance/expenses::fixed-500-50::10
- old version syn:expenses-2023 says: "if this is not practicable to do due to the group size, then the team member who organised the meal should pay the bill"

## ov-42 (outdated_version, test)

**Q:** Do I need pre-approval before claiming co-working space costs at GitLab?

**Expected:** Yes, pre-approval is needed before submitting claims.

- `hb:finance/expenses`
  > Coworking space is reimbursable for monthly space and one-off days during business travel. Pre-Approval is needed prior to submitting claims.
  - gold chunks: hb:finance/expenses::fixed-500-50::13
- old version syn:expenses-2023 says: "coworking space is reimbursable for monthly space and one-off days during business travel. pre-approval is optional prior to submitting claims."

## ov-43 (outdated_version, test)

**Q:** How much optical coverage per year do GitLab UK team members get?

**Expected:** £200 per year (80% reimbursement) plus £25 for annual eye tests.

- `hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk`
  > Optical coverage: £200 per year (80% reimbursement) plus £25 for annual eye tests
  - gold chunks: hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk::fixed-500-50::0
- old version syn:ltd-benefits-uk-2023 says: "optical coverage: £150 per year (80% reimbursement) plus £25 for annual eye tests"

## ov-44 (outdated_version, tune)

**Q:** What discount on legal fees does GitLab's US legal services benefit provide?

**Expected:** 25% fee discounts (plus free 30-minute consultations).

- `hb:total-rewards/benefits/general-and-entity-benefits/inc-benefits-us`
  > Free 30-minute consultations and 25% fee discounts
  - gold chunks: hb:total-rewards/benefits/general-and-entity-benefits/inc-benefits-us::fixed-500-50::5
- old version syn:inc-benefits-us-2023 says: "free 30-minute consultations and 20% fee discounts"

## rp-01 (real_pair, tune)

**Q:** Under the GitLab Testing Agreement, is the customer required to give feedback on testing features?

**Expected:** No, it is optional: the customer MAY provide feedback (versions v1-v4 said the customer WILL provide it).

- `hb:legal/testing-agreement`
  > Customer may provide suggestions, ideas, enhancement requests, or other recommendations
  - gold chunks: hb:legal/testing-agreement::fixed-500-50::2
- real old version(s) with the old rule: hb:legal/testing-agreement-v1, hb:legal/testing-agreement-v2, hb:legal/testing-agreement-v3, hb:legal/testing-agreement-v4

## rp-02 (real_pair, test)

**Q:** Under the University of Cambridge's Hybrid Working Policy, where must the remote working environment be?

**Expected:** Within the UK (the 2023 policy states the remote working environment will be based within the UK; the 2022 draft's definition did not).

- `pdf:cambridge-hybrid-working-2023`
  > Under this Policy, the remote working environment will be based within the UK.
  - gold chunks: pdf:cambridge-hybrid-working-2023::fixed-500-50::2
- real old version(s) with the old rule: pdf:cambridge-hybrid-working-draft-2022

## hi-01 (history, test)

**Q:** What was GitLab's nightly hotel limit in its 2023 travel and expense policy?

**Expected:** $250 USD per night.

- `syn:expenses-2023`
  > Hotel stays are reimbursable up to $250 USD (or equivalent local currency) inclusive of tax per night for standard rooms
  - gold chunks: syn:expenses-2023::fixed-500-50::8
- current version (should NOT be preferred here): hb:finance/expenses

## hi-02 (history, tune)

**Q:** What minimum password length did GitLab's 2022 password standard require?

**Expected:** 8 characters.

- `syn:password-standard-2022`
  > minimum password length needs to be set to 8 characters
  - gold chunks: syn:password-standard-2022::fixed-500-50::1
- current version (should NOT be preferred here): hb:security/policies_and_standards/password-standard

## hi-03 (history, tune)

**Q:** How often did GitLab run phishing simulations under its 2022 phishing program?

**Expected:** At least twice per fiscal year.

- `syn:phishing-program-2022`
  > one phishing simulation campaign will take place twice per fiscal year
  - gold chunks: syn:phishing-program-2022::fixed-500-50::0, syn:phishing-program-2022::fixed-500-50::3
- current version (should NOT be preferred here): hb:security/security-assurance/governance/phishing

## hi-04 (history, tune)

**Q:** How long was US parental leave at GitLab under the 2022 leave policy?

**Expected:** 12 weeks.

- `syn:us-leave-of-absence-2022`
  > Parental Leave | 12 weeks
  - gold chunks: syn:us-leave-of-absence-2022::fixed-500-50::1
- current version (should NOT be preferred here): hb:people-policies/leave-of-absence/us

## hi-05 (history, test)

**Q:** Under GitLab's 2021 equity policy, how long did departing team members have to exercise vested options?

**Expected:** 30 days after termination.

- `syn:stock-options-2021`
  > they have 30 days post termination to exercise their vested options.
  - gold chunks: syn:stock-options-2021::fixed-500-50::0
- current version (should NOT be preferred here): hb:total-rewards/stock-options

## hi-06 (history, tune)

**Q:** Under GitLab's 2023 expense policy, how long after purchase could an expense claim be submitted without manager approval?

**Expected:** 60 days.

- `syn:expenses-2023`
  > Expense claims over 60 days from purchase date will not be reimbursed unless approved by the Manager.
  - gold chunks: syn:expenses-2023::fixed-500-50::1, syn:expenses-2023::fixed-500-50::2
- current version (should NOT be preferred here): hb:finance/expenses

## hi-07 (history, tune)

**Q:** In GitLab's 2023 token management standard, what was the maximum expiry for personal access tokens?

**Expected:** 90 days.

- `syn:token-management-standard-2023`
  > Personal Access Tokens - 90 days
  - gold chunks: syn:token-management-standard-2023::fixed-500-50::3, syn:token-management-standard-2023::fixed-500-50::4
- current version (should NOT be preferred here): hb:security/policies_and_standards/token-management-standard

## hi-08 (history, tune)

**Q:** Under GitLab's 2022 referral process, for how long did a referral count as yours?

**Expected:** 12 months.

- `syn:referral-process-2022`
  > Your referral is classified as your referral for 12 months
  - gold chunks: syn:referral-process-2022::fixed-500-50::2
- current version (should NOT be preferred here): hb:hiring/referral-process

## hi-09 (history, tune)

**Q:** Under GitLab's 2022 people policies, after how many days of unreported absence could a team member be terminated for job abandonment?

**Expected:** Five consecutive workdays.

- `syn:people-policies-2022`
  > When a team member is absent from work for five consecutive workdays
  - gold chunks: syn:people-policies-2022::fixed-500-50::5
- current version (should NOT be preferred here): hb:people-policies

## hi-10 (history, tune)

**Q:** In GitLab's 2023 Support on-call guide, how long could a new alert go unacknowledged before the Support Manager on-call was alerted?

**Expected:** 15 minutes.

- `syn:support-on-call-2023`
  > If a new alert has not been acknowledged after 15 minutes, the Support Manager on-call is alerted.
  - gold chunks: syn:support-on-call-2023::fixed-500-50::3
- current version (should NOT be preferred here): hb:support/on-call

## hi-11 (history, tune)

**Q:** Under GitLab's 2022 business travel insurance, how long could a trip last and still be covered?

**Expected:** Less than 90 days.

- `syn:travel-safety-2022`
  > Trip Duration | Covered for trips less than 90 days
  - gold chunks: syn:travel-safety-2022::fixed-500-50::1
- current version (should NOT be preferred here): hb:finance/travel

## hi-12 (history, tune)

**Q:** Under GitLab's 2023 expense policy, could room service be expensed as a meal?

**Expected:** No, room service was not reimbursable as a meal.

- `syn:expenses-2023`
  > Room service is not reimbursable as a meal for e.g. breakfast/lunch/dinner.
  - gold chunks: syn:expenses-2023::fixed-500-50::9
- current version (should NOT be preferred here): hb:finance/expenses

## na-01 (no_answer, tune)

**Q:** What is GitLab's dress code for video calls with customers?

**Expected:** I couldn't find this in the documents.

- /dress code/ in whole corpus: 0 matches
- closest BM25 hits (not answers): hb:finance/growth-and-development/learning-development (22.8); hb:hiring/candidate-faq (22.4); hb:support/support-engineer-responsibilities (21.8)

## na-02 (no_answer, test)

**Q:** What is the fire evacuation procedure for Lancaster City Council staff?

**Expected:** I couldn't find this in the documents.

- /evacuat|fire drill|fire alarm/ in pdf:lancaster: 0 matches
- closest BM25 hits (not answers): pdf:lancaster-sickness-absence (31.9); pdf:lancaster-sickness-absence (30.3); pdf:lancaster-sickness-absence (25.8)

## na-03 (no_answer, tune)

**Q:** How much does a staff parking permit cost at Middlesex University?

**Expected:** I couldn't find this in the documents.

- /parking/ in pdf:middlesex: 0 matches
- /parking permit/ in whole corpus: 0 matches
- closest BM25 hits (not answers): pdf:middlesex-annual-leave (23.7); pdf:middlesex-annual-leave (23.2); pdf:middlesex-annual-leave (22.7)

## na-04 (no_answer, test)

**Q:** What is the prize budget for GitLab's internal hackathons?

**Expected:** I couldn't find this in the documents.

- /hackathon/ in whole corpus: 0 matches
- closest BM25 hits (not answers): hb:legal/marketing-collaboration (28.9); hb:legal/marketing-collaboration (25.1); hb:legal/process-for-ux-research-prize-draws/index (23.6)

## na-05 (no_answer, tune)

**Q:** How long is the paid lunch break for Lancaster City Council employees?

**Expected:** I couldn't find this in the documents.

- /lunch|meal break|rest break/ in pdf:lancaster: 0 matches
- closest BM25 hits (not answers): pdf:lancaster-sickness-absence (32.3); pdf:lancaster-sickness-absence (28.9); pdf:lancaster-sickness-absence (28.5)

## na-06 (no_answer, tune)

**Q:** Does Heriot-Watt University contribute to home broadband costs for hybrid workers?

**Expected:** I couldn't find this in the documents.

- /broadband|internet|wi-?fi/ in pdf:heriot: 0 matches
- closest BM25 hits (not answers): pdf:heriot-watt-hybrid-working (39.5); pdf:heriot-watt-hybrid-working (35.0); pdf:cambridge-hybrid-working-draft-2022 (34.1)

## na-07 (no_answer, tune)

**Q:** What discount do University of Salford staff get at the campus gym?

**Expected:** I couldn't find this in the documents.

- /gym|leisure|sport/ in pdf:salford: 0 matches
- closest BM25 hits (not answers): pdf:qmul-hybrid-working (29.1); pdf:qmul-hybrid-working (28.7); pdf:qmul-hybrid-working (28.6)

## na-08 (no_answer, tune)

**Q:** Are staff allowed to bring dogs onto Queen Mary University of London campuses?

**Expected:** I couldn't find this in the documents.

- /\bdogs?\b|\bpets?\b|animal/ in pdf:qmul: 0 matches
- closest BM25 hits (not answers): pdf:qmul-hybrid-working (50.2); pdf:qmul-hybrid-working (49.1); pdf:qmul-hybrid-working (48.3)

## na-09 (no_answer, test)

**Q:** What overtime pay rate does West Sussex County Council offer its staff?

**Expected:** I couldn't find this in the documents.

- /overtime/ in pdf:west-sussex: 0 matches
- closest BM25 hits (not answers): pdf:west-sussex-data-protection (32.4); pdf:west-sussex-data-protection (26.2); pdf:west-sussex-data-protection (25.8)

## na-10 (no_answer, tune)

**Q:** How many days of paid study leave do University of Roehampton staff get?

**Expected:** I couldn't find this in the documents.

- /study leave/ in pdf:roehampton: 0 matches
- closest BM25 hits (not answers): pdf:middlesex-annual-leave (29.2); pdf:middlesex-annual-leave (29.1); pdf:roehampton-whistleblowing (27.2)
