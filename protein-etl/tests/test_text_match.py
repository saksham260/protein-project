"""Unit tests for src/engine/text_match.py — Suite 2 test cases."""

import pytest
from src.engine.text_match import find_term_spans, pick_longest_matches


# ==========================================
# 2.1 find_term_spans
# ==========================================

def test_find_term_spans_exact():
    spans = find_term_spans("palm oil, cocoa", "palm oil")
    assert spans == [(0, 8)]


def test_find_term_spans_no_match_substring():
    # "palm" inside "palmolein" should not match whole-word
    spans = find_term_spans("palmolein oil", "palm")
    assert spans == []


def test_find_term_spans_multiple_matches():
    spans = find_term_spans("palm oil, refined palm oil", "palm oil")
    assert spans == [(0, 8), (18, 26)]


def test_find_term_spans_regex_special_chars():
    # INS 965(i) has parentheses which require escaping
    spans = find_term_spans("contains ins 965(i) sweetener", "ins 965(i)")
    assert len(spans) == 1
    assert spans == [(9, 19)]


def test_find_term_spans_empty_text():
    assert find_term_spans("", "palm oil") == []


def test_find_term_spans_empty_term():
    # empty term matches every non-word boundary position or behaves deterministically
    spans = find_term_spans("palm", "")
    assert isinstance(spans, list)


def test_find_term_spans_at_start():
    assert find_term_spans("maltitol, sugar", "maltitol") == [(0, 8)]


def test_find_term_spans_at_end():
    text = "sugar, maltitol"
    assert find_term_spans(text, "maltitol") == [(7, 15)]


def test_find_term_spans_case_sensitive():
    # find_term_spans expects text to be already normalized/lowered
    assert find_term_spans("Palm Oil", "palm oil") == []
    assert find_term_spans("palm oil", "palm oil") == [(0, 8)]


# ==========================================
# 2.2 pick_longest_matches
# ==========================================

def test_pick_longest_matches_non_overlapping():
    candidates = [((0, 8), "palm oil"), ((10, 15), "sugar")]
    chosen = pick_longest_matches(candidates)
    assert len(chosen) == 2
    assert chosen == [((0, 8), "palm oil"), ((10, 15), "sugar")]


def test_pick_longest_matches_corn_syrup_overlap():
    # "high fructose corn syrup" (0, 24) overlaps "corn syrup" (14, 24)
    candidates = [
        ((14, 24), "corn syrup"),
        ((0, 24), "high fructose corn syrup"),
    ]
    chosen = pick_longest_matches(candidates)
    assert len(chosen) == 1
    assert chosen[0] == ((0, 24), "high fructose corn syrup")


def test_pick_longest_matches_glucose_syrup_overlap():
    # "hydrogenated glucose syrup" (0, 26) overlaps "glucose syrup" (13, 26)
    candidates = [
        ((13, 26), "glucose syrup"),
        ((0, 26), "hydrogenated glucose syrup"),
    ]
    chosen = pick_longest_matches(candidates)
    assert len(chosen) == 1
    assert chosen[0] == ((0, 26), "hydrogenated glucose syrup")


def test_pick_longest_matches_empty():
    assert pick_longest_matches([]) == []


def test_pick_longest_matches_single():
    cand = [((0, 5), "apple")]
    assert pick_longest_matches(cand) == cand
