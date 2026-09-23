# Dataspaces 101 — reserve question bank

> Purpose: a pool of pre-written multiple-choice questions for rotating into the
> Dataspaces 101 Coach's fixed knowledge check, or for future modules.
> NOT part of the RAG corpus — this directory is never ingested.
>
> Provenance: questions written by ARDC (Sept 2026). Topic coverage informed by the
> structure of the IDSA Data Space Body of Knowledge v1.1 (proposed recommendation)
> and a third-party Dataspaces training course reviewed for scope; no text from
> either source is reproduced. Every answer is verifiable against the ARDC
> educator's own knowledge base (IDS-RAM, IDSA Rulebook, DSSC, ARDC Wiki Brain).
>
> Format: question, options A–D, [correct letter], one-line rationale.

## Roles and architecture

R1. Which participant offers data to a dataspace under usage conditions?
A) Data consumer B) Data provider C) Clearing house D) Certification body [B]
— The provider holds the data and sets the conditions; the consumer requests and uses it.

R2. The registry where participants discover what data is available is the:
A) Clearing house B) Identity provider C) Metadata broker / catalogue D) Vocabulary hub [C]
— The broker/catalogue publishes dataset descriptions and usage policies for discovery.

R3. Which component records transactions to support auditing and dispute resolution?
A) Connector B) Clearing house C) Catalogue D) Identity wallet [B]
— The clearing house is the transaction log of the dataspace.

R4. One organisation participating in a dataspace can:
A) Hold only one role, fixed at onboarding B) Hold multiple roles (e.g. provider and consumer) C) Only consume until certified D) Only provide if government-owned [B]
— Roles describe activity, not identity; a participant can act as both provider and consumer.

R5. In the control-plane / data-plane distinction, contract negotiation happens:
A) On the data plane B) On the control plane C) In the vocabulary hub D) Outside the dataspace entirely [B]
— The control plane carries identity, policy and negotiation; the data plane carries the approved transfer.

## Governance

G1. Dataspace governance typically operates at which levels?
A) Only the technical level B) Ecosystem/dataspace level and individual data-exchange level C) Only national legislation D) Vendor level [B]
— Rules exist for the community as a whole (rulebook) and per exchange (contracts/policies).

G2. The document that sets the community's common rules, roles and dispute arrangements is the:
A) Reference architecture B) Rulebook C) Connector specification D) Data catalogue [B]
— The rulebook is the governance core; architecture documents describe the technology.

G3. A usage policy attached to a dataset in machine-readable form is commonly expressed in:
A) ODRL B) HTML C) CSV D) BPMN [A]
— The Open Digital Rights Language expresses permissions, prohibitions and obligations.

G4. "Rules before tools" implies the FIRST serious work in a new dataspace is:
A) Choosing a connector vendor B) Agreeing business value, legal terms and governance C) Buying cloud infrastructure D) Building dashboards [B]
— Communities that start with agreement move; those that start with technology stall.

G5. Breach handling in a well-governed dataspace is defined:
A) Ad hoc after the first incident B) In the rulebook and reflected in contracts before sharing begins C) By the software licence D) Only by criminal law [B]
— Consequences for misuse are agreed up front and enforceable through the governance framework.

## Trust, identity and sovereignty

T1. Trust between two organisations that have never met is established primarily through:
A) Verified identities and attributes checked at exchange time B) Reputation on social media C) Manual phone calls D) Sharing small data first [A]
— Identity verification and attribute/credential checks underpin machine-scale trust.

T2. Data sovereignty is best described as:
A) Storing data onshore B) The provider's exclusive right to decide usage of their data as an asset C) Government ownership of research data D) Encrypting everything [B]
— Sovereignty is about decision rights over usage, not physical location alone.

T3. A verifiable credential in a dataspace context is:
A) A university degree B) A digitally signed attestation about a participant, checkable with its issuer C) A password D) An SSL certificate for a website [B]
— Credentials carry claims (e.g. certification status) that other parties can verify.

T4. Usage control differs from access control because it:
A) Is weaker B) Also governs what may be done with data AFTER access is granted C) Only applies to open data D) Replaces contracts [B]
— Access control gates entry; usage control constrains purpose, duration and onward sharing.

## Interoperability

I1. The European Interoperability Framework describes which layers?
A) Legal, organisational, semantic, technical B) Physical, network, transport, application C) Bronze, silver, gold D) Local, state, federal [A]
— Dataspace interoperability spans all four; technical compatibility alone is insufficient.

I2. Semantic interoperability means:
A) Using the same database vendor B) Exchanged data carries shared, unambiguous meaning via common vocabularies C) All data in English D) One global schema for all participants [B]
— Shared vocabularies give meaning without forcing a universal schema.

I3. ISO/IEC 20151 addresses:
A) Information security management B) Dataspace concepts and characteristics C) Cloud portability only D) Medical devices [B]
— It is the emerging international standard defining what makes a dataspace a dataspace.

## Building a dataspace (the journey)

J1. A sensible first milestone for a new dataspace initiative is:
A) Full production deployment B) A scoped use case with committed partners and a pilot to validate the approach C) A national launch event D) Procuring hardware [B]
— Pilots validate governance and value before scale-up.

J2. Both the IDSA and DSSC guidance on starting a dataspace agree that:
A) Technology selection comes first B) A community with shared purpose and agreed rules precedes infrastructure C) Only governments may start one D) Certification is optional forever [B]
— Different frameworks, same sequence: agreement, then architecture.

J3. The "cold start" problem in dataspaces refers to:
A) Server boot time B) Low early participation limiting value until a critical mass of providers and consumers joins C) Winter outages D) Slow first query [B]
— Network effects: value grows with participation, so early incentives matter.

J4. Typical onboarding of a new participant includes:
A) Identity verification, agreeing to the rulebook, connector setup B) A press release C) Rewriting their internal databases D) Purchasing shares [A]
— Verification against the trust framework plus technical connection.

## Business and value

B1. In many operating dataspaces, participants pay:
A) Nothing, ever B) Fees to service providers operating shared services, rather than "to the dataspace" itself C) A percentage of company revenue D) Only in cryptocurrency [B]
— Costs typically flow through service contracts (hosting, operation, value-added services).

B2. A reasonable KPI for a dataspace use case is:
A) Number of press mentions B) Volume/frequency of governed data exchanges supporting the use case C) Lines of code written D) Number of meetings held [B]
— Measure governed sharing that delivers the use case's value, not activity for its own sake.

B3. The main commercial reason a provider joins a dataspace is:
A) Obligation B) Sharing data under enforceable conditions unlocks value that unprotected sharing would put at risk C) Cheaper storage D) Marketing reach [B]
— Sovereignty-preserving sharing enables collaboration that raw handover would prevent.

B4. Risk categories a dataspace business case should address include:
A) Security, operational, legal/regulatory and reputational risks B) Only cyber risk C) Only financial risk D) Weather [A]
— A rounded risk view spans technical, legal and trust dimensions.
