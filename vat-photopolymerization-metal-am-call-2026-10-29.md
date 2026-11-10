# Call with Sam Hales on metal DLP projects (Oct 29, 2026)

This is a corrected transcript of a 23-minute Zoom call on Thursday, Oct 29, 2026 (4:04 pm MDT), between Sam Hales
(BYU) and Sterling Baird about research projects for a metal DLP company. Nathan Crane (BYU) heard a talk from the
company and talked with it afterwards. It has no university partners yet, and Sam is gathering project ideas to send
to it through Nathan. The call never names the company.

Left out: the greetings, some camera trouble, a personal aside and the goodbyes. One name that the captions garble
is replaced with [name unclear]. Everything else is as said, cleaned only for grammar and filler words.

## How the captions were corrected

Tactiq's captions are corrected from context, using digital-alloy-lab issue 228 and PR 229 for the technical
terms.
- Words in [brackets] replace a mishearing or fill a gap, (?) marks a guess, and […] marks a garbled fragment that
  was dropped.
- Filler words, stutters, false starts and one-word caption noise are removed without a mark.
- Short backchannel lines ("Yeah.", "Okay.", "Mm-hmm.") that break into the other person's turn are dropped, and
  that person's turn is joined back up.

The table at the end gives the raw captions for each correction that changes the meaning.

## Transcript

**01:16 Sterling Baird:** So tell me about this a little bit more.

**01:36 Samuel Hales:** So, as far as I understand, this is a [metal] 3D printing company that Nathan Crane listened
to a talk from, and then he chatted with them a little bit afterwards about some of the things they've been trying to
work with. They've got a number of problems with their process that they're trying to improve on.

**02:02 Samuel Hales:** So he reached out to me, and we chatted with one of their employees this last week. And it
seems like they've got lots of different problems; there are lots of different things we could try to do to help
them out. It doesn't seem like they've really done any partnerships with universities before. They said they'd
probably be willing to donate an old printer to BYU, and they might have funding to fund, like, a graduate student.
And there may be a bunch of professors [who'd] tell them what to do with [it] (?). Because I guess right now we're
just going around and talking to people and seeing what all we could do, and just pitching some things: here's some
research areas, this is about how much things would cost for some of these areas. And yeah, see what they're
interested in.

**03:07 Sterling Baird:** They look like they do steel, and… was it steel and something else?

**03:20 Samuel Hales:** Yeah, I don't recall the specific materials, but yeah, all [vat] photopolymerization, so
resin printing. I've done ceramic resin printing, but I haven't done it with metals before, and I'm not familiar
with many people who do it for metals. It seems like metals are pretty well established in powder bed fusion and
binder jetting and such, but there's not as much for resin printing, [where] you can potentially get some better
resolutions.

**03:55 Samuel Hales:** But a lot of their problems have just been with getting good fluid flow, where they're
getting particles jamming. Mostly, to me, it seems like they're not getting very good penetration depth, UV
penetration depth, into their fluids. [It] seems like their particles are a little bit too big for the layer heights
they're going for, and so you get particle jamming, you get particles pulling out, and they get some separation of
their particles in the fluid. But with metal DLP, and for ceramics too (well, I guess I can mostly just speak about
the ceramic stuff), every research group that I've looked at, everybody has their own special formulation.
Everybody uses different monomers and dispersants, different chemicals in there. And there's not a lot of
verification on when you should use one versus something else. And I think their process is similar, in that there
are so many different knobs to tune, where being able to test out a bunch of different formulations, and then
testing how well [they] cure, cure depth, and those sorts of things, would be very helpful.

**05:04 Sterling Baird:** Yeah. Which gets me wondering [about] maybe an autonomous platform for doing that kind of
screening of different [monomers] and…

**05:16 Samuel Hales:** Yeah. Yeah, it would be a helpful thing, I guess, for [a] pretty wide community there, I
think.

**05:31 Sterling Baird:** Maybe you mentioned this already, but I don't know if you have an idea of what kind of
properties people would be interested in? You mentioned particles kind of getting non-uniformly distributed,
particles that are clumping and not [getting] a uniform [distribution]…

**05:59 Samuel Hales:** Yeah, agglomerations and things. Yeah, rheological properties are definitely interesting. I
think just depth of cure and degree of cure. I'm sure we could do some sort of hardness testing. You get a
measurement of how thick of a layer you're able to cure with a certain amount of UV exposure.

**06:23 Samuel Hales:** Really, I think they need some smaller particle sizes, and then mess around with formulations
to see where you can still get a decent cure depth and have those smaller particles. They were saying that their
particles are normally in the range of, like, 10 [to] 25 microns, which, lots of times, your layer heights in DLP
are about that same thickness. And that's kind of what they're seeing, or what they said, at least: [if] they use
smaller particles, their cure depth would go down, and so then they'd have to use a shorter layer height, and then
you still kind of have the same problems.

**07:08 Sterling Baird:** So they see moving to a smaller particle size [as] not ideal, right?

**07:08 Samuel Hales:** Yeah, but I don't know that they've gone down into the nanoparticle range. And right now
their particle sizes are on the same order, about the same size as their layer height, which seems not ideal to me. I
don't feel like that should really work.

**07:25 Sterling Baird:** Yeah. That's funny.

**07:32 Samuel Hales:** But I guess it's something to look at. I don't know how good their particles are or anything.
Like, with ceramics, it's a lot harder to get spherical particles. So I have some nice spherical ceramic particles
for alumina, but it's hard to find many things that are that spherical. But it seems like for metals, it's pretty
common to have your plasma spheroidization process and get some good particles there. I know you have [a few] nice
process[es] for that, which could be of benefit.

**08:13 Sterling Baird:** Yeah, so if there's a compositional exploration there, or even just kind of custom powder
supply, that would be…

**08:26 Samuel Hales:** Yeah, it could be helpful.

**08:29 Samuel Hales:** So I guess [the] primary question, and I guess from talking to Nathan Crane this last time:
definitely making an automated process would be awesome and could fix a lot of things, but [it would] probably be
pretty time-consuming and take a lot of money, and so it might be harder starting up. But I wanted to get your
thoughts on that, on how much you think we could do there.

**08:58 Sterling Baird:** If it was focused just on monomers, or sorry, the formulation aspect, and not actually
printing with it, so really just looking more at the [rheological] properties and not actually doing [debinding and
sintering] and all that, then I think that's a pretty standard lift, I would say.

**09:24 Sterling Baird:** You scope out the project, you think, like, okay, yeah, I think somebody could do this in
three months, and then you change that to a year because of just students and uncertainty there. I think that would
be kind of a year-long project, up to a year for our first major results coming off of that, but it's not multiple
years.

**09:49 Samuel Hales:** Yeah, not terrible.

**09:55 Sterling Baird:** I think for actually printing, if they did provide us with an old printer, then, I don't
know, that feels more like a two-years-out kind of lift. Maybe I'm also thinking [of] my own bandwidth to
participate.

**10:10 Samuel Hales:** Yeah. Yes.

**10:17 Sterling Baird:** I don't know if you have thoughts on that, because you and Nathan both would have [more]
experience with doing the [debinding] and sintering.

**10:42 Samuel Hales:** Yeah, to me, I think just looking at polymer properties initially sounds like a good project.
You get a lot from that: just getting something where you're not getting things jamming and binding up, and getting a
reasonable depth of cure and whatnot. You should be able to see that just in the raw material.

**11:04 Sterling Baird:** Yeah. And is there something special to their platform over a typical SLA? It seemed like
it wasn't actually a vat, but it was just sort of spreading a slurry over it.

**11:19 Samuel Hales:** Yeah, yes, they do just spread.

**11:21 Sterling Baird:** Like, a lot more [doctor blading].

**11:23 Samuel Hales:** Yeah, so [they] do just spread one layer at a time. I think they said maybe, like, 50 micron
layer thickness, and then they put their build platform in there. Which is at least somewhat similar to how ceramic
[vat photo] normally goes, except [they] said that a lot of it kind of gets recycled, which they like, but [it] also
can cause more problems. You can get extra gunk that goes back into your source [resin] and such. But yeah,
otherwise, it's pretty standard.

**12:03 Sterling Baird:** Yeah, and I guess, do you find the application enticing and relevant in terms of research?
Would that be a benefit to [the] portfolio you're building out, or do you see [it] as more of a nice side gig?
Because I know ceramics have been the core focus.

**12:25 Samuel Hales:** Yeah, yeah, ceramics. I guess I've been more [focused on and] excited about ceramics, since
that's what I did at NIST. But really, it doesn't feel like it should be that much different. And I think there's
advantages. I had thought about [it] before coming here, figuring out a metal DLP process, because I just don't see
many papers on it.

**12:50 Samuel Hales:** And potentially, I think what's exciting about [vat photo] processes is I feel like [they]
can scale a lot faster than a lot of other printing processes. Which depends; I guess with binder jetting, you can add
more nozzles and things. But just the fact that you can project an image and get one layer within a few seconds, and
then come up and project a new image. And then if it's possible to ever do something that's more like… there are more
continuous [vat photo] printing methods, if you're familiar with any of those, like [CLIP], where […] at the bottom of
the vat, you have a film that's oxygen-permeable, and so the resin doesn't cure next to that oxygenated layer. And so
you can project an image and it'll cure just above that layer, and you can keep projecting images and keep pulling
your part out, so you can [print] a big part in just a couple of minutes instead of…

**13:58 Samuel Hales:** Yeah, which, I guess, volumetric printing: [name unclear] said he was doing some of that
too. What was that?

**14:00 Sterling Baird:** Cool. Holography, you know? Oh, holography.

**14:08 Samuel Hales:** Yeah, yeah, yes. Because you're working with light, there's some weird things you can do
there. So it'd be cool to have a good method for printing metals. It seems like it still needs some work, which is
kind of a good thing from a research perspective.

**14:27 Sterling Baird:** Yeah. It doesn't seem like there's been a lot… I think there [hasn't] been a lot of
government funding flowing towards it (?). [I've] definitely seen some. I kind of wonder… It looks like there is an
active award. That one could be worth looking at.

**15:13 Sterling Baird:** This one might [be good] just in terms of chatting with some people. Good to get started,
to [get] outside opinions there.

**15:36 Samuel Hales:** Yeah, that's true. [It's not] pulling up much for me (?). [But] good to look into that sort
of stuff too, for sure.

**15:51 Sterling Baird:** Oh, yeah, then it does seem like [Janis Terpenny] from CMMI Advanced Manufacturing is
really the person to talk to about federal funding related to this.

**16:10 Samuel Hales:** For all this sort of space.

**16:12 Sterling Baird:** Like, almost all of the federal ones have been through [Janis]. Nice. Yeah, so that sounds
interesting. Do you know what kind of next steps are?

**16:29 Samuel Hales:** So at this point, we're just [gathering] together some potential research projects and
sending that over to him, and seeing what they're interested in.

**16:46 Samuel Hales:** So really, you just need, like, a couple sentences on what we would do with automation.

**16:56 Sterling Baird:** Yeah, I think it kind of comes down to… So on the automation side, doing the autonomous
formulation studies. That's one. On the machine learning side, very much just AI, machine learning decision-making.
[That] still fits into the formulation screen, but also then becomes, like, oh, do we try to optimize the print
parameters? Do we try to change which powder we're using, and change things about [the] powder that we're actually
putting in and kind of mixing in with the… So, […] have they… I guess I'm wondering if they've kind of expressed
interest one way or another.

**17:51 Samuel Hales:** For the automated stuff, or just…?

**17:55 Sterling Baird:** Just in general, like, what their challenges [are], or…

**17:58 Samuel Hales:** I mean, essentially it seemed like they don't really have any partners at universities right
now, and they've got lots of problems. And so… so they picked one, I guess.

**18:08 Sterling Baird:** Yeah, […]. Yeah, that sounds good. Yeah, feel free to… I can send you a couple sentences
on the monomer, you know, [binder], formulation optimization. What else goes in there?

**18:32 Samuel Hales:** Yeah, I think different particle sizes and shapes, and the binder. They put some wax in there
too, which is not as common for the ceramics, but it seems like they keep their solids loading a little bit lower
than you normally would, just to get a little bit more penetration depth.

**18:55 Sterling Baird:** And then, I don't know, I guess another thing is just the exploration, like, oh, what if you
use different alloy systems? Because it seems like they've got a pretty narrow set of [alloy] systems that [they're]
looking at, and I don't know why it is.

**19:10 Samuel Hales:** And that's what you've been looking into, right? You've been trying different alloys here.

**19:14 Sterling Baird:** Yeah, very much, like, compositional tuning, [alloy] discovery.

**19:19 Samuel Hales:** Yeah, putting that in there would be cool. Yeah, and I guess just the final… being able to
look at the cure depth and the hardness and such. There may be some other properties we can add in, but yeah, I think
that could be really interesting.

**19:40 Sterling Baird:** Yeah, that sounds good. Keep me posted. I'll send over one or two short paragraphs, and feel
free to use that or…

**19:49 Samuel Hales:** Sounds good. Yeah, thank you. For automating that sort of process, I guess, what would be the
most expensive steps there? I mean, we can get a cheapo printer if we're wanting to UV-expose something. You've done
a lot of automated mixing of things. Do you already have a sort of setup that could be used for that?

**20:13 Sterling Baird:** The closest match would be this liquid-handling robot that we have, and we could handle
viscous liquids and mix them in different ratios, and pretty easily attach some kind of curing light: either attach a
curing light that we move along with the liquid handler['s] gantry system, or we move well plates or other vials,
whatever it may be, to a curing station. And there's a precedent for doing that as well.

**20:49 Sterling Baird:** […] So I think, yeah, both of those are three-month lifts that turn into a year because
[the] student gets busy and…

**21:02 Samuel Hales:** How life works. Yeah.

**21:04 Sterling Baird:** Yeah, yeah. Like, I feel pretty confident, you know, given a month, if I was fully invested
and ordered things in advance, and maybe there's a student working with me, but it's 100% what I'm doing, then yeah,
in a month that can be done. But I think it's more like a year-long project, based on prior experience and anecdotes.
And that's with pushing, you know; that is with trying to drive [it].

**21:31 Samuel Hales:** Sounds good. And you're able to mix things that are more of a paste with your setup?

**21:44 Sterling Baird:** Yes, with caveats. People have done it, and it's usually not out of the box, but people do
it, and they can do it reasonably well. It's easier now than it was four years ago, because you can get clever with
how you [dose] (?), or you can get a little more clever with less overhead, to try to make sure you get the thing to
where you want it to be.

**22:14 Samuel Hales:** Okay, that's good. You know the sort of stuff.

**22:17 Sterling Baird:** But it would be a lot easier to know if there was a list of, oh, here are the binders, and
here's a prototypical formulation and the viscosity for it, and here's the types of mixtures that we'd be planning on
making for it. And so with those questions [answered], I could give a pretty definitive answer [on] how hard it would
be to do that kind of formulation.

**22:40 Samuel Hales:** Sounds good. Yeah, they've said they'd be willing to share their formulation with us, and I
guess they've said, kind of in general terms, the kind of stuff that's in there, but I don't know all of it at this
point.

**22:52 Sterling Baird:** I mean, even if it was just… even if it's just, like, here's the viscosity of it, it's
like, okay. And is it… does it move more like a slurry, or more like a resin?

**23:09 Samuel Hales:** Yeah, I think a little bit more of a slurry. But yeah, I guess it's probably not quite [a]
paste.

**23:17 Sterling Baird:** I had actually done… that's right, I had done a project focused on slurries, battery
[slurries] (?) in particular.

**23:26 Samuel Hales:** Okay. In any case, I think it's a good place to start from either way.

## Notes for the reader

- **The company.** The call never names it. It covers things the company told Nathan and Sam: its process
  problems, particle sizes, binder contents (wax, lower solids loading), a possible donated printer and possible
  graduate student funding. Keep the company unnamed wherever these are repeated.
- **"This liquid-handling robot that we have" (20:13)** is the OT-2 that digital-wetlab runs. Sterling asked for the
  "Formulation work on the OT-2" section of PR 229's note during this call, about seven minutes in.
- **"A few nice processes for that" (08:08)** is Sam's reference to making spherical metal powder, presumably the
  lab's ultrasonic atomizer. Sterling's reply about compositional exploration and custom powder supply points the
  same way.
- **The funding remarks (14:27–16:12)** are Sterling reading PR 229's funding comment: the active awards, and Janis
  Terpenny as program officer on most of the NSF ones.
- **"Sending that over to him" (16:29)** is Nathan Crane, who is collecting the projects for the company.
- **Sterling's estimates:**
  - formulation screening alone is "a pretty standard lift": a three-month job that becomes up to a year to first
    major results with a student, "but it's not multiple years";
  - printing on a donated printer, including the debinding and sintering, is "more like a two-years-out kind of
    lift";
  - pastes are possible "with caveats".

## Corrections that change the meaning

| Time | Captions | Reading |
|---|---|---|
| 01:36 | "Mental 3D printing company" | [metal] 3D printing company |
| 05:04 | "screening of different monitors" | [monomers] |
| 08:08 | "I know you have fewer nice process for that" | [a few] nice process[es] |
| 08:58 | "the real logical Property"; "not actually doing sintering and binding, or sorry, binding and all that" | [rheological] properties; [debinding and sintering], with the self-correction dropped |
| 10:17 | "would have our experience with doing by Doing the centering Sorry, de binding and sintering" | [more] experience with doing the [debinding] and sintering |
| 11:21 | "Like a lot more Dr. Blaine's" | [doctor blading] |
| 11:23, 12:50 | "ceramic fat photo"; "that photo processes"; "continuous fat photo printing methods" | [vat photo], Sam's shorthand for vat photopolymerization |
| 11:48 | "your source res" | source [resin] |
| 12:25 | "more folks excited about ceramics" | more [focused on and] excited about ceramics |
| 12:50 | "like clip. where they… Um, daddy. that you have at the bottom of the vat" | [CLIP], with "daddy" dropped as […]. It may be "dead zone", CLIP's name for the uncured layer (?) |
| 14:27 | "I think you're kind of has been a lot of government funding flowing towards it" | there [hasn't] been a lot (?), which matches PR 229's finding that federal money for this is scarce |
| 15:36 | "But stop pulling up much for me" | [It's not] pulling up much for me (?) |
| 15:51, 16:12 | "Janice Turpini"; "Janice" | [Janis Terpenny], NSF CMMI Advanced Manufacturing |
| 16:56 | "Trippington Have they" | […] have they |
| 17:58 | "So they picked one, I guess." | kept as heard; it could also be "so, take your pick, I guess" |
| 18:08 | "I'm just finding both"; "the Monomer you know. Finder Formulation optimization" | […]; monomer, [binder], formulation optimization |
| 18:55, 19:14 | "a pretty narrow set of avail systems"; "compositional tuning outlet discovery" | [alloy] systems; compositional tuning, [alloy] discovery |
| 20:49 | "You'd be curious, Ashley" | […] |
| 21:44 | "how you dosage" | how you [dose] (?) |
| 23:17 | "Battery studies in particular" | battery [slurries] (?) in particular |
