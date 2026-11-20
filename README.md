SRAC Reference Pilot
Scope
This repository is an independent Safety Relevance Assertion Capability (SRAC) reference pilot.

SPARTA CM0022 Criticality Analysis concepts are used as a representative mission assurance example for evaluating SRAC traceability workflows.

No affiliation with, endorsement by, or extension of the SPARTA framework is implied.

Objective
The objective of this pilot is to demonstrate how existing engineering information, including SBOMs, mission functions, assurance evidence, and supplier assertions, can be connected through machine-readable SRAC metadata to support faster impact analysis and review workflows.

The pilot focuses on understanding the potential mission impact of software vulnerabilities, software updates, configuration changes, and supplier-provided software components without requiring the creation of a separate assurance ecosystem.

Problem
When a software component changes or a vulnerability is discovered, engineers often need to manually review multiple engineering artifacts to understand:

Which mission functions depend on the component
Which assurance determinations may require reassessment
Which requirements, hazards, and verification artifacts apply
What supporting evidence already exists
Which organizations or stakeholders need to review the change
This information typically exists across multiple engineering repositories but is not easily exchangeable or machine-readable.

Solution
SRAC provides traceability across existing engineering information.

CVE
↓
Software Component
↓
Mission Function
↓
Authority
↓
Assurance Evidence
↓
Impact Analysis Report