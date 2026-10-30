# Utility networks and responsibility

Reviewed 2026-10-25 against the 236-source public catalogue. This release adds four City of Surrey feeds. Network lines remain lines; actual service areas remain polygons. It does not infer connection capacity, private service branches, a right to connect, or surveyed excavation alignment.

| Published feed | Features at review | Public fields | Native geometry |
| --- | ---: | ---: | --- |
| [Water mains](https://www.arcgis.com/home/item.html?id=299f2ce317ff47548505e89fbacde3ae) | 30,952 | 23 | LineString / MultiLineString |
| [Sanitary sewer mains](https://www.arcgis.com/home/item.html?id=1fcb20e92b574a1997f8fbba0da81eca) | 34,577 | 25 | LineString / MultiLineString |
| [Stormwater drainage mains](https://www.arcgis.com/home/item.html?id=9a9e2f0b3bd24ccb8349e15734b41315) | 47,506 | 36 | LineString / MultiLineString |
| [Water service areas](https://www.arcgis.com/home/item.html?id=c520c8f0cc8d47f2b121819f0b4ea1ce) | 30 | 7 | Polygon / MultiPolygon |

Each line feed includes `OWNER`, `MAINTENANCE_RESPONSIBILITY`, and `OPERATIONAL_RESPONSIBILITY`. They describe different published responsibilities and remain separate. Reviewed records include both Surrey and private ownership; blank and null responsibility stays unknown. The service-area layer publishes area names and pressure-zone status, but no per-area operator field. Its publisher is not assigned as every area's operator.

All public fields in the reviewed hosted layers are requested and preserved, including status, material, dimensions, original facility identifiers, source maintenance dates where supplied, and source nulls. Proposed and abandoned statuses are not silently promoted to in-service assets. Source edit times are separate from asset installation dates and survey dates. Original publisher field definitions and domains are retained in `data/utilities/surrey-verification.json`.

## Verification and daily operation

The four hosted services are owned by `SurreyGIS` and allow public CORS requests. Full identifier inventories match their independent counts before capture and remain stable afterward. The production loader retrieved every selected identifier and field for a bounded test area: 217 water lines, 224 sanitary lines, and 240 drainage lines. It also retrieved all 30 service-area polygons with closed, finite WGS84 rings. No simplification, buffering, inferred geometry, or coordinate rounding is applied. Live checks used about 1.18 MB total; geometry is not checked into this repository.

`expectedGeometry: "line"` explicitly opts into published `esriGeometryPolyline` metadata and valid GeoJSON line geometry. Existing configurations continue to require polygons. LineString paths need at least two finite WGS84 positions; MultiLineString requires every component to pass. Both forms retain the existing complete identifier inventory, schema checks, stable source revision check, and last-good cache behavior. The loader preserves the 1–24 selected-area union and deduplicates shared identifiers.

The existing daily map-service checker discovers `data/catalog-utility-networks.json` automatically and applies the same metadata geometry/schema checks and independent count request. No new workflow or checker file is required. Daily health checks are not a daily survey or a complete geometry recapture. Users load bounded native geometry on demand; large views ask for a closer zoom instead of truncating records. Strict requested-field and geometry checks reject incomplete native responses.

## Reuse and attribution

[Surrey's open-data portal](https://opendata-surrey.hub.arcgis.com/) links its [Open Government License - Surrey](https://opendata-surrey.hub.arcgis.com/pages/55089a19491a4fe59a41e059fd8af708). The current official page grants commercial reuse with attribution, disclaims warranty, and excludes rights in personal information, third-party material, and official marks. The source and map attribution is: Contains information licensed under the Open Government License – City of Surrey. No official logo or endorsement is used. The exact licence page is available through the [publisher page API](https://www.arcgis.com/sharing/rest/content/items/55089a19491a4fe59a41e059fd8af708/data?f=json).

## Remaining gaps and next useful sources

- **BC electrical distribution:** [BC Hydro - Electrical Utility Data](https://catalogue.data.gov.bc.ca/dataset/bc-hydro-electrical-utility-data) lists overhead and underground primary/secondary lines, circuits, transformers and other assets, but requires an ICI Society Data Sharing Licence. It is an access gap, not an open layer to copy. Existing BC transmission corridors do not replace detailed distribution or service connections.
- **Vancouver water and sewer:** the existing catalogue only references water transmission mains. Official [water distribution mains](https://opendata.vancouver.ca/explore/dataset/water-distribution-mains/), [sewer mains](https://opendata.vancouver.ca/explore/dataset/sewer-mains/), and [Metro Vancouver trunk sewers](https://opendata.vancouver.ca/explore/dataset/gvrd-sewer-trunk-mains/) have a public Opendatasoft API and explicit weekly extraction notes. Commercial and residential connections are expressly excluded. A separate bounded Opendatasoft loader or snapshot adapter is needed; they are not ArcGIS feature layers.
- **Washington electricity:** the [UTC Energy page](https://www.utc.wa.gov/regulated-industries/utilities/energy) links an [official electric-service viewer](https://wutc.maps.arcgis.com/apps/instant/basic/index.html?appid=39cd8428f872494e91b13da94a5cd3cd). Its [native service-area layer](https://services2.arcgis.com/lXwA5ckdH5etcXUm/arcgis/rest/services/UTC_Regulated_Electric_Service_Areas/FeatureServer/2) includes a published utility name. The [publisher item](https://www.arcgis.com/home/item.html?id=ef94dd5f2fa747f3ba3e70ba7413add7) explicitly restricts the warranty to display use; it covers selected investor-owned utilities, not all Washington suppliers, distribution lines, or legally guaranteed service territories. Metadata is verified; full geometry validation and release remain separate.
- **National US electricity:** [DHS's HIFLD catalogue record](https://catalog.data.gov/dataset/electric-retail-service-territories) is a useful dated lead, but reports a 2022 dataset update. A recently created ArcGIS copy is not proof of current utility responsibility or original-publisher authority. No arbitrary copy was added.
- **National Canadian networks:** existing Statistics Canada ODI references cover electrical grid, potable water, and wastewater/stormwater with uneven source jurisdiction coverage. Archives were not bulk-downloaded in this milestone; they need per-source licence, operator-field and coverage audit before map integration.

These additions fill a verified municipal gap. They do not claim complete Canadian or US utility coverage.
