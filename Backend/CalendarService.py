"""
CalendarService.py
Calendar and scheduling integration for JARVIS.
"""

import os
import json
import time
from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional
import calendar
import threading

class JarvisCalendarService:
    """
    Calendar and scheduling service with:
    - Event creation and management
    - Reminder system
    - Schedule viewing
    - Calendar integration
    - Meeting scheduling
    """
    
    def __init__(self, data_dir: str = "Data/calendar"):
        self.data_dir = data_dir
        self.calendar_file = os.path.join(data_dir, "calendar.json")
        self.reminders_file = os.path.join(data_dir, "reminders.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.events = self._load_events()
        self.reminders = self._load_reminders()
        
        # Start reminder monitoring thread
        self.reminder_thread = threading.Thread(target=self._monitor_reminders, daemon=True)
        self.reminder_thread.start()
    
    def _load_events(self) -> List[Dict[str, Any]]:
        """Load events from file."""
        try:
            if os.path.exists(self.calendar_file):
                with open(self.calendar_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading events: {e}")
            return []
    
    def _save_events(self):
        """Save events to file."""
        try:
            with open(self.calendar_file, 'w') as f:
                json.dump(self.events, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving events: {e}")
    
    def _load_reminders(self) -> List[Dict[str, Any]]:
        """Load reminders from file."""
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading reminders: {e}")
            return []
    
    def _save_reminders(self):
        """Save reminders to file."""
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving reminders: {e}")
    
    def create_event(self, title: str, start_time: str, end_time: str = None, 
                    description: str = "", location: str = "", reminder_minutes: int = 15) -> str:
        """
        Create a new calendar event.
        
        Args:
            title: Event title
            start_time: Start time (format: YYYY-MM-DD HH:MM or "today 2pm", "tomorrow 10am")
            end_time: End time (optional, defaults to 1 hour after start)
            description: Event description
            location: Event location
            reminder_minutes: Minutes before event to remind (default: 15)
        """
        try:
            # Parse start time
            start_dt = self._parse_time(start_time)
            if not start_dt:
                return f"❌ Invalid start time format: {start_time}"
            
            # Parse end time
            if end_time:
                end_dt = self._parse_time(end_time)
                if not end_dt:
                    return f"❌ Invalid end time format: {end_time}"
            else:
                end_dt = start_dt + timedelta(hours=1)  # Default 1 hour duration
            
            # Create event
            event = {
                'id': len(self.events) + 1,
                'title': title,
                'start_time': start_dt.isoformat(),
                'end_time': end_dt.isoformat(),
                'description': description,
                'location': location,
                'created_at': datetime.now().isoformat(),
                'reminder_minutes': reminder_minutes,
                'status': 'active'
            }
            
            self.events.append(event)
            self._save_events()
            
            # Create reminder if specified
            if reminder_minutes > 0:
                reminder_time = start_dt - timedelta(minutes=reminder_minutes)
                if reminder_time > datetime.now():
                    self._create_reminder(title, reminder_time, f"Event reminder: {title}")
            
            return f"✅ Created event: '{title}' on {start_dt.strftime('%Y-%m-%d at %H:%M')}"
            
        except Exception as e:
            return f"❌ Error creating event: {str(e)}"
    
    def _parse_time(self, time_str: str) -> Optional[datetime]:
        """Parse various time formats."""
        try:
            time_str = time_str.lower().strip()
            now = datetime.now()
            
            # Handle relative times
            if time_str.startswith('today'):
                date_part = now.date()
                time_part = time_str.replace('today', '').strip()
            elif time_str.startswith('tomorrow'):
                date_part = now.date() + timedelta(days=1)
                time_part = time_str.replace('tomorrow', '').strip()
            elif time_str.startswith('yesterday'):
                date_part = now.date() - timedelta(days=1)
                time_part = time_str.replace('yesterday', '').strip()
            else:
                # Try to parse as absolute time
                try:
                    return datetime.fromisoformat(time_str.replace(' ', 'T'))
                except:
                    # Assume it's today with time
                    date_part = now.date()
                    time_part = time_str
            
            # Parse time part
            hour = now.hour
            minute = 0
            
            if time_part:
                if 'am' in time_part or 'pm' in time_part:
                    # 12-hour format
                    time_part = time_part.replace('am', '').replace('pm', '').strip()
                    if ':' in time_part:
                        hour_str, minute_str = time_part.split(':')
                        hour = int(hour_str)
                        minute = int(minute_str)
                    else:
                        hour = int(time_part)
                    
                    # Handle AM/PM
                    if 'pm' in time_str and hour != 12:
                        hour += 12
                    elif 'am' in time_str and hour == 12:
                        hour = 0
                else:
                    # 24-hour format
                    if ':' in time_part:
                        hour_str, minute_str = time_part.split(':')
                        hour = int(hour_str)
                        minute = int(minute_str)
                    else:
                        hour = int(time_part)
            
            return datetime.combine(date_part, datetime.min.time().replace(hour=hour, minute=minute))
            
        except Exception as e:
            print(f"⚠️ Time parsing error: {e}")
            return None
    
    def list_events(self, date_filter: str = None, days_ahead: int = 7) -> str:
        """
        List upcoming events.
        
        Args:
            date_filter: Filter by specific date (YYYY-MM-DD) or 'today', 'tomorrow'
            days_ahead: Number of days ahead to show (default: 7)
        """
        try:
            if date_filter:
                if date_filter.lower() == 'today':
                    target_date = datetime.now().date()
                elif date_filter.lower() == 'tomorrow':
                    target_date = (datetime.now() + timedelta(days=1)).date()
                else:
                    target_date = datetime.fromisoformat(date_filter).date()
                
                filtered_events = [
                    event for event in self.events
                    if datetime.fromisoformat(event['start_time']).date() == target_date
                    and event['status'] == 'active'
                ]
            else:
                # Show events for next N days
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=days_ahead)
                
                filtered_events = [
                    event for event in self.events
                    if start_date <= datetime.fromisoformat(event['start_time']).date() <= end_date
                    and event['status'] == 'active'
                ]
            
            if not filtered_events:
                filter_desc = date_filter or f"next {days_ahead} days"
                return f"📅 No events scheduled for {filter_desc}"
            
            # Sort by start time
            filtered_events.sort(key=lambda x: x['start_time'])
            
            # Format response
            response = f"📅 **Calendar Events**\n\n"
            
            current_date = None
            for event in filtered_events:
                event_dt = datetime.fromisoformat(event['start_time'])
                event_date = event_dt.date()
                
                # Add date header if new date
                if current_date != event_date:
                    current_date = event_date
                    if event_date == datetime.now().date():
                        date_header = "📅 **Today**"
                    elif event_date == (datetime.now() + timedelta(days=1)).date():
                        date_header = "📅 **Tomorrow**"
                    else:
                        date_header = f"📅 **{event_date.strftime('%A, %B %d, %Y')}**"
                    response += f"\n{date_header}\n"
                
                # Event details
                start_time = event_dt.strftime('%H:%M')
                end_dt = datetime.fromisoformat(event['end_time'])
                end_time = end_dt.strftime('%H:%M')
                
                response += f"   🕒 **{start_time} - {end_time}** {event['title']}\n"
                
                if event.get('location'):
                    response += f"      📍 {event['location']}\n"
                
                if event.get('description'):
                    desc = event['description'][:100] + "..." if len(event['description']) > 100 else event['description']
                    response += f"      📝 {desc}\n"
                
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error listing events: {str(e)}"
    
    def delete_event(self, event_id: int) -> str:
        """Delete an event by ID."""
        try:
            event = next((e for e in self.events if e['id'] == event_id), None)
            if not event:
                return f"❌ Event with ID {event_id} not found"
            
            event['status'] = 'deleted'
            self._save_events()
            
            return f"✅ Deleted event: '{event['title']}'"
            
        except Exception as e:
            return f"❌ Error deleting event: {str(e)}"
    
    def update_event(self, event_id: int, **kwargs) -> str:
        """Update an event."""
        try:
            event = next((e for e in self.events if e['id'] == event_id), None)
            if not event:
                return f"❌ Event with ID {event_id} not found"
            
            # Update allowed fields
            allowed_fields = ['title', 'description', 'location', 'reminder_minutes']
            for field, value in kwargs.items():
                if field in allowed_fields:
                    event[field] = value
            
            self._save_events()
            
            return f"✅ Updated event: '{event['title']}'"
            
        except Exception as e:
            return f"❌ Error updating event: {str(e)}"
    
    def create_reminder(self, title: str, reminder_time: str, description: str = "") -> str:
        """
        Create a standalone reminder.
        
        Args:
            title: Reminder title
            reminder_time: When to remind (format: YYYY-MM-DD HH:MM or relative)
            description: Reminder description
        """
        try:
            reminder_dt = self._parse_time(reminder_time)
            if not reminder_dt:
                return f"❌ Invalid reminder time format: {reminder_time}"
            
            if reminder_dt <= datetime.now():
                return "❌ Reminder time must be in the future"
            
            reminder = {
                'id': len(self.reminders) + 1,
                'title': title,
                'reminder_time': reminder_dt.isoformat(),
                'description': description,
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            self.reminders.append(reminder)
            self._save_reminders()
            
            return f"✅ Created reminder: '{title}' for {reminder_dt.strftime('%Y-%m-%d at %H:%M')}"
            
        except Exception as e:
            return f"❌ Error creating reminder: {str(e)}"
    
    def _create_reminder(self, title: str, reminder_time: datetime, description: str):
        """Internal method to create reminder."""
        reminder = {
            'id': len(self.reminders) + 1,
            'title': title,
            'reminder_time': reminder_time.isoformat(),
            'description': description,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        self.reminders.append(reminder)
        self._save_reminders()
    
    def _monitor_reminders(self):
        """Background thread to monitor and trigger reminders."""
        while True:
            try:
                current_time = datetime.now()
                
                # Check for due reminders
                due_reminders = [
                    r for r in self.reminders
                    if datetime.fromisoformat(r['reminder_time']) <= current_time
                    and r['status'] == 'active'
                ]
                
                for reminder in due_reminders:
                    # Mark as triggered
                    reminder['status'] = 'triggered'
                    reminder['triggered_at'] = current_time.isoformat()
                    
                    # Here you would typically send a notification
                    # For now, we'll just print to console
                    print(f"🔔 REMINDER: {reminder['title']}")
                    if reminder['description']:
                        print(f"   {reminder['description']}")
                
                if due_reminders:
                    self._save_reminders()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"⚠️ Reminder monitoring error: {e}")
                time.sleep(60)
    
    def list_reminders(self, status: str = 'active') -> str:
        """List reminders by status."""
        try:
            filtered_reminders = [
                r for r in self.reminders
                if r['status'] == status
            ]
            
            if not filtered_reminders:
                return f"📋 No {status} reminders found"
            
            # Sort by reminder time
            filtered_reminders.sort(key=lambda x: x['reminder_time'])
            
            response = f"📋 **{status.title()} Reminders**\n\n"
            
            for reminder in filtered_reminders:
                reminder_dt = datetime.fromisoformat(reminder['reminder_time'])
                time_str = reminder_dt.strftime('%Y-%m-%d %H:%M')
                
                response += f"🔔 **{reminder['title']}**\n"
                response += f"   🕒 {time_str}\n"
                
                if reminder['description']:
                    response += f"   📝 {reminder['description']}\n"
                
                response += f"   🆔 ID: {reminder['id']}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error listing reminders: {str(e)}"
    
    def get_schedule_summary(self, days: int = 7) -> str:
        """Get a summary of upcoming schedule."""
        try:
            events_response = self.list_events(days_ahead=days)
            
            # Count events by day
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=days)
            
            active_events = [
                e for e in self.events
                if start_date <= datetime.fromisoformat(e['start_time']).date() <= end_date
                and e['status'] == 'active'
            ]
            
            active_reminders = [
                r for r in self.reminders
                if start_date <= datetime.fromisoformat(r['reminder_time']).date() <= end_date
                and r['status'] == 'active'
            ]
            
            summary = f"📊 **Schedule Summary (Next {days} Days)**\n\n"
            summary += f"📅 **Events:** {len(active_events)}\n"
            summary += f"🔔 **Reminders:** {len(active_reminders)}\n\n"
            
            if active_events:
                summary += "📅 **Upcoming Events:**\n"
                for event in active_events[:5]:  # Show first 5
                    event_dt = datetime.fromisoformat(event['start_time'])
                    summary += f"   • {event['title']} - {event_dt.strftime('%m/%d %H:%M')}\n"
                
                if len(active_events) > 5:
                    summary += f"   ... and {len(active_events) - 5} more events\n"
            
            summary += "\n" + events_response
            
            return summary
            
        except Exception as e:
            return f"❌ Error getting schedule summary: {str(e)}"
    
    def get_calendar_help(self) -> str:
        """Get help information for calendar features."""
        return """📅 **Calendar & Scheduling Help**

🔧 **Creating Events:**
   • 'create event Meeting today 2pm'
   • 'schedule Conference tomorrow 10am to 11am'
   • 'add event Birthday party 2024-12-25 18:00'

📋 **Managing Events:**
   • 'list events' - Show next 7 days
   • 'list events today' - Show today's events
   • 'list events tomorrow' - Show tomorrow's events
   • 'delete event [ID]' - Delete event by ID
   • 'update event [ID] title New Title' - Update event

🔔 **Reminders:**
   • 'create reminder Call mom tomorrow 9am'
   • 'remind me Submit report 2024-12-20 17:00'
   • 'list reminders' - Show active reminders

📊 **Schedule Information:**
   • 'schedule summary' - Overview of upcoming events
   • 'what's on my calendar' - View schedule
   • 'busy today' - Check today's schedule

💡 **Time Formats:**
   • 'today 2pm', 'tomorrow 10am'
   • '2024-12-25 18:00' (24-hour format)
   • '2pm', '10am' (assumes today)

📝 **Examples:**
   • 'create event Team meeting tomorrow 2pm to 3pm'
   • 'schedule Doctor appointment today 4pm'
   • 'remind me Buy groceries tomorrow 9am'
   • 'list events this week'
"""
