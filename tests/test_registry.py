import unittest

from campus_events.registry import load_registry


class RegistryTests(unittest.TestCase):
    def test_registry_loads_documented_sources(self) -> None:
        sources = load_registry("source_registry.yaml")
        self.assertTrue(sources)
        self.assertTrue(any(source.id == "rsis_event_rss" for source in sources))
        self.assertTrue(any(source.id == "ntu_scelse_all_events" for source in sources))
        self.assertTrue(any(source.active for source in sources))
        self.assertTrue(any(not source.active for source in sources))
