# R2 Embodied Role Title Audit

Status: **APPROVED THROUGH PUBLIC CHAPTER 118**

This audit applies `r2/TITLE_POLICY.md` to the current selected/public R2 frontier.

The governing question is:

> **Who is Greg in this chapter?**

The audit intentionally allows repeated roles. Repetition is preferable to inventing a cute synonym when Greg is materially inhabiting the same role again. Broad roles are also acceptable when the chapter genuinely embodies them.

The audit rejects titles that primarily name an object, place, event, time span, anatomical detail, monster, deadline, or chapter topic. The selected role is grounded in Greg's actual work, relationship, social position, temporary function, or situational identity in the chapter.

Chapters 001-026 retain the previously established R2 role-title decisions where they still fit current selected prose. Chapters 027-118 were re-audited against the current selected written authority on the `r2/role-title-authority-118` branch.

## Editorial notes

A few recurring identities are deliberate:

- `The Correspondent` recurs when Greg is materially sustaining relationships through letters and packet logistics.
- `The Candidate` recurs across formal advancement, expedition selection, certification, and return-to-field assessment chapters.
- `The Crewman` recurs during Westreach when the important truth is that Greg is one working member of Field Support Three rather than the hero of a named obstacle.
- `The Partner`, `The Friend`, `The Neighbor`, and `The Host` may recur because relationship roles are durable identities, not one-use labels.
- `The Thief` remains Greg's role through the immediate consequence chapter after the theft. Returning Faultglass does not erase what he did.

The approved map below is the editorial decision source. Mechanical tooling may propagate it but must not invent replacements.

## Approved title map

```text
001 The Boy
002 The Novice
003 The Borrower
004 The Contractor
005 The Partner
006 The Troubleshooter
007 The Extra Guard
008 The Defender
009 The Backstop
010 The Returner
011 The Gate Hand
012 The Stranger
013 The Fighter
014 The Helper
015 The Friend
016 The Investor
017 The Extra Hand
018 The Applicant
019 The Maintainer
020 Ward Hand
021 The Letter Writer
022 The Neighbor
023 The Adventurer
024 The Watchman
025 The Hired Sword
026 The Adventurer
027 The Correspondent
028 The Friend
029 The Card Player
030 The Partner
031 The Friend
032 The Neighbor
033 The Passenger
034 The Correspondent
035 The Promise-Keeper
036 The Neighbor
037 The Companion
038 The Host
039 The Visitor
040 The Citizen
041 The Field Hand
042 The Correspondent
043 The Aspirant
044 The Yard Hand
045 The Adventurer
046 The Road Hand
047 The Trainee
048 The Host
049 The Field Guard
050 The Tinkerer
051 The Field Guard
052 The Aspirant
053 The Second Guard
054 The Second Guard
055 The Second Guard
056 The Visitor
057 The River Hand
058 The Ward Specialist
059 The Ward Specialist
060 The Candidate
061 The Returner
062 The Silver Adventurer
063 The Second
064 The Second
065 The Builder
066 The Delver
067 The Load Specialist
068 The Host
069 The Field Load Specialist
070 The Field Lead
071 The Field Load Specialist
072 The Candidate
073 The Candidate
074 The Candidate
075 The Specialist
076 The Crewman
077 The Crewman
078 The Support Specialist
079 The Maintainer
080 The Crewman
081 The Crewman
082 The Crewman
083 The Returner
084 The Partner
085 The Worker
086 The Trainee
087 The Hunter
088 The Friend
089 The Delver
090 The Correspondent
091 The Hunter
092 The Candidate
093 The Structural Support
094 The Repair Hand
095 The Patient
096 The Amputee
097 The Rebuilder
098 The Tenant
099 The Planner
100 The Tester
101 The Relearner
102 The Candidate
103 The Partner
104 The Specialist
105 Their Specialist
106 The Adapter
107 The Fighter
108 The Veteran
109 The Partner
110 The Seeker
111 The Demonstrator
112 The Buyer
113 The Thief
114 The Betrayer
115 The Student
116 The Thief
117 The Traveler
118 The Partner
```

## Migration boundary

Applying this map may change only title-bearing surfaces:

- the title segment of the first selected-written heading
- `title` in `r2/data/chapters/chNNN.json`
- `title` in an existing `r2/data/chapter-registry.json` entry
- `title` in an existing `greg-again/audio/manifest.json` chapter entry
- explicit title assertions in tests or documentation that are intended to mirror public authority

It must not change prose below the first heading, stable chapter IDs, route paths, display numbers, audio binaries, audio ownership, take maps, or publication state.
