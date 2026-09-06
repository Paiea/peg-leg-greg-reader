#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_exact(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count == 1:
        p.write_text(text.replace(old, new), encoding="utf-8")
        print(f"normalized {path}: {old[:70]!r}")
        return
    if count == 0 and new in text:
        print(f"already normalized {path}: {new[:70]!r}")
        return
    raise SystemExit(f"DRIFT: {path}: expected exactly one old phrase, found {count}: {old!r}")


# Ch10: turn the 5s -> 10s contradiction into explicit financing damage.
old_10 = (
    "The gauge was still mine once I produced ten silver, which was simultaneously an absurd bargain and ten silver I did not currently possess. "
    "Antonius had reduced the price from the original forty-gold revelation to something that remained painful enough to teach me not to tell a lender how valuable his trash was. "
    "He claimed this was generosity. I claimed he was a bastard. We were both correct."
)
new_10 = (
    "The gauge was still mine once the account attached to it reached ten silver, which was simultaneously an absurd bargain and a brutal lesson in short-term financing. "
    "We had negotiated five silver for the gauge itself. Vale's interest had done the rest. Antonius claimed this was educational. "
    "I claimed he was a bastard. We were both correct."
)
for path in ["chapters/010.html", "light/010.html"]:
    replace_exact(path, old_10, new_10)

# Ch471: trusted commercial witness work belongs in low silver.
p = "state/manuscript/Peg_Leg_Greg_Chapter_471_EXACT_WIP.md"
replace_exact(p, "**TRANSFER SEAL WITNESS / EAST LANDING / 5C / HALF DAY / ONE DISTRICT FIELD REFERENCE / NO APPRAISAL AUTHORITY**", "**TRANSFER SEAL WITNESS / EAST LANDING / 2S / HALF DAY / ONE DISTRICT FIELD REFERENCE / NO APPRAISAL AUTHORITY**")
replace_exact(p, "Five copper.\n\nHalf day.\n\nMore important:", "Two silver.\n\nHalf day.\n\nMore important:")
replace_exact(p, "Five copper.\n\nTen to fifteen.\n\nStill below thirty.\n\nBut purse was not the important part.", "Two silver.\n\nMy copper purse stayed ten.\n\nThe silver sat beside it as working capital.\n\nBut purse was not the important part.")
replace_exact(p, "Late afternoon, I had fifteen copper again.\n\nFive above floor.\n\nSame place I'd been before returning Lakeward archive.", "Late afternoon, I had ten copper and two silver.\n\nThe old copper floor still existed.\n\nThe new money sat above it in a different tier.")
replace_exact(p, "Transfer seal witness completed, +5c.", "Transfer seal witness completed, +2s.")
replace_exact(p, "Cash 15c.\n\nThirty target unchanged.", "Cash 10c + 2s.\n\nReserve target now needs silver-scale recalibration.")

# Ch472: preserve the point that copper-only thinking is the wrong scale.
p = "state/manuscript/Peg_Leg_Greg_Chapter_472_EXACT_WIP.md"
replace_exact(p, "Yesterday five copper for half a day had felt like proof that I could climb out of the one-copper, two-copper sludge I'd been treating as normal.", "Yesterday two silver for half a day had felt like proof that trusted work could finally move above the one-copper, two-copper sludge I'd been treating as normal.")

# Ch473: gray freight needs a real risk premium and a transaction large enough to support it.
p = "state/manuscript/Peg_Leg_Greg_Chapter_473_EXACT_WIP.md"
replace_exact(p, "The legal way to Cinder Cross cost five copper.\n\nThe illegal way paid six.", "The legal way to Cinder Cross cost five copper.\n\nThe illegal way paid enough silver to make the risk an actual decision.")
replace_exact(p, "Fifteen copper.\n\nTwenty-three with Vale.\n\nTen-copper floor.", "Fifteen copper.\n\nVale still open.\n\nTen-copper floor.")
replace_exact(p, '"One silver for the whole mixed load if he takes it as listed."', '"Forty-eight silver for the whole mixed load if he takes it as listed."')
replace_exact(p, 'Then said, "One copper extra if it clears."\n\nHe said, "Two."\n\n"One."\n\n"Then take your own wagon."\n\nShe looked at me as if this were my fault.\n\nIt was a little.\n\n"One and six bits."\n\nHe considered.\n\n"Fine."', 'Then said, "Two silver extra if it clears."\n\nHe said, "Four."\n\n"Three."\n\n"Then take your own wagon."\n\nShe looked at me as if this were my fault.\n\nIt was a little.\n\n"Four silver."\n\nHe considered.\n\n"Fine."')
replace_exact(p, '"Ride east. Three copper if buyer takes full load."\n\n"No."\n\n"You haven\'t done anything."\n\n"I\'m already improving payroll."\n\nDriver laughed.\n\nShe did not.\n\n"Four."\n\n"Six."\n\n"Absolutely not."\n\n"Your sale is one silver and misses window if you wait legal release. I am not asking percentage because we don\'t have a conversion I trust and I\'m not pretending we do. Six copper plus ride if buyer accepts full load. Two copper plus ride if he rejects route lots but takes remainder because my screening helped preserve sale. Zero if I materially misrepresent what I know."\n\n"Four full. One partial."\n\n"Five full. Two partial."', '"Ride east. Six silver if buyer takes full load."\n\n"No."\n\n"You haven\'t done anything."\n\n"I\'m already improving payroll."\n\nDriver laughed.\n\nShe did not.\n\n"Eight."\n\n"Twelve."\n\n"Absolutely not."\n\n"Your sale is forty-eight silver and misses window if you wait legal release. Twelve silver plus ride if buyer accepts full load. Eight silver plus ride if he rejects the marked route lot but takes the remainder because my screening helps preserve the sale. Zero if I materially misrepresent what I know."\n\n"Ten full. Six partial."\n\n"Twelve full. Eight partial."')
replace_exact(p, 'He said, "Pay him five so we can leave."', 'He said, "Pay him twelve so we can leave."')
replace_exact(p, '"Five," she said. "Ride included."', '"Twelve full. Eight partial," she said. "Ride included."')
replace_exact(p, "Five copper upside.\n\nFree five-copper ride.", "Twelve silver upside if the whole load cleared.\n\nRide included.")
replace_exact(p, "Five copper saved.\n\nFive copper potentially earned.", "Five copper fare avoided.\n\nTwelve silver potentially earned.")
replace_exact(p, '"One silver was for clean paper."', '"Forty-eight silver was for clean paper."')
replace_exact(p, "My contract said two copper if buyer rejected route lots but took remainder because my screening helped preserve sale.\n\nThat was what happened.\n\nTwo copper.\n\nPlus free ride worth five.\n\nNot five cash.\n\nNot nothing.\n\nFreight woman paid two.\n\nFifteen to seventeen.", "My contract said eight silver if buyer rejected the marked route lot but took the remainder because my screening helped preserve the sale.\n\nThat was what happened.\n\nEight silver.\n\nPlus the ride.\n\nNot the full twelve.\n\nNot nothing.\n\nFreight woman paid eight silver.\n\nMy copper purse stayed fifteen.")
replace_exact(p, "One copper floor.\n\nSeventeen to sixteen.\n\nStill six above survival floor after arriving east.", "One copper lodging.\n\nFifteen to fourteen copper.\n\nEight silver stayed eight silver.")
replace_exact(p, "My fee: 2c + transport.\n\nCash: 17 before lodging, 16 after.", "My fee: 8s + transport.\n\nCash: 8s + 14c after lodging.")
replace_exact(p, "Six copper better than legal baseline.\n\nSilver-scale goods beginning to move around me.", "Five copper of fare avoided and eight silver earned on a legally exposed transaction.\n\nThe scale had changed.")

# Ch474: sourcing commission moves to low silver; preserve ordinary copper expenses.
p = "state/manuscript/Peg_Leg_Greg_Chapter_474_EXACT_WIP.md"
replace_exact(p, "I stood at the west gate with sixteen copper, twenty-three still with Vale, one Lakeward specification folded inside notebook, and exactly enough confidence to be irritating.", "I stood at the west gate with fourteen copper, eight silver, Vale still open, one Lakeward specification folded inside notebook, and exactly enough confidence to be irritating.")
replace_exact(p, "Potential five-copper commission if landed terms beat north quote materially.", "Potential two-silver commission if landed terms beat north quote materially.")
replace_exact(p, "CONFIRM WHETHER LANDED TERMS QUALIFY 3C OR 5C INTRODUCTION CONDITION IF FINAL INSPECTION PASSES.", "CONFIRM WHETHER LANDED TERMS QUALIFY 1S OR 2S INTRODUCTION CONDITION IF FINAL INSPECTION PASSES.")
replace_exact(p, "The wagon left.\n\nI had fourteen copper.\n\nFive-copper commission pending, not earned yet.\n\nTwenty-three with Vale.", "The wagon left.\n\nI had twelve copper and eight silver.\n\nTwo-silver commission pending, not earned yet.\n\nVale still open.")

# Ch475: urgent heavy-yard coordination moves to meaningful silver.
p = "state/manuscript/Peg_Leg_Greg_Chapter_475_EXACT_WIP.md"
replace_exact(p, "I had fourteen copper.\n\nTwenty-three still with Vale.\n\nFive copper possibly traveling toward me from Lakeward if six bundles of reed glass survived a road, an inspection, and at least one person with authority finding a reason to be difficult.", "I had twelve copper and eight silver.\n\nVale still open.\n\nTwo silver possibly traveling toward me from Lakeward if six bundles of reed glass survived a road, an inspection, and at least one person with authority finding a reason to be difficult.")
replace_exact(p, 'Buyer said, "Two copper."', 'Buyer said, "Three silver."')
replace_exact(p, '"Three copper."\n\n"Two."\n\n"If the long frame clears west bay before second bell and nothing gets put in the wrong place, four."', '"Five silver."\n\n"Three."\n\n"If the long frame clears west bay before second bell and nothing gets put in the wrong place, five."')
replace_exact(p, '"Three if everything clears."\n\n"Four if frame clears west bay and receiving record closes before second bell. Two if we finish later but clean."', '"Four if everything clears."\n\n"Five if frame clears west bay and receiving record closes before second bell. Three if we finish later but clean."')
replace_exact(p, '"Four," buyer said. "No injuries."', '"Five," buyer said. "No injuries."')
replace_exact(p, "Buyer gave me four copper.\n\nFourteen to eighteen.\n\nI counted because transaction required counting, not because eighteen copper had become a spiritual condition.", "Buyer counted five silver into my hand.\n\nI still had twelve copper. Silver moved from eight to thirteen.\n\nI counted because transaction required counting, not because thirteen silver had become a spiritual condition.")
replace_exact(p, '"Then why did I pay you four?"', '"Then why did I pay you five silver?"')
replace_exact(p, "Not because eighteen was a bigger emotion.\n\nBecause it had stopped being the only number that mattered.", "Not because thirteen silver was a bigger emotion.\n\nBecause the purse had stopped being the only number that mattered.")

# Ch476: artifact auction scales with Greg's new silver liquidity so the loss remains real.
p = "state/manuscript/Peg_Leg_Greg_Chapter_476_EXACT_WIP.md"
replace_exact(p, "Eighteen copper was enough to buy something stupid.", "Thirteen silver was enough to buy something stupid.")
replace_exact(p, "I had eighteen copper in my purse, twenty-three still sitting with Vale, a five-copper reed-glass commission somewhere west of me in the dangerous metaphysical state called probably, and one Tool House reference proving I could tell people not to stand under eleven hundred units of iron.", "I had twelve copper and thirteen silver in my purse, Vale still open, a two-silver reed-glass commission somewhere west of me in the dangerous metaphysical state called probably, and one Tool House reference proving I could tell people not to stand under eleven hundred units of iron.")
replace_exact(p, "**OPEN 4C**", "**OPEN 4S**")
replace_exact(p, "Four copper opening.\n\nI could afford four.\n\nI could afford eight without crossing ten-copper floor.\n\nEight was not one silver.\n\nEight was also not nothing.", "Four silver opening.\n\nI could afford four.\n\nI could afford eight without crossing my five-silver operating floor.\n\nEight silver was not gold.\n\nEight silver was also not nothing.")
replace_exact(p, "Tag opened at one silver.", "Tag opened at one gold.")
replace_exact(p, "Eighteen copper.\n\nTen floor.\n\nFive pending.\n\nTwenty-three Vale.\n\nWork-limb deposit already sunk.\n\nStillhook opening four.", "Thirteen silver plus ordinary copper.\n\nFive-silver operating floor.\n\nTwo silver pending.\n\nVale still open.\n\nWork-limb deposit already sunk.\n\nStillhook opening four silver.")
replace_exact(p, '"Road survey stillhook. Two live plates. One failed. No current body certification. Demonstrated only to posted test. Opening four copper."', '"Road survey stillhook. Two live plates. One failed. No current body certification. Demonstrated only to posted test. Opening four silver."')
replace_exact(p, "At six, two people wanted current visible utility.", "At six silver, two people wanted current visible utility.")
replace_exact(p, "Eight.\n\nNot because eight was value.\n\nBecause eight was maximum I could deploy without crossing floor", "Eight silver.\n\nNot because eight was value.\n\nBecause eight silver was maximum I could deploy without crossing floor")
replace_exact(p, '"Seven."\n\nThe woman in back looked at me.', '"Seven silver."\n\nThe woman in back looked at me.')
replace_exact(p, '"Seven."\n\nMan from viewing said, "Eight."', '"Seven silver."\n\nMan from viewing said, "Eight silver."')
replace_exact(p, 'The woman in back said, "Nine."', 'The woman in back said, "Nine silver."')
replace_exact(p, 'Man frowned.\n\n"Ten."', 'Man frowned.\n\n"Ten silver."')
replace_exact(p, 'Then: "Eleven."', 'Then: "Eleven silver."')
replace_exact(p, "Eleven.\n\nMore than I could spend while preserving floor.\n\nAlso still below obvious new barrier-plate tier, whatever silver meant relative to copper.", "Eleven silver.\n\nMore than I could spend while preserving floor.\n\nAlso still below the obvious one-gold barrier-plate tier.")
replace_exact(p, "Sold eleven copper.", "Sold eleven silver.")
replace_exact(p, '"Why eleven?"', '"Why eleven silver?"')
replace_exact(p, '"Because two working plates are worth eight to me, hook assembly two, and I can gamble one on ceramic."', '"Because two working plates are worth eight silver to me, hook assembly two, and I can gamble one on ceramic."')
replace_exact(p, '"Stillhook sold eleven."', '"Stillhook sold eleven silver."')
replace_exact(p, '"What did you bid?"\n\n"Seven."', '"What did you bid?"\n\n"Seven silver."')
replace_exact(p, "**Market:** opened 4c, sold 11c. Multiple bidders. Broken does not mean worthless.", "**Market:** opened 4s, sold 11s. Multiple bidders. Broken does not mean worthless.")

# Ch484: real brokerage moves an 8s-scale transaction and pays a 2s commission.
p = "state/manuscript/Peg_Leg_Greg_Chapter_484_EXACT_WIP.md"
replace_exact(p, "**NORTH FREIGHT YARD SEEKS 4 YARD SWAY SHOES / OLD DISTRICT PATTERN ACCEPTABLE / OPEN DISPOSAL OR CLEAN PRIVATE CHAIN REQUIRED / CURRENT LOAD RATING NOT REQUIRED / BENCH FUNCTION MUST PASS / OFFER TO 1S 2C FOR FOUR**", "**NORTH FREIGHT YARD SEEKS 4 YARD SWAY SHOES / OLD DISTRICT PATTERN ACCEPTABLE / OPEN DISPOSAL OR CLEAN PRIVATE CHAIN REQUIRED / CURRENT LOAD RATING NOT REQUIRED / BENCH FUNCTION MUST PASS / OFFER TO 8S FOR FOUR**")
replace_exact(p, "**CROSS STREET SURPLUS / 5 OLD YARD SHOES / DISTRICT MARKS / SELL LOT / 1S 6C / NO SPLIT**", "**CROSS STREET SURPLUS / 5 OLD YARD SHOES / DISTRICT MARKS / SELL LOT / 10S / NO SPLIT**")
replace_exact(p, "And I had fifteen copper.\n\nWhich was not enough to buy seller lot without violating every intelligent thought I had possessed this month.\n\nGood.\n\nNo inventory.", "And I had enough silver to buy the seller lot if I wanted to be stupid.\n\nThat was no longer the same thing as having a reason to own it.\n\nGood.\n\nNo inventory.")
replace_exact(p, '"Four copper if I bring a buyer who completes at at least one silver two copper for the four receipt-matched shoes."', '"Two silver if I bring a buyer who completes at eight silver or more for the four receipt-matched shoes."')
replace_exact(p, '"Four copper?"', '"Two silver?"')
replace_exact(p, '"Three."\n\n"Four."\n\n"Three and one bit for copying."\n\n"Four. You keep fifth."', '"One."\n\n"Two."\n\n"One silver and one bit for copying."\n\n"Two silver. You keep fifth."')
replace_exact(p, '"Four if they pay one silver three," she said.\n\n"Four if they pay one silver two or more."\n\n"Three if one-two. Four if one-three."', '"Two if they pay nine silver," she said.\n\n"Two if they pay eight silver or more."\n\n"One if eight. Two if nine."')
replace_exact(p, '"Fine. Three if completed at one silver two. Four if one silver three or more. You pay records bits if we need them."', '"Fine. Two silver if completed at eight silver or more. You pay records bits if we need them."')
replace_exact(p, "**Greg introduction / transaction assist. Seller pays 3c if four receipt-matched sway shoes sell for at least 1s2c. Seller pays 4c if completed price at least 1s3c. Seller covers agreed public-record copy/inspection bits. No fee if no completed sale. Fifth shoe excluded unless separately agreed.**", "**Greg introduction / transaction assist. Seller pays 2s if four receipt-matched sway shoes sell for at least 8s. Seller covers agreed public-record copy/inspection bits. No fee if no completed sale. Fifth shoe excluded unless separately agreed.**")
replace_exact(p, '"Paid by who?"\n\n"Seller. Three copper if sale completes at one silver two. Four if one silver three or more."', '"Paid by who?"\n\n"Seller. Two silver if sale completes at eight silver or more."')
replace_exact(p, '"Good. Then I want one silver one."\n\n"Your posted offer says to one silver two."', '"Good. Then I want seven silver."\n\n"Your posted offer says to eight silver."')
replace_exact(p, 'Quartermaster said, "Three at nine copper."', 'Quartermaster said, "Three at five silver."')
replace_exact(p, '"Nine each?" she asked.\n\n"Nine total."', '"Five each?" she asked.\n\n"Five total."')
replace_exact(p, '"You\'re not taking four at nine."', '"You\'re not taking four at five silver."')
replace_exact(p, 'She said, "One silver four for all four, fourth delivered functioning before sixth day."\n\nQuartermaster laughed.\n\n"No."\n\n"Your notice says to one-two."\n\n"For four passing now."\n\n"Then one-two with fourth later."', 'She said, "Nine silver for all four, fourth delivered functioning before sixth day."\n\nQuartermaster laughed.\n\n"No."\n\n"Your notice says to eight."\n\n"For four passing now."\n\n"Then eight with fourth later."')
replace_exact(p, '"One silver one. Three now. Fourth after pass. No fourth by sixth day, three copper withheld."', '"Seven silver. Three now. Fourth after pass. One silver held until the fourth passes."')
replace_exact(p, 'Quartermaster said, "One silver for three. Two copper for fourth after pass."\n\nSeller looked.\n\n"One silver one for three. One copper fourth."\n\n"No."\n\n"One silver for three. Two for fourth. You collect fourth only when it passes here."', 'Quartermaster said, "Six silver for three. Two silver for fourth after pass."\n\nSeller looked.\n\n"Seven for three. One for fourth."\n\n"No."\n\n"Six for three. Two for fourth. You collect the fourth only when it passes here."')
replace_exact(p, "That recreated buyer's posted one silver two total.", "That recreated buyer's posted eight-silver total.")
replace_exact(p, "My commission agreement: completed sale reaches one silver two or more.", "My commission agreement: completed sale reaches eight silver or more.")
replace_exact(p, '"I said, \"My fee only if fourth completes and total reaches one silver two.\""', '"I said, \"My fee only if fourth completes and total reaches eight silver.\""')
replace_exact(p, "North Freight Yard bought three now for one silver.\n\nFourth remained seller's.\n\nConditional: buyer would buy fourth for two copper if it passed same bench before sixth-day frame deadline.", "North Freight Yard bought three now for six silver.\n\nFourth remained seller's.\n\nConditional: buyer would buy fourth for two silver if it passed same bench before sixth-day frame deadline.")
replace_exact(p, "Quartermaster paid two copper.\n\nTotal deal: one silver + two copper.\n\nSeller paid me three copper under agreement.\n\nFifteen to eighteen.\n\nThere.\n\nThree copper.\n\nAgain.\n\nBut not a three-copper day job.", "Quartermaster paid two silver.\n\nTotal deal: eight silver.\n\nSeller paid me two silver under agreement.\n\nThere.\n\nTwo silver.\n\nNot a day-labor fee.\n\nA commission.")
replace_exact(p, "Still three copper.\n\nDifferent engine.", "Still bounded.\n\nDifferent engine.")
replace_exact(p, 'Seller counted my coins.\n\n"Three."', 'Seller counted my coins.\n\n"Two silver."')
replace_exact(p, '"You should have taken two."', '"You should have taken one."')
replace_exact(p, "**Final completed price: 1s2c**\n**My fee: 3c**\n**Cash 15 -> 18**", "**Final completed price: 8s**\n**My fee: 2s**\n**Silver +2s; ordinary copper unchanged**")

# Ch485-486: multi-crew organizer work crosses cleanly into tens of silver.
p = "state/manuscript/Peg_Leg_Greg_Chapter_485_EXACT_WIP.md"
replace_exact(p, "I had eighteen copper.\n\nTwenty-three with Vale.\n\nBits unspecified.\n\nTen floor.\n\nEight above it.", "I had a mixed purse now: ordinary copper for daily life and enough silver that tiny jobs no longer defined the whole problem.\n\nVale still open.\n\nBits unspecified.")
replace_exact(p, '"You owe me twenty-three copper."', '"You still have an active account with me."')
replace_exact(p, "**4C ON ACCEPTED START PLAN + CONFIRMED CREW/TRANSPORT CONTACTS**\n\n**10C ON COMPLETION OF FOUR-DAY HANDOFF IF ALL DAILY ORGANIZER RECORDS ACCEPTED**", "**6S ON ACCEPTED START PLAN + CONFIRMED CREW/TRANSPORT CONTACTS**\n\n**12S ON COMPLETION OF FOUR-DAY HANDOFF IF ALL DAILY ORGANIZER RECORDS ACCEPTED**")
replace_exact(p, "Fourteen copper total.\n\nI read again.\n\nNot silver.\n\nStill more than a seven-copper day.\n\nMore importantly, I was not being paid to clear a ditch.", "Eighteen silver total.\n\nI read again.\n\nActually silver.\n\nMore importantly, I was not being paid to clear a ditch.")
replace_exact(p, '"How much?"\n\n"Twenty-three copper."', '"How much?"\n\n"I haven\'t reconciled the whole account recently. Enough that I should."')
replace_exact(p, "If plan accepted, four copper.", "If plan accepted, six silver.")
replace_exact(p, '"Four copper if they accept start plan. Ten more after four-day handoff if records accepted."\n\nShe did math with face.\n\n"Fourteen."', '"Six silver if they accept start plan. Twelve more after four-day handoff if records accepted."\n\nShe did math with face.\n\n"Eighteen silver."')
replace_exact(p, '"You have eighteen."\n\n"Yes."\n\n"So if you don\'t ruin crops you get thirty-two."', '"And if you don\'t ruin crops, the term actually matters."')
replace_exact(p, "Thirty-two.\n\nAbove the thirty-copper reserve target I had been circling for months.\n\nIf.\n\nNot mine yet.\n\nImportant.\n\n\"Four first,\" I said.", "Eighteen silver total.\n\nA different tier from the copper jobs I had been stacking.\n\nIf.\n\nNot mine yet.\n\nImportant.\n\n\"Six first,\" I said.")
replace_exact(p, "Four copper on table.\n\nThere.\n\nNot completion.\n\nNot fourteen.\n\nFour.\n\nI counted once.\n\nEighteen to twenty-two.", "Six silver on table.\n\nThere.\n\nNot completion.\n\nNot eighteen.\n\nSix.\n\nI counted once.")
replace_exact(p, "I put four copper away.\n\nTwenty-two.\n\nTen floor.\n\nTwelve above it.\n\nCloser.\n\nNot there.", "I put six silver away.\n\nOperating reserve intact.\n\nTwelve more silver still conditional.\n\nCloser.\n\nNot there.")
replace_exact(p, "I put four new copper beside the rest.\n\nTwenty-two.\n\nNot thirty-two.\n\nNot yet.\n\nTen completion copper sat in someone else's future obligation, contingent on three more days and acceptable records.", "I put six new silver beside the rest.\n\nNot eighteen silver for the term.\n\nNot yet.\n\nTwelve completion silver sat in someone else's future obligation, contingent on three more days and acceptable records.")

p = "state/manuscript/Peg_Leg_Greg_Chapter_486_EXACT_WIP.md"
replace_exact(p, "Completion fee lived in future.\n\nTwenty-two copper remained twenty-two.", "Completion fee lived in future.\n\nThe six-silver start payment stayed in reserve with the rest of my working money.")
replace_exact(p, "Still no completion money.\n\nTwenty-two.", "Still no completion money.\n\nSix silver from the start term was already real. Twelve more remained conditional.")
replace_exact(p, '"Completion fee?"\n\n"Still ten copper."', '"Completion fee?"\n\n"Still twelve silver."')
replace_exact(p, "Ten copper.\n\nPut it on table.\n\nI counted again.\n\nNot because I distrusted her.\n\nBecause money deserved witnesses.\n\nTen.\n\nCash twenty-two to thirty-two.\n\nNo conversion.\n\nNo celebration.\n\nJust thirty-two copper.", "Twelve silver.\n\nPut it on table.\n\nI counted again.\n\nNot because I distrusted her.\n\nBecause money deserved witnesses.\n\nTwelve.\n\nNo conversion.\n\nNo celebration.\n\nJust an eighteen-silver organizer term completed exactly as written.")
replace_exact(p, 'At home I put ten copper on table.\n\nLyssa looked at it.\n\nThen me.\n\n"How much?"\n\n"Ten."\n\n"For today?"\n\n"For finishing four-day organizer term."\n\n"That sounds better."\n\n"It is."\n\n"How much now?"\n\n"Thirty-two cash."', 'At home I put twelve silver on table.\n\nLyssa looked at it.\n\nThen me.\n\n"How much?"\n\n"Twelve."\n\n"For today?"\n\n"Completion half. Eighteen silver for the four-day organizer term total."\n\n"That sounds better."\n\n"It is."')
replace_exact(p, '"Plus Vale?"\n\n"Vale is the opposite direction."\n\n"Right."\n\nTwenty-three copper still owed.\n\nThere it was.\n\nFor the first time, that number did not feel larger than my entire life.\n\nTwenty-three owed.\n\nThirty-two cash.\n\nTen floor.\n\nWork limb still existed.\n\nOther obligations might exist.\n\nBits existed.\n\nFood existed.\n\nTomorrow existed.\n\nThirty-two did not mean twenty-three was free to leave.\n\nIt meant I could finally look at old numbers without assuming every answer was no.', '"Plus Vale?"\n\n"Vale is the opposite direction."\n\n"Right."\n\nVale still existed.\n\nThere it was.\n\nFor the first time, the existence of that account did not feel larger than my entire life.\n\nI had enough independent earning power to stop guessing what I owed and finally reconcile the whole ugly thing.\n\nWork limb still existed.\n\nOther obligations might exist.\n\nBits existed.\n\nFood existed.\n\nTomorrow existed.\n\nThe silver did not mean Vale was free to leave.\n\nIt meant I could finally look at old numbers without assuming every answer was no.')
replace_exact(p, 'Lyssa said, “Are you going to hand Antonius all of it tomorrow and come home proud and broke?”', 'Lyssa said, “Are you going to hand Antonius all of it tomorrow and come home proud and broke?”')
replace_exact(p, "Thirty-two copper.\n\nTwenty-three Vale.\n\nTen floor.\n\nA completed organizer reference folded with my papers.", "Eighteen silver earned across the organizer term.\n\nVale still open and due for reconciliation.\n\nOperating reserve intact.\n\nA completed organizer reference folded with my papers.")

modified_wips = [
    "state/manuscript/Peg_Leg_Greg_Chapter_471_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_472_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_473_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_474_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_475_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_476_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_484_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_485_EXACT_WIP.md",
    "state/manuscript/Peg_Leg_Greg_Chapter_486_EXACT_WIP.md",
]
for path in modified_wips:
    text = (ROOT / path).read_text(encoding="utf-8")
    if "—" in text:
        raise SystemExit(f"EM DASH FOUND after normalization: {path}")

print("economy normalization source pass complete")
