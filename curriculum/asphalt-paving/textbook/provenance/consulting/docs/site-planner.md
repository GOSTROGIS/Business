# Site Planner

Open **Site planner** in the map ribbon.

1. In **Site**, choose Canada or United States, enter an address or place and press **Search**. Review a result, inspect its location or adjust the pin, then select **Confirm site**. You can also enter latitude/longitude or place a pin directly.
2. In **Addresses**, add legal descriptions, parcel identifiers, civic/street, rural, mailing, PO box, postal/ZIP, intersection, place, coordinate or other records. **Save site record** retains their original text and identifies manually entered records as user supplied.
3. Load the map layers and project areas needed for the project. In **Travel**, press **Load destinations**, then filter by entity type or text. All eligible loaded records are paginated; polygons without an access point remain available with **Location required**. Select a record and confirm its published point or place an access pin.
4. Set maximum road kilometres and drive minutes, then press **Calculate route**. Use **Within limits only** to filter successful comparisons. Results retain provider, direction, calculation time and unreachable/error status. Distances follow the returned car route; no straight-line fallback is used.
5. In **Contents**, style or remove **Site locations** and **Road routes**. **Clear map** cancels requests and removes their map overlays. The selected site record remains available; reopening the app does not redraw it until **Show site** is selected.

## Data and provider boundaries

Search is submitted explicitly. No address, parcel or route inventory is downloaded at startup. Only one selected site record is stored in the browser, with a 256 KiB limit; provider result lists, travel comparisons and route geometry are not persisted. User-submitted searches and route endpoints go to the named external provider. A changed layer selection, source response or project area invalidates prior destination comparisons.

The Canadian lookup uses NRCan Geolocator; the U.S. lookup uses Census's documented JSONP transport inside an isolated sandbox. Source rows, address components, identifiers and reported precision are preserved. A geocoder result does not establish legal title or postal deliverability. Source coordinates are retained when a user adds an access pin.

The public routing service permits individual manual car routes. Bulk supplier matrices, truck restrictions, traffic and alternative travel profiles require a suitable configured service. The module supports bounded comparisons against such a service, but the public app does not configure one. National legal/parcel search and licensed postal validation are separate integrations, tracked in [the implementation backlog](implementation-backlog.md) and [provider design](address-routing-design.md).

## Published verification

Published on 2026-10-26 in `1a44edb6`, with successful repository validation, interface checks and [Pages deployment](https://github.com/GOSTROGIS/CONSULTING/actions/runs/40270114808). [Sixteen actual public checks](evidence/site-planner-public-2026-10-26.json) verified Canadian and U.S. address results, complete source records, explicit location confirmation, two road routes, all 53 loaded point/polygon destinations, styling, filter invalidation, Clear/reload and mobile focus. No source-data or code substitutions were used. [All ten published program hashes](evidence/site-planner-public-code-2026-10-26.json) matched the tested candidate.
