# RTB Lead Retargeting Sequences

Every free entry point (call, class, workshop) feeds one of two sequences. The job of both is
the same: get the person to the 21 Day Strength Reset ($150, in the gym) or, if they train
elsewhere, the RTB program on TrainHeroic (7 days free, then $40 a month).

Voice rules: short sentences, full stops, no dashes, sounds like Josh talking. Every message
has one link. SMS under 300 characters.

Links:
- Reset, buy now: https://raisethebarmobi.app.link/YrXSO1QeP0b
- Reset, workshop price: https://raisethebarmobi.app.link/OxKTJIKeP0b
- Online program trial: https://marketplace.trainheroic.com/brand/rtb-raise-the-bar
- Book a call: [site]/call.html
- Book a free class: [site]/experience.html

Existing workshop show up sequence (booking to the night) lives in WORKSHOP-SEQUENCES.md.
This file starts where that one ends: the person has had their free thing and has not bought.

---

## SEQUENCE A. Attended something, didn't buy
Fires the day after a call, a free class or a workshop for anyone with no Reset purchase.
Stop the sequence the moment they buy.

### A1. Day 1, 9am. Email
Subject: Thanks for coming [yesterday / in]

Hi [First],

Thanks for coming in [yesterday]. Good to meet you.

Here is the deal I mentioned. Two options, pick the one that fits.

Option 1. You want to train with us.
The 21 Day Strength Reset. Three weeks of coached strength sessions at RTB, every set coached, capped at 12. Onboarding with me, a body scan, a nutrition consult with Liz, and a program that's yours to keep. $150 all in.
Grab it here: [Reset link]

Option 2. You already train somewhere else.
The exact program we run on the floor is on your phone. New program every month, the app tells you the weight. Seven days free.
Start here: [Online trial link]

We cap classes at 12 and we are close to full, so if you want in, don't sit on it.

Any questions, hit reply. It comes straight to me.

Josh

### A2. Day 3, 5pm. SMS
Hey [First], Josh from RTB. Did you get a session in since [day]? The Reset spot is still there if you want it: [Reset link]. Reply STOP if you'd rather I left it.

### A3. Day 6, 9am. Email
Subject: The thing everyone gets wrong

Hi [First],

Quick one. The reason most people stall in the gym isn't effort. It's that nobody tells them what weight to lift or when to go heavier. So they guess. Too light and nothing changes. Too heavy and something hurts.

At RTB you never guess. Every set has a number on it, worked off your own max, and it moves up when you earn it. That is the whole system. It's why the results on our site look the way they do.

If you want that, the Reset is the way in: [Reset link]
If you'd rather run it from your own gym: [Online trial link]

Josh

### A4. Day 10, 5pm. SMS
[First], last one from me on this. Reset is $150 for 21 days, unlimited sessions, coached every set. If it's a yes: [Reset link]. If it's a not now, no worries, I'll check in down the track.

### A5. Day 21, 9am. Email (the not now list)
Subject: Where are you at?

Hi [First],

Three weeks since you came in. Honest question. Are you training, and is it working?

If yes, good. Keep going.
If no, the Reset is still $150 and the next intake starts Monday. Book a quick call and we'll sort a plan: [Call link]

Josh

### A6. Day 45. Email
Subject: 21 days from now

Hi [First],

Everyone who started the Reset the week you came in has finished it. Body scanned, numbers tested, most of them now members.

Twenty one days from today you could be at the same point. Or in the same spot as now. Your call.

[Reset link]

Josh

Then: move to the monthly newsletter list. One email a month, a member result and one offer.

---

## SEQUENCE B. Booked, didn't show
Fires the morning after a missed call, class or workshop.

### B1. Next morning, 9am. SMS
Hey [First], Josh from RTB. We missed you [yesterday]. No stress. Want me to rebook you? Reply with a day that suits or grab a time here: [Book link]

### B2. Day 3, 9am. Email
Subject: Rebook in ten seconds

Hi [First],

Life gets in the way. You booked because something wasn't working with your training, and that hasn't changed.

Pick a new time here and I'll see you then: [Book link]

If you'd rather skip the visit and just start, the 21 Day Reset is $150 all in: [Reset link]

Josh

### B3. Day 8, 5pm. SMS
[First], last nudge. Free class / call spot is still yours if you want it: [Book link]. Otherwise I'll leave you be.

Then: into Sequence A at A5 (day 21).

---

## SEQUENCE C. Online trial started, didn't convert
Fires when a TrainHeroic 7 day trial ends with no subscription. (Trial start and end come
from TrainHeroic, not Hapana. Needs a manual export or Zapier until wired.)

### C1. Trial day 5. Email
Subject: Two days left. How's it going?

Hi [First],

Two days left on your trial. Quick check. Did the weights the app gave you feel right? Too easy, too hard, or about right?

Reply and tell me. I read every one and I'll adjust your working max if it's off.

Josh

### C2. Trial day 8 (expired). SMS
Hey [First], your RTB trial finished yesterday. $40 a month keeps the program going, new block drops on the 1st: [Online trial link]. Any questions, reply here.

### C3. Day 14. Email
Subject: What next month looks like

Hi [First],

New block drops on the first. [Strength / hypertrophy] month, testing week at the end, your working max carried over from the trial.

If you want back in it's $40 a month, cancel any time: [Online trial link]

And if you're ever near Windsor or Chelsea Heights, your first class in the gym is free: [Class link]

Josh

---

## SEQUENCE D. Reset buyers, week 2 close (existing upsell path, for completeness)
Covered by the in gym process: week 2 membership close with the EOFY style discount, then the
Liz nutrition plan at $200. Not an email job. Keep it on the floor.

---

## Setup notes
- Hapana CRM handles A and B (tag on attendance, tag on no show, remove tag on purchase).
- Sequence C needs TrainHeroic data. Until that's automated, export trialists weekly and
  load them into Hapana with a tag.
- Every link carries a UTM: utm_source=hapana&utm_medium=email|sms&utm_campaign=seqA|seqB|seqC&utm_content=A1 etc.
- Numbers to watch: A1 open rate, A1 to A4 purchase rate, B1 rebook rate, C2 to subscription rate.
