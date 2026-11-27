# Aluminum alloys for aerospace and space: a student's interview with Sterling Baird, 2026-11-24 (redacted)

A student turning a long, technical review article into a plain-language piece for a writing class interviewed
Sterling in his office on Nov 24, 2026, as someone working in the field. The article is M. A. Tunes, "The Legacy and
Future of Aluminum Alloys: Space Exploration and Extraterrestrial Settlement", *ACS Materials Au* 6(1), 1–27 (2026),
[doi:10.1021/acsmaterialsau.5c00139](https://doi.org/10.1021/acsmaterialsau.5c00139) (open access, CC-BY; full text
also at Europe PMC, PMC12810036). Before the meeting the student watched Sterling's MS&T 2026 talk, "Let's discover
stronger aerospace alloys 10x faster with AI at a tenth of the cost"
([YmvaeqOQAU4](https://www.youtube.com/watch?v=YmvaeqOQAU4)). The student had emailed three questions ahead: what
Sterling does to test new materials and get them ready for space, whether current materials like aluminum get adapted
to the needs of space, and what other applications these materials have.

**Redacted for a public repo.** The student is not named; keep it that way in commits, PRs and comments. Left out: the
student's name, course and the closing logistics (marked *[...]*). Nothing Sterling said about the subject is cut.

How to read it:

- Sterling answered from memory, in conversation. The [table of his statements](#sterlings-statements-to-check) below
  numbers the ones to check.
- The words are Whisper `large-v3`'s, from two full passes, checked against the phone's own transcript, then cleaned.
  **[Square brackets]** mark words that were changed or added for sense, or a best guess at a misheard word (see the
  [corrections](#corrections) at the end). **(?)** marks a reading that is still a guess. *Italics* are stage
  directions. Filler words, false starts and repeated "yeah"/"okay" replies are trimmed without a mark.
- Times are mm:ss from the start of the 15:21 recording.

## Summary

- **The assignment (00:00):** turn a long, technical article into plain language, and interview someone in the field.
- **Testing for space (00:55):** cryogenic and elevated-temperature mechanical testing, since performance depends on
  temperature and space is very cold, and at times very hot.
- **Adapting aluminum, and making alloys do different things (01:49):** the materials science tetrahedron (structure, properties,
  processing, performance, with characterization in the middle; Sterling emailed the student the figure during the
  meeting). Start from performance requirements, find the properties and tests tied to them, and tune composition and
  processing. There are almost always trade-offs. People have done this for millennia; some now use autonomous
  experimentation, as Sterling's lab does.
- **Other applications (05:31):** automotive, especially anything weight-sensitive such as the frame. Launch cost per
  pound is why weight matters so much in space. The "quadrillion dollars" in the video was the cost of exploring the
  composition search space.
- **Navy ships (06:58):** little aluminum, a lot of copper and bronze, because weight matters less for something that
  floats, and because of cost and seawater corrosion.
- **Corrosion (07:57):** aircraft face corrosion over decades of service; for rockets the concern is the trip up.
  Arrhenius behavior (diffusion) and the galvanic series; low temperature and a ductile-to-brittle transition; damage
  done before launch; what the metal touches inside a rocket.
- **Why aluminum (12:02):** the sweet spot of weight, strength and cost. Titanium is strong and light but costs more,
  and aluminum is easier to process in many methods. A 50-50 aluminum-copper alloy would be a compromise that serves
  neither aerospace nor naval use well. Metal matrix composites trade properties too.

## Sterling's statements to check

Numbered for the check Sterling asked for ("validating statements that I made and finding support and resources
for that"). Each is Sterling's own wording from the transcript, trimmed; the time is where it starts. The right-hand
column says what a check would need to settle. It does not say whether the statement is right.

| No. | Time | Sterling said | What to check |
|---|---|---|---|
| 1 | 01:11 | Testing new materials for space: "Cryogenic testing is one: cryogenic mechanical performance, and elevated-temperature mechanical performance." In space "it's really cold, or at certain times it's really hot", so "the performance is going to depend a lot on [temperature]." | Which tests actually qualify an aluminum alloy for spaceflight, and whether temperature extremes lead the list (alongside thermal cycling, vacuum, atomic oxygen, radiation and impact). The temperatures structures see |
| 2 | 01:49 | Asked (in the student's email) whether current materials like aluminum get adapted to fit the needs of space: "I would say very much so with aluminum alloys. And maybe the video kind of gave a sense of that." (The student summed the video up as "we need better aluminum alloys for aerospace applications.") | How today's aerospace aluminum alloys were adapted for space (for example Al-Li for cryogenic tanks), and what they still can't do (temperature capability, printability, strength at low density) |
| 3 | 02:55, 04:11 | The materials science tetrahedron: "structure, properties, processing and performance, with characterization [in the middle]." Start from the performance requirements, find the properties tied to them and the tests that measure them; composition and processing are "your tunable variables." | Where the tetrahedron comes from and its usual form; whether design practice really runs from performance back to composition and processing |
| 4 | 04:11 | "There are almost always trade-offs between those kinds of things", agreeing that an alloy made more radiation resistant "probably loses properties in, like, tensile strength." | Strength against ductility and toughness in general; radiation resistance against strength in aluminum alloys in particular |
| 5 | 04:50 | People "have been asking this question for millennia" (the Bronze Age, the Iron Age, steel industrialization), "and then some people are using autonomous experimentation" to work out how composition, processing and structure connect. | Self-driving labs and closed-loop alloy discovery: what has been shown so far, especially for aluminum alloys |
| 6 | 05:42, 06:31 | Beyond aerospace, "automotive is pretty huge": the frame, for example, and "anything that is particularly sensitive to weight." | How aluminum demand splits by sector, and where aluminum is used in cars today |
| 7 | 05:46 | "The amount of money it costs to send a pound into space is ridiculous." | Launch cost per pound or kilogram, then and now |
| 8 | 06:10 | The "one quadrillion dollars" in the video was the cost "to explore all of the compositions": "that was the search space." | The figure in Sterling's MS&T 2026 talk and how it was worked out |
| 9 | 06:58 | "One place where you don't find aluminum very much is in Navy ships. You find a lot of copper and bronze on Navy ships." | Where naval ships use aluminum (superstructures, aluminum-hulled classes, fast craft) and where they use copper alloys (propellers, seawater piping, valves, pumps) |
| 10 | 07:17 | "Aluminum has much lower density than copper and bronze. But it's not that hard to get something to float. The weight requirements are far less restrictive for ships." | How much weight matters in ship design (stability and topside weight, speed, fuel), and the densities |
| 11 | 07:39 | For copper and bronze on ships, "part of it is cost, but a lot of it has to do with corrosion resistance. Copper and bronze have better corrosion resistance than the aluminum alloys in seawater." | Seawater corrosion of marine aluminum alloys (5xxx, 6xxx) against copper-nickel and nickel-aluminum bronze, including biofouling and galvanic coupling |
| 12 | 08:08 | Airplanes "go through a lot of different conditions", and "these things will be in service for decades", so "having corrosion affect key mechanical properties, that could be a big deal." | Corrosion in aging aircraft: how it affects structural properties, and well-documented cases |
| 13 | 09:04 | "For rocketry, it's more on the way there. On the way there, things might be very hot, and you might get accelerated corrosion based on differences in temperature." | Which corrosion and oxidation problems launch vehicles actually have: on the pad, in ascent, and in orbit |
| 14 | 10:00 | "The Arrhenius equation... that one's more for diffusivity... At higher temperature, you get more diffusion." Then (10:28, most likely Sterling): "So the higher the temperature, the more corrosive things get." | Whether corrosion rates follow Arrhenius behavior, and where they don't (for example falling dissolved oxygen in open systems) |
| 15 | 10:35 | "You can still get corrosion at low temperatures. And that can be even worse sometimes, because you can get the ductile-to-brittle transition... it's still brittle." | Whether aluminum alloys have a ductile-to-brittle transition at all, how they behave at cryogenic temperatures, and which metals do embrittle in the cold |
| 16 | 11:11, 11:29 | Corrosion on the ground means "you may have already compromised your mechanical performance by the time you're there." And, flagged "I would need to check on this one": what the metal is "in contact with inside of the rocket" could affect it, "a lot of different fluids and gases... especially when you've got people involved." | Corrosion before launch; compatibility of aluminum alloys with propellants, oxidizers and hydrogen (embrittlement), and with crew-cabin humidity |
| 17 | 12:24 | "Copper and bronze are generally less expensive" (correcting the student, who had said they were a little more expensive). | Price of copper and bronze against aluminum and its alloys, per kilogram and per unit volume |
| 18 | 12:34 to 13:15 | Aluminum is "the sweet spot of mechanical properties, weight, strength, and cost." Titanium "is awesome for the weight and the strength. Not as much on the cost." Aluminum can be easier to process in a given manufacturing method, has "a very rich history" in these applications, and "you might be able to do things with aluminum that would be hard to do with titanium." | Specific strength against cost for aluminum, titanium, steel and magnesium; manufacturing differences between aluminum and titanium |
| 19 | 13:27, 14:25 | Asked whether the two can be mixed: "you can do a 50-50 aluminum-copper alloy," but it would be "middle of the road for everything": not competitive on weight and strength for aerospace, and "not as corrosion resistant, and it's more expensive" for naval use. "There are applications like that. I just don't know, off the top of my head, anything that's using aluminum-copper alloys." | What aluminum-copper alloys look like across the composition range (the phases near 50-50), and which are in service: 2xxx aluminum alloys in aerospace, aluminum bronzes and nickel-aluminum bronze in naval use. The student may have meant aluminum and titanium (titanium had just come up), so titanium alloys with aluminum too |
| 20 | 15:03 | "Exactly", agreeing that metal matrix composites, too, gain some properties and lose others. | What reinforcement (for example SiC in aluminum) gains and costs |

## Transcript

### 00:00 The assignment

**[00:00] Student:** The article I sent you... the whole assignment basically is: take an article like that, where it's
long and wordy and science-y, and shift it into something that normal people understand, into normal people's terms.
So this is an assignment, not a semester-long project.

**[00:18] Sterling:** Okay. Gotcha.

**[00:20] Student:** And then they're like, "interview someone that's in that field." And I was like, I'm pretty sure
Sterling does stuff with space materials.

**[00:31] Sterling:** Yeah. So what kind of questions do you have?

**[00:35] Student:** Let's see what I said. And then I also watched your video that you sent me, which was helpful. That
was kind of cool.

### 00:55 Testing materials for space

**[00:55] Student:** The first question was: what do you do to test new materials and get them ready for space?

**[01:11] Sterling:** Cryogenic testing is one: cryogenic mechanical performance, and elevated-temperature mechanical
performance.

**[01:22] Student:** What was cryogenic testing? What kind of testing?

**[01:24] Sterling:** It's just very low-temperature testing. So if you put something in space, it's really cold, or at
certain times it's really hot. So the performance is going to depend a lot on [temperature].

**[01:41] Student:** Cool.

### 01:49 Adapting aluminum, and making alloys do different things

**[01:49] Sterling:** Oh yeah, some of your other questions. *(He reads the questions the student emailed; the second asked
whether current materials like aluminum get adapted to fit the needs of space.)* So yeah, I would say very much so with
aluminum alloys. And maybe the video kind of gave a sense of that.

**[02:03] Student:** Yeah, [it] gave a sense of that. It was like, "we need better aluminum alloys for aerospace
applications." And that was one question I thought of after watching the video: when you're making the aluminum
alloys, when you're melting them down and doing that whole process, how do you make them structurally different, to do
different things? Because, at least in the article too, it talks about how you want some to be able to prevent
radiation poisoning, some to be very durable with all the random debris just floating around in space, corrosion
resistance. How does the process go, to make them do different things?

**[02:55] Sterling:** Yeah, this, I would say, ties a lot back to the materials science tetrahedron, if you want to put
some kind of figure in here. *(He sketches it.)* Your structure, properties, processing and performance, with
characterization [in the middle]: that's kind of the thing you need to be able to know what any of these are.

**[03:32] Student:** Can I take a picture of that?

**[03:35] Sterling:** Yeah, or I'll just... here, let me just send you the [figure]. *(He emails the student Wikimedia's
materials science tetrahedron.)* And the question is, how do we get something that is better suited towards, like,
radiation resistance...

**[04:01] Student:** ...or the different things that it needs? Because I assume that if it's more radiation resistant,
it probably loses properties in, like, tensile strength.

**[04:11] Sterling:** There are almost always trade-offs between those kinds of things. And so: okay, what are your
performance requirements? All right, what properties do we need to measure, or what properties are tied to that
performance? What kind of tests would you need to run there? And then your structure and processing, with composition
being a part of this: what's the composition, and what processing did you use to get it to its final state? Those are
now your tunable variables, to try to figure out how we get the properties that we need for the performance that we
want.

**[04:50] Sterling:** And that's what people have been doing for millennia, trying to answer those questions. [That's]
kind of why we have the Bronze Age and the Iron Age, and steel industrialization and things like that. People have been
asking this question for millennia. And then some people are using autonomous experimentation to try to figure out
how [composition], structure and processing [connect]...

**[05:17] Student:** That's what you guys do, right?

**[05:22] Sterling:** Yeah. That's right.

### 05:31 Other applications, and why weight matters

**[05:31] Student:** Then you also have: what other applications do these materials have?

**[05:36] Sterling:** So, beyond aerospace, is that what you're saying?

**[05:38] Student:** Yeah, more in, like, everyday life, I guess.

**[05:42] Sterling:** Automotive is a big one. So automotive is pretty huge. And as you can imagine, space has really
stringent [weight requirements]: the amount of money it costs to send a pound into space is ridiculous.

**[06:00] Student:** Oh yeah, I bet. And I remember seeing... I don't know if it was talking about sending things to
space, but one thing the video talked about, I was like, "one quadrillion dollars"...

**[06:10] Sterling:** Oh yeah. To explore all of the compositions.

**[06:13] Student:** Yeah, okay.

**[06:16] Sterling:** Yeah, so that was the search space. [Not] outer space things (?). Automotive is a big one.

**[06:26] Student:** What parts of automotive? Like, I guess, like the [fender]?

**[06:31] Sterling:** Oh yeah. For example, the frame. You get into some different... that's one you'd probably [want
to] look into: where does aluminum get used in cars right now? And then it kind of becomes anything that is
particularly sensitive to weight.

### 06:58 Navy ships: copper and bronze rather than aluminum

**[06:58] Sterling:** And so one place where you don't find aluminum very much is in Navy ships. You find a lot of
copper and bronze on Navy ships.

**[07:13] Student:** Just because aluminum's too dense?

**[07:17] Sterling:** So, aluminum has much lower density than copper and bronze. But it's not that hard to get
something to float. The weight requirements are far less restrictive for ships.

**[07:32] Student:** Oh yeah, because you've got buoyancy. So you might as well have denser things that make it float
harder.

**[07:39] Sterling:** And copper and bronze: I think part of it is cost, but a lot of it has to do with corrosion
resistance. Copper and bronze have better corrosion resistance than the aluminum alloys in seawater.

**[07:51] Student:** Yeah, that makes sense.

**[07:54] Sterling:** So I think between cost and corrosion, that's where [it comes from].

### 07:57 Corrosion in space, in aircraft and in rockets

**[07:57] Student:** Yeah, that makes sense. So, speaking of corrosion: what kind of corrosion happens out in space?
Because there's not as much water floating around.

**[08:08] Sterling:** Yeah, it's a vacuum. So when it comes to... yeah, that's an interesting question. I hadn't thought
of that either until just now. So if we take airplanes rather than rockets: airplanes will go through a lot of
different conditions. You've got snow, and you're going around the world. So while it might not be at the same level as
seawater, like something being submersed in seawater constantly, that does have its own corrosion requirements. And
[there's] the fact that these things will be in service for decades. So over the course of decades, having corrosion
affect key mechanical properties, that could be a big deal. I think for rocketry, it's more on the way there. On the
way there, things might be very hot, and you might get accelerated corrosion based on differences in temperature as
well.

**[09:22] Student:** Yeah, makes sense. That's right, because there's that one... I'm trying to remember my materials
science right now. I don't remember the equation right now. Never mind. 'Cause I feel like, at least in materials
science, you guys taught something about, like, a galvanic [series].

**[09:54] Sterling:** Yeah, the galvanic [series].

**[09:56] Student:** But then I feel like there's also something else with corrosion that, like, was [about]
temperature.

**[10:00] Sterling:** Yeah. Arrhenius, sometimes. This Arrhenius equation. But that one's more for diffusivity.

**[10:08] Student:** Yeah.

**[10:09] Sterling:** Like diffusivity constants: at higher temperature, you get more diffusion. I'm trying to think,
for corrosion... I can't remember.

**[10:16] Student:** I'd have to go back and look at [my] notes and stuff. Maybe it had nothing to do with corrosion;
maybe I'm just thinking that it does right now. But yeah, temperature effects.

**[10:28] Sterling (?):** So the higher the temperature, the more corrosive things get. Does that make sense?

### 10:35 Cold, brittleness, and damage before launch

**[10:35] Sterling:** And you can still get corrosion at low temperatures. And that can be even worse sometimes, because
you can get the ductile-to-brittle transition, for example. And so then you get this mix of: well, maybe the corrosion
was slowed down, but the fact that we're in this low-temperature range means that it's still brittle, which is what we
don't want.

**[10:59] Student:** Is it possible that, as it's corroding, it gets up into space, where the water kind of disappears
for the most part, but then, just because of that low temperature and the corrosion that's already happened...

**[11:11] Sterling:** You may have already compromised your mechanical performance by the time you're [there].

**[11:16] Student:** Or even if the mechanical performance is technically still good at the instant you entered space,
over time, because of that cold temperature, it could reduce it even more, from the corrosion that's already happened.

**[11:29] Sterling:** Yeah. And I would need to check on this one, but depending on what it is in contact with inside
of the rocket, [that] could be affecting things.

**[11:46] Student:** Yeah, that makes sense.

**[11:49] Sterling:** Because you deal with a lot of different fluids and gases inside the rocket, especially when
you've got people involved.

### 12:02 Why aluminum, and not copper, bronze or titanium

**[12:02] Sterling:** Cool. Yeah, any other questions?

**[12:05] Student:** One last question I just thought of: why aluminum specifically, and its alloys, over different
metals? I know you talked about how copper and bronze [are] a little bit more expensive and more dense...

**[12:24] Sterling:** Copper and bronze are generally less expensive.

**[12:28] Student:** Oh, yeah, sorry. So why not use copper and bronze, I guess? Or other materials?

**[12:34] Sterling:** It's the sweet spot of mechanical properties, like weight, strength and cost.

**[12:43] Student:** Oh, okay. So titanium...

**[12:44] Sterling:** [Titanium] is awesome for the weight and the strength. Not as much on the cost. And then you can
get into some other things, like: well, maybe it's easier to process aluminum in this manufacturing method than it is
for other ones. So you get manufacturability for a given application. There's a very rich history of using aluminum in
these kinds of applications.

**[13:15] Student:** That makes sense.

**[13:15] Sterling:** You might be able to do things with aluminum that would be hard to do with titanium.

### 13:21 Mixing aluminum and copper

**[13:21] Student:** Makes sense. Is there a way to potentially mix the two?

**[13:27] Sterling:** Yeah. So you can do a 50-50 aluminum-copper alloy. And I guess I'm trying to think of why... those
get used in different applications. But let's say it was just a complete trade-off: okay, this is a really nice
aluminum alloy, [and this is a] really nice copper alloy, and you get something that's sort of middle of the road for
everything. Well, now you're not very competitive in terms of the weight and strength for the aerospace applications,
and also you're not as corrosion resistant, and it's more expensive, for the naval [applications]. So aerospace and
maritime, naval applications have such different requirements that if you pick something in the middle, it's like,
well, what application is that serving?

**[14:23] Student:** Yeah, that makes sense.

**[14:25] Sterling:** And there are applications like that. I just don't know, off the top of my head, anything that's
using aluminum-copper alloys.

**[14:34] Student:** That makes sense. Lots of different things. 'Cause I also remember, from materials science, I think
they were talking more about metals versus mixing with polymers or something: how you could have metal matrix
composites, or something like that, where you had something in the middle, and the outer thing to help reinforce the
middle, for more properties. But then that, like you said, also reduced other properties.

**[15:03] Sterling:** Exactly.

### 15:06 Wrapping up

**[15:06] Sterling:** Cool. Does that seem like enough?

**[15:07] Student:** Yeah, that should be enough. Thank you.

*[...] Logistics. The recording ends at 15:21.*

## Corrections

What each source wrote, and why the transcript says what it does. "Pass 1" is Whisper with a one-sentence prompt and
voice-activity filtering; "pass 2" is Whisper with neither; "Recorder" is the phone's own transcript.

| Time | Heard | Written | Why |
|---|---|---|---|
| 00:27 | "Serling" (pass 1), "surely" (Recorder) | Sterling | Pass 2 |
| 01:11 | "chirogenic" (Recorder, pass 2 at 01:17) | cryogenic | Sterling's answer is about low-temperature testing |
| 01:34 | "the performance is going to depend a lot on, cool" | depend a lot on [temperature] | The sentence breaks off; temperature is what the sentence is about |
| 02:37 | "erosion resistance" (pass 2) | corrosion resistance | Pass 1 and Recorder |
| 02:55 | "Material Science of? Tetrahedron" (Recorder), "materials science of the tetrahedron" (pass 1) | the materials science tetrahedron | The figure Sterling emailed during the meeting (20:46 UTC) is Wikimedia's materials science tetrahedron |
| 04:50 | "Millenniums" (Recorder), "a millennium" (pass 1) | millennia | Sterling says "millennia" a sentence later |
| 04:57 | "Lebron's age and the. I'm an agent" (Recorder) | the Bronze Age and the Iron Age | Pass 1 has it; the sentence is about millennia of metallurgy |
| 06:11 | "explore all of the opposition" (pass 1) | explore all of the compositions | Recorder; the talk's figure is for the composition search space |
| 06:16 | "our space" (passes 1 and 2, and a beam-8 re-run), "Outer space on things" (Recorder) | [Not] outer space things (?) | Reads as Sterling separating the composition "search space" from outer space; unsure |
| 06:26 | "the defender" | the [fender] | A car part; Sterling answers "for example, the frame" |
| 07:05 | "Thank you for watching." (pass 1) | *(dropped)* | Invented in a stretch pass 1 skipped (07:00 to 07:40); taken from pass 2 and Recorder |
| 07:32 | "chips oh yeah because you've got point c" (pass 2) | Oh yeah, because you've got buoyancy | Recorder ("got buoyancy") and the re-run |
| 07:44 | "copper runs" (Recorder) | copper and bronze | Passes 1 and 2 |
| 07:48 | "than any of the aluminum Alloys" (Recorder) | than the aluminum alloys | Passes 1 and 2 and the re-run all lack "any of" |
| 08:00 | "what kind of corrosion happens with eye out in space" (Recorder) | out in space | Passes 1 and 2 |
| 09:53 | "galvanic scale" (all three) | galvanic [series] | The usual name; both speakers said "scale" |
| 10:01 | "Arenius", "Arenas" (Recorder) | Arrhenius | Passes 1 and 2; it is about diffusivity and temperature |
| 10:15 | "nodes" | [notes] | The student means class notes |
| 10:38 | "the ductile the brittle transition" (Recorder) | the ductile-to-brittle transition | The standard term; pass 1 has "ductile to brittle" |
| 10:49 | "that's going to get it's still incorporated" (Recorder) | it's still brittle | Pass 1 |
| 11:32 | "Owning to and check on this one" (Recorder) | I would need to check on this one | Pass 1 |
| 12:24 | "Copper and bronze, generally less expensive, oh, less" (Recorder) | Copper and bronze are generally less expensive | All three agree. Sterling is correcting the student, who had said "a little bit more expensive"; the student answers "Oh, yeah, sorry" |
| 13:01 | "other mods" (Recorder) | other [metals] | The comparison is with titanium |
| 13:36 | "different athletes" (Recorder) | different applications | Pass 1 |
| 14:05 | "navel" (Recorder) | naval | Pass 1, and "maritime, naval applications" right after |
| 14:28 | "off the top right hand" (Recorder) | off the top of my head | Pass 1 |
| 14:46 | "Matrix Composites" (Recorder) | metal matrix composites | Pass 1 |
| 15:02 | "Thank you for your time, and I'll see you next time." (pass 1) | *(dropped)* | Invented at the end of the recording |
