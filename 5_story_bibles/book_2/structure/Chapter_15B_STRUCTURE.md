# Chapter 15B: Solo Operation

```yaml
# Scene Generation Metadata
book: 2
chapter: 15B
type: scene_generation_prompt
scene_id: "book2_ch15b_solo_intel"
scene_type: investigation

# Scene parameters
timeline: { month: 6, event: "gala_infiltration_continued" }
location: "police_gala_fundraiser"
participants: [tess, korede, chief_whitford]
pov: tess

touchpoint_a: "Tess and Korede processing SecDef warning"
touchpoint_b: "Tess delivers CADENS corruption intel to Go Squad"

# Narrator persona
narrator_persona:
  pov_character: "tess"
  voice_reference: "2_method_actor/stewards/Tess_Whitford_Steward.md"
  voice_attributes:
    - cold precision in dangerous moments
    - warmth only with Leta
    - physical stillness preceding action
    - cutting humor as deflection

# Character knowledge states at chapter start
character_knowledge_states:
  tess:
    knows:
      - cadens_involved_in_cover_up (just learned)
      - secdef_coordinated
      - father_complicit
      - she_is_being_watched
    doesnt_know:
      - director_bourn_specifically
      - money_trail_details
      - full_quid_pro_quo
    believes:
      - must_continue_despite_warning
    emotional_state: "controlled_determined"

  korede:
    knows:
      - cops_are_racist
      - isaiah_cover_up_exists
      - tess_is_investigating
      - secdef_threatened_them
    doesnt_know:
      - tess_is_go_squad
    believes:
      - cant_go_back_in_there
    emotional_state: "exhausted_angry"

# Scene constraints
constraints:
  - Korede extracts cleanly (operational security)
  - Tess must remain to gather more intel
  - No physical violence
  - Father confrontation must be emotional, not direct accusation
  - Team identities protected

# Scene requirements
requirements:
  - Korede extracts with cover intact
  - Tess gathers complete intel (Who, What, How, Why)
  - Father hug scene - Tess nearly reveals disgust
  - Tess delivers intel to Go Squad at chapter end
  - Background news seed: "Mass disappearance of military junta leadership"

# Dependencies
dependencies:
  - 2_method_actor/stewards/Tess_Whitford_Steward.md
  - 2_method_actor/stewards/Korede_Owolowo_Steward.md
  - 2_method_actor/stewards/Ruth_Carter_Steward.md
  - 7_characters/arcs/CHARACTER_STATE_INDEX.yaml

tags: [investigation, father_daughter, institutional_betrayal, intel_gathering]
```

---

## Summary

After SecDef's warning, Korede extracts while Tess operates solo to gather complete intel. Tess overhears conversations revealing the full scope: Director Bourn ordered cover-up, SecDef paid from Defense budget, Chief Whitford coordinated locally. The father goodbye scene nearly breaks her cover. Chapter ends with Tess delivering devastating intel to Go Squad.

**Emotional Arc:** Decision to continue → Solo operation → Father confrontation → Team revelation

---

## SCENE 1: Decision to Split (Beats 1-25)

**Location:** Gala hallway
**Present:** Tess, Korede
**Tone:** Tactical planning under pressure

### Touchpoint A
Processing SecDef's warning. Deciding whether to abort or continue.

### Beats

1. Tess and Korede still in hallway, processing warning
2. Korede: "We should leave. He's onto us."
3. Tess: "We got CADENS. That's huge. But there's more here."
4. Korede: "Tess, he basically threatened us—"
5. Tess: "He threatened YOU. You're the one who asked questions."
6. Korede realizing: "You want me to leave. Give you cover."
7. Tess: "You're at your limit. I can see it. And you got the most important piece."
8. Korede: "Leta would kill me if I left you here alone."
9. Tess: "Leta would kill me if I kept you in a room full of racists discussing her girlfriend's investigation."
10. Korede knowing she's right, hating it
11. Tess: "You're not faking being sick anymore. You're actually done."
12. Korede: "What's your cover for me leaving?"
13. Tess: "Food poisoning. Oysters. I stay because I'm daddy's girl."
14. Korede: "And if something goes wrong?"
15. Tess: "Then you're outside, ready to call backup."
16. Returning to ballroom together, Korede visibly unwell (not faking)
17. Chief Whitford approaching: "Son, you look terrible."
18. Korede: "Think the oysters, sir. Should probably go home."
19. Chief (to Tess): "Take him. I'll call you a car."
20. Tess: "Dad, I can't leave your event. This is important to you."
21. Chief pleased—daughter choosing him over boyfriend
22. Korede: "Really, I'll be fine. Don't want to ruin Tess's night."
23. Tess walking Korede to entrance, private moment
24. Tess (whispered): "Park across the street. Watch the entrance. If I text 'headache,' something's wrong."
25. Korede leaving. Tess alone.

### Touchpoint B
Korede extracted cleanly. Tess operating solo now. Stakes higher but less volatile.

---

## SCENE 2: Solo Intel Gathering (Beats 26-70)

**Location:** Gala ballroom, various conversations
**Present:** Tess, officers, donors, guests
**Tone:** Surveillance, piecing together the puzzle

### Touchpoint A
Tess alone, playing Chief's proud daughter, hunting for intel.

### Beats

26. Tess turning back to ballroom, different energy now
27. Not girlfriend on a date—Chief's daughter at daddy's event
28. Officers greeting her differently: "Tess! Sorry about your boyfriend."
29. Tess: "He'll be fine. Weak stomach." (Laughing it off)
30. Chief at her side: "Proud of you, sweetheart. Staying to support me."
31. Tess (daughter role): "Of course, Dad. This is your night."
32. Chief's arm around her shoulders—possessive, affectionate
33. Tess feeling sick at the affection—he has no idea who she is

**First Intel Piece: CADENS Forensics**

34. Tess circulating, champagne in hand (not drinking, prop)
35. Two senior officers discussing "the Bennett situation"
36. Officer 1: "Thank God for federal assistance. Local forensics would've been a mess."
37. Officer 2: "SecDef came through. Owed Chief Whitford a favor from golf course."
38. Tess (innocent curiosity): "Federal assistance? For what?"
39. Officer 1: "Just procedural stuff. Inter-agency cooperation."
40. Officer 2 (slightly drunk): "CADENS has tech we can't touch. Enhanced imaging..."
41. Officer 1 giving him a look—shut up
42. Officer 2: "All public record anyway. Investigation cleared our guys."
43. **INTEL: CADENS provided "enhanced" forensics. SecDef coordinated. Chief Whitford requested.**
44. Excusing herself, moving to next group

**Second Intel Piece: The Altered Evidence**

45. At buffet table, overhearing conversation behind her
46. Three officers, not realizing she's Chief's daughter
47. Officer A: "Still can't believe they turned it around in 48 hours."
48. Officer B: "That's CADENS for you. Brought in their team, re-examined everything."
49. Officer C: "Re-examined? They changed the whole narrative."
50. Officer B: "Corrected inconsistencies. That's different."
51. Officer A: "Either way, bodycam footage suddenly showed 'justified force.'"
52. **Tess freezing: Bodycam footage was altered**
53. Officer C: "I heard the original analyst quit. Refused to sign off on revision."
54. Officer B: "Who told you that?"
55. Officer C: "Doesn't matter. Point is, CADENS analyst signed instead."
56. **INTEL: 48-hour turnaround. Original analyst refused. CADENS analyst signed altered report.**

**Third Intel Piece: The Money Trail**

57. Near bar, overhearing donor conversation
58. Not police—civilian donors, wealthy supporters
59. Donor 1: "Chief handled that crisis beautifully. Barely a ripple in polls."
60. Donor 2: "CADENS consultation doesn't come cheap. Where'd funding come from?"
61. Donor 1: "Defense budget, I heard. SecDef authorized personally."
62. Donor 2: "Unusual. CADENS usually bills through Homeland Security."
63. Donor 1: "Special circumstances. Wanted it quiet."
64. **INTEL: SecDef paid CADENS from Defense budget. Bypassed normal channels.**
65. Donor 2: "I'm sure it's buried in classified line items. Who audits Defense?"
66. Tess thinking: Ben could find this. Financial trail.

**Fourth Intel Piece: The Name—Director Bourn**

67. Circling back toward father, finding him with SecDef in alcove
68. They're speaking quietly—Tess approaching carefully
69. Chief seeing her: "Tess! Come here, sweetheart."
70. SecDef's eyes calculating as she joins them

### Touchpoint B
Three pieces gathered. About to get the final piece—Director Bourn's name.

---

## SCENE 3: The Full Picture (Beats 71-95)

**Location:** Gala alcove
**Present:** Tess, Chief Whitford, SecDef
**Tone:** Revelation disguised as casual conversation

### Touchpoint A
Tess joining father and SecDef. Fishing for final piece.

### Beats

71. Chief: "SecDef was saying what a lovely young woman you've become."
72. Tess: "Thank you, sir. Dad's always made sure I had opportunities."
73. SecDef: "Your father is very... protective of those he cares about."
74. Chief: "Absolutely. Family first, always."
75. SecDef: "That's why our arrangement worked so well. We both understand protecting what matters."
76. Tess playing confused: "Arrangement, sir?"
77. Chief (warning look at SecDef): "Just inter-agency cooperation, honey."
78. SecDef ignoring warning: "Your father needed help managing a public perception problem."
79. **SecDef: "I needed CADENS Director Bourn to understand the value of cooperative relationships."**
80. **DIRECTOR BOURN—the name**
81. Tess's brain firing: Bourn. CADENS Director. She ordered cover-up.
82. Chief uncomfortable: "We should discuss this later—"
83. SecDef: "Why? Miss Whitford seems smart. She understands how the world works."
84. SecDef (to Tess): "Sometimes doing the right thing means protecting institutions."
85. Tess: "Protecting the department's reputation, you mean?"
86. SecDef: "Exactly. One unfortunate incident shouldn't destroy public trust."
87. Chief: "The officers acted in good faith. Situation was ambiguous—"
88. SecDef: "Ambiguous situations require clear narratives. That's what CADENS provided."
89. **Tess hearing it: They KNOW it wasn't justified. Saying it out loud.**
90. Chief: "Director Bourn understood the bigger picture. Political stability requires—"
91. SecDef: "It requires people like us making hard choices."
92. Tess fighting to keep face neutral
93. SecDef: "Of course, Bourn's cooperation came at a price. Budget appropriations, facility access..."
94. **INTEL: Quid pro quo. CADENS covered up murder for funding.**
95. SecDef checking watch: "I should make remarks. Chief, shall we?"

### Touchpoint B
COMPLETE INTEL: Who (Bourn), What (altered forensics), How (Defense budget), Why (political stability + CADENS funding).

---

## SCENE 4: The Goodbye That Almost Breaks (Beats 96-130)

**Location:** Gala stage area → private office
**Present:** Tess, Chief Whitford
**Tone:** Emotional devastation masked as family moment

### Touchpoint A
Tess has complete intel. Needs to extract. Chooses to say goodbye to father.

### Beats

96. Chief on stage, preparing for speech
97. Tess approaching during pause—proper daughter behavior, less suspicious
98. Chief seeing her, smiling warmly: "Sweetheart? Everything okay?"
99. Tess: "Just wanted to say goodbye. Not feeling well. Heading home."
100. Chief: "Of course. Come here." Arms open for hug.
101. **Tess stepping into embrace. For ONE SECOND—**
102. **Her face shows it. Pure disgust. Revulsion.**
103. The man who covered up murder, hugging her like loving father
104. She can't hide it—just for that flash
105. Chief feels her stiffen, pulls back
106. Catches tail end of expression before she masks it
107. Chief (confused, hurt): "Tess... did I do something wrong?"
108. Question hanging in air, loaded
109. SecDef's attention sharpening from across room
110. Tess scrambling for recovery
111. Chief's eyes searching hers: "You looked at me like... what's going on?"
112. Tess's mind racing—what excuse makes sense?
113. Chief: "Talk to me. You're scaring me."
114. Officers nearby starting to notice tension on stage

**The Redirect**

115. Tess making a choice: Use truth, redirect it
116. Tess (voice shaking): "Dad... can we talk? Not here?"
117. Chief immediately protective: "Of course. My office. Now."
118. Leading her off stage, arm around shoulders
119. Into private office, door closing
120. Chief: "What happened? Did someone say something? Your boyfriend—"
121. Tess: "Korede. One of your officers..."
122. Chief's expression darkening: "What did they say to him?"
123. Tess: "Racist comments. 'Articulate.' 'One of the good ones.'"
124. Chief (angry): "Who? Give me names."
125. Tess: "That's not the point. I brought him here. To YOUR event."
126. Tess: "And your colleagues treated him like he didn't belong."
127. Tess (real tears): "How could I not see that coming? How could YOU not see that?"
128. Chief (defensive): "Not all my officers—"
129. Tess: "Enough of them. Enough that he left sick. Not from food."
130. Chief processing—daughter defending boyfriend, not attacking him

### Touchpoint B
Redirect worked. Father believes she's upset about racism, not about murder cover-up.

---

## SCENE 5: The Escape (Beats 131-150)

**Location:** Chief's office → gala exit → street
**Present:** Tess, Chief Whitford, then Korede
**Tone:** Contained urgency, final extraction

### Touchpoint A
Tess must exit cleanly while father is placated.

### Beats

131. Chief: "I'll talk to them. Address it at next meeting—"
132. Tess: "It's not about one meeting. It's the culture."
133. Chief (deflecting): "We're working on that. Bias training—"
134. Tess: "Are you? Or are you just protecting your guys when they screw up?"
135. Words landing harder than intended—too close to truth
136. Chief (sharp): "What does that mean?"
137. Tess backpedaling: "Nothing. I'm just upset. About Korede."
138. Chief studying her: "This is about more than your boyfriend."
139. Tess: "I just want to go home. Can we talk another time?"
140. Chief: "Tess. You looked at me with disgust."
141. Tess: "Because I'm embarrassed! I brought someone I care about into—"
142. Chief: "Into what? Careful."
143. Tess on knife's edge—too much truth, he'll know
144. Tess: "Full of people who don't see him as equal."
145. Chief (softer): "I'm sorry. I should have prepared you."
146. Chief: "Come here." Opening arms again.
147. **Tess forcing herself to hug him—expecting it this time, controlled**
148. Chief (in her ear): "I love you. You know that, right?"
149. **Tess (whispered): "I know, Dad." (The saddest lie she's ever told)**
150. Pulling away, leaving his office, walking through ballroom

### Touchpoint B
Clean exit achieved. Cover intact. Soul damaged.

---

## SCENE 6: Background News Seed (Beats 151-155)

**Location:** Gala venue
**Tone:** Innocuous worldbuilding (reader doesn't connect to Ahdia)

### Beats

151. TV screens in gala showing news during party
152. **Ticker: "Mass disappearance of military junta leadership - 8 generals missing"**
153. Guests commenting: "Chaos overseas again. Thank God for American stability."
154. Officers laughing about foreign instability while covering up domestic murder
155. Tess notices irony but can't process it now

*[Sixth of seven news seeds. Reader won't connect to Ahdia until Ruth's discovery.]*

---

## SCENE 7: Debrief with Korede (Beats 156-175)

**Location:** Korede's car, across street
**Present:** Tess, Korede
**Tone:** Processing, protecting

### Touchpoint A
Tess exits gala. Korede waiting. Debriefing.

### Beats

156. Outside into cool night air, breathing hard
157. Korede appearing from across street: "Tess!"
158. Running to him, barely holding it together
159. Korede: "What happened? You were in there forever—"
160. Tess: "Not here. Car. Now."
161. Into Korede's borrowed car, doors closed
162. Tess (hands shaking): "I almost blew it. He saw—"
163. Korede: "Saw what?"
164. Tess: "My face. When I hugged him. I couldn't hide it."
165. Korede: "What did you tell him?"
166. Tess: "The truth. Sort of. About the racism. About you being treated like shit."
167. Korede: "And that worked?"
168. Tess: "He bought it. Thought I was upset about his colleagues, not about..."
169. Korede: "What did you learn?"
170. Tess: "CADENS Director Bourn ordered the cover-up. SecDef paid for it. My dad coordinated."
171. Tess: "They altered forensics in 48 hours. Original analyst refused to sign. CADENS analyst did."
172. Korede processing: "They know it was murder."
173. Tess: "They admitted it. Not directly, but they know. And they don't care."
174. Korede: "What do we do now?"
175. Tess: "I need to tell people who can use this information."

### Touchpoint B
Intel transferred. Korede knows the scope. Next: Go Squad.

---

## SCENE 8: Korede Goes Home (Beats 176-190)

**Location:** Outside Leta's apartment building
**Present:** Tess, Korede
**Tone:** Protective dismissal

### Touchpoint A
Tess protecting Korede by shutting him out of next phase.

### Beats

176. Tess: "I'm taking you home."
177. Korede: "What people? The protest organizers?"
178. Tess not answering directly
179. Korede: "Can I meet them?"
180. Tess: "No."
181. Korede (stung): "You don't trust me?"
182. Tess: "I'm protecting you. There's a difference."
183. Korede: "What you did tonight was incredible. But now you're shutting me out."
184. Tess: "I'm taking you home. Where seventeen-year-olds should be."
185. Pulling up to building
186. Korede: "Will you tell Leta I helped?"
187. Tess: "I'll tell her you were brave. That you endured things you shouldn't have."
188. Korede getting out: "Be careful. These people killed someone."
189. Tess: "I know. That's why I'm staying."
190. Watching him go inside, waiting for text

### Touchpoint B
Korede extracted. Tess heading to Go Squad alone.

---

## SCENE 9: Team Convergence (Beats 191-210)

**Location:** Parkour Academy
**Present:** Tess, Ruth, Ben, Victor, Leah
**Tone:** Revelation, dawning horror

### Touchpoint A
Tess arrives at team meeting with devastating intel.

### Beats

191. Text arrives: "Inside. Safe."
192. Tess: "Don't tell your sister how racist those cops were. She'll try to burn down city hall."
193. Korede: "Too late. Already planning the arson."
194. Tess driving to Parkour Academy
195. Team members already assembled: Ruth, Ben, Victor, Leah
196. Tess entering, changed from formal wear
197. Ruth: "Where's the asset who helped infiltrate?"
198. Tess: "Sent him home. Civilian. Seventeen."
199. Ben: "Operational security compromised?"
200. Tess: "He thinks I'm activist doing intel. Doesn't know about Go Squad."
201. Ruth: "Keep it that way. What did you find?"
202. Tess: "I know who covered up Isaiah Bennett's murder. And why."
203. Tess: "And it connects to everything we've been investigating."
204. Beat of silence
205. Ruth: "Tell us."
206. Tess takes breath
207. **Tess: "Director Bourn. CADENS. She ordered the forensics altered personally."**
208. **Ruth going pale—she works WITH Bourn**
209. Tess: "SecDef paid from classified Defense budget. My father coordinated locally."
210. Ben: "There's a paper trail?"

### Touchpoint B (CHAPTER END)
Intel delivered. Ruth realizes she's been briefing corrupt director. Team in crisis.

---

## CHAPTER 15B - END

---

## Complete Intel Package

**WHO:**
- CADENS Director Bourn (ordered cover-up)
- SecDef (paid for it, coordinated)
- Chief Whitford (actively complicit)

**WHAT:**
- Bodycam footage altered
- Forensic report falsified
- Original analyst refused, CADENS analyst signed instead
- "Ambiguous" situation given "clear narrative" of justified force

**HOW:**
- SecDef paid CADENS from classified Defense budget
- Bypassed normal appropriations
- 48-hour turnaround

**WHY:**
- "Protecting institutions" (political stability)
- Quid pro quo: CADENS gets funding, provides political cover

---

## Character Costs

**Tess:**
- Father relationship permanently damaged
- "I love you, Dad" — the saddest lie she's ever told
- Must deliver devastating news to Ruth

**Korede:**
- Shut out of next phase (protective, but stings)
- First operation complete, baptism by fire

**Ruth (setup):**
- Just learned she's been briefing corrupt director
- Institutional trust collapsing

---

## Prose Notes

- Tess POV—colder as chapter progresses
- Father hug scene is emotional devastation, not confrontation
- The lie ("I love you, Dad") should break reader's heart
- Final scene at Parkour Academy: quick, devastating revelation
- Ruth's reaction (going pale) is the hook into Chapter 16

---

**Continues in Chapter 16: Team Convergence**
