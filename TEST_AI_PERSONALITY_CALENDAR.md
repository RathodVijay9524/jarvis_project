# 🧠 AI Personality & 📅 Calendar Testing Guide

## 🧠 AI Personality System Testing

### **What is AI Personality?**
The AI Personality system makes JARVIS smarter by:
- Analyzing user emotions and context
- Learning from conversations
- Adapting response style
- Building personality traits
- Maintaining conversation flow

### **🧪 AI Personality Test Commands:**

#### **1. Basic Personality Queries:**
```
"tell me about yourself"
"what is your personality"
"how are you feeling today"
"what are you thinking"
"what have you learned"
```

#### **2. Emotional Intelligence Tests:**
```
"I'm feeling sad today"
"I'm really excited about my project"
"I'm frustrated with work"
"I'm happy to see you"
"I'm worried about tomorrow"
```

#### **3. Context Learning Tests:**
```
"I like programming in Python"
"My favorite color is blue"
"I work as a software engineer"
"I prefer tea over coffee"
"I enjoy listening to rock music"
```

#### **4. Conversation Flow Tests:**
```
"Let's talk about artificial intelligence"
"What do you think about space exploration"
"Can you help me with coding"
"Tell me a joke"
"What's your opinion on technology"
```

#### **5. Personality Profile Commands:**
```
"show my personality profile"
"what's my conversation context"
"what insights have you gained"
"update your helpfulness trait"
"how would you describe our conversations"
```

---

## 📅 Calendar System Testing

### **What is Calendar Service?**
The Calendar service provides:
- Event creation and management
- Reminder system with notifications
- Schedule viewing and planning
- Meeting scheduling
- Time-based alerts

### **🧪 Calendar Test Commands:**

#### **1. Event Creation:**
```
"create event meeting with team tomorrow at 3 PM"
"schedule doctor appointment on Friday at 10 AM"
"add birthday party event on December 25th at 6 PM"
"create event gym workout today at 7 AM"
"schedule conference call next Monday at 2 PM"
```

#### **2. Reminder Management:**
```
"remind me to buy groceries in 2 hours"
"set reminder call mom at 8 PM today"
"remind me about project deadline tomorrow"
"create reminder pay bills on 1st of next month"
"remind me to take medicine at 9 AM daily"
```

#### **3. Schedule Viewing:**
```
"show my schedule for today"
"what events do I have this week"
"show my calendar for tomorrow"
"list all my upcoming events"
"what's on my schedule for Friday"
```

#### **4. Event Management:**
```
"update my meeting time to 4 PM"
"cancel my gym workout event"
"delete reminder about groceries"
"reschedule doctor appointment to next week"
"modify birthday party location"
```

#### **5. Calendar Queries:**
```
"when is my next meeting"
"do I have any events today"
"show me this month's calendar"
"what reminders are active"
"how many events do I have this week"
```

---

## 🚀 **How to Test in JARVIS GUI:**

### **Step 1: Start JARVIS**
```bash
python Main.py modern
```

### **Step 2: Test AI Personality**
1. Try emotional queries: *"I'm feeling excited today!"*
2. Ask about personality: *"tell me about yourself"*
3. Test learning: *"I love pizza"* then later ask *"what do you know about me"*

### **Step 3: Test Calendar**
1. Create events: *"create event lunch meeting tomorrow at 1 PM"*
2. Set reminders: *"remind me to call John in 30 minutes"*
3. View schedule: *"show my schedule for today"*

### **Step 4: Test Integration**
1. Mix personality and calendar: *"I'm stressed about my meeting tomorrow"*
2. JARVIS should show empathy and offer to check your schedule

---

## 📊 **Expected Behaviors:**

### **AI Personality:**
- ✅ Responds with appropriate emotions
- ✅ Remembers your preferences
- ✅ Adapts conversation style
- ✅ Shows learning insights
- ✅ Maintains context across conversations

### **Calendar:**
- ✅ Creates events successfully
- ✅ Sets reminders with notifications
- ✅ Shows schedule in organized format
- ✅ Manages time conflicts
- ✅ Provides calendar summaries

---

## 🔧 **Troubleshooting:**

**AI Personality not responding?**
- Try: *"what's your personality profile"*
- Check if AI Personality is initialized in logs

**Calendar not working?**
- Try: *"show my calendar"*
- Check if `Data/calendar/` folder exists

**Features seem basic?**
- These are foundational systems that learn over time
- Try multiple interactions to see improvement

---

## 💡 **Pro Tips:**

1. **Be conversational** - AI Personality works better with natural language
2. **Use specific times** - Calendar works best with clear time references
3. **Test regularly** - Both systems improve with more interactions
4. **Mix features** - Try combining personality with calendar queries
5. **Check Data folder** - Both systems save data in `Data/personality/` and `Data/calendar/`

**Happy Testing! 🎉**
