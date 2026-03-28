#!/usr/bin/env python3
"""
Calculate true total flight cost including all fees based on traveler profile.
Re-ranks flights by actual cost to pay.

Usage:
    python fee_calculator.py --flights results.json --bags 1 [--loyalty VN:gold]

Output: JSON with re-ranked flights including fee breakdown.
"""

import argparse
import json
import sys
from pathlib import Path

# Add shared scripts to path
shared_scripts = str(Path(__file__).parent.parent.parent.parent / "scripts")
sys.path.insert(0, shared_scripts)

# --- Airline Fee Database ---
# Fees in USD. Source: published airline policies (subject to change).
AIRLINE_FEES = {
    # Low-Cost Carriers
    "VJ": {  # VietJet
        "type": "LCC",
        "carry_on_included": True,
        "carry_on_weight": "7kg",
        "carry_on_size": "56×36×23cm",
        "checked_bag_1": 25,
        "checked_bag_2": 45,
        "seat_selection": 5,
        "priority_boarding": 8,
        "meal": 5,
        "change_fee": 30,
        "cancel_refund": "voucher_only",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": False,
    },
    "AK": {  # AirAsia
        "type": "LCC",
        "carry_on_included": True,
        "carry_on_weight": "7kg",
        "carry_on_size": "54×38×23cm (paid cabin bag)",
        "checked_bag_1": 30,
        "checked_bag_2": 55,
        "seat_selection": 6,
        "priority_boarding": 10,
        "meal": 5,
        "change_fee": 35,
        "cancel_refund": "none",
        "payment_surcharge_cc": 3,
        "loyalty_bag_waiver": False,
    },
    "NK": {  # Spirit
        "type": "ULCC",
        "carry_on_included": False,  # Only personal item
        "carry_on_weight": "None (personal item: 45×35×20cm)",
        "carry_on_size": "45×35×20cm (personal item only free)",
        "checked_bag_1": 40,
        "checked_bag_2": 50,
        "carry_on_fee": 45,  # Spirit charges for overhead bin
        "seat_selection": 10,
        "priority_boarding": 0,
        "meal": 8,
        "change_fee": 99,
        "cancel_refund": "credit_within_24h",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,  # Gold/Silver status
    },
    "FR": {  # Ryanair
        "type": "ULCC",
        "carry_on_included": False,
        "carry_on_weight": "10kg (paid)",
        "carry_on_size": "40×20×25cm (free small bag only)",
        "checked_bag_1": 30,
        "checked_bag_2": 45,
        "carry_on_fee": 8,
        "seat_selection": 4,
        "priority_boarding": 6,
        "meal": 5,
        "change_fee": 45,
        "cancel_refund": "none",
        "payment_surcharge_cc": 2,
        "loyalty_bag_waiver": False,
    },
    # Legacy/Full-Service Carriers
    "VN": {  # Vietnam Airlines
        "type": "FSC",
        "carry_on_included": True,
        "carry_on_weight": "12kg (economy)",
        "carry_on_size": "56×36×23cm",
        "checked_bag_1": 0,  # Included in most fares
        "checked_bag_2": 50,
        "seat_selection": 0,
        "priority_boarding": 0,
        "meal": 0,  # Included
        "change_fee": 50,
        "cancel_refund": "partial",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,
    },
    "SQ": {  # Singapore Airlines
        "type": "FSC",
        "carry_on_included": True,
        "carry_on_weight": "7kg",
        "carry_on_size": "55×40×20cm",
        "checked_bag_1": 0,
        "checked_bag_2": 0,  # 30kg included in economy
        "seat_selection": 0,
        "priority_boarding": 0,
        "meal": 0,
        "change_fee": 75,
        "cancel_refund": "partial",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,
    },
    "UA": {  # United
        "type": "FSC",
        "carry_on_included": True,
        "carry_on_weight": "No limit",
        "carry_on_size": "56×35×22cm",
        "checked_bag_1": 35,  # International may vary
        "checked_bag_2": 45,
        "seat_selection": 0,  # Basic economy has fee
        "priority_boarding": 0,
        "meal": 0,
        "change_fee": 0,  # United eliminated change fees
        "cancel_refund": "credit",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,
    },
    "KE": {  # Korean Air
        "type": "FSC",
        "carry_on_included": True,
        "carry_on_weight": "10kg",
        "carry_on_size": "55×40×20cm",
        "checked_bag_1": 0,
        "checked_bag_2": 0,  # 23kg × 2 on most international
        "seat_selection": 0,
        "priority_boarding": 0,
        "meal": 0,
        "change_fee": 60,
        "cancel_refund": "partial",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,
    },
    "TK": {  # Turkish Airlines
        "type": "FSC",
        "carry_on_included": True,
        "carry_on_weight": "8kg",
        "carry_on_size": "55×40×23cm",
        "checked_bag_1": 0,
        "checked_bag_2": 0,
        "seat_selection": 0,
        "priority_boarding": 0,
        "meal": 0,
        "change_fee": 50,
        "cancel_refund": "partial",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,
    },
    "WN": {  # Southwest
        "type": "FSC",
        "carry_on_included": True,
        "carry_on_weight": "No limit",
        "carry_on_size": "61×41×28cm",
        "checked_bag_1": 0,
        "checked_bag_2": 0,  # 2 free bags!
        "seat_selection": 0,
        "priority_boarding": 15,
        "meal": 3,
        "change_fee": 0,
        "cancel_refund": "credit",
        "payment_surcharge_cc": 0,
        "loyalty_bag_waiver": True,
    },
}

# Default for unknown airlines
DEFAULT_FSC_FEES = {
    "type": "FSC",
    "carry_on_included": True,
    "carry_on_weight": "7-10kg",
    "checked_bag_1": 0,
    "checked_bag_2": 50,
    "seat_selection": 0,
    "priority_boarding": 0,
    "meal": 0,
    "change_fee": 75,
    "cancel_refund": "partial",
    "payment_surcharge_cc": 0,
    "carry_on_fee": 0,
    "loyalty_bag_waiver": True,
}

DEFAULT_LCC_FEES = {
    "type": "LCC",
    "carry_on_included": True,
    "carry_on_weight": "7kg",
    "checked_bag_1": 30,
    "checked_bag_2": 55,
    "seat_selection": 6,
    "priority_boarding": 8,
    "meal": 5,
    "change_fee": 40,
    "cancel_refund": "none",
    "payment_surcharge_cc": 2,
    "carry_on_fee": 0,
    "loyalty_bag_waiver": False,
}


def get_airline_fees(airline_code):
    """Get fee structure for an airline."""
    if airline_code in AIRLINE_FEES:
        fees = AIRLINE_FEES[airline_code].copy()
        fees.setdefault("carry_on_fee", 0)
        return fees
    # Guess based on common LCC indicators
    lcc_codes = {"VJ", "AK", "FD", "QZ", "NK", "F9", "FR", "U2", "W6", "TR", "5J", "6E", "JT"}
    if airline_code in lcc_codes:
        return DEFAULT_LCC_FEES.copy()
    return DEFAULT_FSC_FEES.copy()


def calculate_true_total(flight, passengers, checked_bags, loyalty=None):
    """
    Calculate true total price including all fees.

    Args:
        flight: Unified flight object from normalize.py
        passengers: {"adults": N, "children": N, "infants": N}
        checked_bags: Number of checked bags per passenger
        loyalty: dict of {airline_code: tier} e.g., {"VN": "gold"}

    Returns:
        dict with fee breakdown and true_total
    """
    total_pax = passengers.get("adults", 1) + passengers.get("children", 0)
    primary_airline = flight["airlines"][0] if flight["airlines"] else "XX"
    fees = get_airline_fees(primary_airline)

    base_price = flight["price_total"]

    # Fee calculations
    carry_on_fee = 0
    if not fees.get("carry_on_included", True):
        carry_on_fee = fees.get("carry_on_fee", 0) * total_pax

    bag_fee = 0
    if checked_bags >= 1:
        per_bag_1 = fees.get("checked_bag_1", 0)
        # Loyalty waiver
        if loyalty and primary_airline in loyalty and fees.get("loyalty_bag_waiver"):
            per_bag_1 = 0
        bag_fee += per_bag_1 * total_pax

    if checked_bags >= 2:
        bag_fee += fees.get("checked_bag_2", 0) * total_pax

    seat_fee = fees.get("seat_selection", 0) * total_pax
    payment_fee = fees.get("payment_surcharge_cc", 0) * total_pax

    total_fees = carry_on_fee + bag_fee + seat_fee + payment_fee
    true_total = base_price + total_fees

    return {
        "original_price": base_price,
        "fee_breakdown": {
            "carry_on": carry_on_fee,
            "checked_bags": bag_fee,
            "seat_selection": seat_fee,
            "payment_surcharge": payment_fee,
        },
        "total_fees": round(total_fees, 2),
        "true_total": round(true_total, 2),
        "airline_type": fees["type"],
        "carry_on_size": fees.get("carry_on_size", "Standard"),
        "carry_on_weight": fees.get("carry_on_weight", "7kg"),
        "change_fee": fees.get("change_fee", 0),
        "cancel_policy": fees.get("cancel_refund", "unknown"),
    }


def rerank_flights(flights, passengers, checked_bags, loyalty=None):
    """Calculate true totals and re-rank flights."""
    ranked = []
    for i, flight in enumerate(flights):
        analysis = calculate_true_total(flight, passengers, checked_bags, loyalty)
        ranked.append({
            "original_rank": i + 1,
            "flight": {k: v for k, v in flight.items() if k != "raw"},
            **analysis,
        })

    ranked.sort(key=lambda x: x["true_total"])

    for i, item in enumerate(ranked):
        item["new_rank"] = i + 1
        item["rank_changed"] = item["new_rank"] != item["original_rank"]

    return ranked


def main():
    parser = argparse.ArgumentParser(description="Fee analysis and true total calculator")
    parser.add_argument("--flights", required=True, help="Path to flight results JSON file")
    parser.add_argument("--bags", type=int, default=0, help="Checked bags per person (0-2)")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--children", type=int, default=0)
    parser.add_argument("--loyalty", help="Loyalty: AIRLINE:TIER (e.g., VN:gold)")
    args = parser.parse_args()

    # Load flights
    with open(args.flights) as f:
        flights = json.load(f)

    passengers = {"adults": args.adults, "children": args.children}
    loyalty = {}
    if args.loyalty:
        code, tier = args.loyalty.split(":")
        loyalty[code] = tier

    ranked = rerank_flights(flights, passengers, args.bags, loyalty)

    # Output
    result = {
        "profile": {
            "passengers": passengers,
            "checked_bags_per_person": args.bags,
            "loyalty": loyalty,
        },
        "ranked_flights": ranked,
        "rank_reversals": [r for r in ranked if r["rank_changed"]],
    }

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
