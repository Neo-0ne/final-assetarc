"""
This file contains the business logic for the lifecycle engine's modules.
"""

# This is a simplified representation of which templates are needed for which structure.
# In a real system, this might be more complex or stored in a database.
STRUCTURE_TEMPLATE_MAP = {
    "za_pty_ltd": {
        "name": "Private Company (Pty) Ltd",
        "description": "A standard limited liability company in South Africa, good for general business operations and liability protection.",
        "required_templates": [
            "company.incorp_checklist.za.v1",
            "company.board_resolution.za.v1",
            "company.share_certificate.za.v1"
        ]
    },
    "za_trust": {
        "name": "Inter-Vivos Trust",
        "description": "An entity created during one's lifetime to hold assets for beneficiaries. Excellent for asset protection and estate planning.",
        "required_templates": [
            "trust.deed.za.v1",
            "trust.letter_of_wishes.za.v1",
            "trustee.resolution.za.v1"
        ]
    },
    "mu_ibc": {
        "name": "Mauritius GBC (International Business Company)",
        "description": "An offshore company in Mauritius, ideal for international trade, investment holding, and tax optimization.",
        "required_templates": [
            "ibc.moa.v1",
            "ibc.nominee_agreement.v1",
            "ibc.kyc_checklist.v1"
        ]
    }
}


def design_corporate_structure(goals: list[str], jurisdiction: str) -> dict:
    """
    Proposes a corporate structure based on goals and jurisdiction.
    This is a simple rule-based implementation.
    """

    # Normalize inputs
    goals = [goal.lower() for goal in goals]
    jurisdiction = jurisdiction.lower()

    proposed_structures = []

    # --- Rule Engine ---
    if "liability_protection" in goals and jurisdiction == "za":
        if "za_pty_ltd" not in [p['id'] for p in proposed_structures]:
            proposed_structures.append({
                "id": "za_pty_ltd",
                **STRUCTURE_TEMPLATE_MAP["za_pty_ltd"]
            })

    if "asset_protection" in goals and jurisdiction == "za":
        if "za_trust" not in [p['id'] for p in proposed_structures]:
            proposed_structures.append({
                "id": "za_trust",
                **STRUCTURE_TEMPLATE_MAP["za_trust"]
            })

    if "international_trade" in goals or "tax_efficiency" in goals:
        # Suggesting Mauritius as a default for international goals
        if "mu_ibc" not in [p['id'] for p in proposed_structures]:
            proposed_structures.append({
                "id": "mu_ibc",
                **STRUCTURE_TEMPLATE_MAP["mu_ibc"]
            })

    # --- Fallback/Default ---
    if not proposed_structures:
        if jurisdiction == "za":
            proposed_structures.append({
                "id": "za_pty_ltd",
                **STRUCTURE_TEMPLATE_MAP["za_pty_ltd"]
            })
        else:
            # Default international suggestion
            proposed_structures.append({
                "id": "mu_ibc",
                **STRUCTURE_TEMPLATE_MAP["mu_ibc"]
            })

    return {
        "proposed_structures": proposed_structures,
        "inputs": {
            "goals": goals,
            "jurisdiction": jurisdiction
        }
    }
