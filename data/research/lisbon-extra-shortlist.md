# Lisbon deepening pass 2026-08-05 — shortlist, chosen from ICNF (data/registers/portugal-icnf.json)

69 ICNF entries sit in concelho Lisboa. Published: 12 (lis_001..lis_012).

## Pin disagreement found (register vs our published pin, >50 m)
- **lis_005 "The Tipu of Jardim de Sao Bento"** 38.71165,-9.15478 vs ICNF **KNJ1/347** tipuana,
  lugar "Praca de S.Bento", 38.71360,-9.15350 = **244 m apart**. Same species, adjacent places
  (Jardim de Sao Bento vs Praca de Sao Bento). Either two different classified tipuanas or one
  tree with one bad coordinate. Needs an on-the-ground/second-source resolution before either is
  called confirmed. lis_005 is currently location_precision "confirmed".
- lis_002 (Ajuda Dragon Tree) has NO register entry within 600 m; nearest is a different species.
  That is absence, not disagreement.
- Everything else lines up within 65 m.

## Selected (walk-thickening, not lonely singletons)

WALK A — Principe Real / Avenida da Liberdade (already holds lis_003 cedar, lis_009 paineira)
1. AIP11066144I  Moreton Bay Fig n.2, Jardim Franca Borges (Praca do Principe Real)
   38.71675,-9.14911 | girth 6.05 m | h 21 m | age 145 at 2015 -> ~156 in 2026 | 65 m from lis_003
   Fold: n.1 (AIP11066142I, 4.8 m) and n.3 (AIP11066145I, 4.7 m) are the same 30 m huddle -> leads.
2. AIP11065607I  Yew (Taxus baccata), Jardim Braamcamp Freire / Campo Santana
   38.72170,-9.14000 | girth 3.80 m | h 14 m | age 123 at 2016 -> ~133 | 621 m from lis_009
   Classified 1968, one of the oldest classifications in the city.
3. AIP11065608I  Ficus benjamina ("matapalo"), same garden
   38.72153,-9.13983 | girth 5.00 m | h 20 m | age 123 at 2016 -> ~133 | 619 m from lis_009

WALK B — Estrela / Campo de Ourique (already holds lis_005, lis_011, lis_012)
4. AIP11065946I  Taxodium, Jardim Teofilo Braga (Jardim da Parada)
   38.71810,-9.16530 | girth 6.60 m | h 26 m | age NULL in register | 597 m from lis_012
   SPECIES CONFLICT: ICNF says Taxodium mucronatum, Wikipedia PT + Junta say Taxodium distichum.
5. AIP11065947I + AIP11065948I  Metrosideros excelsa twins, same garden, ~10 m apart
   38.71779,-9.16539 (girth 4.55, h 18.7) and 38.71787,-9.16541 (girth 4.90, h 15).
   FOLD into one entry; record the second processo as a lead.
6. AIP11066601C  Moreton Bay Fig, Largo Hintze Ribeiro (Rato/Amoreiras)
   38.71869,-9.15517 | girth 4.00 m | h 20.5 m | age 100 at 2016 -> ~110 | 581 m from lis_012
   NOTE tipo = "Conjunto arboreo" despite naming one fig. Check whether it is one tree.

WALK C — Santos (new, 1.0 km from lis_005; Jardim 9 de Abril, verified public in
data/research/lisbon-extra-santos.md)
7. KNJ1/400  Tipuana tipu   38.70460,-9.16260 | girth 3.20 | h 22.2 | age 133 at 2015 -> ~144
8. KNJ1/401  Brachychiton   38.70450,-9.16250 | girth 3.30 | h 16   | age 133 at 2015 -> ~144
9. KNJ1/402  Phoenix dactylifera 38.70450,-9.16270 | girth 1.62 | h 26.7 | age 133 at 2015 -> ~144
   All three classified by Aviso n.15 612/2001. Only two will ship.

## Rejected up front
- KNJ1/279 + KNJ1/280 Celtis australis, "Rua do O Seculo - Quintal do n.79" = a private back yard. BLOCKED.
- AIP11065609C bela-sombra (4) + metrosidero (2), Campo Santana: conjunto of six, not a collectible point.
- KNJ3/008 tamareira (3), Largo Barao de Quintela: conjunto of three palms, no single point.
- All Parque Florestal de Monsanto entries: woodland stands, not points.
- KNJ1/331/332 Quinta Nova da Conceicao, KNJ1/070 Quinta da Fonte school garden: access to establish, likely closed.

## OUTCOME (pass closed 2026-08-05)

Shipped to data/research/lisbon-extra.json, 7 trees, lis_013..lis_019:
- lis_013 Strangler Fig of Principe Real (AIP11066144I) | approximate | no photo
- lis_014 Yew of Campo Santana (AIP11065607I) | confirmed | no photo
- lis_015 Weeping Fig of Campo Santana (AIP11065608I) | approximate | no photo
- lis_016 Taxodium of the Jardim da Parada (AIP11065946I) | confirmed | photo approved
- lis_017 Pohutukawa of the Jardim da Parada (AIP11065947I + 948I folded) | approximate | photo approved | best_time May/Jun flowers
- lis_018 Tipuana of the Ninth of April Garden (KNJ1/400) | confirmed | no photo
- lis_019 Date Palm of the Ninth of April Garden (KNJ1/402) | confirmed | no photo

DROPPED from the shortlist after checking:
- AIP11066601C Largo Hintze Ribeiro fig: the register calls it a Conjunto arboreo and the square holds
  nine large figs. Not a collectible point. -> blocked.
- KNJ1/401 Brachychiton, Jardim 9 de Abril: register species is only "Brachychiton spp.", so no canonical
  common name can be set without breaking the hard-rule-9 build check. -> lead, worth resolving, it would
  make the Santos walk three trees.

Leads/blocked written to data/leads/lisbon.json: 29 leads, 22 blocked, every blocked entry with a reason.
Photo hunting stopped at 2 approved (max is 3): no openly licensed portrait of the Principe Real figs,
the Campo Santana yew or the Jardim 9 de Abril trees exists on Commons under a usable licence.
