# Desktop LPBF project chat, Nov 17, 2026 (redacted excerpt)

A redacted, trimmed transcript of a 30-minute in-person conversation on Tuesday, Nov 17, 2026 (about 1:20 pm MST)
between Sterling Baird and an undergraduate student about a research project: designing and building the lab's own
desktop laser powder bed fusion (LPBF) system with generative CAD. Sterling recorded it with Google Recorder. It is
cut down for the desktop LPBF work in `vertical-cloud-lab/digital-alloy-lab` (PR 266), which is public.

**Left out**, with an italic note where each cut falls: the student's name, background and plans (00:00–01:39); a
personal aside and FDM printer talk (13:21–15:05); a tangent on AI reasoning levels (19:43–20:21); arrangements for
the student's involvement, lab communication and people to contact (24:06–29:01); and the goodbyes (29:56–30:35).
Other students are not named. The recording runs on silently after 30:35.

**How to read it:**

- The words are Whisper `large-v3`'s, checked against Recorder's own transcript. Where Whisper skipped about 25 s
  (23:12–23:42), a second, targeted Whisper run recovered it.
- Speakers are **Sterling** and **Student**, labeled by reading, since Recorder's speaker labels were unreliable.
  "(?)" after a name means unsure.
- **[Square brackets]** mark words that were changed or added. **(?)** marks a guess, and **[…]** a dropped fragment.
  Filler words, false starts and short "yeah"/"okay" interjections are removed without a mark.
- Times are mm:ss from the start of the recording.

## Design points raised (summary, not transcript)

1. **Start from an adjacent machine.** Modifying a laser engraver that takes a MOPA fiber laser module came up at
   21:58, probably as the student's question to Sterling (the speaker labels there are unsure): "if it can cut metal,
   it can sinter it for sure." Sterling liked the idea: laser engravers are "about as adjacent as you can get" and
   already have a gantry, so powder spreading is the main LPBF-specific addition (21:58–24:06). Earlier he framed the
   build as a modified gantry or CNC-type system assembled from mostly OEM parts, where "the assembly [is] the custom
   part", with complete control over software, firmware and programmability. The student warned that commercial
   printer boards are often locked down, so the electronics may need replacing (07:08–08:31).
2. **A heated build plate matters for aluminum.** Pretty much no desktop system has one, and research-grade systems
   with heated plates and the right laser powers cost close to $400,000. The student's approach: a heating element
   inside a walled aluminum plate (aluminum spreads heat more evenly and quickly than steel), set on the engraver bed
   in place of its slats (22:30–23:42).
3. **The laser choice is one of the main decisions.** The lab won't make its own laser. The build uses mostly
   off-the-shelf components and probably reuses spreaders (21:49, 22:30).
4. **Two aims and a go/no-go point.** (a) Stay current on generative design of whole systems, not just generative
   CAD, and (b) get the system ordered, assembled, tested and in use as soon as possible. Partway through the
   semester, check whether the timeline is heading toward the multi-year build this would have been a year ago.
   Buying a commercial desktop unit stays an option, probably after the semester (15:05–16:11, 20:21–21:49).
5. **Oxygen.** Fine metal powders oxidize, so keeping oxygen out is one of the hardest parts. Powder always carries
   more oxygen than cast metal, and its surface oxides end up inside the part (03:59–04:21).
6. **Agents in the design loop, with a check on materials.** Agents could select build materials, look up cost, and
   run FEA and laser simulations (16:23). The student found AI material picks unreliable: every model he asked
   first recommended a PEI build plate for printing Ultem, which is itself a PEI. Giving the model options to choose
   between helps (16:40–19:36).
7. **Powder handling.** Turnkey powder-dosing systems cost $100,000–300,000 and don't suit alloy powders or the
   quantities needed (a couple hundred milliliters or more). The lab built its own powder doser with generative CAD
   (08:57–11:04).
8. **Phasing.** The student would start with assembly and manufacturing of parts. Materials-science work comes once
   the equipment is "more or less fixed" (29:01–29:55).

## Transcript

*[00:00–01:39 left out: the student's background and plans.]*

### 01:39–06:49: Why metal powder bed fusion, and why build one now

**01:39 Sterling:** I'm trying to think. There's one thing that pops to mind. So these laser powder bed fusion systems, which, excuse me, at this point [I've] shown a couple times…

**02:10 Student:** They're definitely getting bigger, especially in aerospace applications, both everything and space. So I wondered how they make the powder. […] That was a copper powder, right?

**Sterling:** Yeah. Aluminum and copper. […] I don't remember if I showed this, but with [the] laser SLS process…

**Student:** Yeah, exactly. So I've seen videos on SLS before. [I've seen] a lot of people using it for [titanium and nickel alloys] (?). So they can make custom parts that would be really difficult and really expensive to machine. Especially when it comes to titanium and nickel alloys, a lot of the times it's the thermal properties you want, a little bit less [the] mechanical properties. Because SLS and powder directed energy deposition, they're still mechanically more brittle, right?

**03:24 Sterling:** Yeah, the microstructures [aren't] the best.

**03:29 Student:** It's porous, so like cast iron, it's got little flaws on the inside, and [in] tension those flaws spread out.

**03:39 Sterling:** And in most cases, the powders being used for metal 3D printing are based off of an alloy that was cast, traditionally cast and wrought and stuff. So a big part of it is: can we find ones that are uniquely geared towards metal [AM]?

**03:59 Student:** Especially since almost all metals have strong oxidation reactions when they're in fine powder form?

**Sterling:** Yes.

**Student:** So keeping oxygen out is probably going to be one of the most difficult parts. You're always going to have a higher oxygen content in the powder than [in] a cast part.

**Sterling:** So [you] deal with surface oxides.

**04:21 Student:** [And] now your surface oxide is [in] the middle of the part.

**04:25 Sterling:** Yeah, yeah. A lot of things like that. I think there's some interesting research here. In terms of a potential project you could work on: right now we're looking into buying a desktop-sized metal 3D printer, and they're becoming more popular. They're growing, they're dropping in price right now too. We've got almost a race right now to see who can come up with the most consumer-, prosumer-friendly SLS desktop printer.

**04:57 Student (?):** Yeah, I'm kind of wondering, is Formlabs going to try to do that? […] Formlabs, they only do plastics. They have mostly nylon and TPU SLS powders. They're trying to bridge into… they do have ceramics and other stuff that's a total pain to work with. Their ceramics are still technically resin or SLS: it's basically bits of ceramic suspended in a plastic matrix, and then you have to [sinter] it afterwards. So you get a ceramic part, but it's…

**05:40 Sterling (?):** So yeah, it does seem like a race to find that kind of sweet spot. It's probably [going to be] in the next five years [that] we're going to see somebody that has an SLS metal 3D printer under [$]10,000.

**05:56 Student:** I don't see it ever being [Bambu]-level or Elegoo-level pricing. […] The powder itself is so expensive to manufacture.

**06:05 Sterling:** So that's a good point. […] [It's] why we're never going to see a successful consumer printer that can do PEEK. So with that, there are some that we could buy that would not have the same level of customizability that we actually want. And a year ago, I wouldn't have gone down this line of thinking very, very far. It wouldn't even really [have] crossed my mind four years ago, because of just how kind of tedious it would be. But I think in the current frame of things, designing and building our own laser powder bed fusion system is not all that out of the question.

### 06:49–08:57: Buy, modify or build; an open gantry instead of a locked-down printer

**06:49 Student:** It's better to buy, and then better to modify, and then better to make it yourself. That's what […] all of us kind of explain to people. We have a lot of engineers that are like, "we want to make this screw for a thing." No, buy the screw.

**07:05 Sterling:** You can buy the screw. […] And with this one, it is becoming so easy to do the equivalent of reverse engineering or from-scratch design that, for this particular one, it would be a modification of an existing gantry-based system with a lot of OEM parts, but [put] together [differently]. It's more about the assembly being the thing that is the custom part.

**07:42 Student:** So take apart the gantry, build [it] into a [new] gantry, put it in, update the firmware so it operates well with the same gantry.

**07:48 Sterling:** Yeah.

**07:49 Student:** And then what would the purpose of this modification be?

**07:53 Sterling:** To have a lab-scale, yeah, like one of these desktop-size laser powder [bed] fusion systems, with complete control over the software, firmware, programmability.

**08:04 Student:** So you have to be careful: a lot of printers, their boards are kind of locked down. You can't just reprogram the boards. A lot of the electronics you might have to replace from scratch too.

**08:19 Sterling:** Yeah, it's more like potentially using a modified CNC, not taking some existing printer necessarily, but [as] for FDM, taking just some kind of [gantry] system.

**08:31 Student:** A lot of desktop FDM printers are pretty easy to modify, and that's why Enders are so popular, even though they're really unreliable. Every single part, there's a million different versions you can find on Amazon to swap it out with. People turn them into paste extruders, or hot glue extruders, or even marker-writing things.

### 08:57–11:04: Powder handling, and the lab's generative-CAD powder doser

**08:57 Sterling:** I brought up the powder dosing a little bit; there's a poster downstairs. A longstanding challenge in laboratory automation has been powder handling. We're pretty solid [on] liquids, even viscous liquids, which is tough; people can do it. Powders are hard, especially fine powders. And if you were to buy a turnkey system for most of these, it's between $100,000 to $300,000 to basically say, "okay, I've got [20] powders and I want to dose them in different ratios." It's kind of at that scale for things, but they are not well suited to alloys, like alloy powders and the amounts that you need. A lot of times it's just focused on chemistry automation and little flasks about the size of [a vial].

**09:52 Student:** And you're going to deal with a couple [liters] at a time?

**09:55 Sterling:** Yeah, [potentially]. So even if it's a couple hundred milliliters, that's still beyond what a lot of these other vendors offer. And then they're not tested on these kinds of metal alloy precursors. That's one where we…

**10:13 Student:** Probably a lot of weighing powder by hand.

**10:15 Sterling:** Yeah, that's a very typical thing. We ended up making a powder doser based on using generative CAD. [Two students, one of them in the machine design class,] were primarily the ones [spearheading it]. It was an interesting timeline. We've got, like, week one: "oh, we're going to be using generative CAD, we're a little bit worried about job security." […] Trying it out for a couple weeks: "our jobs are totally secure, we're fine." But then in the last couple months they're like, "oh, this is [a] night and day difference between when we started using this and [now]."

### 11:04–13:21: Generative CAD tools, and printing through an agent

**11:04 Student:** […] A lot of these things, I have the idea of what I want it to look like. It's just [that] CAD is a lot of little steps.

**11:55 Sterling:** […] I'm kind of interested to see how the pre-packaged options for some of these things are, like if you just go to ChatGPT.com and [ask for] this CAD thing, versus [an agent] running [in an environment]. I guess it just depends on what the environment has access to. At some point, they can install things.

**12:22 Student (?):** I really like having [it] use an existing CAD software instance [instead of] just creating a straight STEP file.

**12:27 Sterling (?):** Oh yeah. Anything like OpenSCAD, [CadQuery] (?).

**12:31 Student:** [Someone I know has] been having ChatGPT design stuff for him. He says the newest version of ChatGPT has been working really, really well, just creating STEP [and] STL files so he can 3D print, [and he] even tried having [it] slice one for him in Bambu Studio.

**12:51 Sterling:** And we, in the lab, when we print things (and this is maybe about 50% of our prints, maybe a little bit less), we have a specific workflow, [a `claude-print` GitHub workflow], and that spins up an environment that has the permissions and credentials to send prints to our 3D printers.

**13:11 Student:** What printers do you have in your lab?

**13:12 Sterling:** We have a bunch of Bambu printers, and they're pretty good with remote access and API stuff.

*[13:21–15:05 left out: a personal story, the student's own printers, filament choices, and the lab's multi-material FDM prints.]*

### 15:05–16:40: The project: an open-source LPBF system, designed with generative CAD

**15:05 Sterling:** So I think, with [your] background […], the design and assembly of an open-source laser powder bed fusion system, with this focus on generative CAD and kind of seeing how far we can take generative CAD on this, is the clearest immediate fit for a project that I'd see. That's really timely. And maybe we do just buy one. Buying one would probably be after the semester's over, in terms of the off-the-shelf [one].

**16:00 Student:** I think for sure, let's see what we can design on our own. Let's see how feasible it is. We might look at it and end up deciding, "you know what, it's going to take us three years longer and cost us just as much to make."

**16:11 Sterling:** And that's where, a year ago, I would have not even given it much thought. Things have changed, and things are changing.

**16:23 Sterling (?):** Now [with] generative AI, you actually have the manpower, I guess, to design all the parts. […] And in terms of agents, it's like selection of the build materials, looking at cost, running FEA on things, like running simulations of the laser.

### 16:40–19:32: How far to trust an AI's material choices

**16:40 Student:** How good is it getting at material selection? I found, in my experience with all the AIs I've tried, material selection can be a little bit iffy.

**16:49 Sterling:** That's interesting, yeah. I haven't been too particular about it. It's usually kind of assumed [what] we're going to be using [as the] material, or maybe it's a little looser sometimes: just finding what's on McMaster, and it happens to choose aluminum or some form of steel. Or [if] we're going to be printing it, it's defaulting to PLA or…

**17:12 Student (?):** [It] defaults to PETG a lot. If you have an H2D, there's better filaments than PETG.

**17:20 Sterling:** Yeah. And so then sometimes we will say, like, "okay, we probably want a specialty filament for this."

**17:30 Student:** A while ago, as I've been learning more about 3D printing, I decided to start trying all the different [AIs], and I asked [them]: if I'm printing with Ultem, what material should my build plate be made of? It's an interesting test, because everything online basically says that PEI build plates are like the thing for 3D printers. Any FDM 3D printer you look at that's consumer or prosumer level, it's a PEI build plate of some sort.

**18:04 Sterling:** Yeah. Textured, if it's Bambu.

**18:06 Student:** PEI and Ultem are the same thing.

**18:08 Sterling:** Oh, okay. Gotcha.

**18:10 Student:** So each AI, [Claude], Gemini, ChatGPT, they all said, "oh yeah, use a PEI build plate." And then I point out to them: hey, they're the same material, they [bond] and damage each other. And [they'd] be like, "oh yeah, you might want to put some glue or some tape in between." I think [Claude] was the only one who was like, "oh, maybe try these other options." […] In industry, they print with Ultem and other high-temperature plastics all the time, but because it's these commercial-level printers, there's just not as much information about it online. So all the AIs I've [tried] failed at that material selection test quite spectacularly.

**19:03 Sterling:** When was that?

**19:05 Student:** That was like two months ago, so it might be different now.

**19:10 Sterling:** I mean, six months ago versus two months ago, a year versus six months: I don't know how things are going to change. But for me, within the last two months is equivalent to now.

**19:26 Student:** It might have been a little bit longer than two months. It might have been at the very end of the summer.

**19:28 Sterling:** Still relatively recent. And then it's like, what tools are available to it, in terms of…

**19:36 Student:** Or if you give it options to choose between, then it can evaluate those options a little bit better sometimes too.

*[19:43–20:21 left out: a tangent on AI reasoning levels and multi-agent tools.]*

### 20:21–21:58: Two aims, a go/no-go check, and mostly off-the-shelf parts

**20:21 Sterling:** So, if you'd be open to that, I would have you maybe set up a time to chat with [the two students who built the powder doser] about their experience with doing [the] generative CAD process and things like that. And I would see there being kind of this twofold approach here. One is: we get to figure out and really stay current on generative systems design, more than just generative CAD, really whole-systems design of things. [It's], I would say, like a race, right? I think for something where there is [a lot of] potential. And then on the other side: if we just get the system up and running, we get things ordered, assembled, tested, to try to start using it as soon as possible.

**21:19 Sterling:** And I think that we could also have a point in the semester [where] it's like, "okay, this is not going well," like this is projecting the timeline out to, like you're saying, a three-year delay. That's what this project would have been a year ago. It was like a three-year project sort of thing, in terms of [the] sort of classical "oh, we're going to build this thing from scratch," and it's very naive. But I think for this one, we're using mostly off-the-shelf components. We're not going to make our own laser. We'll probably be reusing spreaders and other stuff.

### 21:58–24:06: A laser engraver with a MOPA fiber laser as the base, and a heated build plate

**21:58 Student (?):** Have you thought about trying to modify a laser engraver with a MOPA fiber laser attachment?

**22:04 Sterling (?):** Ooh, I have not thought about that. But yeah, modifying a system that has… you know, in some sense, yeah, just finding a system with the right [fiber laser]. If [it] can cut metal, it can [sinter] it for sure.

**22:16 Student:** MOPA lasers tend to have that spread that's really nice for engraving. I know that [a company (name unclear)] came out with a laser engraver very recently that had a MOPA fiber laser attachment you could get for it.

**22:30 Sterling:** Okay. Yeah. So yeah, that would probably be one of the main things: just selecting the laser. Here's the other part: all of the desktop systems, pretty much none of them have heated build plates, which is really important for aluminum. And so either we need to spend close to $400,000 for the research-grade systems that have heated build plates and the right laser powers… Heated build plates for the miniaturized ones don't seem to be much of a thing yet.

**23:02 Student:** No. But [a] heated build plate isn't the hardest thing to add. You can just put a heating element inside an aluminum plate, put some walls on that aluminum plate, which should give a pretty even spread. You can even do steel; steel doesn't spread heat as evenly [or] as quickly. And then you can put that on top of almost any existing system: any laser engraver has slats already, where you can put your wood or whatever. You don't have to worry about stuff falling through anymore, so you can take the slats out and put the…

**23:42 Sterling:** Yeah, I like the idea of maybe we could do some modification of an adjacent system, and laser engravers are about as adjacent as you can get to that. […] The spreading [is] kind of the other thing that's unique to laser powder bed versus [a] laser engraver, but you'd already have a [very accurate (?)] gantry system.

*[24:06–29:01 left out: arrangements for the student's involvement, lab communication, and people to contact.]*

### 29:01–29:55: Where the student would start

**29:01 Sterling:** Because it's very multidisciplinary: from materials science to machine design to CS. So part of
it is to give a little bit of a sampling and then see where [you] might kind of fit.

**29:30 Student:** In my case, it's probably going to be something about assembly and manufacturing of parts. […] I
love making things.

**29:42 Sterling:** So if you enjoy that and you'd be open to at least starting out [on] the projects like that, then
it could be: "okay, well, now we have the equipment, and this is more or less fixed, and we're going to be tackling
some of these more materials-science challenges."

*[29:56–30:35 left out: scheduling and goodbyes.]*
