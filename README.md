GS → PN Intercompany Invoice Synchronization & Reconciliation

This repository contains the Python implementation of the GS Denmark → PN Norway intercompany invoice synchronization and reconciliation system. The solution validates the integrity of invoice and credit memo transfers between GS NAV and PN NAV, ensuring that PN NAV remains a complete and accurate mirror of GS NAV for domestic invoicing and VAT reporting. All SQL queries use fake tables, and all sample data is fully masked (GDPR‑safe).

Core Capabilities

Line‑level reconciliation of GS and PN invoice data

Detection of missing or mismatched PN lines

Validation of VAT‑critical fields

Preparation of PN posting payloads for failed transfers

Schema normalization across GS and PN datasets

Robust merge logic using NAV‑native keys (DocumentNo + LineNo)

SQL‑based extraction via config‑driven queries

Why This Matters
PN Norway acts as the domestic invoicing entity for Norwegian end‑customers.
GS Denmark handles fulfillment and posts the financial transaction.
The GS → PN transfer tool must therefore:

Recreate GS invoices in PN NAV with full fidelity

Apply Norwegian VAT rules

Enable PN to issue compliant domestic invoices

Maintain strict data integrity

This project ensures that every GS invoice is transferred correctly and that PN NAV remains a reliable, compliant financial ledger.

Designed For

Intercompany NAV/BC environments

EDI‑driven order flows

Cross‑border VAT compliance

High‑integrity financial data pipelines

Automated invoice distribution systems