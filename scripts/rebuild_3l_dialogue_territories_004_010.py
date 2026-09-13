from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(record: str) -> tuple[Path, str]:
    path = ROOT / "3l" / "manuscript" / f"record-{record}.md"
    return path, path.read_text(encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


# 004: preserve the remembered-life chapter and add one clean Ithar checkpoint.
path, text = read("004")
anchor = "It was the assumption that I still wanted the same life."
insert = """It was the assumption that I still wanted the same life.

The cave returned around me.

Ithar had not moved.

His eye rested on the hands I had been remembering young.

“You woke with forty years of knowledge and treated the second life as a chance to perform the first more efficiently. You did not yet want another life. You wanted the same one with fewer mistakes. Keep that distinction. It will matter when you tell me when it stopped being true.”

I looked at him.

“At nineteen, I didn't know it was an assumption.”

The dragon's eye stayed on me.

Then Guild Hall came back."""
text = replace_once(text, anchor, insert, "004 checkpoint")
write(path, text)


# 005: add one clean checkpoint before the original closing line.
path, text = read("005")
old = """That was what the paper said.

I believed the paper too."""
new = """That was what the paper said.

The cave came back before I could hide inside the word temporary.

Ithar's claw rested against the gold.

“You describe East Four as a detour because that is how you protected the decision from becoming a decision. Twelve silver went west. Eight stayed near home. The paper lanterns matter because you remembered them when the old road was still available. You changed the route before you admitted you were changing it.”

I rubbed my thumb against the edge of the rank pin.

“At the time it felt temporary.”

His eye held mine.

I closed my eyes again.

I believed the paper too."""
text = replace_once(text, old, new, "005 checkpoint")
write(path, text)


# 006: consolidate the opening examination into one Ithar territory.
path, text = read("006")
start = text.index('“How long?”')
end_marker = "I closed my eyes again."
end = text.index(end_marker, start) + len(end_marker)
new_open = """The number four pulled me out of the memory.

I opened my eyes.

The cave came back all at once.

Black glass scales.

Gold.

Heat.

My pack beside the stone.

My left leg aching because apparently memory did not count as rest.

Ithar had not moved.

That felt unfair.

“You said the contract was four weeks. You remained at East Four for eleven years. Do not give me eleven years as though the number is the answer. You removed the years and called the removal a summary. If most of that time was work, then tell me about work. If it was repetitive, then repetition occupied eleven years of your life too.”

I looked toward the passage.

The passage remained neutral.

Useless thing.

“Eleven years is a long time.”

The dragon did not need to answer that.

“For me.”

Still nothing.

I sighed.

Ithar settled his chin more comfortably onto the stone.

He had won without doing anything.

I hated patient people.

I hated patient dragons more.

“Fine.”

I closed my eyes again."""
text = text[:start] + new_open + text[end:]

stew_start = text.index("Ithar's voice entered the memory so cleanly")
stew_end_marker = "I closed my eyes again."
stew_end = text.index(stew_end_marker, stew_start) + len(stew_end_marker)
new_stew = """Ithar interrupted only once.

The question did not need his voice to survive in mine.

Why did I remember the stew?

Because it was good.

Apparently that was sufficient."""
text = text[:stew_start] + new_stew + text[stew_end:]
write(path, text)


# 007: collapse the Halden/future-confidence cave examination into one Dragon block.
path, text = read("007")
start = text.index("Ithar interrupted.")
end_marker = "So I did."
end = text.index(end_marker, start) + len(end_marker)
new_interlude = """The kitchen disappeared.

The cave returned.

I opened my eyes.

Ithar was watching me.

“You remember those names because in the first history they died and in the second they did not. You acted from a remembered outcome before you understood its mechanism. Then you inspected the mechanism, changed it, and Halden survived. From that point forward, every later memory inherited a question: what else changed because this man remained alive?

“You did not know whether Halden mattered enough to alter anything larger. That uncertainty is the important part. Tell me what it did to your confidence in the future you remembered.”

I looked down at my hands.

“Made it worse.”

Not useless.

Worse.

“The first few years, the memories felt like a map. Not perfect. Roads change. People are people. But big things were where I expected them. After Halden lived, every event downstream had a question attached.”

Did Halden matter enough to alter continental history?

I did not know.

That was the point.

I had started learning that recognized uncertainty was more useful than invented certainty.

Ithar's eye narrowed slightly.

That was enough examination for one interruption.

I closed my eyes again."""
text = text[:start] + new_interlude + text[end:]
write(path, text)


# 008: merge the two Nessa/rescue examinations into one sustained Ithar territory.
path, text = read("008")
start = text.index("Ithar pulled me out again.")
end_marker = "So I went back to the ward."
end = text.index(end_marker, start) + len(end_marker)
new_interlude = """The cave pulled me out of the ward.

I opened my eyes.

Ithar's gaze had settled on the shoulder that still carried a piece of that day.

“You knew Nessa Vale first as a name on a board of dead people. By the time the remembered death arrived, she was no longer a name. She was your friend, and already more complicated than that word admits.

“You attempted to prevent an outcome you remembered without understanding the mechanism that produced it. You dropped the wrong feed. You made the failure worse before you understood what was beneath the station. Then you saved her.

“Separate motive from method. Wanting her alive does not make the method correct. Surviving the mistake does not make the motive foolish. What did the difference teach you?”

I looked at my right hand.

The two fingers that did not close properly now had nothing to do with East Four.

The leg did not either.

Life had plenty left to take.

But the shoulder did.

A little piece of that day had stayed all the way to the mountain.

“Knowing what happens isn't the same as knowing why.”

The dragon waited.

I thought of Nessa asleep six beds away.

Fourteen names that never went on a board.

A hidden chamber beneath a station I had worked in for five years.

“The future got less useful every time I touched it.”

Ithar's head moved slightly.

Approval, maybe.

Or breathing.

I was still working with limited information.

I closed my eyes and went back to the ward."""
text = text[:start] + new_interlude + text[end:]
write(path, text)


# 009: consolidate the reasons-for-staying examination while preserving Greg's answer.
path, text = read("009")
start = text.index("Ithar's voice came from the cave.")
end_marker = "I closed my eyes."
end = text.index(end_marker, start) + len(end_marker)
new_interlude = """The cave came back around me.

Ithar was watching the red letter in my memory like it still sat between us.

“You have given me several reasons without giving me the decision beneath them. Nessa. Your family. Fear. Home. Certainty. The table. You had already climbed to S-class once. You knew what that road gave you and what it cost. What did you refuse to pay again?”

I rubbed the heel of my hand against my forehead.

“I'd already done it.”

Not accomplishment.

Not because S-class was nonrepeatable.

“I knew what it was. I spent the first life climbing because every step showed me another step. E to D. D to C. Better contract. Better team. Harder work. More money. More authority. Then A. Then S. Then people start telling you there are only six others and somehow that feels like a reason to keep proving it.”

I looked at him.

“I knew where that road went. It was good. A lot of it was fucking great.”

I did not want it enough to pay again.

The cave went quiet.

That sentence had come from somewhere deeper than I expected.

“In the first life, every choice toward strength felt temporary. Six months away. One more contract. One more season. One more place I had to be because I was finally good enough to be needed there.”

I looked down at my leg.

It was not the leg from that time.

Not yet in the memory, anyway.

“I kept thinking life would start when the work settled down. In the second life, it already had.”

Ithar let that sit before taking the floor again.

“Then the table belongs in the answer. Not because a table is profound. Because it is not. The ordinary things are evidence that the life had already begun while you were still treating it as the delay before the important part. Do not discard them because they look small beside S-class.”

I laughed.

“Yes. The fucking table.”

He was a dragon sitting on a mountain of gold explaining my own table to me.

Smugness felt plausible whether he admitted it or not.

I laughed harder than I should have.

My ribs hurt.

Old ribs.

Present ribs.

When I stopped, I told him what came next.

Four more years at East Four.

Then staying in the city.

Then staying with Nessa.

Then staying for things I did not know I was staying for until they happened.

My nephew gripping one finger with his whole hand.

My mother's hair going gray.

Nessa asleep with a book open against her chest.

A ring I carried for eleven days because I kept finding reasons the moment was wrong.

A child who did not exist in the first history.

Then another.

I stopped.

Ithar heard the silence change.

For once, he let it.

I closed my eyes."""
text = text[:start] + new_interlude + text[end:]
write(path, text)


# 010: consolidate the Bren examination and the final naming of Life Two.
path, text = read("010")
start = text.index("Ithar's voice came softly from the cave.")
end_marker = '“My life.”'
end = text.index(end_marker, start) + len(end_marker)
new_interlude = """The cave returned softly around me.

I opened my eyes.

Ithar was quiet for long enough that the silence itself became the question.

Then he took the floor.

“You never told Bren. You had information about him and chose not to use it. That is unusual in an account where foreknowledge has repeatedly become action.

“You loved him in the first history. Brother without shared parents, by your description. In the second history he did not know you. You knew what he liked, where he would go, what made him trust someone. You could have manufactured the conditions under which he might become close to you again.

“You refused. Why?”

For once the answer was simple.

“He didn't owe me the man I remembered.”

I rubbed my thumb against the edge of my pin again.

Same habit.

Different badge.

“I could have made myself useful. I could have put myself in the right places. But then I wouldn't know if he chose me.”

First life, we became friends because we were idiots on the same bad contract.

We annoyed each other honestly.

Apparently that mattered.

Losing him the second time was not noble.

It was sad.

Ithar considered that.

Then he nodded once.

The movement was tiny.

Coming from him, it felt enormous.

When he spoke again, the question was larger than Bren.

“You had already observed events changing. Halden survived. North Vey did not rupture. Your remembered future had been becoming less reliable for years. Yet you still treated the first life as the real version and the second as a return into it.

“Bren looked at you and did not know you. His ankle was whole. His rank had arrived by another road. The page after the one you remembered no longer existed.

“Was that when you stopped calling it going back? What did you call it instead?”

I looked toward the dark passage.

Not because I wanted to leave this time.

Because the answer needed room.

“I think that was it. Bren. North Vey. Halden. All of it.”

The first few years, I had still thought of the old life as the real version.

Like I had gone back into a book I already read and scribbled in the margins.

Then one of the characters looked at me and had no idea who I was.

And the page after that wasn't there anymore.

I looked at Ithar.

“My life.”"""
text = text[:start] + new_interlude + text[end:]
write(path, text)

print("Patched 3L Records 004-010 dialogue territories.")
