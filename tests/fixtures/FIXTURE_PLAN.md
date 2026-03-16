# Fixture Plan

This file lists the first raw fixtures to capture for parser work. It is derived from the validated registry in [source_registry.yaml](/Users/scelsenus/Desktop/CampusEvents/source_registry.yaml).

## Capture Rules

- Save raw responses, not cleaned output.
- Capture one listing fixture and one detail fixture when the source has both.
- Name fixtures with the source slug and capture date.
- Prefer HTML as returned by the server, or XML for RSS.

## Phase 1 Fixtures

| Priority | Source ID | Parser Family | Listing Fixture | Detail Fixture | Reason |
| --- | --- | --- | --- | --- | --- |
| High | `nus_coe_rss_directory` | `nus_coe_rss_directory` | `nus_coe_rss_directory_2026-03-16.xml` | none | Core NUS feed index; may unlock multiple downstream RSS sources |
| High | `rsis_event_rss` | `generic_rss` | `rsis_event_rss_2026-03-16.xml` | optional linked item HTML | Simple RSS baseline parser |
| High | `nus_osa_events` | `nus_osa_events` | `nus_osa_events_2026-03-16.html` | `nus_osa_event_detail_sample_2026-03-16.html` | High-value mixed public events source |
| High | `nus_arts_festival` | `nus_arts_festival` | `nus_arts_festival_2026-03-16.html` | `nus_arts_festival_detail_sample_2026-03-16.html` | Performance-heavy source |
| High | `nus_museum` | `museum_cards` | `nus_museum_home_2026-03-16.html` | `nus_museum_event_detail_sample_2026-03-16.html` | Exhibition parsing pattern |
| High | `nus_cqt_upcoming_events` | `upcoming_events_listing` | `nus_cqt_upcoming_events_2026-03-16.html` | `nus_cqt_event_detail_sample_2026-03-16.html` | Institute upcoming-events pattern |
| High | `nus_mbi_seminar_series` | `seminar_series_listing` | `nus_mbi_seminar_series_2026-03-16.html` | `nus_mbi_event_detail_sample_2026-03-16.html` | Seminar-series parsing pattern |
| High | `ntu_main_events` | `ntu_event_portal` | `ntu_main_events_2026-03-16.html` | `ntu_main_event_detail_sample_2026-03-16.html` | Core NTU university parser |
| High | `ntu_ias_events` | `ntu_event_detail_listing` | `ntu_ias_events_2026-03-16.html` | `ntu_ias_event_detail_sample_2026-03-16.html` | Representative NTU school/institute detail pattern |
| High | `ntu_museum_exhibitions` | `museum_listing` | `ntu_museum_exhibitions_2026-03-16.html` | `ntu_museum_exhibition_detail_sample_2026-03-16.html` | NTU cultural listings |
| High | `ntu_cceb_seminars` | `seminar_hub` | `ntu_cceb_seminars_2026-03-16.html` | `ntu_cceb_seminar_detail_sample_2026-03-16.html` | Distinct seminar hub pattern |
| High | `ntu_scelse_all_events` | `filtered_event_cards` | `ntu_scelse_all_events_2026-03-16.html` | `ntu_scelse_event_detail_sample_2026-03-16.html` | Filterable institute event cards |

## Phase 2 Fixtures

| Priority | Source ID | Parser Family | Listing Fixture | Detail Fixture | Reason |
| --- | --- | --- | --- | --- | --- |
| Medium | `nus_baba_house` | `heritage_programmes` | `nus_baba_house_home_2026-03-16.html` | `nus_baba_house_programme_sample_2026-03-16.html` | Cultural programme pattern |
| Medium | `nus_lkcnhm` | `museum_cards` | `nus_lkcnhm_home_2026-03-16.html` | `nus_lkcnhm_whats_on_sample_2026-03-16.html` | Tours and workshops variation |
| Medium | `nus_fass_events` | `taxonomy_events` | `nus_fass_events_2026-03-16.html` | `nus_fass_event_detail_sample_2026-03-16.html` | Faculty taxonomy event pattern |
| Medium | `nus_sph_events` | `detail_cards` | `nus_sph_events_2026-03-16.html` | `nus_sph_event_detail_sample_2026-03-16.html` | School event detail pattern |
| Medium | `nus_math_events` | `series_and_conference_index` | `nus_math_events_2026-03-16.html` | `nus_math_event_series_sample_2026-03-16.html` | Series-and-conference pattern |
| Medium | `ntu_mae_events` | `ntu_event_detail_listing` | `ntu_mae_events_2026-03-16.html` | `ntu_mae_event_detail_sample_2026-03-16.html` | Additional NTU school variant |
| Medium | `ntu_sbs_events` | `ntu_event_detail_listing` | `ntu_sbs_events_2026-03-16.html` | `ntu_sbs_event_detail_sample_2026-03-16.html` | Symposium variation |
| Medium | `ntu_cee_events` | `ntu_event_detail_listing` | `ntu_cee_events_2026-03-16.html` | `ntu_cee_event_detail_sample_2026-03-16.html` | Distinguished seminar variation |
| Medium | `ntu_erian_news_events` | `institute_news_events` | `ntu_erian_news_events_2026-03-16.html` | `ntu_erian_event_detail_sample_2026-03-16.html` | Institute mixed news-events pattern |

## Out Of Scope For Initial Fixture Capture

- candidate-only sources still under validation
- rejected sources
- discovery pages that are not canonical event listings
