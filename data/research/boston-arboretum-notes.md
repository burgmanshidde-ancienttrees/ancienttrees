# Boston Arboretum verify pass, 2026-11-03

Method: the Arboretum's public plant inventory GIS (ArcGIS FeatureServer Sci_Name_and_Acc_Num, layer 0, 30,448 records, fields incl. IS_SIG_SPEC, IS_CENTENARIAN, DBH_NUM in cm, CHECK_DT, CONDITION, point geometry, queried with outSR=4326) gives a mapped point per accession: used as confirmed pin. Largest DBH in the layer is about 100 cm (no record above), so girth = DBH x pi for these. arboretum.harvard.edu returns 403 to curl; WebFetch works.
Delivered 9 (bos_030 to bos_038); 4 flagged (single source or old check).
More candidates in the same layer if wanted (all Good condition, accession pre-1900, DBH 90 to 100): chestnut oak 16355*B (1876, 42.293746 -71.129816), black oak 16893*A (1882), river birch 1199*N (1877), sugar maple 12565*C (1883, wild-collected), honeylocust 22514*A (1881), Japanese pagoda tree 17250*A (1891), weeping hemlock 1514-2*A (1881, 3.6 m, sig), Konara oak 16823*B (1892, Japan wild), Castor and Maackia 10928*A (1919 Japan wild). Needs a story source each.
Not done: Forest Hills Cemetery and Larz Anderson Park yielded no individually placeable documented tree in searches (no tour PDF or register rows found); Park Lane oaks rejected as residential.
Ages are time since accession, not tree age.
