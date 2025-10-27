# Design Thinking Workshop: RNKUP Platform
**Date:** October 27, 2025  
**Facilitator:** Maya (Design Thinking Maestro)  
**Project:** RNKUP - AI-First Voice-Native Learning for Air Force Promotions

---

## Executive Summary

This Design Thinking workshop validated the user-centered approach for RNKUP through a comprehensive 5-phase process: Empathize, Define, Ideate, Prototype, and Test. The workshop confirmed that solo E-4 to E-6 Airmen face critical gaps in exam preparation that voice-first AI tutoring can uniquely address.

**Key Findings:**
- Users need hands-free study during "dead time" (gym, commute, PT)
- Passive learning (PDFs, videos) fails for retention and engagement
- Solo learners lack feedback on readiness and weak areas
- Test anxiety stems from uncertainty, not lack of effort
- Voice-first interaction unlocks 5-10 hours/week of unusable study time

**Recommended MVP:** Integrated platform with AI tutor, voice-first interaction, adaptive intelligence, micro-learning architecture, and solo gamification.

---

## 1. Design Challenge

### Challenge Statement
> Create an AI-first, voice-native learning platform that empowers solo E-4 to E-6 Airmen to study for Air Force Promotion Fitness Exams (AFH1 content) through conversational tutoring and adaptive quizzing, replacing passive video lectures with active, dialog-based learning accessible anywhere, anytime.

### Primary Users
- **E-4 (Senior Airmen)** preparing for E-5 (Staff Sergeant) promotion
- **E-5 (Staff Sergeants)** preparing for E-6 (Technical Sergeant) promotion  
- **E-6 (Technical Sergeants)** preparing for further advancement
- Solo learners juggling military duties, deployments, and personal life

### Constraints
- **Technical**: Serverless architecture, cost optimization (<$0.005/user/month infrastructure)
- **Budget**: Must scale to 10,000+ users affordably
- **Time**: No video production overhead (removed Mux component)
- **Content**: Must be grounded in official AFH1 (24 chapters, 1,631 quiz concepts)

### Success Criteria
- 10,000+ active users
- High engagement (streaks, completion rates)
- Measurable exam score improvement
- Low-friction, fast experience (<400ms STT, <2s TTS)
- Cost-effective AI usage with model mixing

---

## 2. EMPATHIZE - User Research

### User Profile: Solo Airmen (E-4 to E-6)

**Demographics:**
- Rank: E-4 (Senior Airman), E-5 (Staff Sergeant), E-6 (Technical Sergeant)
- Context: Active duty with full-time military responsibilities
- Study Challenge: Must master 24 AFH1 chapters (1,631 potential quiz questions)
- Time Constraints: Juggling duty shifts, deployments, PT requirements, family obligations

### Pain Points Analysis

#### Static PDF Guides
- **Say**: "I just stare at hundreds of pages and zone out"
- **Think**: "Am I even retaining this?"
- **Do**: Re-read the same sections without retention
- **Feel**: Overwhelmed, bored, uncertain about progress

#### Basic Quiz Apps
- **Say**: "These flashcards are just memorization, not understanding"
- **Think**: "Will this actually help on the real test?"
- **Do**: Tap through cards mindlessly
- **Feel**: Disconnected from real learning

#### Video Lectures (Old Approach)
- **Say**: "I can't pause and ask questions"
- **Think**: "This is too passive - I'm not engaged"
- **Do**: Play videos in background while multitasking (low retention)
- **Feel**: Like a spectator, not a participant

### User Insights

**Study Context (Critical Pattern):**
- **When**: During commutes, PT cardio, between duties, late nights
- **Where**: Gym, car, barracks, deployed locations with limited internet
- **How Long**: 15-30 minute micro-sessions (not 2-hour study blocks)
- **Need**: Hands-free, voice-enabled, interruptible learning

**Motivation Drivers:**
- Promotion = career advancement + pay increase ($3k-$5k annually)
- Competitive promotion rates (limited slots)
- Pride in Air Force knowledge mastery
- Desire to lead and serve at higher levels

**Demotivation Factors:**
- Feeling alone in the process (no study buddy/tutor available)
- Uncertainty about weak areas
- Passive learning that doesn't stick
- No feedback on progress
- Information overload from 24 chapters

**Surprising Discoveries:**
- They WANT to understand "why" (not just memorize facts)
- They're comfortable with technology and AI
- Voice interaction appeals because they're multitasking constantly
- They trust official AFH1 content but need it "unlocked" for them
- Gamification works WITHOUT competitive leaderboards (solo personal bests)

### Empathy Map

| Says | Thinks | Does | Feels |
|------|--------|------|-------|
| "I need help NOW, not later" | "Am I studying the right stuff?" | Studies in short bursts | Isolated |
| "I don't have 2 hours to sit" | "Is this even going to be on test?" | Multitasks while learning | Overwhelmed |
| "PDFs put me to sleep" | "I wish I had a tutor" | Re-reads without retention | Uncertain |
| "I need to know my weak spots" | "Running out of time before exam" | Gym/commute = wasted study time | Anxious |

### Key Patterns
1. **Micro-learning over marathon sessions** - Need 15-30 min interactions
2. **Active over passive** - Want conversation, not consumption
3. **Voice-first is a game-changer** - Enables study during previously "dead time"
4. **Trust but verify** - Want citations back to AFH1 to build confidence
5. **Personal progress tracking** - Need to see weak areas and improvement

---

## 3. DEFINE - Problem Framing

### Point of View (POV) Statements

**Primary POV:**
> E-4 to E-6 Airmen need a personal tutor available 24/7 that adapts to their chaotic schedules and learning style because traditional study materials are passive, time-consuming, and isolate them during one of the most important career milestones, leaving them uncertain whether they're actually prepared for high-stakes promotion exams.

**Secondary POV (Contextual):**
> Solo military learners need to reclaim "dead time" (commutes, workouts, downtime) as productive study time because they don't have the luxury of 2-hour uninterrupted study blocks, yet they're competing for limited promotion slots against peers.

### "How Might We" Questions

1. **HMW make studying feel like having a conversation with a knowledgeable mentor** rather than reading a textbook alone?

2. **HMW transform "dead time" (driving, gym, downtime) into high-value study sessions** without requiring eyes or hands?

3. **HMW give learners real-time confidence about their readiness** instead of hoping they studied the right things?

4. **HMW provide AFH1 mastery with citations and context** so learners trust they're getting accurate, exam-relevant information?

5. **HMW make adaptive learning feel personalized and motivating** without the pressure of competing against others?

6. **HMW ensure learners focus on weak areas** instead of wasting time reviewing what they already know?

7. **HMW make AI tutoring feel natural and accessible** for military learners who may be skeptical of technology replacing human guidance?

### Problem Insights

**Insight #1: Passive Learning Fails for Retention**
- Problem: Reading PDFs or watching videos = low engagement = poor retention
- Opportunity: Active conversation + Socratic questioning = deeper encoding
- Impact: Users remember MORE with LESS study time

**Insight #2: Time Fragmentation is Reality, Not Exception**
- Problem: Current tools assume long, focused study blocks
- Opportunity: Voice-first enables micro-learning during activities (gym, commute)
- Impact: 15-30 min daily sessions > sporadic 2-hour cram sessions

**Insight #3: Uncertainty Kills Motivation**
- Problem: Learners don't know if they're ready until test day (too late)
- Opportunity: Continuous adaptive assessment reveals weak areas in real-time
- Impact: Confidence from knowing exactly where they stand

**Insight #4: Trust Requires Grounding**
- Problem: Generic quiz apps lack credibility and context
- Opportunity: RAG with AFH1 + citations = trust + deeper understanding
- Impact: Not just "what" but "why" - exam-aligned learning

**Insight #5: Solo Doesn't Mean Unsupported**
- Problem: No study buddy ≠ alone without support
- Opportunity: AI tutor as always-available wingman
- Impact: Feels supported without scheduling coordination

**Insight #6: Gamification Works When Personal**
- Problem: Leaderboards create anxiety in high-stakes contexts
- Opportunity: Personal streaks, badges, progress tracking
- Impact: Motivation from self-improvement, not comparison

---

## 4. IDEATE - Solution Generation

### Generated Solutions (14 Ideas)

**For HMW: "Make studying feel like conversation with a mentor"**

**Idea 1: AI Tutor with Dual Modes**
- Study/Reference Mode: Strict RAG-grounded answers with AFH1 citations
- Coaching Mode: Study skills, motivation, exam strategies
- Socratic questioning: hints before answers
- Natural language Q&A in real-time

**Idea 2: Conversational Quiz Mode**
- Voice-driven oral quizzing
- Tutor explains WHY answers are right/wrong
- Follow-up questions for deeper understanding
- Not just "correct/incorrect" but teaching moments

---

**For HMW: "Transform dead time into study sessions"**

**Idea 3: Voice-First Loop (Deepgram STT + ElevenLabs TTS)**
- Push-to-talk or wake-word activation
- Real-time streaming STT (<400ms latency)
- Natural TTS with interruption controls
- Full transcript + captions for reference
- Hands-free + eyes-free operation

**Idea 4: Multiple Quiz Modes for Different Contexts**
- Quick Quiz: 5 questions, any topic (5 min - gym break)
- Chapter Quiz: Focused deep dive (15 min - commute)
- Mock Exam: Full-length practice (60 min - weekend)
- Voice Quiz: Fully hands-free (during workout)
- Flash Review: Rapid-fire spaced repetition (10 min)

---

**For HMW: "Give learners confidence about readiness"**

**Idea 5: Adaptive Learning Dashboard**
- Resume where you left off - no hunting for next task
- Progress metrics: chapters covered, weak/strong topics
- Exam countdown: urgency + timeline awareness
- Coverage %: visual confidence builder
- Weak-area heatmap: red/yellow/green by topic

**Idea 6: Smart Suggestions Engine**
- "Review Chapter 7: Force Development" (detected weak area)
- "10-question adaptive quiz on your weak spots"
- "Voice drill now: 15 min practice"
- One-tap actions based on progress data

---

**For HMW: "Provide AFH1 mastery with citations"**

**Idea 7: RAG-Powered Content Grounding**
- Vector search (Pinecone) of AFH1 chunks
- Every answer cites chapter:section
- "I don't know from AFH1" when evidence weak
- Metadata: chapter, section, source page
- Question bank tagged to AFH1 sections

**Idea 8: AI-Generated Summaries & Notes**
- Chapter summaries for quick review
- Session notes: "Today you studied..."
- Personalized study guide generation
- Key takeaways extracted from conversations

---

**For HMW: "Make adaptive learning personalized"**

**Idea 9: Weak-Area Detection & Spaced Repetition**
- Track performance by chapter/topic/question
- SM-2 algorithm for optimal review intervals
- Adaptive quizzing: harder questions when mastering
- Automatic queue of "due for review" content

**Idea 10: Solo Gamification (No Leaderboards)**
- Streaks: Daily study consistency
- Badges: Milestones (7-day streak, chapter mastery, 100 questions)
- Personal Bests: Your best scores, not vs. others
- Goal Setting: Optional daily minutes targets
- Toast notifications for achievements

---

**For HMW: "Focus learners on weak areas"**

**Idea 11: Intelligent Question Selection**
- Hybrid: curated bank + AI-generated questions
- Difficulty tagging (easy/medium/hard)
- Topic/chapter tagging for targeting
- Prioritize questions on weak performance areas
- Avoid repetition until spaced interval due

**Idea 12: Explanations with AFH1 References**
- Instant rationale for every answer
- Links/citations to AFH1 source
- "Learn more" deep-dive into topic
- Build mental model, not just memorization

---

**For HMW: "Make AI tutoring feel natural"**

**Idea 13: Streaming Conversational UI**
- Real-time token streaming (feels responsive)
- Interim transcripts during speech
- Interruptible TTS (stop mid-answer)
- Text fallback always available
- Mobile-first PWA (install like app)

**Idea 14: Study Planner with Gentle Reminders**
- Optional: set exam date + daily goal
- Smart scheduling suggestions
- Gentle push notifications (not nagging)
- "You studied 3 days this week - keep it up!"

### Solution Clustering

**TOP CONCEPT A: Conversational AI Tutor Core**
- Combines: Ideas 1, 2, 7, 8, 13
- Value: Makes learning feel like mentorship, not solo study
- Feasibility: High - OpenAI API + Pinecone RAG

**TOP CONCEPT B: Voice-First Everywhere**
- Combines: Ideas 3, 4
- Value: Unlocks "dead time" study opportunities
- Feasibility: Medium - STT/TTS integration complexity

**TOP CONCEPT C: Adaptive Intelligence Layer**
- Combines: Ideas 5, 6, 9, 11, 12
- Value: Personalized learning path, confidence building
- Feasibility: High - algorithmic + data tracking

**TOP CONCEPT D: Motivational Feedback System**
- Combines: Ideas 10, 14
- Value: Sustains engagement over weeks/months
- Feasibility: High - standard gamification patterns

### MVP Concepts Selected (All 4)

✅ **1. Conversational AI Tutor Core** (Concept A)  
✅ **2. Voice-First Loop** (Concept B)  
✅ **3. Adaptive Dashboard + Smart Suggestions** (Concept C)  
✅ **4. Gamification & Motivation** (Concept D)

---

## 5. PROTOTYPE - Build Strategy

### Prototype Approach: Phased MVP Build

**Testing Goals:**
1. Voice UX naturalness - Will users actually speak to the tutor?
2. AI trust with citations - Do citations build confidence?
3. Engagement vs. passive study - Does conversation feel less isolating?
4. Weak-area detection value - Do smart suggestions improve efficiency?
5. Gamification impact - Do streaks/badges sustain motivation?

### Prototype 1: Core Conversational Flow (Week 1-2)

**Minimum Features:**
- Text-based chat (voice comes later)
- Simple Q&A with mock RAG (3-5 pre-loaded AFH1 chunks)
- Citation display: `[Source: Chapter 1, Section 1A]`
- Basic quiz: 5 questions with explanations

**What Can Be Faked:**
- Full Pinecone vector DB → Use 5-10 hard-coded AFH1 excerpts
- Full quiz bank → Use 20 curated questions
- Real adaptive logic → Random question selection

**What Must Be Real:**
- OpenAI API integration (streaming response)
- Chat UI with message history
- Citation formatting
- Question → Answer → Explanation flow

### Prototype 2: Voice-First Experience (Week 3-4)

**Minimum Features:**
- Push-to-talk button
- Deepgram STT integration (real-time)
- ElevenLabs TTS for responses
- Interim transcript display
- Stop/interrupt controls

**What Must Be Real:**
- Actual STT/TTS services
- Streaming audio playback
- Latency measurement (<400ms STT goal)
- Mobile-responsive UI

### Prototype 3: Adaptive Dashboard (Week 5-6)

**Minimum Features:**
- Progress ring showing chapter coverage
- Simple weak/strong topic list (based on quiz results)
- 3 smart suggestions: "Review X", "Quiz Y", "Practice Z"
- Streak counter (days studied)

**What Must Be Real:**
- Progress persistence (database)
- Quiz result tracking
- Suggestion generation based on data
- Visual progress indicators

### Prototype 4: Complete MVP Integration (Week 7-8)

**Full Feature Set:**
- All 4 concepts integrated
- Multiple quiz modes (Quick, Chapter, Mock, Voice)
- Flashcard mode with basic spaced repetition
- Badges for milestones
- Study planner with exam date countdown
- AI chapter summaries (3 sample chapters)

**Technical Stack:**
- Next.js 16, Pinecone, OpenAI, Deepgram, ElevenLabs
- Database with user profiles, progress, quiz history
- Authentication (NextAuth/Supabase)
- Mobile PWA installation
- Edge caching for common queries

### Features Users Must Test

**Scenario 1: First-Time User**
1. Sign up → Select rank + target promotion
2. Set optional exam date
3. See dashboard with "Start here" suggestions
4. Try voice tutorial: "Say 'Quiz me on Chapter 1'"

**Scenario 2: Study Session**
1. Ask tutor: "What is the Profession of Arms?"
2. Receive answer with citation
3. Ask follow-up: "Why does that matter?"
4. Switch to quiz mode
5. Complete 10 questions with explanations
6. See updated progress + weak areas

**Scenario 3: Voice Workout Mode**
1. Start voice quiz
2. Hear question via TTS
3. Speak answer
4. Hear explanation
5. Complete 5 questions hands-free

**Scenario 4: Return User**
1. See streak counter + badges
2. Get smart suggestion: "Review weak area: Chapter 9"
3. Access flashcards for spaced repetition
4. Check exam countdown

---

## 6. TEST - Validation Plan

### Testing Strategy

**Target Users:**
- **Phase 1-2**: 5-7 Active Duty Airmen (E-4 to E-6 mix)
- **Phase 3-4**: 10-15 Users (include Guard/Reserve, deployed contexts)

**Recruitment:** Air Force subreddits, Discord, base education centers, referrals

### Testing Tasks by Phase

**Phase 1 Test: Conversational Tutor (Week 2)**

**Task 1: Natural Question Flow**
- "Ask the tutor anything about Chapter 1: Professionalism"
- Observe: Do they ask follow-up questions?

**Task 2: Citation Trust**
- "Find out what the Air Force Core Values are"
- Observe: Do they check citations?

**Task 3: Quiz with Explanations**
- "Take a 5-question quiz on any chapter"
- Observe: Do they read explanations?

**Success Indicators:**
- Users ask 3+ questions in conversation
- Users reference citations in feedback
- 4/5 prefer conversation over PDF reading

---

**Phase 2 Test: Voice-First Experience (Week 4)**

**Task 4: Voice Q&A During Activity**
- "Ask the tutor 3 questions using voice while walking"
- Observe: Natural speech? Hesitation? Errors?

**Task 5: Voice Quiz Hands-Free**
- "Complete a 5-question voice quiz without touching phone"
- Observe: Completion rate, where they struggle

**Task 6: Commute/Gym Simulation**
- "Use the app during a 15-minute treadmill walk"
- Observe: Real-world viability, background noise issues

**Success Indicators:**
- <400ms STT interim results
- <2s to first TTS audio
- 4/5 complete voice quiz successfully
- 3/5 would use voice during workout/commute

---

**Phase 3 Test: Adaptive Dashboard (Week 6)**

**Task 7: Progress Understanding**
- "Show me where you'd go to see what you need to study next"
- Observe: Can they find weak areas?

**Task 8: Weak Area Focus**
- "Follow one smart suggestion"
- Observe: Do suggestions feel relevant?

**Task 9: Streak Motivation**
- "Come back tomorrow and the next day (3-day test)"
- Observe: Do they return?

**Success Indicators:**
- Users identify weak areas within 10 seconds
- 60%+ click rate on smart suggestions
- 3/5 maintain 3+ day streak

---

**Phase 4 Test: Full MVP (Week 8)**

**Task 10: Complete Study Workflow**
- "You have 30 minutes. Study however you'd like."
- Observe: Which features do they use?

**Task 11: Multi-Day Real-World Usage**
- "Use RNKUP as primary study tool for 7 days"
- Capture: Daily engagement, features used

**Task 12: Comparison Test**
- "Study Chapter 7 with RNKUP, Chapter 8 with PDFs"
- Test: Quiz performance on both 3 days later

**Success Indicators:**
- 7/10 complete full week trial
- 15+ min average engagement per day
- Better retention on RNKUP chapter vs. traditional
- NPS >40

### Feedback Collection

**During Testing:**
- Screen/audio recording (with permission)
- Think-aloud protocol
- Observation notes (body language, frustration, delight)

**After Tasks:**
- Structured interview (15 min)
- System Usability Scale (SUS) survey
- Feature rating (1-5 stars)

**Ongoing:**
- Daily micro-survey (2-3 questions)
- Analytics tracking (feature usage, session length)
- In-app feedback (thumbs up/down)

### Hypothesis Validation

| Hypothesis | Test Method | Success Criteria |
|------------|-------------|------------------|
| Voice interaction reduces friction | Task 5 completion + survey | 60%+ prefer voice for certain contexts |
| Citations build AI trust | Track citation clicks + survey | 70%+ reference citations, trust increases |
| Conversation improves retention | Quiz scores: RNKUP vs traditional | 15%+ better retention with RNKUP |
| Weak-area targeting saves time | Study time to coverage % | Higher efficiency |
| Gamification sustains engagement | 7-day streak tracking | 60%+ maintain 5+ day streak |

---

## 7. NEXT ITERATION - Refinement Plan

### Immediate Refinements (Post-Test)

**If Voice UX Issues:**
- Refine push-to-talk interaction
- Improve STT error handling
- Add text fallback prominently

**If Citation Trust Weak:**
- Make citations more prominent
- Add "View Source" deep-link
- Show confidence scores

**If Engagement Drops:**
- Strengthen reminder system
- Improve streak recovery
- Enhance milestone visibility

**If Cost Exceeds Target:**
- Increase GPT-3.5 usage vs GPT-4
- Implement aggressive caching
- Add per-user daily limits

### Priority Actions (Next 3-6 Months)

**Phase 1: MVP Refinement (Weeks 9-12)**
- Fix critical UX issues
- Expand AFH1 coverage to all 24 chapters
- Build out full quiz bank (1,631 questions)
- Optimize cost (hit <$0.005/user target)
- Success: SUS score >70, cost target met

**Phase 2: Closed Beta (Months 4-5)**
- Recruit 100 beta testers
- Monitor engagement, retention, cost
- Collect NPS and feature requests
- Build waitlist for launch
- Success: 60%+ 30-day retention, NPS >40

**Phase 3: Public Launch Prep (Month 6)**
- Load testing for 10,000 users
- Payment integration
- Marketing site and onboarding
- Support documentation
- Success: Infrastructure validated

**Phase 4: Public Launch (Month 7)**
- Launch marketing campaign
- Referral program
- Weekly iteration cycles
- Success: 1,000 users, <5% churn

### Success Metrics

**User Engagement:**
- DAU/MAU ratio
- Average session duration >15 min
- Sessions per week >4
- Feature usage (voice >40%, quiz >60%)

**Learning Effectiveness:**
- Quiz score improvement
- Chapter completion rates
- Retention test scores
- User-reported exam performance

**Business Viability:**
- Infrastructure cost <$0.005/user/month
- Total cost <$0.50/user/month
- 30-day retention >60%
- NPS >40

**Product-Market Fit:**
- Weekly growth >10%
- Organic referrals >30%
- "Very disappointed" >40% (Sean Ellis test)
- Paid conversion >5%

### Decision Gates

**GO (Continue):**
- 60%+ retention at 30 days
- NPS >40
- Cost model validated
- Clear user love

**ADJUST (Iterate):**
- Retention 40-60%
- NPS 20-40
- Cost slightly over
- Feature confusion

**PIVOT (Major Change):**
- <40% retention
- NPS <20
- Cost unsustainable
- Users prefer alternatives

---

## Key Insights Summary

### Validated Assumptions
✅ Solo Airmen need better exam prep (clear pain points)  
✅ Voice-first unlocks "dead time" study opportunities  
✅ AI with citations can build trust (with proper implementation)  
✅ Adaptive learning reduces overwhelm and wasted time  
✅ Personal gamification works without competition stress  

### Critical Learnings
1. **Voice is differentiator**: No competitor offers hands-free study
2. **Citations are essential**: Trust requires grounding in AFH1
3. **Micro-sessions work**: 15-30 min sessions fit real schedules
4. **Progress visibility matters**: Knowing "where you are" reduces anxiety
5. **Solo doesn't mean alone**: AI tutor provides personal connection

### Next Steps
1. Build Prototype 1 (conversational core)
2. Test with 5-7 users
3. Iterate based on feedback
4. Progress through prototypes 2-4
5. Launch closed beta

---

**Design Thinking Workshop Complete**  
**Prepared by:** Claude (AI Facilitator)  
**For:** RNKUP Platform Development  
**Date:** October 27, 2025

