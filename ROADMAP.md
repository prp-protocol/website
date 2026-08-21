# PRP technical roadmap

This roadmap describes evidence gates and external dependencies. It does not
promise dates, standards-body decisions, identifier assignments, or RFC
publication.

The public summary appears on <https://prp-protocol.org/#roadmap>. Published
protocol status is recorded in the
[PRP official publications repository](https://github.com/prp-protocol/specifications),
while editorial authority remains in the canonical `prp-spec` project.

The currently published document set is:

- [PRP Architecture v1 RC1](https://github.com/prp-protocol/specifications/blob/main/prp-architecture-v1-rc1.md);
- [PRP Wire v1 working draft](https://github.com/prp-protocol/specifications/blob/main/prp-wire-v1-draft.md);
- [PRP Encapsulation Profiles v1](https://github.com/prp-protocol/specifications/blob/main/prp-encapsulation-v1.md); and
- [PRP v1 Wire Registry](https://github.com/prp-protocol/specifications/blob/main/wire-registry-v1.md).

The repository is a publication channel, not an independent editorial working
tree. Draft development, vectors, tests, and promotion decisions belong to the
canonical `prp-spec` project.

## Status language

- **Active:** work currently controlled and performed by the project.
- **Planned:** project work that follows completion of stated prerequisites.
- **Conditional:** work undertaken only if the final architecture needs the
  external resource.
- **External:** an outcome decided by a standards body or technical community,
  not by the project.

Project documents use `working draft`, `candidate architecture`, and
`candidate specification` for internal maturity. `Internet-Draft`, `Proposed
Standard`, `Internet Standard`, and `RFC` are used only with their IETF
meanings.

## Track 1 — PRP core

**Current state:** active.

The project has a candidate architecture, working wire and encapsulation
drafts, implementations, and conformance evidence. Promotion to a project
candidate specification requires:

1. stable architectural boundaries and normative terminology;
2. stable wire framing, version negotiation, registries, and migration rules;
3. a threat model and privacy analysis covering core protocol behavior;
4. machine-readable positive and rejection vectors;
5. a public conformance suite;
6. interoperability between independent implementations; and
7. documented operational and security review results.

## Track 2 — IETF standardization

**Current state:** planned; final outcomes are external.

Before submission, the project will establish document licensing,
contribution rights, IPR disclosure practice, authorship, registry governance,
and a stable change-control process.

The intended path is:

1. separate the problem statement, architecture, core protocol, and carrier
   bindings into reviewable document scopes;
2. prepare RFCXML sources with Security, Privacy, Operational, and IANA
   Considerations;
3. submit individual Internet-Drafts;
4. seek early review and identify an appropriate Working Group, DISPATCH, or
   sponsored path;
5. revise based on open community review and implementation experience; and
6. seek RFC publication only if the applicable IETF process reaches consensus.

An Internet-Draft is a discussion document. Its publication does not imply
IETF adoption or endorsement.

## Track 3 — carrier identifiers

Carrier bindings are replaceable realization mechanisms. Each assignment has
its own technical gate and does not change PRP identity or relationship
semantics.

### UDP adapter — IANA

**Current state:** conditional on a stable UDP carrier specification.

The implementation's current dynamic/private port is for development and is
not a global assignment. A request for an IANA service name and one UDP user
port will occur only after the adapter specifies:

- exact use of the port and why an existing service is insufficient;
- traffic bounds and congestion behavior;
- discovery, multicast, and amplification behavior;
- security and version negotiation; and
- a stable public technical reference.

### PRP over Ethernet — IEEE

**Current state:** conditional on a stable Ethernet binding.

The PRP EtherType identifies PRP carrier units transported directly over
Ethernet. Any values used during development are non-authoritative until
registry audit and assignment. The binding must provide its own subtype and
version evolution without consuming further EtherTypes before an IEEE request
is made.

### Bluetooth

**Current state:** no assignment required for the existing GATT profile.

The GATT carrier uses project-owned 128-bit UUIDs. A Bluetooth SIG assignment
is considered only when a stable future profile demonstrates a concrete need,
such as a compact 16-bit service UUID, Company Identifier data, or a separately
specified L2CAP CoC bearer. No such profile is an implicit fallback from GATT.

## Track 4 — independent Ethernet discovery

**Current state:** active as an independent carrier-side protocol.

Ethernet discovery is not part of the PRP wire protocol and is not required by
every PRP deployment. It observes carrier-local participants; it does not
define PRP identity, relationship authority, or permission to communicate.

Its roadmap is therefore separate:

1. stabilize discovery framing, lifecycle, bounds, and security properties;
2. preserve independent versioning and failure behavior;
3. demonstrate operation without coupling PRP core evolution to discovery;
4. keep local experimental EtherType use inside controlled development
   networks; and
5. request a distinct IEEE EtherType only if the discovery protocol is ready
   for public deployment outside that administrative boundary.

The PRP EtherType and the discovery EtherType must not be multiplexed merely to
reduce assignment count. Their separation preserves the boundary between a
carrier mechanism and the protocol it carries.

## Additional assignment review

URI schemes, media types, DNS-SD names, multicast addresses, internal IANA
registries, or other global identifiers will be requested only when a stable
specification demonstrates that they are necessary. No implementation-local
number becomes a protocol assignment by use or publication.

## Public evidence

Each completed milestone should link to durable evidence: a specification
revision, conformance manifest, interoperability report, security review,
standards-body submission, or registry entry. The website status is updated
only after that evidence is public.
