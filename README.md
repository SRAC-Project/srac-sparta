SRAC-SPARTA
Safety Relevance Assertion Capability (SRAC) reference implementation for SPARTA mission assurance, change impact analysis, and traceability.

Problem
When a component changes or a vulnerability is discovered, determining mission impact requires searching across multiple engineering artifacts.

Solution
SRAC provides traceability from:

CVE ↓ Component ↓ Mission Function ↓ Authority ↓ Evidence

Prototype
Current implementation supports:

SRAC Assertions
SPDX SBOM
Component Impact Analysis
Report Generation
Example
OpenSSL ↓ AUTH-CMD-001 ↓ REQ-101 HAZ-22 TEST-15
Pilot Scenarios
The reference implementation demonstrates the following scenarios:

Mission Assurance Traceability
Software component → Mission Function → Evidence

Example:

OpenSSL ↓ AUTH-CMD-001 ↓ REQ-101 HAZ-22 TEST-15

Vulnerability Impact Analysis
A vulnerability can be mapped to affected mission functions and assurance evidence.

Example:

CVE-2026-1234 ↓ OpenSSL ↓ AUTH-CMD-001

Shared Library Analysis
A shared software library may support multiple mission functions, allowing impact analysis across multiple operational capabilities.

Reassessment Workflow
When a software component changes or a vulnerability is discovered, the implementation identifies mission functions and existing assurance evidence that may require review.

Supplier Exchange
Assurance information can be exchanged between a supplier and a mission integrator using structured SRAC metadata.

Automated Reporting
Impact analysis results are automatically exported as reports for review and decision support.