import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from activity import summarize, window


class ContributionTests(unittest.TestCase):
    TODAY = date(2026, 10, 28)

    def calendar(self, counts=None, today=None):
        today = today or self.TODAY
        start, _ = window(today)
        counts = counts or {}
        days = [{"date": (start + timedelta(days=i)).isoformat(),
                 "contributionCount": counts.get(start + timedelta(days=i), 0)} for i in range(365)]
        return {"totalContributions": sum(d["contributionCount"] for d in days),
                "weeks": [{"contributionDays": days}]}

    def test_empty_calendar_is_a_real_zero(self):
        result = summarize(self.calendar(), self.TODAY)
        self.assertEqual((result["total"], result["current"], result["longest"]), (0, 0, 0))

    def test_today_and_yesterday_are_valid_streak_endpoints(self):
        for offset in (0, 1):
            counts = {self.TODAY - timedelta(days=i + offset): 2 for i in range(3)}
            result = summarize(self.calendar(counts), self.TODAY)
            self.assertEqual((result["total"], result["current"], result["longest"]), (6, 3, 3))

    def test_gap_breaks_current_and_preserves_longest(self):
        counts = {self.TODAY - timedelta(days=i): 1 for i in range(2, 7)}
        result = summarize(self.calendar(counts), self.TODAY)
        self.assertEqual((result["current"], result["longest"]), (0, 5))

    def test_cross_year_and_leap_day(self):
        for today in (date(2026, 1, 2), date(2024, 3, 1)):
            counts = {today - timedelta(days=i): 1 for i in range(5)}
            result = summarize(self.calendar(counts, today), today)
            self.assertEqual(result["current"], 5)

    def test_missing_duplicate_negative_and_wrong_total_fail(self):
        for change in ("missing", "duplicate", "negative", "total"):
            calendar = self.calendar()
            days = calendar["weeks"][0]["contributionDays"]
            if change == "missing":
                days.pop()
            elif change == "duplicate":
                days.append(days[0])
            elif change == "negative":
                days[0]["contributionCount"] = -1
            else:
                calendar["totalContributions"] = 10
            with self.assertRaises(ValueError):
                summarize(calendar, self.TODAY)

    def test_longest_is_capped_to_window(self):
        start, _ = window(self.TODAY)
        counts = {start + timedelta(days=i): 1 for i in range(365)}
        result = summarize(self.calendar(counts), self.TODAY)
        self.assertEqual((result["active_days"], result["longest"], result["current"]), (365, 365, 365))


if __name__ == "__main__":
    unittest.main()
