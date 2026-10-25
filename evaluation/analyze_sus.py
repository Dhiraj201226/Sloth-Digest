"""
Sloth Digest — Empirical Usability Evaluation (SUS Analysis Script)
Analyzes System Usability Scale (SUS) scores across participants.
Formula:
  For odd-numbered items (1, 3, 5, 7, 9): score - 1
  For even-numbered items (2, 4, 6, 8, 10): 5 - score
  Sum of adjusted scores * 2.5 = SUS Score (0-100)
"""

from typing import List, Dict, Any


def calculate_individual_sus(responses: List[int]) -> float:
    """
    Calculates individual SUS score from 10 item responses (1-5 Likert scale).
    """
    if len(responses) != 10:
        raise ValueError(f"Expected 10 responses, got {len(responses)}")

    adjusted_scores = []
    for idx, score in enumerate(responses):
        if not (1 <= score <= 5):
            raise ValueError(f"Response at index {idx} must be between 1 and 5 (got {score})")
        if idx % 2 == 0:  # Odd item (1, 3, 5, 7, 9 in 1-indexed)
            adjusted_scores.append(score - 1)
        else:  # Even item (2, 4, 6, 8, 10 in 1-indexed)
            adjusted_scores.append(5 - score)

    return sum(adjusted_scores) * 2.5


def calculate_cohort_sus(participant_responses: Dict[str, List[int]]) -> Dict[str, Any]:
    """
    Computes cohort statistics. Returns empty stats if no participant data exists.
    """
    if not participant_responses:
        return {
            "participant_count": 0,
            "individual_scores": {},
            "mean_sus": None,
            "status": "Awaiting participant empirical test sessions (DO NOT INVENT RESULTS)",
        }

    scores = {}
    for pid, resp in participant_responses.items():
        scores[pid] = calculate_individual_sus(resp)

    mean_score = sum(scores.values()) / len(scores)
    return {
        "participant_count": len(scores),
        "individual_scores": scores,
        "mean_sus": round(mean_score, 1),
        "grade": (
            "A+ (Best-in-class)" if mean_score >= 84.1
            else "A (Excellent)" if mean_score >= 80.3
            else "B (Good)" if mean_score >= 68.0
            else "C (Average / OK)" if mean_score >= 51.0
            else "F (Unacceptable)"
        ),
    }


if __name__ == "__main__":
    # Test script self-check
    print("SUS Analyzer initialized.")
    # Intentionally empty participant cohort — awaiting real empirical sessions
    empty_cohort = {}
    results = calculate_cohort_sus(empty_cohort)
    print("Cohort status:", results["status"])
