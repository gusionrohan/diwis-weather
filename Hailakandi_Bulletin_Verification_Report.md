# Hailakandi Daily Bulletin — Verification Report

**Review date:** 24 October 2026  
**Bulletin reviewed:** `DDMA_Hailakandi_Daily_Report (1).md`  
**Bulletin issue time:** 20 October 2026, 16:37 IST  
**Scope:** Desk review of the bulletin's stated values and source claims against the DIWIS code paths and documentation available for this review.

## Summary

The rainfall-departure arithmetic in the bulletin does not match its stated rainfall and normal values. Several other numerical or location-specific claims cannot be verified from the bulletin because it does not include the dated source records or raw data used to produce them. In addition, some claims—particularly sector-level lightning predictions and catchment inflow predictions—are not supported by the DIWIS feeds and report-generation paths reviewed.

This is a verification of calculations and documented data provenance, not certification against physical ground truth. No independent station logs, original dated IMD/RMC records, or authorized IITM-ILDN source records were provided for this review.

## Findings

| Bulletin item | Verification result | Evidence and interpretation |
|---|---|---|
| Past 24-hour rainfall: **0.1 mm** | **Unverified** | The bulletin does not include the original dated observation record or a station identifier. DIWIS can use the IMD district rainfall page, an Assam RMC station report, or an explicitly labelled IMD grid estimate. These sources represent different coverage and measurement types; the bulletin does not identify which specific record produced 0.1 mm. |
| Normal rainfall: **2.7 mm** | **Unverified** | No normal-period definition, reference climatology, or source record is provided. The app paths reviewed do not establish this benchmark for this bulletin. |
| Rainfall departure: **−95% (Large Deficient)** | **Arithmetic does not match the stated inputs** | Using `(actual − normal) / normal × 100`, the stated values give `(0.1 − 2.7) / 2.7 × 100 = −96.296…%`, or **−96.3%** (approximately **−96%** rounded to a whole percentage point), not −95%. The category also cannot be independently verified without the applicable official thresholds and validated source inputs. |
| Current temperature, maximum/minimum, humidity, and wind | **Unverified** | DIWIS's documented temperature forecast is an Open-Meteo model forecast at a representative point inside a district, not an observation. The reviewed report-generation path does not establish the bulletin's ambient temperature, humidity, or wind values as verified district observations. The bulletin supplies no station, observation timestamp, or original source record for these values. |
| Five-day temperature table | **Unverified as historical values** | DIWIS can fetch five-day Open-Meteo maximum/minimum forecasts at a district reference point. That confirms a possible type of data path, not that these particular values or dates were returned on 20 October 2026. The dated API response or saved source payload was not provided. |
| Five-day rainfall forecast marked “Dry” for every day | **Unverified as historical values** | DIWIS uses the IMD five-day district rainfall feed and can fall back to matching Meteorological Centre district forecast PDFs for missing days. The bulletin does not attach the dated feed/PDF records or identify a source per row, so these entries cannot be confirmed. |
| Hailakandi “High Risk” lightning alert, 3–6 hour window, named sectors, coordinates, and storm-track direction | **Not verified; unsupported by the reviewed DIWIS integration** | DIWIS's official warning/nowcast integration is district-level. Its Bhuvan lightning integration reports recent observed strikes, not future strike locations. The reviewed code and documentation do not generate these sector-level forecast zones, the stated storm track, or the 3–6 hour prediction. The bulletin provides no original RMC/IITM-ILDN product, issue time, validity period, probability, or authorized spatial data to substantiate them. |
| Upstream catchment rainfall and river-inflow predictor table | **Not verified; unsupported by the reviewed DIWIS report path** | The DIWIS generated report explicitly states that it contains no catchment analysis, and selected secondary-district values are not represented as hydrological analysis. No upstream catchment observations, river gauge data, model, or forecast product is attached to the bulletin. |
| Synoptic weather analysis | **No content to verify** | The bulletin contains the section heading but no analysis text or supporting source record. |

## Time validity

The bulletin was issued on **20 October 2026 at 16:37 IST**. Its stated “next 3 to 6 hours” lightning window would end approximately between **19:37 and 22:37 IST on 20 October 2026**. It is therefore expired and must not be presented as a current alert on the review date, **24 October 2026**.

## DIWIS provenance context

- DIWIS's temperature forecast function requests Open-Meteo daily maximum/minimum values for a representative point derived from the district boundary. This is a model forecast, not a district-wide observation ([`app.py`](D:/WebScrap/app.py)).
- DIWIS's rainfall logic distinguishes IMD district observations, Assam station readings, and area-weighted IMD grid estimates. A station value is not a district average, and a grid result is an estimate ([`README.md`](D:/WebScrap/README.md)).
- DIWIS's official district warning and nowcast sources provide district-level outlooks. Bhuvan lightning points are recent observations and do not forecast future strike locations ([`README.md`](D:/WebScrap/README.md)).
- The generated DIWIS bulletin says “No catchment analysis” and does not claim the secondary district section is hydrological analysis ([`app.py`](D:/WebScrap/app.py)).

## Conclusion and recommended correction

Do not circulate the attached bulletin as a fully verified official operational product in its current form. Correct the stated rainfall departure to **−96.3% (about −96%)** if—and only if—the 0.1 mm and 2.7 mm inputs are confirmed from valid source records. Otherwise, mark the departure and its category as **not verified**.

For the remaining values, retain them only after attaching the original dated source records and documenting the source, location or station, issue/observation time, valid period, and whether the value is observed, modelled, or derived. Remove or clearly label the sector-level lightning zones, storm track, and catchment predictions unless an authorized product that actually provides those details is supplied. Do not present the 20 October lightning window as current.

**Verification limitation:** This report checks the supplied bulletin text against DIWIS's documented implementation and verifies the departure arithmetic. It does not independently retrieve or authenticate archived source data for 20 October 2026, and it does not establish physical ground truth.
