# Gold evidence review

Every quote below was checked automatically against the ingested corpus by `python -m src.testset`.

## lk-01 (lookup, tune)

**Q:** What is GitLab's daily reimbursement limit for internet access while travelling?

**Expected:** Up to $50 USD (or local equivalent) per day.

- `hb:finance/expenses`
  > Internet while traveling is reimbursable for up to $50 USD (or local equivalent currency) per day.
  - gold chunks: hb:finance/expenses::fixed-500-50::12

## lk-02 (lookup, tune)

**Q:** What is the monthly limit for reimbursing a co-working space at GitLab?

**Expected:** $700 per month (pre-approval is needed).

- `hb:finance/expenses`
  > $700.00 Limit per month.
  - gold chunks: hb:finance/expenses::fixed-500-50::13

## lk-03 (lookup, test)

**Q:** Within how many working days does GitLab's Accounts Payable team process expense reports that need AP Admin review?

**Expected:** Within 7 working days from the date submitted.

- `hb:finance/expenses`
  > Review and process all expense reports that require AP Admin review, within 7 working days from the date submitted.
  - gold chunks: hb:finance/expenses::fixed-500-50::1

## lk-04 (lookup, test)

**Q:** How many one-off co-working days per month can a GitLab team member expense without Manager or Finance approval?

**Expected:** Up to 5 one-off days in a calendar month.

- `hb:finance/expenses`
  > Up to 5 One-off Days in a calendar month related to co-working space do not require Manager or Finance approval.
  - gold chunks: hb:finance/expenses::fixed-500-50::14

## lk-05 (lookup, test)

**Q:** How far in advance should GitLab team members book domestic flights?

**Expected:** At least 14 days in advance.

- `hb:finance/expenses`
  > Domestic: At least 14 days in advance
  - gold chunks: hb:finance/expenses::fixed-500-50::5

## lk-06 (lookup, tune)

**Q:** How long does GitLab retain security incident communications sent to customers?

**Expected:** 3 years.

- `hb:security/policies_and_standards/records-retention-deletion`
  > Security incident communication to customers | 3 years
  - gold chunks: hb:security/policies_and_standards/records-retention-deletion::fixed-500-50::1

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

## lk-09 (lookup, tune)

**Q:** What are the eligibility requirements for FMLA leave at GitLab in the US?

**Expected:** 1 year of service and 1,250 hours worked in the year immediately before the leave starts.

- `hb:people-policies/leave-of-absence/us`
  > 1 year of service, AND1250hrs worked in the year immediately priorto the start of leave
  - gold chunks: hb:people-policies/leave-of-absence/us::fixed-500-50::1

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

## lk-20 (lookup, test)

**Q:** What are GitLab's limits for taxis and ride-shares on business trips?

**Expected:** $300 per round trip and $150 for a single trip.

- `hb:finance/expenses`
  > Ground Transportation (taxis, ubers) at $300 limit per round trip and $150 limit for single trip.
  - gold chunks: hb:finance/expenses::fixed-500-50::11

## pp-01 (paraphrase, tune)

**Q:** How far from my home can a co-working space be for GitLab to pay for it?

**Expected:** Within a commutable distance (about 50 km) of your primary residence, except one-off day passes while travelling.

- `hb:finance/expenses`
  > located within a commutable distance (+-50km) of the Team Member's primary residence
  - gold chunks: hb:finance/expenses::fixed-500-50::13

## pp-02 (paraphrase, tune)

**Q:** If GitLab pays for my co-working desk for a whole month, can I still claim my home internet?

**Expected:** No; with a full month of co-working, home internet cannot be expensed (a few co-working days still allows it).

- `hb:finance/expenses`
  > if you expense a co-working space for a full month then internet for home cannot be expensed.
  - gold chunks: hb:finance/expenses::fixed-500-50::14, hb:finance/expenses::fixed-500-50::19

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

## pp-07 (paraphrase, test)

**Q:** How does GitLab cover the tax bill when my restricted stock units become mine?

**Expected:** Shares are automatically sold at vesting to pay the taxes, based on your country's tax rate.

- `hb:total-rewards/stock-options`
  > Shares are sold to pay the taxes due on the RSU vesting.
  - gold chunks: hb:total-rewards/stock-options::fixed-500-50::1

## pp-08 (paraphrase, tune)

**Q:** Can I get a bonus for recommending a friend for an internship at GitLab?

**Expected:** No, contract or temporary roles including internships are not eligible (unless the intern later converts to a team member).

- `hb:hiring/referral-process`
  > Contract or temporary roles, including Internships, are not eligible for referral bonuses.
  - gold chunks: hb:hiring/referral-process::fixed-500-50::0

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

## pp-14 (paraphrase, tune)

**Q:** Can I buy second-hand work equipment from an individual and claim it back from GitLab?

**Expected:** Yes, purchases from private sellers are allowed, with a screenshot of the transaction as proof.

- `hb:finance/expenses`
  > Purchasing from Private Sellers (e.g. either new or used equipment) is allowed.
  - gold chunks: hb:finance/expenses::fixed-500-50::16

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

## ex-02 (exact_term, test)

**Q:** Which company provides GitLab's phishing simulations?

**Expected:** ProofPoint.

- `hb:security/security-assurance/governance/phishing`
  > Phishing simulations are provided by ProofPoint
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0

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

## md-07 (multi_doc, test)

**Q:** Which third parties deliver GitLab's annual security awareness training and its phishing simulations?

**Expected:** Right Hand Cybersecurity delivers the annual security awareness training; ProofPoint runs the phishing simulations.

- `hb:security/security-assurance/governance/sec-training`
  > provided annually via Right Hand Cybersecurity, GitLab's third-party provider
  - gold chunks: hb:security/security-assurance/governance/sec-training::fixed-500-50::1
- `hb:security/security-assurance/governance/phishing`
  > Phishing simulations are provided by ProofPoint
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0

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

## md-10 (multi_doc, tune)

**Q:** What is RED data at GitLab, and how often must access to Red Data systems be reviewed?

**Expected:** RED is GitLab's most sensitive restricted data with explicitly approved, privileged access; access to Red Data systems is reviewed annually.

- `hb:security/policies_and_standards/data-classification-standard`
  > This is GitLab's most sensitive data and access to it should be considered privileged and must be explicitly approved.
  - gold chunks: hb:security/policies_and_standards/data-classification-standard::fixed-500-50::1
- `hb:security/security-assurance/security-compliance/access-reviews`
  > Red Data Systems | Annual
  - gold chunks: hb:security/security-assurance/security-compliance/access-reviews::fixed-500-50::2

## ov-01 (outdated_version, test)

**Q:** After the initial term, how much notice is needed to terminate GitLab's Technology Partner Agreement?

**Expected:** Sixty (60) days' prior written notice.

- `hb:legal/technology-partner-agreement`
  > Following the Initial Term, either Party may terminate this Agreement upon sixty (60) days' prior written notice to the other Party.
  - gold chunks: hb:legal/technology-partner-agreement::fixed-500-50::7
- same text in old version(s): hb:legal/technology-partner-agreement-v1

## ov-02 (outdated_version, tune)

**Q:** How can either party terminate the GitLab Testing Agreement for convenience?

**Expected:** Immediately, upon written notice to the other party (email is sufficient).

- `hb:legal/testing-agreement`
  > Upon written notice to the other party (email is sufficient), either party may terminate this Agreement immediately for convenience.
  - gold chunks: hb:legal/testing-agreement::fixed-500-50::4
- same text in old version(s): hb:legal/testing-agreement-v4, hb:legal/testing-agreement-v5
- fact differs in old version(s): hb:legal/testing-agreement-v1, hb:legal/testing-agreement-v2, hb:legal/testing-agreement-v3

## ov-03 (outdated_version, tune)

**Q:** When will the University of Cambridge's Hybrid Working Policy be reviewed?

**Expected:** 12 months after the implementation date (and periodically after that).

- `pdf:cambridge-hybrid-working-2023`
  > The Policy will be reviewed 12 months after the implementation date
  - gold chunks: pdf:cambridge-hybrid-working-2023::fixed-500-50::10
- same text in old version(s): pdf:cambridge-hybrid-working-draft-2022

## ov-04 (outdated_version, test)

**Q:** Under North Lanarkshire Council's IT acceptable use policy, is personal use of council IT monitored?

**Expected:** Yes, all personal use is subject to the same monitoring as business use.

- `pdf:north-lanarkshire-it-acceptable-use-v5`
  > all personal use is subject to the same monitoring activities as business use
  - gold chunks: pdf:north-lanarkshire-it-acceptable-use-v5::fixed-500-50::9
- same text in old version(s): pdf:north-lanarkshire-it-acceptable-use-v4

## ov-05 (outdated_version, tune)

**Q:** Which law governs GitLab's Vendor Terms and Conditions?

**Expected:** The laws of California, U.S.A. (courts in San Francisco).

- `hb:finance/procurement/vendor-guidelines/vendor-agreement`
  > This Agreement shall be construed and enforced in accordance with the laws of California, U.S.A.
  - gold chunks: hb:finance/procurement/vendor-guidelines/vendor-agreement::fixed-500-50::10
- same text in old version(s): hb:finance/procurement/vendor-guidelines/legacy-vendor-agreement-v1

## ov-06 (outdated_version, tune)

**Q:** How long after the purchase date can I submit a GitLab expense claim and still be reimbursed without manager approval?

**Expected:** Up to 90 days; claims over 90 days are not reimbursed unless approved by the manager.

- `hb:finance/expenses`
  > Expense claims over 90 days from purchase date will not be reimbursed unless approved by the Manager.
  - gold chunks: hb:finance/expenses::fixed-500-50::1, hb:finance/expenses::fixed-500-50::2
- fact differs in old version(s): syn:expenses-2023

## ov-07 (outdated_version, tune)

**Q:** What is GitLab's nightly hotel limit for business travel?

**Expected:** $300 USD per night including tax, for standard rooms.

- `hb:finance/expenses`
  > Hotel stays are reimbursable up to $300 USD (or equivalent local currency) inclusive of tax per night for standard rooms
  - gold chunks: hb:finance/expenses::fixed-500-50::8
- fact differs in old version(s): syn:expenses-2023

## ov-08 (outdated_version, tune)

**Q:** How much can I spend on meals per day while travelling for GitLab?

**Expected:** Up to $120 USD (or local equivalent) per day.

- `hb:finance/expenses`
  > Meals while traveling on Company business are reimbursable, up to $120 USD (or local equivalent currency) per day.
  - gold chunks: hb:finance/expenses::fixed-500-50::9, hb:finance/expenses::fixed-500-50::10
- fact differs in old version(s): syn:expenses-2023

## ov-09 (outdated_version, test)

**Q:** What minimum password length does GitLab's password standard require?

**Expected:** 12 characters.

- `hb:security/policies_and_standards/password-standard`
  > For systems where a password can be configured the minimum password length needs to be set to 12 characters.
  - gold chunks: hb:security/policies_and_standards/password-standard::fixed-500-50::1
- fact differs in old version(s): syn:password-standard-2022

## ov-10 (outdated_version, test)

**Q:** What is the maximum expiry period for a GitLab personal access token?

**Expected:** 30 days.

- `hb:security/policies_and_standards/token-management-standard`
  > Personal Access Tokens - 30 days
  - gold chunks: hb:security/policies_and_standards/token-management-standard::fixed-500-50::3, hb:security/policies_and_standards/token-management-standard::fixed-500-50::4
- fact differs in old version(s): syn:token-management-standard-2023

## ov-11 (outdated_version, tune)

**Q:** How long is parental leave for GitLab team members in the US?

**Expected:** 16 weeks (job protected, except in certain circumstances).

- `hb:people-policies/leave-of-absence/us`
  > Parental Leave | 16 weeks
  - gold chunks: hb:people-policies/leave-of-absence/us::fixed-500-50::1
- fact differs in old version(s): syn:us-leave-of-absence-2022

## ov-12 (outdated_version, tune)

**Q:** For how long does someone I refer to GitLab count as my referral?

**Expected:** 6 months from the date Talent Acquisition receives the referral, for jobs in the same job family.

- `hb:hiring/referral-process`
  > Your referral is classified as your referral for 6 months
  - gold chunks: hb:hiring/referral-process::fixed-500-50::2
- fact differs in old version(s): syn:referral-process-2022

## ov-13 (outdated_version, tune)

**Q:** How long do I have to exercise vested GitLab stock options after leaving the company?

**Expected:** 90 days after termination.

- `hb:total-rewards/stock-options`
  > they have 90 days post termination to exercise their vested options.
  - gold chunks: hb:total-rewards/stock-options::fixed-500-50::0
- fact differs in old version(s): syn:stock-options-2021

## ov-14 (outdated_version, tune)

**Q:** How often does GitLab run phishing simulation campaigns?

**Expected:** At least once each fiscal quarter.

- `hb:security/security-assurance/governance/phishing`
  > At a minimum, one phishing simulation campaign will take place each fiscal quarter.
  - gold chunks: hb:security/security-assurance/governance/phishing::fixed-500-50::0, hb:security/security-assurance/governance/phishing::fixed-500-50::3
- fact differs in old version(s): syn:phishing-program-2022

## ov-15 (outdated_version, test)

**Q:** After how many days of unreported absence can a GitLab team member be terminated for job abandonment?

**Expected:** Three consecutive workdays with no calendar entry and no contact with their supervisor (unless otherwise required by law).

- `hb:people-policies`
  > When a team member is absent from work for three consecutive workdays
  - gold chunks: hb:people-policies::fixed-500-50::5
- fact differs in old version(s): syn:people-policies-2022

## na-01 (no_answer, tune)

**Q:** What is GitLab's dress code for video calls with customers?

**Expected:** I couldn't find this in the documents.

- /dress code/ in whole corpus: 0 matches
- closest BM25 hits (not answers): hb:finance/growth-and-development/learning-development (22.8); hb:hiring/candidate-faq (22.4); hb:support/support-engineer-responsibilities (21.8)

## na-02 (no_answer, test)

**Q:** What is the fire evacuation procedure for Lancaster City Council staff?

**Expected:** I couldn't find this in the documents.

- /evacuat|fire drill|fire alarm/ in pdf:lancaster: 0 matches
- closest BM25 hits (not answers): pdf:lancaster-sickness-absence (31.7); pdf:lancaster-sickness-absence (30.1); pdf:lancaster-sickness-absence (25.6)

## na-03 (no_answer, tune)

**Q:** How much does a staff parking permit cost at Middlesex University?

**Expected:** I couldn't find this in the documents.

- /parking/ in pdf:middlesex: 0 matches
- /parking permit/ in whole corpus: 0 matches
- closest BM25 hits (not answers): pdf:middlesex-annual-leave (23.5); pdf:middlesex-annual-leave (22.9); pdf:middlesex-annual-leave (22.4)

## na-04 (no_answer, test)

**Q:** What is the prize budget for GitLab's internal hackathons?

**Expected:** I couldn't find this in the documents.

- /hackathon/ in whole corpus: 0 matches
- closest BM25 hits (not answers): hb:legal/marketing-collaboration (28.7); hb:legal/marketing-collaboration (24.9); hb:legal/process-for-ux-research-prize-draws/index (23.5)

## na-05 (no_answer, tune)

**Q:** How long is the paid lunch break for Lancaster City Council employees?

**Expected:** I couldn't find this in the documents.

- /lunch|meal break|rest break/ in pdf:lancaster: 0 matches
- closest BM25 hits (not answers): pdf:lancaster-sickness-absence (32.2); pdf:lancaster-sickness-absence (28.9); pdf:lancaster-sickness-absence (28.3)

## na-06 (no_answer, tune)

**Q:** Does Heriot-Watt University contribute to home broadband costs for hybrid workers?

**Expected:** I couldn't find this in the documents.

- /broadband|internet|wi-?fi/ in pdf:heriot: 0 matches
- closest BM25 hits (not answers): pdf:heriot-watt-hybrid-working (39.0); pdf:heriot-watt-hybrid-working (34.6); pdf:cambridge-hybrid-working-draft-2022 (34.3)

## na-07 (no_answer, tune)

**Q:** What discount do University of Salford staff get at the campus gym?

**Expected:** I couldn't find this in the documents.

- /gym|leisure|sport/ in pdf:salford: 0 matches
- closest BM25 hits (not answers): pdf:qmul-hybrid-working (28.7); pdf:qmul-hybrid-working (28.4); pdf:qmul-hybrid-working (28.2)

## na-08 (no_answer, tune)

**Q:** Are staff allowed to bring dogs onto Queen Mary University of London campuses?

**Expected:** I couldn't find this in the documents.

- /\bdogs?\b|\bpets?\b|animal/ in pdf:qmul: 0 matches
- closest BM25 hits (not answers): pdf:qmul-hybrid-working (49.6); pdf:qmul-hybrid-working (48.5); pdf:qmul-hybrid-working (47.7)

## na-09 (no_answer, test)

**Q:** What overtime pay rate does West Sussex County Council offer its staff?

**Expected:** I couldn't find this in the documents.

- /overtime/ in pdf:west-sussex: 0 matches
- closest BM25 hits (not answers): pdf:west-sussex-data-protection (31.9); pdf:west-sussex-data-protection (25.8); pdf:west-sussex-data-protection (25.5)

## na-10 (no_answer, tune)

**Q:** How many days of paid study leave do University of Roehampton staff get?

**Expected:** I couldn't find this in the documents.

- /study leave/ in pdf:roehampton: 0 matches
- closest BM25 hits (not answers): pdf:middlesex-annual-leave (29.5); pdf:middlesex-annual-leave (29.3); pdf:roehampton-whistleblowing (26.9)
