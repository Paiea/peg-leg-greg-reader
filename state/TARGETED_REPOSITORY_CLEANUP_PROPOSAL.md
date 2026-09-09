# Targeted Repository Cleanup Proposal

Status: **PROPOSAL ONLY. NO DELETIONS AUTHORIZED OR PERFORMED.**

Prepared from current `main` after PR #25 was squash-merged as commit
`a6a8ca8151edcb7fa1baec118c678dac78919f74`.

This document defines a possible later destructive cleanup PR. That later PR requires
explicit human approval and must rerun the repository and asset audits immediately
before deleting anything.

## Hard boundaries

The proposed cleanup must not delete or rewrite:

- manuscript files or manuscript authority;
- Git history;
- unique visual source material;
- `Peg_Leg_Greg_Heavy_Edit.md`;
- either of the two unique, unreferenced chapter-art files without human review;
- contact sheets, batch manifests, rejected candidates, or development material
  without a deliberate curation decision.

## 1. Exact byte-duplicate staging and harvest copies

The image asset manifest identifies **56 SHA-256 groups** containing **69
unreferenced staging or harvest files** whose bytes are preserved in one or more
promoted `visual/chapter_art/` paths. Removing only the staging/harvest paths
listed below would reclaim **43,621,270 bytes (41.60 MiB)** from the
working tree while retaining the listed promoted files.

These are high-confidence candidates for a later deletion PR, subject to a fresh
pre-deletion audit proving:

1. every candidate still has the recorded SHA-256;
2. every promoted path still exists with the same SHA-256;
3. no code, manifest, documentation, or build step references the candidate path;
4. the deletion diff contains only the approved paths.

| Candidate path | Bytes | SHA-256 | Preserved promoted copy or copies |
|---|---:|---|---|
| `harvested_photos/Ch100_Lyssa-Table-Convo.png` | 551662 | `e9a6398994866ae32afc921e19d52d21ebd429d48f2f5914873210618fab23bf` | `visual/chapter_art/100/Ch100_Lyssa-Table-Convo.png` |
| `visual/production/standalone/Ch100_Lyssa-Table-Convo.png` | 551662 | `e9a6398994866ae32afc921e19d52d21ebd429d48f2f5914873210618fab23bf` | `visual/chapter_art/100/Ch100_Lyssa-Table-Convo.png` |
| `harvested_photos/Ch101_Rainy-Alley-Walk.png` | 2510183 | `f96834d57fa6bdf1acee18ad228b46ef1d30704b339e3c657c9076925d332cfd` | `visual/chapter_art/101/Ch101_Rainy-Alley-Walk.png` |
| `visual/production/standalone/Ch101_Rainy-Alley-Walk.png` | 2510183 | `f96834d57fa6bdf1acee18ad228b46ef1d30704b339e3c657c9076925d332cfd` | `visual/chapter_art/101/Ch101_Rainy-Alley-Walk.png` |
| `harvested_photos/Ch102_Training-Duel.png` | 893101 | `0422e44a159482e04d08cf8007665d2c1c952b4c146e72c9f6f080799f7c74c8` | `visual/chapter_art/102/Ch102_Training-Duel.png` |
| `visual/production/standalone/Ch102_Training-Duel.png` | 893101 | `0422e44a159482e04d08cf8007665d2c1c952b4c146e72c9f6f080799f7c74c8` | `visual/chapter_art/102/Ch102_Training-Duel.png` |
| `harvested_photos/Ch104_Valley-Overlook-Reflection.png` | 3137375 | `87e428cd1d87c302baa7420eadcca9c0e1250c8fd297f08003999f8a3f081670` | `visual/chapter_art/104/Ch104_Valley-Overlook-Reflection.png` |
| `visual/production/standalone/Ch104_Valley-Overlook-Reflection.png` | 3137375 | `87e428cd1d87c302baa7420eadcca9c0e1250c8fd297f08003999f8a3f081670` | `visual/chapter_art/104/Ch104_Valley-Overlook-Reflection.png` |
| `harvested_photos/Ch105_Campfire-Companions.png` | 2632260 | `49b956231f889a9143829d72fbe9a39f76debd5efec4b9e994dda09c3124864e` | `visual/chapter_art/105/Ch105_Campfire-Companions.png` |
| `visual/production/standalone/Ch105_Campfire-Companions.png` | 2632260 | `49b956231f889a9143829d72fbe9a39f76debd5efec4b9e994dda09c3124864e` | `visual/chapter_art/105/Ch105_Campfire-Companions.png` |
| `harvested_photos/Ch95_Harbor-Lighthouse-Watch.png` | 2888046 | `b2a5eda454dbdfdac71f72dfcff134f363d831c951fc7b86668fdc8d0b563b62` | `visual/chapter_art/095/Ch95_Harbor-Lighthouse-Watch.png` |
| `visual/production/standalone/Ch95_Harbor-Lighthouse-Watch.png` | 2888046 | `b2a5eda454dbdfdac71f72dfcff134f363d831c951fc7b86668fdc8d0b563b62` | `visual/chapter_art/095/Ch95_Harbor-Lighthouse-Watch.png` |
| `harvested_photos/Ch99_Scholar-at-the-Worktable.png` | 2931618 | `fc654b8b5f95d3253aece4c33e7255ac07d2fc9643a4654a7cf3fd073ec44023` | `visual/chapter_art/099/Ch99_Scholar-at-the-Worktable.png` |
| `visual/production/standalone/Ch99_Scholar-at-the-Worktable.png` | 2931618 | `fc654b8b5f95d3253aece4c33e7255ac07d2fc9643a4654a7cf3fd073ec44023` | `visual/chapter_art/099/Ch99_Scholar-at-the-Worktable.png` |
| `visual/production/standalone/svgPLG_Ch45_Turnip.png` | 261042 | `a3de31a1eb27cf255f0bc0806e705434b9ab413df765523b5c90b28efa7b0b64` | `visual/chapter_art/045/svgPLG_Ch45_Turnip.png` |
| `visual/production/standalone/svgPLG_Ch46_Move-the-Cobblers-Table.png` | 298947 | `6e7fbaf161df7c60421145e14d7d14ff2a19661c0b6fdda2f5dba76672c7a605` | `visual/chapter_art/046/svgPLG_Ch46_Move-the-Cobblers-Table.png` |
| `visual/production/standalone/svgPLG_Ch47_Marker-at-the-Ford.png` | 267939 | `ace22550ad60d3184630cdbfcf929759a478f104a073803d4644644974317635` | `visual/chapter_art/047/svgPLG_Ch47_Marker-at-the-Ford.png` |
| `visual/production/standalone/svgPLG_Ch48_HR_Stove-at-the-Turn.png` | 3986857 | `ad81a06aa05d153405fe1a92ec3fb14c05556fbbe4e1627ebdf5c416228a800a` | `visual/chapter_art/048/svgPLG_Ch48_HR_Stove-at-the-Turn.png` |
| `visual/production/standalone/svgPLG_Ch49_Vessas-Vibration-Frame.png` | 263719 | `1078360442c3a4d4a031d5ba0770f8da5108681bab2cf44c580e669ed5218a42` | `visual/chapter_art/049/svgPLG_Ch49_Vessas-Vibration-Frame.png` |
| `visual/production/standalone/svgPLG_Ch50_The-Small-Click.png` | 178178 | `23c250c2d24dad73ed18b74c4bb59a0a4fd3e939951d8f1f1b663c6c191ba6b3` | `visual/chapter_art/050/svgPLG_Ch50_The-Small-Click.png` |
| `visual/production/standalone/svgPLG_Ch52_Report-Work.png` | 174543 | `e88381362a78851eb7a70ef76fa48f3e29425487178e538f0e2d8e38d3e2a937` | `visual/chapter_art/052/svgPLG_Ch52_Report-Work.png` |
| `visual/production/standalone/svgPLG_Ch53_The-Bath.png` | 225014 | `3bcdedb7a959c1bda9ce409eedf69bfd00685f47e85dcd7b91f2745558329ad2` | `visual/chapter_art/053/svgPLG_Ch53_The-Bath.png` |
| `visual/production/standalone/svgPLG_Ch54_Horse-Watches-Back.png` | 162666 | `f3bd425cd5a0f615636aff2fceb47971d58deb7c130fd00699e133f2a1510186` | `visual/chapter_art/054/svgPLG_Ch54_Horse-Watches-Back.png` |
| `visual/production/standalone/svgPLG_Ch56_East-Lamp-Works.png` | 258584 | `81eabc9eccf44d15b25fa8db100be7fb0920edfee74454238ea45cdcb6d2a058` | `visual/chapter_art/056/svgPLG_Ch56_East-Lamp-Works.png` |
| `visual/production/standalone/svgPLG_Ch57_North-Freight-Arch.png` | 265858 | `3bff43ae5b7b3f0c395363de93ad63e89424c4a746517c395b6e0eea735632c9` | `visual/chapter_art/057/svgPLG_Ch57_North-Freight-Arch.png` |
| `visual/production/standalone/svgPLG_Ch59_Another-Week.png` | 221556 | `9984fb5140b664f07a65c92313a81ce6ea0fe45c2a7180b0b3596f02c0301946` | `visual/chapter_art/059/svgPLG_Ch59_Another-Week.png` |
| `visual/production/standalone/svgPLG_Ch65_Ward-Morning.png` | 208478 | `cca4ec1974e850b76f1cf692873da15dda82ec3e8d9f30139e8cd50eb6cda7d9` | `visual/chapter_art/065/svgPLG_Ch65_Ward-Morning.png` |
| `visual/production/standalone/svgPLG_Ch68_First-Crutch-Work.png` | 189129 | `859d2abecb0df0108c74e90f39d7ba51e66ac9c54fa34ccba086aa1abd168b3e` | `visual/chapter_art/068/svgPLG_Ch68_First-Crutch-Work.png` |
| `visual/production/standalone/svgPLG_Ch75_First-Fourteen-Steps.png` | 171381 | `4c0f95de7ce065c0b16a8920afaa553b61c816f2723e20071b8453426d2bab79` | `visual/chapter_art/075/svgPLG_Ch75_First-Fourteen-Steps.png` |
| `visual/production/standalone/svgPLG_Ch77_Holls-Sorting-Test.png` | 143432 | `c78d9ff8a1113d0312b49463d8f1db7b71412c34c88d530eea3ce1c88aca8a1b` | `visual/chapter_art/077/svgPLG_Ch77_Holls-Sorting-Test.png` |
| `visual/production/standalone/svgPLG_Ch79_Watching-the-Yard.png` | 183960 | `17b8e52127f6b862e9a026b351dd642e0b7769e493b9f936e63ea75cc3ea2f39` | `visual/chapter_art/079/svgPLG_Ch79_Watching-the-Yard.png` |
| `visual/production/standalone/svgPLG_Ch80_Green-Door-Laughter.png` | 170148 | `5f089386efb415bc1db4925a79cba903b572905fb8ff5b0cf8c8a33ef33d32dd` | `visual/chapter_art/080/svgPLG_Ch80_Green-Door-Laughter.png` |
| `visual/production/standalone/svgPLG_Ch82_Bounded-Invoice-Work.png` | 184993 | `601ee69209d15ec984c0c7a3b300ff04b50ed65f75f960fc2c948040c17f53c9` | `visual/chapter_art/082/svgPLG_Ch82_Bounded-Invoice-Work.png` |
| `visual/production/standalone/Ch83_Date-Kiss.png` | 123075 | `f8ed087d45dd9db3de135a37c8e0170728ba6078db59b6d2e83cd5c303965b81` | `visual/chapter_art/083/Ch83_Date-Kiss.png` |
| `visual/production/standalone/Ch83_Mirror-Before-the-Date.png` | 131423 | `c6c16785c3de70469f09c9699f3868dcbdec0605979bfe113b1e4ee115888f92` | `visual/chapter_art/083/Ch83_Mirror-Before-the-Date.png` |
| `visual/production/standalone/Ch83_Night-Market-on-Crutches.png` | 138655 | `d87eaa647c2a79c522143e697569cf0f36a13db3d99383d587de7f9b85531449` | `visual/chapter_art/083/Ch83_Night-Market-on-Crutches.png` |
| `visual/production/standalone/Ch83_Night-Market-with-Lyssa.png` | 133334 | `ec6907319551f9bc1c3cbba7265446db25dab8c7916f8a28cf6aac6c355716b9` | `visual/chapter_art/083/Ch83_Night-Market-with-Lyssa.png` |
| `visual/production/standalone/Ch84_North-Road-Wagon.png` | 131552 | `f8780b4310990f4392947fcb3ffd4881ff8b3679846e8151f27060b1e0bcad7f` | `visual/chapter_art/084/Ch84_North-Road-Wagon.png` |
| `visual/production/standalone/Ch84_Road-Beyond-Carrow.png` | 135535 | `2e7e80a20594802c4bcfc2dfe447b89791e05b7d9cb6e107e9d1367409e16060` | `visual/chapter_art/084/Ch84_Road-Beyond-Carrow.png` |
| `visual/production/standalone/Ch84_Roadside-Rest-with-Horse.png` | 136066 | `d0ba1d0661c1481b3d78cdea0a05e350446d3da476a9cd35dfdcb834a283cf6c` | `visual/chapter_art/084/Ch84_Roadside-Rest-with-Horse.png` |
| `visual/production/standalone/Ch85_Arbiter-Calculations.png` | 133652 | `40de6781c2246f6699be3825bda5093089d16415e58fd595d6b09982913cb87a` | `visual/chapter_art/085/Ch85_Arbiter-Calculations.png`<br>`visual/chapter_art/091/Ch91_Notes-After-Channel-Test.png`<br>`visual/chapter_art/094/Ch94_Subject-at-the-Table.png`<br>`visual/chapter_art/097/Ch97_Variable-Notes.png` |
| `visual/production/standalone/Ch91_Notes-After-Channel-Test.png` | 133652 | `40de6781c2246f6699be3825bda5093089d16415e58fd595d6b09982913cb87a` | `visual/chapter_art/085/Ch85_Arbiter-Calculations.png`<br>`visual/chapter_art/091/Ch91_Notes-After-Channel-Test.png`<br>`visual/chapter_art/094/Ch94_Subject-at-the-Table.png`<br>`visual/chapter_art/097/Ch97_Variable-Notes.png` |
| `visual/production/standalone/Ch94_Subject-at-the-Table.png` | 133652 | `40de6781c2246f6699be3825bda5093089d16415e58fd595d6b09982913cb87a` | `visual/chapter_art/085/Ch85_Arbiter-Calculations.png`<br>`visual/chapter_art/091/Ch91_Notes-After-Channel-Test.png`<br>`visual/chapter_art/094/Ch94_Subject-at-the-Table.png`<br>`visual/chapter_art/097/Ch97_Variable-Notes.png` |
| `visual/production/standalone/Ch97_Variable-Notes.png` | 133652 | `40de6781c2246f6699be3825bda5093089d16415e58fd595d6b09982913cb87a` | `visual/chapter_art/085/Ch85_Arbiter-Calculations.png`<br>`visual/chapter_art/091/Ch91_Notes-After-Channel-Test.png`<br>`visual/chapter_art/094/Ch94_Subject-at-the-Table.png`<br>`visual/chapter_art/097/Ch97_Variable-Notes.png` |
| `visual/production/standalone/Ch85_Holls-Working-Sheets.png` | 138034 | `e86e1fd71b610f76338a3b677439389bfbf9d284f19547bea167fb71f8935756` | `visual/chapter_art/085/Ch85_Holls-Working-Sheets.png` |
| `visual/production/standalone/Ch85_Testing-Pieces-and-Marks.png` | 124044 | `5e7c7ef1adbf1540b6ec7a9d4a769767b4302844e135f2968439189882301f21` | `visual/chapter_art/085/Ch85_Testing-Pieces-and-Marks.png`<br>`visual/chapter_art/089/Ch89_Guild-Ledger.png` |
| `visual/production/standalone/Ch89_Guild-Ledger.png` | 124044 | `5e7c7ef1adbf1540b6ec7a9d4a769767b4302844e135f2968439189882301f21` | `visual/chapter_art/085/Ch85_Testing-Pieces-and-Marks.png`<br>`visual/chapter_art/089/Ch89_Guild-Ledger.png` |
| `visual/production/standalone/Ch86_Guild-Side-Court.png` | 133435 | `8673fc7dc39da85ace250e3c927574c55af9db7d5a5082f2b5b7cb9e56af2620` | `visual/chapter_art/086/Ch86_Guild-Side-Court.png` |
| `visual/production/standalone/Ch86_Walking-with-Nowhere-to-Be.png` | 134471 | `ea7f9a357851c5552f895fb0ba6189f12bbd27a0af8d1f2d67fbf566a93cb9be` | `visual/chapter_art/086/Ch86_Walking-with-Nowhere-to-Be.png` |
| `visual/production/standalone/Ch87_Four-Doors-Table.png` | 131081 | `b2d2a70a6761824baa402359f68ee2537ff391254aab9e4f98b59c3cbcc7fb85` | `visual/chapter_art/087/Ch87_Four-Doors-Table.png` |
| `visual/production/standalone/Ch88_Fourteen-Stairs.png` | 133811 | `a2907036b2269fcdeacc084f272bd54cfc0e3de2e61c722927789bb5d8c4cf0f` | `visual/chapter_art/088/Ch88_Fourteen-Stairs.png` |
| `visual/production/standalone/Ch88_Fried-Dough-Upstairs.png` | 126588 | `7950946edf307e7c932ad62297a0531b6c7e78deb121411bd15a2ae7f172df41` | `visual/chapter_art/088/Ch88_Fried-Dough-Upstairs.png` |
| `visual/production/standalone/Ch88_Lyssa-in-Gregs-Room.png` | 124113 | `dd46f35a8b51a65645b61ec8cd908e0e5e83162ea7cb75163206dfaa143f8a0e` | `visual/chapter_art/088/Ch88_Lyssa-in-Gregs-Room.png` |
| `visual/production/standalone/Ch88_Room-Still-Mine.png` | 127426 | `01f6801bb5edf961ad4946ee4785ec0422e7b29fcb2142d11191cbf1aaacb9c1` | `visual/chapter_art/088/Ch88_Room-Still-Mine.png` |
| `visual/production/standalone/Ch89_Substitute-at-the-Guild-Desk.png` | 135440 | `fe43dec3c7e5891fe20cea00944703ed13ffc6cf4f90cc1f81d174ad274e3702` | `visual/chapter_art/089/Ch89_Substitute-at-the-Guild-Desk.png` |
| `visual/production/standalone/Ch90_Chair-Delivery-Stairs.png` | 125138 | `c0de81a0b3a0f7d098ad7429a88695e9ea50701d27ba5d39c7b7e0409e259520` | `visual/chapter_art/090/Ch90_Chair-Delivery-Stairs.png` |
| `visual/production/standalone/Ch90_Chair-by-the-Window.png` | 126463 | `a7b80427183102bb113e0e91a126f181fe7b9e5ea335ca2f1fcd46da84575360` | `visual/chapter_art/090/Ch90_Chair-by-the-Window.png` |
| `visual/production/standalone/Ch90_Furniture-Shop-Bargain.png` | 128540 | `a696b97c26c95742d84e1bc55d0a989c236e78d16ebbb686b86c171885382a90` | `visual/chapter_art/090/Ch90_Furniture-Shop-Bargain.png` |
| `visual/production/standalone/Ch91_Hessas-Test-Table.png` | 128991 | `21691408a004c358ad262444d4688623605245c2e7b1443e57689895602fac00` | `visual/chapter_art/091/Ch91_Hessas-Test-Table.png`<br>`visual/chapter_art/094/Ch94_Copper-Strip-Assessment.png`<br>`visual/chapter_art/097/Ch97_Second-Mana-Draw.png` |
| `visual/production/standalone/Ch94_Copper-Strip-Assessment.png` | 128991 | `21691408a004c358ad262444d4688623605245c2e7b1443e57689895602fac00` | `visual/chapter_art/091/Ch91_Hessas-Test-Table.png`<br>`visual/chapter_art/094/Ch94_Copper-Strip-Assessment.png`<br>`visual/chapter_art/097/Ch97_Second-Mana-Draw.png` |
| `visual/production/standalone/Ch97_Second-Mana-Draw.png` | 128991 | `21691408a004c358ad262444d4688623605245c2e7b1443e57689895602fac00` | `visual/chapter_art/091/Ch91_Hessas-Test-Table.png`<br>`visual/chapter_art/094/Ch94_Copper-Strip-Assessment.png`<br>`visual/chapter_art/097/Ch97_Second-Mana-Draw.png` |
| `visual/production/standalone/Ch92_Pessa-and-the-Question.png` | 132144 | `7cb807d089a79fd25fb1585a8d12d18ba300db2321b3d3356cd4e6b1c0443161` | `visual/chapter_art/092/Ch92_Pessa-and-the-Question.png` |
| `visual/production/standalone/Ch93_Shield-Balance-Test.png` | 132492 | `db72efec47593a605bcfb882416c2a0802766a1ee755867d5813698de42eae81` | `visual/chapter_art/093/Ch93_Shield-Balance-Test.png` |
| `visual/production/standalone/Ch95_Pepper-Stall-with-Jorren.png` | 136489 | `a32874ea3e0ed8a786635708db412d6c95cb536c23dabc0e919e970c87c9afc9` | `visual/chapter_art/095/Ch95_Pepper-Stall-with-Jorren.png` |
| `visual/production/standalone/Ch95_Sitting-by-the-Water.png` | 137361 | `0f9d3e4eebc42b97597290cb464bfd32eb5cc7d68d5eb009dd830e614661e5e0` | `visual/chapter_art/095/Ch95_Sitting-by-the-Water.png` |
| `visual/production/standalone/Ch96_Holls-Testing-Room.png` | 132607 | `2acca5550422bd244370a8860797d7d3ea74c9ee63b1267e6ef371bae1cc96da` | `visual/chapter_art/096/Ch96_Holls-Testing-Room.png` |
| `visual/production/standalone/Ch96_Sample-Pieces.png` | 132571 | `e086afa9cc969c3ac3ff2d9df6bd4c969e56ce57b5b2c2ce87fa02a4428caa95` | `visual/chapter_art/096/Ch96_Sample-Pieces.png` |
| `visual/production/standalone/Ch96_Watching-the-Testers.png` | 127834 | `9574593a5d730f673ee119f20de1be5e1c45d9425b81e59e23acb4e9462fb7a6` | `visual/chapter_art/096/Ch96_Watching-the-Testers.png` |
| `visual/production/standalone/Ch97_After-the-Variable.png` | 121009 | `b8e60eef487af8169be58490e4a44af0b1a8b302942df0c38507c7901dbfc846` | `visual/chapter_art/097/Ch97_After-the-Variable.png` |

Important: identical art promoted under several chapter filenames is a separate
editorial/art question. This proposal removes no promoted copy and does not decide
whether cross-chapter reuse is desirable.

## 2. Two unreferenced files under `visual/chapter_art`

These files are not reader-referenced, but neither is an exact duplicate of another
audited image. They are therefore **human-review items**, not safe deletion
candidates.

| Chapter | Path | Dimensions | Bytes | SHA-256 | Finding |
|---:|---|---:|---:|---|---|
| 10 | `visual/chapter_art/010/v28_c10_s01_dead-mans-hand.png` | 368×214 | 186136 | `01343b55f1bf6cf6960d8aa4e664155fc69e2551a288910944169815d05810e7` | Unique hash; unreferenced; low-resolution flag |
| 24 | `visual/chapter_art/024/v28_c24_s01_boat-on-the-wagon.png` | 302×335 | 220663 | `544224c789b0631e6714d98a872e4b2dc68ff5997f963139323ab59a6499e260` | Unique hash; unreferenced; low-resolution flag |

Review must determine whether each is a rejected composition, a temporarily
unsurfaced promoted asset, or unique source art worth preserving. Low resolution
alone is not deletion evidence.

## 3. Obsolete generated manifests and proven replacements

### High-confidence duplicate candidate

- `state/manuscript_manifest_v65_historical.json` and
  `state/manuscript_manifest_v65.json` are byte-identical:
  SHA-256
  `1699e255539f2111c285c52aa6464520c002d0e8c8a3e477cb71e950d013f08d`,
  7,669 bytes each.
- A later cleanup may remove one copy only after authority documentation confirms
  which path is canonical and all references are rechecked.
- Until that confirmation, both remain in place.

### Current comprehensive generated replacements

- `publishing/image_asset_manifest.json` is the current machine-readable image
  inventory and records path, dimensions, format, size, references, duplicate
  group, SHA-256, technical flags, and recommended action.
- `publishing/chapter_art_coverage.json` is the current chapter coverage and
  broken-reference report.
- `publishing/repository_inventory.json` is the current repository-wide file and
  manuscript-range inventory.
- All three are reproducibly generated by `scripts/audit_repository_assets.py`.

### Not yet proven obsolete

The following are unreferenced by active code according to the repository inventory,
but they may preserve visual-production provenance, prompt/batch associations,
curation decisions, or historical reconciliation evidence. They must not be deleted
merely because the comprehensive manifests now exist:

- `publishing/art_curation_ch30_44.json`
- `publishing/art_reconciliation_v45.json`
- `publishing/image_batch_ch007_137_002.json`
- `publishing/image_batch_ch063_155_fast_coverage_006.json`
- `publishing/image_batch_ch120_152_fast_coverage_005.json`
- `publishing/image_batch_ch138_147_fast_coverage_004.json`
- `publishing/image_batch_ch98_121_001.json`
- `publishing/image_batch_fast_coverage_003_a.json`
- `publishing/image_batch_fast_coverage_003_b.json`
- `publishing/image_batch_fast_coverage_003_c.json`
- `publishing/manuscript_manifest_v45.json`
- `publishing/reconciliation_v31_to_v45.json`
- `publishing/title_schema_watch.json`
- range-stamped `state/QA_*.json`, `state/RECONCILIATION_*.json`, and
  `state/manuscript_manifest_ch*.json`

For each candidate, a reviewer must compare its fields against the proposed
replacement and identify any information not reproducible from current authority
and Git history. If unique provenance exists, retain or deliberately migrate only
that information. “Unreferenced” is not sufficient proof.

## 4. Development and contact-sheet material requiring human review

The audit found 13 contact sheets totaling **43,971,391 bytes (41.93
MiB)**. They are not reader assets. They may still carry useful curation context,
including rejected alternatives that are not recoverable from promoted art alone.

| Path | Bytes | SHA-256 | Required action |
|---|---:|---|---|
| `visual/development/contact_sheets/Ch007-119_Fast-Coverage-003_C.png` | 3379091 | `f336338f735e1164644b9017ca8aaf35d1e6127e28a05885ad08b1f478c91cde` | Human review before any deletion |
| `visual/development/contact_sheets/Ch007-137_Coverage-Batch-002_A.png` | 3397902 | `e4b3b8a106b4304a58891ce0566379f9e54885dd0d16a7c221369bdb43170e5f` | Human review before any deletion |
| `visual/development/contact_sheets/Ch007-137_Coverage-Batch-002_B.png` | 3344451 | `e68308252827634075c1c7baac7b18f6a521ecea6ce825d3d973f5d388459625` | Human review before any deletion |
| `visual/development/contact_sheets/Ch007-137_Coverage-Batch-002_C.png` | 3319148 | `b2b9d97cd6eae73c9433dd6b8e37ec55015ccfed8d0e7eae85d9120f5dcc563b` | Human review before any deletion |
| `visual/development/contact_sheets/Ch022-081_Fast-Coverage-003_A.png` | 3405186 | `237c0efe06bd13592144b195ce385762d439ef4211eeaa826a986afe78c59ed7` | Human review before any deletion |
| `visual/development/contact_sheets/Ch039-082_Fast-Coverage-003_B.png` | 3406408 | `802ed3e60892a8413e5e224033d89274630954d6b9095122fabeaf6ffa5cd0e8` | Human review before any deletion |
| `visual/development/contact_sheets/Ch063-155_Fast-Coverage-006.png` | 3183031 | `ddefd715a2e164b29f5b730eaf1df7c29b5a9149549abca110d6403368697a62` | Human review before any deletion |
| `visual/development/contact_sheets/Ch120-152_Fast-Coverage-005.png` | 3332270 | `7cb451bcf297d6a73978f45e06d8cbf73e069cc754b0461f10a3044f76fc9dc6` | Human review before any deletion |
| `visual/development/contact_sheets/Ch138-147_Fast-Coverage-004.png` | 3344185 | `d84f08fbaf8b0b3a8b2bbab74950ba49f005abc416886bda2f1a0660d7c50a07` | Human review before any deletion |
| `visual/development/contact_sheets/Ch98-121_Batch-001.jpg` | 1169405 | `1c68f21375f67adc3ff8535dec60b13428f85b6d65ec8ce9d5c920a0ffe3255a` | Human review before any deletion |
| `visual/development/contact_sheets/batch_001_4panel.png` | 4271144 | `fe7ffb43b9a78fe0ff583f45145a6d94a199296fca96cc8bfdabbfc08d691ea1` | Human review before any deletion |
| `visual/development/contact_sheets/batch_002_15panel.png` | 4228693 | `616589d07ab0b09717cd0c2b0a9b588c612d1ed5e4ba988b9e83750a933bd543` | Human review before any deletion |
| `visual/development/contact_sheets/batch_003_15panel.png` | 4190477 | `49adbfb26c895d477217780efc448144ab8febc6e1edb45842a18ccae998fb8c` | Human review before any deletion |

Review these alongside their matching `publishing/image_batch_*.json` files.
Possible outcomes are:

- keep a contact sheet because it records meaningful source/candidate provenance;
- archive a deliberately selected subset outside the deployed reader path;
- remove it in the later approved cleanup because promoted source assets and useful
  metadata are already preserved;
- mark unknown where the pairing cannot be reconstructed.

No wholesale deletion of `visual/development/` or `visual/production/` is
proposed.

## 5. Non-destructive responsive-image derivative pipeline

### Design

Keep every accepted source image unchanged. Generate disposable web derivatives
into a clearly generated path such as:

`generated/responsive/<source-relative-path>/<width>.webp`

Initial widths should be bounded by the source width and reader layout, for example
480, 800, and 1200 pixels. Do not upscale. Start with WebP; add AVIF only after
browser/output testing proves a useful size benefit.

A small build script should:

1. read `publishing/image_asset_manifest.json`;
2. select only reader-referenced raster images;
3. preserve aspect ratio and embedded orientation;
4. generate deterministic derivatives without touching sources;
5. write a generated derivative manifest containing source SHA-256, output path,
   width, height, bytes, format, and generator version;
6. skip outputs whose recorded source hash and generator version are unchanged;
7. remove no source or stale derivative automatically.

Reader generation should emit:

- intrinsic `width` and `height` to prevent layout shift;
- `srcset` and a layout-specific `sizes` value;
- a safe source fallback;
- `loading="lazy"` and `decoding="async"` for below-fold art;
- eager loading or `fetchpriority="high"` only for a measured above-fold image;
- alt text from current reader metadata, never inferred from filenames at runtime.

### Proposed commands

- `python scripts/build_responsive_images.py --check`
- `python scripts/build_responsive_images.py --write`
- `python scripts/audit_repository_assets.py --check`
- the existing reader checks and test suite

### Rollout gates

1. Implement the generator and tests in a non-destructive PR.
2. Compare visual output and bytes on representative portrait, landscape,
   low-resolution, and high-resolution assets.
3. Confirm GitHub Pages serves the generated formats and paths.
4. Update one small reader sample to consume `srcset`.
5. Measure network bytes and layout shift before broad rollout.
6. Only then decide whether generated derivatives are committed, produced in CI,
   or attached to deployment artifacts.

Low-resolution sources should retain their original presentation ceiling. The
pipeline must never enlarge them merely to fill a responsive width.

## Later destructive PR checklist

A later cleanup PR, opened only after explicit approval, should:

- contain an allow-list of exact paths from this document;
- rerun all audits from the then-current `main`;
- fail if any candidate hash or preserved-copy hash changed;
- delete no directory recursively;
- report exact bytes removed;
- contain no manuscript, source-authority, or Git-history changes;
- leave contact sheets and unique chapter art untouched unless separately approved;
- run manuscript, reader, asset, and build checks;
- remain unmerged for human diff review.

## Recommendation

The first destructive cleanup should be limited to the 69 exact byte-duplicate
staging/harvest files after fresh hash/reference verification. Manifest cleanup and
development-material curation should remain separate review units. The responsive
derivative pipeline belongs in its own non-destructive implementation PR.
